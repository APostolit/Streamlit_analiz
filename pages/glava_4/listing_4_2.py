import streamlit as st
import pandas as pd
import plotly.express as px

def get_data():
    df = pd.DataFrame({'X': [10, 20, 30, 40],
                       'Y': [350, 480, 550, 680]})
    return df

st.subheader('📈Графики с элементом st.plotly_char')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶Набор данных DadaFrame",
     "📈График с st.plotly_char"
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=200):
        # Создать dataframe
        data = get_data()
        st.write('📶Набор данных DataFrame')
        st.write(data)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=600, border=True):
        # Создать диаграмму с st.plotly_chart
        fig = px.line(data, x='X', y='Y',
                      title="📈Линейная диаграмма st.plotly_chart с темой Plotly Express")
        fig.update_layout(xaxis_title='Ось X', yaxis_title='Ось X')
        st.plotly_chart(fig, theme=None)