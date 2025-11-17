import streamlit as st
import pandas as pd
import pmdarima as pm
import plotly.graph_objects as go
import warnings
import statsmodels.api as sm

# Подключить matplotlib к pandas
pd.options.plotting.backend = 'matplotlib'
warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Получение временного ряда из тестового набора данных
        data = sm.datasets.co2.load_pandas()
        df = data.data
        # Параметр 'MS' группирует данные по началу месяца
        df = df['co2'].resample('MS').mean()
        # Заполняем пропуски значениями перед пропущенными значениями
        ser = df.fillna(df.bfill())
        return ser
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🛠️ Анализ временного ряда и оптимизация модели SARIMA')
st.markdown('##### 🚗💨 Данные из Statmodels (содержание в воздухе CO2)')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    series = get_data()

with st.spinner(text="Идет подбор параметров модели...", show_time=True):
    # Подбор оптимальных параметров модели с auto_arima
    # order = pm.auto_arima(series, max_order=None, seasonal=True, m=12)
    # get_param = order.get_params()
    # param = get_param.get('order')
    # p, d, q = param[0], param[1], param[2]
    # s_param = get_param.get('seasonal_order')
    # P, D, Q, S = s_param[0], s_param[1], s_param[2], s_param[3]
    p, d, q = 1, 1, 1
    P, D, Q, S = 1, 0, 1, 12

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Создание модели
    model = sm.tsa.statespace.SARIMAX(series,
                                      order=(p, d, q),
                                      seasonal_order=(P, D, Q, S),
                                      enforce_stationarity=False,
                                      enforce_invertibility=False)
    # обучение модели
    result = model.fit()
    st.toast("Обучения модели завершено!", icon="😍")

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🧹Очищенные данные",
     "🚗💨Динамика содержания СО2",
     "🛠️Диагностика модели"])

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=700):
        col1, col2 = st.columns([1,1])
        with col1:
            st.write('📶🧹Очищенные данные')
            st.write(series)
        with col2:
            st.write('🛠️Оптимальные параметры модели SARIMA')
            st.write('p=', p, ' d=', d, ' q=', q)
            st.write('P=', P, ' D=', D, ' Q=', Q, ' S=', S)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        # Формируем график динамики изменения временного ряда
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=series.index, y=series.values, name="Экспорт нефти"))
        # Обновить подписи осей
        fig.update_layout(xaxis_title="Дата",
                          yaxis_title="Уровень загрязнения",
                          title='📈🚗💨Динамика уровня загрязнения воздуха (СО2)',
                          xaxis_rangeslider_visible=True)
        st.plotly_chart(fig, theme=None)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=600, border=True):
        st.write('🛠️Параметры диагностики модели SARIMA')
        # График из result методом plot библиотеки statsmodels
        fig_d = result.plot_diagnostics(figsize=(10, 10))
        # Вывод графика в streamlit c matplotlib
        st.pyplot(fig_d, width="content")