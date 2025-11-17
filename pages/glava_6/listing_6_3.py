import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Загрузка данных из Yahoo Finance
        tick = 'CL=F'
        ticker = yf.Ticker(tick)
        df = ticker.history(period='5y')
        # Запись набора данных в строковый объект
        data_json = df.to_json(orient='index')
        # Чтение набора данных из строкового объекта
        df_str = pd.read_json(data_json, orient='index')
        # Выбор из набора данных одного столбца
        df_str = df_str['Close']
        return df, df_str
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Получение данных
    df, df_1 = get_data()

st.subheader('📥🧹Загрузка и очистка данных от Yahoo Finance')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶 Сырые данные Yahoo Finance",
     "🧹📶 Очищенные данные",
     "📈 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных из df
    with st.container(width=600):
        st.write('📶Сырые данные от Yahoo Finance')
        st.write(df)

# Вкладка с данными
with t2:
    # Контейнер для данных из df_1
    with st.container(width=300):
        st.write('🧹📶Очищенный набор данных из строки')
        st.write(df_1)


# Создать объект - График (фигура)
fig = go.Figure()
# Добавить на график элемент (линию)
fig.add_trace(go.Scatter(x=df_1.index, y=df_1.values))
fig = px.line(df_1)
fig.update_layout(xaxis_title='Годы', yaxis_title='Цена, $/баррель',
                  title='📈Цена нефти за последние 5 лет по данным Yahoo Finance')

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)