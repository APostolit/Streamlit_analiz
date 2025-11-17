import streamlit as st
import pandas as pd
from datetime import datetime
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

# Игнорировать предупреждения
warnings.filterwarnings("ignore")
# Подключить matplotlib к pandas
pd.options.plotting.backend = 'matplotlib'

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Путь к исходному csv файлу
        name_csv = 'csv/oil_exports.csv'
        # Запрос данных в БД
        ser = pd.read_csv(name_csv, header=0, delimiter=',')
        ser = ser.loc[ser['Oil Type'] == 'Total'].filter(['Period', 'Volume (bbl/d)'])
        ser['Period'] = ser['Period'].transform(lambda x: datetime.strptime(x, '%m/%d/%Y'))
        ser.set_index(keys='Period', drop=True, inplace=True)
        ser = ser.squeeze(axis=1)
        return ser
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🛠️ Анализ и оптимизация параметров модели ARIMA')
st.markdown('##### 🛢️ Данные CSV-файла (динамика экспорта нефти)')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    series = get_data()

with st.spinner(text="Идет подбор параметров модели...", show_time=True):
    # Подбор оптимальных параметров модели с auto_arima
    # order = pm.auto_arima(series, max_order=5, seasonal=True, m=12)
    # get_param = order.get_params()
    # param = get_param.get('order')
    # p, d, q = param[0], param[1], param[2]
    # Оптимальные параметры модели (рассчитаны заранее)
    p, d, q = 2, 1, 2

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Создание модели
    model = ARIMA(series, order=(p, d, q))
    # обучение модели
    result: ARIMAResults = model.fit()
    st.toast("Обучения модели завершено!", icon="😍")

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🧹Очищенные данные",
     "📈️🛢️График динамики экспорта",
     "📈️🛠️Диагностика модели ARIMA"])

# Вкладка с графиком
with t1:
    # Контейнер для данных df
    with st.container(width=600):
        col1, col2 = st.columns([1,1])
        with col1:
            st.write('📶🧹Исходный набор данных series')
            st.write(series)
        with col2:
            st.write('🛠️Оптимальные параметры модели')
            st.write('p=', p, ' d=', d, ' q=', q)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        # Формируем график динамики экспорта нефти
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=series.index, y=series.values, name="Экспорт нефти"))
        # Обновить подписи осей
        fig.update_layout(xaxis_title="Дата",
                          yaxis_title="Экспорт нефти",
                          title='📈️🛢️ Динамика экспорта нефти',
                          xaxis_rangeslider_visible=True)
        st.plotly_chart(fig, theme=None)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=700, border=True):
        st.write('📈 Параметры диагностики модели ARIMA')
        # График из result методом plot библиотеки statsmodels
        fig_d = result.plot_diagnostics(figsize=(10, 8))
        # Вывод графика в streamlit c matplotlib
        st.pyplot(fig_d, width="content")