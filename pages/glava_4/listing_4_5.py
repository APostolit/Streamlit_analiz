import streamlit as st
import plotly.express as px

# Функция для загрузки данных
@st.cache_data
def get_data():
    # Набор данных с параметрами цветка Ирис разных видов
    data = px.data.iris()
    return data

st.subheader('📈⋆.˚Фасетные сетки для группы графиков с методом facet_col')
# Создаем вкладки
t1, t2 = st.tabs(
    ["📶Набор данных DadaFrame",
     "📈⋆.˚ Фасетная сетки",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных
    with st.container(width=600):
        # Создать dataframe
        df = get_data()
        st.write('📶Набор данных DataFrame')
        st.write(df)

# Графики с использованием сетки facet_col
fig = px.scatter(df,
                 x='sepal_width',
                 y='sepal_length',
                 color='species',
                 facet_col='species',
                 title='📈⋆.˚Соотношение ширины и длины чашелистиков для видов цветка Ирис',
                 )
# Подписи к осям x сетки графиков
fig.update_xaxes(title_text="Ширина", row=1, col=1)
fig.update_xaxes(title_text="Ширина", row=1, col=2)
fig.update_xaxes(title_text="Ширина", row=1, col=3)
# Обновление макета
fig.update_layout(legend_title="Виды Ириса", yaxis_title='Длина')

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)