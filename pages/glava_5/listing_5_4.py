import streamlit as st
import plotly.graph_objects as go

st.subheader('👁️ Визуализация данных с элементом st.plotly_chart')

# Контейнер для графика
with st.container(width=700, border=True):
    # Формирование графика с библиотекой Plotly
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[1, 3, 2, 5, 4])
    )
    fig.update_layout(
        xaxis_title="Ось X",
        yaxis_title="Ось Y",
        title="Заголовок графика"
    )
    st.write('📈График plotly.graph_objects с элементом st.plotly_chart')
    st.plotly_chart(fig)