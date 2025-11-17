import streamlit as st
import plotly.express as px

# Функция для загрузки данных
@st.cache_data
def get_data():
    # Набор данных с параметрами цветка Ирис разных видов
    data = px.data.iris()
    return data

st.subheader('📈Графики с Plotly Express')
# Создаем вкладки
t1, t2, t3, t4 = st.tabs(
    ["📶Набор данных DadaFrame",
     "📈График 1",
     "📈График 2",
     "📈График 3",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=600):
        # Создать dataframe
        df = get_data()
        st.write('📶Набор данных DataFrame')
        st.write(df)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        # График ширины чашелистика (одним цветом)
        fig_1 = px.line(df, y="sepal_width",
                        title="📈 Ширины чашелистика цветка Ирис")
        st.plotly_chart(fig_1, theme=None)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        fig_2 = px.line(df, y="sepal_width", line_group='species',
                        title="📈 С разделением сортов цветка (разрывом линий)")
        st.plotly_chart(fig_2, theme=None)

# Вкладка с графиком
with t4:
    # Контейнер для графика 3
    with st.container(width=800, border=True):
        fig_3 = px.line(df, y="sepal_width", line_dash='species', color='species',
                        title="📈 С разделением сортов цветка (линии разного типа и цвета)")
        st.plotly_chart(fig_3, theme=None)