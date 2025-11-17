import streamlit as st
import altair as alt
from vega_datasets import data

st.subheader('👁️ Задание темы для элемента st.altair_chart')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶 Набор данных DadaFrame",
     "📈 Диаграмма Altair с темами",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=800):
        # Набор данных из библиотеки vega_datasets
        source = data.cars()
        st.write('Набор данных source')
        st.write(source)

# Вкладка с графиком
with t2:
# Контейнер для графика
    with st.container(width=800, border=True):
        # Диаграмма с параметрами altair
        chart = (alt.Chart(source).mark_circle().encode(
            x=alt.X('Horsepower',
                    title='Мощность двигателя (л.с)'),
            y=alt.Y('Miles_per_Gallon',
                    title='Расход топлива (мили/галон)'),
            color='Origin', )
                 .interactive())

        st.write('📈Диаграмма altair_chart с разными темами')
        # Вкладки страницы приложения
        tab1, tab2 = st.tabs(["🤫Тема Streamlit (default)", "🌠Тема Altair"])
        with tab1:
            # Диаграмма с темой Streamlit (по умолчанию).
            st.altair_chart(chart, theme="streamlit", use_container_width=True)
        with tab2:
            # Диаграмма с нативной темой Altair
            st.altair_chart(chart, theme=None, use_container_width=True)