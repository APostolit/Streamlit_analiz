import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng

st.subheader('👀Диаграмма рассеяния с элементом st.scatter_chart')
# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "🟢🔴 Диаграмма с точками одного размера",
     "●🔴 Диаграмма с разными точками",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=600):
        # Создание набора данных df1
        df1 = pd.DataFrame(rng(1).standard_normal((10, 3)),
                          columns=["a", "b", "c"])

        # Создание набора данных df2
        df2 = pd.DataFrame(
            rng(1).standard_normal((15, 3)), columns=["col1", "col2", "col3"])
        df2["col4"] = rng(0).choice(["a", "b", "c"], 15)

        # Создать колонки
        col1, col2 = st.columns(2)
        with col1:
            st.write('📶Набор данных df1')
            st.write(df1)
        with col2:
            st.write('📶Набор данных df2')
            st.write(df2)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.write('🟢🔴Диаграмма st.scatter_chart с точками одного размера')
        st.scatter_chart(df1)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.write('●🔴 Диаграмма st.scatter_chart с точками разного размера и цвета')
        st.scatter_chart(df2, x="col1", y="col2", color="col4", size="col3")