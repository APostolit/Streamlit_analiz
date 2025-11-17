import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng

st.subheader('🌍 Визуализация данных с элементом st.map')
# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "🌍🔴 Карта с точками одного разера",
     "🌍●🔴 Карта с разными точками",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=800):
        # Координаты точек в районе г. Москва
        df1 = pd.DataFrame(
            rng(0).standard_normal((100, 2)) / [50, 50] + [55.7522, 37.6156],
            columns=["lat", "lon"],)

        # Координаты точек в районе г. Москва
        df2 = pd.DataFrame(
            {
                "col1": rng(0).standard_normal(100) / 50 + 55.7522,
                "col2": rng(1).standard_normal(100) / 50 + 37.6156,
                "col3": rng(2).standard_normal(100) * 100,
                "col4": rng(3).standard_normal((100, 4)).tolist(),
            }
        )

        col1, col2 = st.columns([1, 3])
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
        st.write('🌍Положение точек на карте г. Москва с элементом st.map_chart')
        st.map(df1)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.write('🌍Карта г. Москва с точками разных цветов и размеров')
        st.map(df2, latitude="col1", longitude="col2", size="col3", color="col4")