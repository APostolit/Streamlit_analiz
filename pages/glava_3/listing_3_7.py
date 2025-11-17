import streamlit as st
import pandas_datareader.data as web
from datetime import datetime

# Функция загрузки данных через API с кэшированием
@st.cache_data
def get_dr_wb(firm, s, start, end):
    try:
        # Интервал дат - американский формат
        d1 = datetime.strptime(start, '%d-%m-%Y')
        d2 = datetime.strptime(end, '%d-%m-%Y')
        data = web.DataReader(firm, s, start=d1, end=d2).dropna()
        return data
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Создать контейнер
with st.container(width=600):
    # Интервал дат строки - европейский формат
    d1_str = '01-01-2024'
    d2_str = '17-04-2025'
    # Фирма
    list_firm = ['MSFT']
    # Источник данных
    sours = 'stooq'
    # Использовать круговой спиннер
    with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
        # Обращение к функции загрузки данных
        df = get_dr_wb(list_firm, sours, d1_str, d2_str)
    st.subheader('💰Динамика изменения стоимости акция по данным Stooq, ($)')
    st.write('📆За период с ', d1_str, ' по ', d2_str)
    st.dataframe(df)