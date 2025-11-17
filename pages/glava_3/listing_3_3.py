import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# Функция загрузки данных через API с кэшированием
@st.cache_data
def api_call(d_start, d_end):
    try:
        # Перевод дат в строки европейский формат
        d1_str = d_start.strftime("%d-%m-%Y")
        d2_str = d_end.strftime("%d-%m-%Y")
        # Формирование URL адреса
        url_cb = 'http://www.cbr.ru/scripts/xml_metall.asp?'
        date_req1 = 'date_req1='
        date_req2 = '&date_req2='
        url = url_cb + date_req1 + d1_str + date_req2 + d2_str
        # Запрос к API ЦБ
        data_api = pd.read_xml(url)
        return data_api
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Создать контейнер
with st.container(width=500):
    # Формирование интервала дат
    d1 = date.today() - relativedelta(years=5)
    d2 = date.today()
    # Использовать круговой спиннер
    with st.spinner(text="📥 Ждите, идет загрузка данных...", show_time=True):
        # Обращение к функции загрузки данных через API
        data = api_call(d1, d2)
    st.subheader('🏛️Динамика цен на драгметаллы по данным Центробанка РФ')
    st.write('📆 За период с ', d1, ' по ', d2)
    st.dataframe(data)