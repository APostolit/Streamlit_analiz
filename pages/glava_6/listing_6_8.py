import streamlit as st
from pandas_datareader import wb
import pandas as pd

# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(indic, countries, start, end):
    try:
        # Извлечение параметров из словаря
        ind_val = None
        ind_key = None
        for key in indic.keys():
            ind_key = key  # Ключ индикатора
        for val in indic.values():
            ind_val = val  # Значение ключа индикатора
        # Загрузка данных
        dat = wb.download(indicator=ind_key,
                          country=countries,
                          start=start,
                          end=end)
        # Изменение формы данных (сводная таблица)
        dfr = dat.reset_index()
        df_pivot = dfr.pivot(index='year', columns='country', values=ind_key)
        return dat, df_pivot, ind_val
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('📥🧹Загрузка и очистка данных из API Всемирного банка🏦')
st.markdown('##### 🌍➜]методом resample (с библиотекой pandas_datareader)')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🏦 Сырые данные",
     "📶🧹 Очищенные данные",
     "📈🏦 График",
     ])

# Индикатор (показатель - экспорт')
dic_indic = {'NE.EXP.GNFS.ZS': 'Exports'}
# Страны (коды ISO для стран)
list_country = ['CN', 'US', 'RUS', 'GB']
# Интервал дат
d1, d2 = 2015, 2023

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Запрос данных в API Всемирного банка
    df1, df, indic_val = get_data(dic_indic, list_country, d1, d2)

# Вкладка с данными
with t1:
    # Контейнер для данных data
    with st.container(width=300):
        st.write('📶Набор сырых данных')
        st.write(df1)

# Вкладка с данными
with t2:
    # Контейнер для данных df
    with st.container(width=500):
        st.write('📶🧹Набор очищенных данных')
        st.write(df)

# Формирование фигуры (графика)
fig = df.plot()
tit = '📈Экспорт стран за период: c ' + str(d1) + ' по ' + str(d2) + ' - ' + indic_val
# Формирование параметров графика
fig.update_layout(
    xaxis=dict(title="Годы"),
    yaxis=dict(title="Экспорт, трлн. $"),
    title=tit,
    hoverlabel=dict(font_size=20),  # Размера шрифта для данных
)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)