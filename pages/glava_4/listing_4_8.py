import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def get_data():
    # Простой набор данных
    data1 = pd.DataFrame({
        'data_x': [1, 2, 3, 4, 5],
        'data_y': [10, 11, 12, 13, 14]})
    # Простой набор данных
    data2 = pd.DataFrame({
        'data_x': [1, 2, 3, 4, 5],
        'data_y': [30, 25, 20, 15, 10]})
    return data1, data2

st.subheader('📈График линий с интерфейсом Plotly Graph Objects')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "📈 График линий",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=400):
        col1, col2 = st.columns(2)
        # Создать dataframe
        df1, df2 = get_data()
        with col1:
            st.write('📶Набор данных df1')
            st.write(df1)
        with col2:
            st.write('📶Набор данных df2')
            st.write(df2)

# Создать объект - График (фигура)
fig = go.Figure()
# Добавить на график элемент (линию)
fig.add_trace(go.Scatter(x=df1['data_x'], y=df1['data_y'], name='Линия 1'))
fig.add_trace(go.Scatter(x=df2['data_x'], y=df2['data_y'], name='Линия 2'))
# Обновить макет
fig.update_layout(title='📈График двух линий с Plotly Graph Objects',
                  xaxis_title='Ось x',
                  yaxis_title='Ось y')

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=700, border=True):
        # Вывод графика
        st.plotly_chart(fig, theme=None)