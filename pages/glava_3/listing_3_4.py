import streamlit as st
import wbdata
from datetime import datetime

# Функция загрузки данных через API с кэшированием
@st.cache_data
def get_data_wb(indicator, countries, s_date, e_date):
    try:
        # Интервал дат - американский формат из строк
        start_d = datetime.strptime(s_date, '%d-%m-%Y')
        end_d = datetime.strptime(e_date, '%d-%m-%Y')
        # Извлечение данных из API Всемирного банка
        dfr = wbdata.get_dataframe(indicator,
                                    country=countries,
                                    date=(start_d, end_d),
                                    parse_dates=True)
        return dfr
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Создать контейнер
with st.container(width=500):
    # Задан показатель (ВВП в текущих долларах США)
    dic_indic = {'NY.GDP.MKTP.CD': 'GDP (current US$)'}
    # Страны (коды ISO для стран)
    list_country = ['CN', 'US', 'RUS', 'GB']
    # Интервал дат - европейский формат - строки
    d1_str = '01-01-2019'
    d2_str = '17-04-2025'
    # Использовать круговой спиннер
    with st.spinner(text='📥 Ждите, идет загрузка данных...', show_time=True):
        # Обращение к функции загрузки данных через API
        df = get_data_wb(dic_indic, list_country, d1_str, d2_str)
    st.subheader('🏦Валовый внутренний продукт по данным Всемирного банка, ($)')
    st.write('📆 За период с ', d1_str, ' по ', d2_str)
    st.dataframe(df)