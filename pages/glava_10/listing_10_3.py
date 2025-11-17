import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import json

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(indicator_id, group_ids=None, years=None):
    try:
        # Значения параметров по умолчанию
        if years is None:
            years = []
        if group_ids is None:
            group_ids = []

        # Фрагмент заголовка URL адреса
        head_url = "https://www.imf.org/external/datamapper/api/v1"
        # Фрагментов URL адреса с географической группой
        list_groups = "/".join(group_ids)
        # Фрагментов URL адреса с периодом
        list_period = "?periods=" + ",".join(years)
        # Полный URL адрес запроса
        url = f"{head_url}/{indicator_id}/{list_groups}{list_period}"

        # Запрос к API
        response = requests.get(url=url)

        # Извлечение текста из формата JSON
        resp_txt = json.loads(response.text)

        # Разбор полученных данных
        response_values = resp_txt.get("values")
        if not response_values:
            return pd.DataFrame()

        # Создание DateFrame
        indicator_df = pd.DataFrame.from_records(
            resp_txt["values"][indicator_id]).sort_index()
        return indicator_df
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('#### 🌍Загрузка данных из API МВФ по коду индикатора🏦')
st.markdown('##### 🌐ВВП в разрезе стран (индикатор NGDPD)')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    ind = 'NGDPD'  # ВВП в текущих ценах
    # Список стран
    list_group = ['RUS','FRA', 'DEU']
    # Период числовой (годы 2015-2024)
    start, end = 2015, 2025
    list_num = list(range(start, end))
    # Создать строковый список лет
    list_years = [str(element) for element in list_num]
    # Загрузка данных
    df = get_data(ind, list_group, list_years)

# Создаем вкладки для данных
t1, t2 = st.tabs([
    "📶Загруженные данные",
    "📈График"
    ])

# Вкладка с данными
with t1:
    title = 'ВВП стран за период c ' + str(start) + ' по ' + str(end - 1)
    st.markdown('#### 📶 ' + title)
    # Создать контейнер
    with st.container(width=600):
        st.write(df)

# Создать объект - График (фигура)
fig = go.Figure()
# Добавить на график элементы (линии)
fig.add_trace(go.Scatter(x=df.index, y=df['DEU'], name='Германия'))
fig.add_trace(go.Scatter(x=df.index, y=df['FRA'], name='Франция'))
fig.add_trace(go.Scatter(x=df.index, y=df['RUS'], name='Россия'))
fig.update_layout(xaxis_title='Годы',
                  yaxis_title='ВВП стран',
                  title=title + '' + ', id индикатора-' + ind)

# Вкладка с графиком
with t2:
    st.markdown('#### 📈 ' + title)
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)