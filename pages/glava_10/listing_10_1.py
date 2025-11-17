import streamlit as st
import pandas as pd
import requests
import json

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # URL адреса для получения списка доступных индикаторов
        url = "https://www.imf.org/external/datamapper/api/v1/indicators"
        # Запрос к API
        response = requests.get(url)
        # Извлечение текста из формата JSON
        ind_txt = json.loads(response.text)
        # Разбор полученных данных
        indicators = [
            {"id": key, **values} for key, values in ind_txt["indicators"].items()
        ]
        # Создание DataFrame
        ind_df = pd.DataFrame.from_records(indicators)
        return ind_df
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🌍Список индикаторов (экономических показателей) в API МВФ🏦')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    df = get_data()

# Создаем вкладки для данных
t1, t2 = st.tabs([
    "📃Столбцы набора данных",
    "📶Список индикаторов"
    ])

# Вкладка с данными
with t1:
    st.markdown('##### 📖Имена столбцов')
    # Создать контейнер
    with st.container(width=200):
        # Series из словаря
        st.write(df.columns)

# Вкладка с данными
with t2:
    st.markdown('#### 📶 Список индикаторов международного валютного фонда (IMF)')
    # Создать контейнер
    with st.container(width=800):
        # Series из списка
        st.write(df)