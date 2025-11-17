import streamlit as st
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pmdarima as pm
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Путь к исходному csv файлу
        path_csv = 'csv/passengers.csv'
        # Загрузка данных из CSV файла
        df_1 = pd.read_csv(path_csv)
        # Превратим дату в индекс
        df_1.set_index('Month', inplace=True)
        df_1.index = pd.to_datetime(df_1.index)
        # Экзогенная переменная
        df_1['month_index'] = df_1.index.month
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🛠️ Анализ временного ряда и оптимизация модели SARIMAX')
st.markdown('##### 🚍👬Данные о пассажиропотоках из файла CSV')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    df = get_data()

# Создаем вкладки
t1, t2, t3, t4 = st.tabs(
    ["📶🧹Очищенные данные",
     "🚍👬Экзогенные данные",
     "📶️🔮Прогноз",
     "📈🛠️️Оценка модели"])

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=350):
        st.write('📶🧹Исходный набор df с экзогенными данными')
        st.write(df)

with st.spinner(text="Идет подбор параметров модели...", show_time=True):
    # Поиск оптимальных параметров модели
    param = pm.auto_arima(df[['Passengers']], exogenous=df[['month_index']],
                          start_p=1, start_q=1,
                          test='adf',
                          max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True,
                          d=1, D=1,
                          trace=False,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)
    # Оптимальные параметры модели
    get_param = param.get_params()
    param = get_param.get('order')
    p, d, q = param[0], param[1], param[2]
    s_param = get_param.get('seasonal_order')
    P, D, Q, S = s_param[0], s_param[1], s_param[2], s_param[3]

with st.spinner(text="Идет обучение модели...", show_time=True):
    # обучающая выборка будет включать данные за первые 9 лет
    train = df[:'2023-12']
    # тестовая выборка будет включать данные за последний год
    test = df['2024-01':]
    # Создание и обучение модели SARIMAX на обучающей выборке
    model = SARIMAX(train['Passengers'], exog=train['month_index'],
                    order=(p, d, q),
                    seasonal_order=(P, D, Q, S))
    results = model.fit()
    st.toast("Обучения модели завершено!", icon="😍")

# Формируем график экзогенных данных
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['month_index']))
fig.update_layout(title='🚍👬Экзогенные данные',
                  xaxis_title="Дата",
                  yaxis_title="Номер месяца",
                  autosize=False,
                  hoverlabel=dict(font_size=15))

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)

# Даты оценки модели на тестовой выборке
start_date = '2024-01-01'
end_date = '2024-12-01'
# Применим метод .predict() - прогноз
predict = results.predict(start_date, end_date, exog=test['month_index'])
# Добавим прогноз в качестве столбца в df
df['predict'] = predict

# Результаты расчета прогноза
df1 = df[df.index >= pd.to_datetime(start_date)]

# Расчет ошибки прогноза
actual = df1['Passengers']
predicted = df1['predict']
mape = np.mean(np.abs((actual - predicted) / actual)) * 100
mape = round(mape, 2)

# Вкладка с данными
with t3:
    # Контейнер для данных df
    with st.container(width=800):
        col1, col2 = st.columns([1.1, 2.9])
        with col1:
            st.write('🛠️Параметры модели')
            st.write('p=', p, ' d=', d, ' q=', q)
            st.write('P=', P, ' D=', D, ' Q=', Q, 'S=', S)
            st.write('🔮Ошибка прогноза', mape, '%')
        with col2:
            st.write('📶️🔮Результаты расчета прогноза')
            st.write(df1)

# Формируем график прогноза по данным тестовой выборки
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Passengers'], name="Наблюдение"))
fig.add_trace(go.Scatter(x=df.index, y=df['predict'], name="Прогноз"))
fig.update_layout(title='📈🛠️Оценка модели по тестовым данным',
                  xaxis_title="Дата",
                  yaxis_title="Пассажиропоток, тыс.чел.",
                  autosize=False,
                  xaxis_rangeslider_visible=True,
                  hoverlabel=dict(font_size=15))

# Вкладка с графиком
with t4:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)