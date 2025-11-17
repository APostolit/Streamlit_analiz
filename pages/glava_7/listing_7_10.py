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
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('⬇️Уменьшение частоты дискретизации данных')
st.markdown('##### 💹 Котировка акций из API Stooq (с библиотекой pandas_datareader)')

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
    df = get_data(d_start, d_end, firms, my_sours)

# Уменьшаем частоту (недельные данные)
# df_w = df.resample(rule="W").count()
df_w = df.resample(rule="W").max()
# df_w = df.resample(rule="W").min()

# Уменьшаем частоту (месячные данные)
df_m = df.resample(rule="ME").mean()

# Создаем вкладки
tab1, tab2, tab3 = st.tabs(
    ["📅Дневные данные",
     "🗓️Недельные данные",
     "🌙Месячные данные"
     ])

# Вкладка tab1
with tab1:
    # Создаем вкладки
    t11, t12 = st.tabs(
        ["📶Набор данных",
         "📈График"
         ])
    with t11:
        # Контейнер для данных df
        with st.container(width=400):
            st.write('📅Набор данных DataFrame из API Stooq (ежедневные)')
            st.write(df)

    with t12:
        # Контейнер для графика
        with st.container(width=800, border=True):
            # Формируем график
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['AAPL'], name="Apple"))
            fig.add_trace(go.Scatter(x=df.index, y=df['GOOGL'], name="Google"))
            fig.add_trace(go.Scatter(x=df.index, y=df['MSFT'], name="Microsoft"))
            # Обновить подписи осей
            tit = '💹📅Котировки акций от Stooq (ежедневные данные)'
            fig.update_layout(xaxis_title="Дата",
                              yaxis_title="Стоимость акций, $",
                              title=tit)
            st.plotly_chart(fig, theme=None)

# Вкладка tab2
with tab2:
    # Создаем вкладки
    t21, t22 = st.tabs(
        ["📶Набор данных",
         "📈График"
         ])
    with t21:
        # Контейнер для данных df_w
        with st.container(width=400):
            st.write('🗓️Набор данных DataFrame из API Stooq (еженедельные)')
            st.write(df_w)

    with t22:
        # Контейнер для графика
        with st.container(width=800, border=True):
            # Формируем график месячных данных
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_w.index, y=df_w['AAPL'], name="Apple"))
            fig.add_trace(go.Scatter(x=df_w.index, y=df_w['GOOGL'], name="Google"))
            fig.add_trace(go.Scatter(x=df_w.index, y=df_w['MSFT'], name="Microsoft"))
            # Обновить подписи осей
            fig.update_layout(xaxis_title="Дата",
                              yaxis_title="Стоимость акций, $",
                              title='💹🗓️Котировки акций от Stooq (еженедельные данные)')
            st.plotly_chart(fig, theme=None)

# Вкладка tab3
with tab3:
    # Создаем вкладки
    t31, t32 = st.tabs(
        ["📶Набор данных",
         "📈График"
         ])
    with t31:
        # Контейнер для данных df_m
        with st.container(width=400):
            st.write('🌙Набор данных DataFrame из API Stooq (ежемесячные)')
            st.write(df_m)

    with t32:
        # Контейнер для графика
        with st.container(width=800, border=True):
            # Формируем график месячных данных
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_m.index, y=df_m['AAPL'], name="Apple"))
            fig.add_trace(go.Scatter(x=df_m.index, y=df_m['GOOGL'], name="Google"))
            fig.add_trace(go.Scatter(x=df_m.index, y=df_m['MSFT'], name="Microsoft"))
            # Обновить подписи осей
            fig.update_layout(xaxis_title="Дата",
                              yaxis_title="Стоимость акций, $",
                              title='💹🌙Котировки акций от Stooq (ежемесячные данные)')
            st.plotly_chart(fig, theme=None)