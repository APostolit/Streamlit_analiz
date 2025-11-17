import streamlit as st
import pandas as pd

# Функция загрузки данных через API с кэшированием
@st.cache_data
def api_call(d_start, d_end):
    try:
        url_cb = 'https://www.cbr.ru/scripts/XML_dynamic.asp?'
        date_req1 = 'date_req1='
        date_req2 = '&date_req2='
        VAL_NM_RQ = '&VAL_NM_RQ='
        kod_val = 'R01235'
        url = url_cb + date_req1 + d_start + date_req2 + d_end + VAL_NM_RQ + kod_val
        # Запрос к API ЦБ
        data_api = pd.read_xml(url)
        return data_api
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Создать контейнер
with st.container(width=500):
    # Даты начала и конца периода
    d1 = '01/01/2020'
    d2 = '12/04/2025'
    # Использовать круговой спиннер
    with st.spinner(text="📥 Ждите, идет загрузка данных...", show_time=True):
        # Обращение к функции загрузки данных через API
        data = api_call(d1, d2)
    st.subheader('️🏛️Динамика курса (руб./$) по данным Центробанка РФ')
    st.write('📆 За период с ', d1, ' по ', d2)
    st.dataframe(data)