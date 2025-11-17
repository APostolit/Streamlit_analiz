import streamlit as st
import altair as alt
import pandas as pd
from numpy.random import default_rng as rng

st.subheader('👁️ Визуализация данных с элементом st.altair_chart')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "📈 Диаграмма Altair",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=400):
        df = pd.DataFrame(rng(0).standard_normal((60, 3)), columns=["a", "b", "c"])
        st.write('📶Набор данных DataFrame')
        st.write(df)

# Диаграмма с параметрами altair
chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.write('📈Диаграмма altair_chart с темой по умолчанию')
        st.altair_chart(chart)