import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def get_data():
    # Простой набор данных
    data = pd.DataFrame({
        'data_x': [1, 2, 3, 4, 5],
        'data_y': [10, 11, 12, 13, 14],
    })
    return data

st.subheader('📈График линии с интерфейсом Plotly Graph Objects')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "📈 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=400):
        # Создать dataframe
        df = get_data()
        st.write('📶 Набор данных DataFrame')
        st.write(df)

# Создать объект - График (фигура)
fig = go.Figure()
# Добавить на график элемент (линию)
fig.add_trace(go.Scatter(x=df['data_x'], y=df['data_y']))
# Обновить макет
fig.update_layout(title='📈 График линии с Plotly Graph Objects',
                  xaxis_title='Ось x',
                  yaxis_title='Ось y')

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=700, border=True):
        # Вывод графика
        st.plotly_chart(fig, theme=None)