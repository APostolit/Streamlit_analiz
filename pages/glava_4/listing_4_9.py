import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Функция для загрузки данных
@st.cache_data
def get_data():
    # Набор данных для столбчатой диаграммы
    data1 = pd.DataFrame({
        'data_x': [2021, 2022, 2023, 2024, 2025],
        'data_y': [10, 20, 30, 40, 50]})

    # Набор данных для круговой диаграммы
    data2 = pd.DataFrame({
        'labels': ['Ноутбуки', 'Телевизоры', 'Мониторы'],
        'values': [50, 20, 30]})

    # Набор данных для линии
    data3 = pd.DataFrame({
        'data_x': ['2021', '2022', '2023', '2024', '2025'],
        'data_y': [10, 11, 12, 13, 14]})

    # Набор данных для линии
    data4 = pd.DataFrame({
        'data_x': ['2021', '2022', '2023', '2024', '2025'],
        'data_y': [300, 250, 200, 150, 100]})
    return data1, data2, data3, data4

st.subheader('📈Сетка графиков с интерфейсом Plotly Graph Objects')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "📈 Сетка графиков",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=600):
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        # Создать dataframe
        df1, df2, df3, df4 = get_data()
        with col1:
            st.write('📶Набор данных df1')
            st.write(df1)
        with col2:
            st.write('📶Набор данных df2')
            st.write(df3)
        with col3:
            st.write('📶Набор данных df3')
            st.write(df1)
        with col4:
            st.write('📶Набор данных df4')
            st.write(df4)

# Формируем 4 области для графиков
fig = make_subplots(rows=2, cols=2,
                    specs=[[{'type': 'xy'}, {'type': 'domain'}],
                            [{'type': 'xy'}, {'type': 'xy'}]],
                    subplot_titles=("👨🏻‍🤝‍👨🏽Динамика роста населения",
                                    "🛍️Структура продаж",
                                    "📈Динамика доходов",
                                    "📉Динамика убытков"))
# Добавить на график элементы
fig.add_trace(go.Bar(x=df1['data_x'], y=df1['data_y'], name='Население'), row=1, col=1)
fig.add_trace(go.Pie(values=df2['values'], labels=df2['labels']), row=1, col=2)
fig.add_trace(go.Scatter(x=df3['data_x'], y=df3['data_y'], name='Доход'), row=2, col=1)
fig.add_trace(go.Scatter(x=df4['data_x'], y=df4['data_y'], name='Убытки'), row=2, col=2)

# Обновить оси x
fig.update_xaxes(title_text="Дата", row=1, col=1)
fig.update_xaxes(title_text="Дата", row=2, col=1)
fig.update_xaxes(title_text="Дата", row=2, col=2)

# Обновить оси Y
fig.update_yaxes(title_text="Население, млн.ч.", row=1, col=1)
fig.update_yaxes(title_text="Доходы,руб.", row=2, col=1)
fig.update_yaxes(title_text="Убытки,руб.", row=2, col=2)

# Обновить макет графика
fig.update_layout(autosize=False,
                  width=800,
                  height=700,
                  hoverlabel=dict(font_size=10))

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)