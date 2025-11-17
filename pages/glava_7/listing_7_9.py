import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas_datareader.data as web
import plotly.graph_objects as go

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(d1, d2, firm, sours):
    try:
        # Загрузка данных из API Stooq
        data_1 = web.DataReader(firm, sours, start=d1, end=d2)
        # Восстановление пропущенных дат
        df_1 = data_1["Close"].resample("1D").mean().ffill()
        return data_1, df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('📥🧹Восстановление непрерывности дат методом resample')
st.markdown('##### 💹 Котировка акций из API Stooq (с библиотекой pandas_datareader)')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🏦 Сырые данные",
     "📶🧹 Очищенные данные",
     "📈🏦 График",
     ])

# Формирование интервала дат
d_start = date.today() - relativedelta(years=1)
d_end = date.today()
# Список фирм
firms = ['AAPL', 'GOOGL', 'MSFT']
# Источник данных
my_sours = 'stooq'

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Запрос данных в API Stooq
    data, df = get_data(d_start, d_end, firms, my_sours)

# Вкладка с данными
with t1:
    # Контейнер для данных data
    with st.container(width=800):
        st.write('📶🏦 Сырые данные из API Stooq')
        st.write(data)

# Вкладка с данными
with t2:
    # Контейнер для данных df
    with st.container(width=400):
        st.write('📶🧹 Очищенные данные с колонкой Close после восстановлением пропущенных дат')
        st.write(df)

# Формируем график
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['AAPL'], name="Apple"))
fig.add_trace(go.Scatter(x=df.index, y=df['GOOGL'], name="Google"))
fig.add_trace(go.Scatter(x=df.index, y=df['MSFT'], name="Microsoft"))
# Обновить подписи осей
tit = '📈🏦Котировки акций от Stooq за период с ' + str(d_start) + ' по ' + str(d_end)
fig.update_layout(xaxis_title="Дата",
                  yaxis_title="Стоимость акций, $",
                  title=tit)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)