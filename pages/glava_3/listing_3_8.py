import streamlit as st
import yfinance as yf
from datetime import datetime as dt

# Функция загрузки данных через API с кэшированием
@st.cache_data
def get_data(firma, start, end):
    try:
        # Даты в американский формат
        d1 = dt.strptime(start, '%d-%m-%Y')
        d2 = dt.strptime(end, '%d-%m-%Y')
        # Загрузка данных
        date = yf.download(firma, start=d1, end=d2,  auto_adjust=True)
        return date
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Создать контейнер
with st.container(width=600):
    # Интервал дат
    d1_str = '01-01-2025'
    d2_str = '17-04-2025'
    # Фирмы
    list_firm = ['AAPL', 'GOOGL']

    # Использовать круговой спиннер
    with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
        # Обращение к функции загрузки данных
        df = get_data(list_firm, d1_str, d2_str)

    st.subheader('💰Динамика изменения стоимости акция по данным Yahoo Finance, ($)')
    st.write('📆За период с ', d1_str, ' по ', d2_str)
    st.dataframe(df)
