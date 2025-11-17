import streamlit as st
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
         # Получение временного ряда из тестового набора данных
        data = sm.datasets.co2.load_pandas()
        df1 = data.data
        # Параметр 'MS' (группирует данные на начало месяца)
        df1 = df1['co2'].resample('MS').mean()
        # Заполняем пропуски значениями перед пропущенными значениями
        s = df1.fillna(df1.bfill())
        # Преобразование Series в DataFrame
        df1 = s.to_frame(name='co2')
        return df1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🌞❄️ Анализ временных рядов на наличие сезонности')
st.markdown('##### 🚗💨 Данные из Statmodels (содержание в воздухе CO2)')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    df = get_data()

# Создаем вкладки
t1, t2 = st.tabs(
    ["📶🧹Очищенные данные",
     "📈🛠️Анализ данных"
     ])

# Вкладка t1
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🧹Исходный набор данных')
        st.write(df)

# применяем функцию декомпозиции к данным df
decompose = seasonal_decompose(df, model='additive', period=12)
observed = decompose.observed.dropna()
trend = decompose.trend.dropna()
seasonal = decompose.seasonal.dropna()
resid = decompose.resid.dropna()

# Формируем график
fig = make_subplots(rows=2, cols=2)
fig.add_trace(go.Scatter(x=observed.index, y=observed, name="Наблюдения"), row=1, col=1)
fig.add_trace(go.Scatter(x=trend.index, y=trend, name="Тренд"), row=1, col=2)
fig.add_trace(go.Scatter(x=seasonal.index, y=seasonal, name="Сезонность"), row=2, col=1)
fig.add_trace(go.Scatter(x=resid.index, y=resid, name="Нерегулярность"), row=2, col=2)

# Формирование параметров графика
fig.update_layout(
    height=600,
    title='📈🛠️ Составляющие временного ряда',
    hoverlabel=dict(font_size=12))  # Размера шрифта для данных

# Вкладка t2
with t2:
    # Контейнер для графика
    with st.container(width=700, border=True):
        st.plotly_chart(fig, theme=None)