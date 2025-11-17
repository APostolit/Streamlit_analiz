import streamlit as st
from pandas_datareader import wb

# Функция загрузки данных через API с кэшированием
@st.cache_data
def get_dr_wb(indic, countries, start, end):
    try:
        # Извлечение параметров из словаря
        ind_key = None
        for key in indic.keys():
            ind_key = key  # Ключ индикатора
        # Загрузка данных
        dat = wb.download(indicator=ind_key,
                          country=countries,
                          start=start,
                          end=end)
        # Изменение формы данных (сводная таблица)
        dfr = dat.reset_index()
        df_pivot = dfr.pivot(index='year', columns='country', values=ind_key)
        return df_pivot
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Создать контейнер
with st.container(width=600):
    # Задан показатель (Экспорт)
    dic_indic = {'NE.EXP.GNFS.ZS': 'Exports'}
    # Страны (коды ISO для стран)
    list_country = ['CN', 'US', 'RUS', 'GB']
    # Интервал дат
    d1_int = 2015
    d2_int = 2024
    # Использовать круговой спиннер
    with st.spinner(text="📥 Ждите, идет загрузка данных...", show_time=True):
        # Обращение к функции загрузки данных
        df_pivot1 = get_dr_wb(dic_indic, list_country, d1_int, d2_int)
    st.subheader('🏦Динамика экспорта стран по данным Всемирного банка')
    st.write('📆Сводная таблица за период с ', str(d1_int), ' по ', str(d2_int))
    st.dataframe(df_pivot1)