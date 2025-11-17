import streamlit as st
import pandas as pd

def get_data():
    df = pd.DataFrame({'X': [10, 20, 30, 40],
                       'Y': [350, 480, 550, 680]}
                      )
    return df

st.subheader('📈Графики с элементом st.line_chart')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶Набор данных DadaFrame",
    "📈График с st.line_chart"
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=200):
        # Создать dataframe
        data = get_data()
        st.write('📶Набор данных DataFrame')
        st.dataframe(data)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=500, border=True):
        # Создать диаграмму с st.line_chart
        st.write('📈Линейная диаграмма st.line_chart с темой Streamlit')
        st.line_chart(data=data, x='X', y='Y',
                      x_label='Ось X', y_label='Ось X')