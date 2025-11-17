import streamlit as st
import matplotlib.pyplot as plt
from numpy.random import default_rng as rng

st.subheader('📊Графики с библиотекой Matplotlib')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "📊 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=200):
        # Данные для гистограммы
        data = rng(0).normal(1, 1, size=100)
        st.write('📶Набор данных data')
        st.write(data)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=500, border=True):
        # Формирование гистограммы с matplotlib
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.hist(data, bins=20)
        st.write('📊График с библиотекой matplotlib')
        st.pyplot(fig, width="content")