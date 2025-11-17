import streamlit as st
import pandas as pd
import wbdata
from datetime import datetime

# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(indicator, countries, s_date, e_date):
    try:
        # Интервал дат - американский формат из строк
        start_d = datetime.strptime(s_date, '%d-%m-%Y')
        end_d = datetime.strptime(e_date, '%d-%m-%Y')
        # Извлечение данных из API Всемирного банка
        dfr = wbdata.get_dataframe(indicator,
                                   country=countries,
                                   date=(start_d, end_d),
                                   parse_dates=True)
        # Измените форму данных
        dfr = dfr.reset_index()
        df_pivot = dfr.pivot(index='date', columns='country', values='GDP (current US$)')
        return dfr, df_pivot
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('📥🧹Загрузка и очистка данных из API Всемирного банка🏦')
st.markdown('##### 🏥 Динамика ВВП стран (с библиотекой wbdata)')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🏦 Сырые данные",
     "📶🏦 Очищенные данные",
     "📈🏦 График",
     ])

# Индикатор (показатель - ВВП в текущих долларах США)
dic_indic = {'NY.GDP.MKTP.CD': 'GDP (current US$)'}
# Список стран (коды ISO для стран)
list_country = ['CN', 'US', 'RUS', 'GB']
# Интервал дат, европейский формат, строки
d1_str = '01-01-1990'
d2_str = '17-04-2025'

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Запрос данных в API Всемирного банка
    df1, df = get_data(dic_indic, list_country, d1_str, d2_str)

# Вкладка с данными
with t1:
    # Контейнер для данных dfr
    with st.container(width=700):
        st.write('🏦Сырые данные из API Всемирного банка')
        st.write(df1)

# Вкладка с данными
with t2:
    # Контейнер для данных df
    with st.container(width=700):
        st.write('🏦Очищенные данные из API Всемирного банка')
        st.write(df)

# Создать объект - График (фигура)
fig = df.plot()
# Формирование параметров графика
fig.update_layout(
    xaxis=dict(title="Годы"),
    yaxis=dict(title="ВВП, трлн. $"),
    title='🏦Динамика ВВП стран за период: c ' + d1_str + ' по ' + d2_str,
    hoverlabel=dict(font_size=15),  # Размера шрифта для данных
)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)