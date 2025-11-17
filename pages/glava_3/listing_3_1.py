import streamlit as st
import requests

# Функция загрузки данных через API с кэшированием
@st.cache_data
def api_call():
    data_api = requests.get("https://randomuser.me/api/")
    return data_api

# Создать контейнер
cont = st.container(width=500)
with cont:
    # Использовать круговой спиннер
    with st.spinner(text="Ждите, идет загрузка данных...", show_time=True):
        try:
            # Обращение к функции загрузки данных через API
            data = api_call()
            st.subheader('Признак успешности загрузки данных')
            st.write(data)
            st.subheader('Данные, загруженные через API')
            st.write(data.text)
        except Exception as e:
            st.error(f'Ошибка загрузки данных: {e}', icon="🚨")