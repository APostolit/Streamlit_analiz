import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

# Функция для загрузки данных из CSV файла
@st.cache_data
def get_data():
    # Имя файла
    path_csv = 'csv/passengers.csv'
    # Чтение данных из файла csv
    df = pd.read_csv(path_csv)
    return df

st.subheader('🔬Декомпозиция временного ряда')
st.markdown('##### 🚍👬Данные о пассажиропотоках из файла CSV')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶 Сырые данные",
     "📶🧹 Очищенные данные",
     "📈 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных из CSV файла
    with st.container(width=300):
        df_pass = get_data()
        st.write('📶Набор сырых данных из файла CSV')
        st.write(df_pass)

# Вкладка с данными
with t2:
    # Контейнер для данных с индексом
    with st.container(width=350,  border=True):
        # Формирование индексной колонки Month
        df_pass.set_index('Month', inplace=True)
        # Трансформация колонки Month в дату
        df_pass.index = pd.to_datetime(df_pass.index)
        st.write('📶🧹Очищенные данные')
        st.write(df_pass)

# Применяем функцию декомпозиции к данным о пассажирах
decompose = seasonal_decompose(df_pass, model='additive', period=12)
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
    title='📈Составляющие временного ряда пассажиропотока',
    hoverlabel=dict(font_size=12))  # Размера шрифта для данных

# Вкладка с графиком
with t3:
    # Контейнер для графика
     with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)