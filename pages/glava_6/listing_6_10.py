import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime as dt

# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(firma, start, end):
    try:
        # Даты в американский формат
        d1 = dt.strptime(start, '%d-%m-%Y')
        d2 = dt.strptime(end, '%d-%m-%Y')
        # Загрузка данных
        data = yf.download(firma, start=d1, end=d2)
        df = data['Close']
        return data, df
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('📥🧹Загрузка и очистка данных из API Yahoo Finance🏬')
st.markdown('##### 💹 Котировка акций (с библиотекой yfinance)')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶Сырые данные",
     "📶🧹 Очищенные данные",
     "📈 График",
     ])

# Фирмы (тикеры)
list_firm = ['AAPL', 'GOOGL']
# Интервал дат строки - европейский формат
d1_str = '01-01-2024'
d2_str = '17-04-2025'

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Запрос данных
    data_1, df_1 = get_data(list_firm, d1_str, d2_str)

# Вкладка с данными
with t1:
    # Контейнер для полных данных data_1
    with st.container(width=800):
        st.write('📶Набор сырых данных из API Yahoo Finance')
        st.write(data_1)

# Вкладка с данными
with t2:
    # Контейнер для усеченных данных df
    with st.container(width=500):
        st.write('📶🧹Набор очищенных данных из API Yahoo Finance)')
        st.write(df_1)

# Формирование фигуры (графика)
fig = df_1.plot()
# Формирование параметров графика
fig.update_layout(
    xaxis=dict(title="Даты"),
    yaxis=dict(title="Стоимость акций, $"),
    title='📈Изменение стоимости акций за период: c ' + d1_str + ' по ' + d2_str,
    hoverlabel=dict(font_size=20),  # Размера шрифта для данных
)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)