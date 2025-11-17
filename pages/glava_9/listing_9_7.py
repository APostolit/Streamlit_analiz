import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objects as go

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Имя файла
        path_csv = 'csv/data_s.csv'
        # Чтение данных из файла csv
        df_1 = pd.read_csv(path_csv)
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('🎁 Прогнозирование продаж торгового центра')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    df = get_data()

 # Создаем группы вкладок
tabs1, tabs2 = st.tabs([
    "📶Данные",
    "📈Графики",
])

# Вкладки с данными
with tabs1:
    # Создаем вкладки для данных
    t1, t2 = st.tabs(["📶🛒Данные о продаже товаров",
                      "📶🔮Данные для Prophet"])
# Вкладки с графиками
with tabs2:
    # Создаем вкладки для графиков
    t3, t4, t5 = st.tabs(["📈🛒Динамика продаж",
                          "📈🔮Прогноз с Prophet",
                          "💹❄️Тренд и сезонность"])

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🛒Исходный набор данных о продажах')
        st.write(df)

# Создать объект - График (фигура)
fig = go.Figure()
# Добавить на график элемент (линию)
fig.add_trace(go.Scatter(x=df['Date'], y=df['Profit']))
# Обновить макет
fig.update_layout(title='📈🛒 Динамика продаж товаров',
                    xaxis_title='Дата',
                    yaxis_title='Сумма')
# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)

# Задаем имена колонок под требования Prophet
df.rename(columns={'Date': 'ds', 'Profit': 'y'}, inplace=True)

# Вкладка с данными
with t2:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🔮Набор данных для Prophet')
        st.write(df)

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Создаем модель
    model = Prophet(yearly_seasonality=True)
    # Обучаем модель
    model.fit(df)
    st.toast("Обучения модели завершено!", icon="😍")

# Делаем прогноз на 365 дней
predict = 365
future = model.make_future_dataframe(periods=predict, freq='D')
forecast = model.predict(future)

# формируем график
fig = plot_plotly(model, forecast)
fig.update_layout(title='📈🔮Динамика и прогноз продаж товаров',
                    xaxis_title='Дата',
                    yaxis_title='Сумма')
# Вкладка с графиком
with t4:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)

# Вкладка с графиком
with t5:
    # Контейнер для графика
    with st.container(width=800, border=True):
        # Графики компонент (тренда и сезонности)
        fig = plot_components_plotly(model, forecast)
        fig.update_layout(title='📈❄️Тренд и сезонности временного ряда')
        st.plotly_chart(fig, theme=None)