import streamlit as st
import pandas as pd
import yfinance as yf

# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(tic, p):
    try:
        ticker = yf.Ticker(tic)
        df = ticker.history(period=p)
        data = df
        # Убрать время из индекса
        df.index = df.index.date
        df = df['Close']
        return data, df
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('📥🧹Загрузка и очистка данных из API Yahoo Finance🏬')
st.markdown('##### 🛢Динамики стоимости нефти (с библиотекой yfinance)')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶 Сырые данные",
     "📶🧹 Очищенные данные",
     "📈 График",
     ])

# Тикер - нефть
ticker = 'CL=F'
# Интервал дат 5 лет
period = '5y'

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    data_1, df_1 = get_data(ticker, period)

# Вкладка с данными
with t1:
    # Контейнер для полных данных data_1
    with st.container(width=600):
        st.write('📶Набор сырых данных API Yahoo Finance')
        st.write(data_1)

# Вкладка с данными
with t2:
    # Контейнер для усеченных данных df
    with st.container(width=200):
        st.write('📶🧹Набор очищенных данных из API Yahoo Finance')
        st.write(df_1)

# Формирование фигуры (графика)
fig = df_1.plot(title="📈Динамики стоимости нефти за последние 5 лет",
                labels=dict(index="Дата",
                            value="Стоимость нефти",
                            variable="Сырая нефть"))

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)