import streamlit as st
import pandas as pd
import plotly.express as px

# Функция для загрузки данных
@st.cache_data
def get_data():
    # Имя файла
    name_json = 'csv/price_oil.json'
    # Чтение данных из файла json
    data = pd.read_json(name_json)
    return data

# Получение данных
df = get_data()

st.subheader('📥🧹Загрузка и очистка данных из файла JSON')
# Создаем вкладки
t1, t2, t3, t4 = st.tabs(
    ["📶 Сырые данные из JSON",
     "🔎Типы данных из JSON",
     "🧹📶 Очищенные данные",
     "📈 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных из JSON файла
    with st.container(width=600):
        st.write('📶Набор данных DataFrame из файла JSON')
        st.write(df)

# Вкладка с данными
with t2:
    # Контейнер для типов данных
    with st.container(width=250,  border=True):
        st.write('🔎Типы данных DataFrame')
        st.text(df.dtypes)

with t3:
    # Контейнер для данных после очистки
    with st.container(width=300):
        df = df['Close']
        st.write('🧹📶Набор данных после очистки')
        st.write(df)

with t4:
    # Контейнер для графика
    with st.container(width=800, border=True):
        fig = px.line(df, title="📈Динамика цены на нефть")
        fig.update_layout(xaxis_title='Годы', yaxis_title='Цена, $/баррель')
        st.plotly_chart(fig, theme=None)