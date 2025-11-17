import pandas as pd
import pydeck as pdk
import streamlit as st
from numpy.random import default_rng as rng

st.subheader('👁️🌍Карты с библиотекой PyDeck и st.pydeck_chart')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "🌍 Карта с PyDeck",
     ])

# Вкладка с данными
with t1:
    with st.container(width=300, border=True):
        # Сгенерировать данные
        df = pd.DataFrame(
            rng(0).standard_normal((100, 2)) / [60, 60] + [55.7522, 37.6156],
            columns=["lat", "lon"])
        st.write('📶Набор данных df')
        st.write(df)


# Создать объект pydeck
fig = pdk.Deck(
    map_style=None,  # Тема Streamlit
    initial_view_state=pdk.ViewState(
        latitude=55.7522,
        longitude=37.6156,
        zoom=11,
        pitch=50, ),
    layers=[
        pdk.Layer(
            type="HexagonLayer",
            data=df,
            get_position="[lon, lat]",
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 500],
            pickable=True,
            extruded=True, ),
        pdk.Layer(
            type="ScatterplotLayer",
            data=df,
            get_position="[lon, lat]",
            get_color="[200, 30, 0, 160]",
            get_radius=200, ),
    ],
)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.write('🌍Карта с библиотекой PyDeck и элементом st.pydeck_chart')
        st.pydeck_chart(fig)