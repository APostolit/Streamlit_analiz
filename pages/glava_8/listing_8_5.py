import streamlit as st
from datetime import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        d1 = '22-06-2024'
        d2 = '22-06-2025'
        d1 = datetime.strptime(d1, "%d-%m-%Y")
        d2 = datetime.strptime(d2, "%d-%m-%Y")
        # Фирма
        firm = ['MSFT']
        # Источник данных
        sours = 'stooq'
        data_1 = web.DataReader(firm, sours, start=d1, end=d2)
        # Создание df для стоимости акций
        df = data_1['Close']
        return data_1, df
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🛠️ Модель ARMA для анализа временных рядов')
st.markdown('##### 💹 Данные Stooq о котировках акций')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    data, df_close = get_data()

# Создаем вкладки
t1, t2, t3, t4, t5  = st.tabs(["📶Сырые данные",
                               "📶🧹Очищенные данные",
                               "📊Гистограмма",
                               "📈Скользящее среднее",
                               "📈Автокорреляция"])
# Вкладка tab1
with t1:
    # Контейнер для данных data
    with st.container(width=500):
        st.write('📶Исходный набор данных data')
        st.write(data)

# Вкладка t2
with t2:
    # Создаем вкладки
    tb1, tb2 = st.tabs(["📶🧹Очищенные данные",
                        "📈График"])
    with tb1:
    # Контейнер для данных df_close
        with st.container(width=300):
            st.write('📶🧹Стоимость акций на момент закрытия торгов (df_close)')
            st.write(df_close)

    with tb2:
        # Контейнер для графика df_close
        with st.container(width=800, border=True):
            # Формируем график котировок акций и прогнозом
            fig_close = df_close.plot()
            fig_close.layout.update(xaxis_title="Дата",
                                    yaxis_title="Стоимость акций",
                                    title='📈Динамика изменения стоимости акций')
            st.plotly_chart(fig_close, theme=None)

# Восстановление пропущенных дат
df_hist = data["Close"].resample("1D").mean().ffill()

# Вкладка t3
with t3:
    # Создаем вкладки
    tb3, tb4 = st.tabs(["📶Данные для гистограммы",
                        "📊Гистограмма"])
    with tb3:
        # Контейнер для данных df_hist
        with st.container(width=300):
            st.write('Набор данных после восстановления пропущенных дат (df_hist)')
            st.write(df_hist)

    with tb4:
        # Контейнер для графика
        with st.container(width=800, border=True):
            # Создание графика (гистограмма)
            fig_hist = df_hist.plot.hist()
            fig_hist.update_layout(xaxis_title="Стоимость акций",
                                    yaxis_title="Частота",
                                    title='📊Гистограмма распределения стоимости акций')
            st.plotly_chart(fig_hist, theme=None)

# Расчет скользящего среднего
n_dn = 30
df_ssr = df_close.rolling(n_dn).mean()

# Вкладка t4
with t4:
    # Создаем вкладки
    tb5, tb6 = st.tabs(["📶Расчетные данные",
                        "📈График"])
    with tb5:
        # Контейнер для данных df_ssr
        with st.container(width=300):
            st.write('📈Расчет скользящего среднего df_ssr (30 дней)')
            st.write(df_ssr)

    with tb6:
        # Создание графика скользящего среднего
        # Контейнер для графика
        with st.container(width=800, border=True):
            fig_ssr = df_ssr.plot()
            fig_ssr.update_layout(xaxis_title="Дата",
                                  yaxis_title="Стоимость акций",
                                  title='📈Скользящее среднее стоимости акций (30 дней)')
            st.plotly_chart(fig_ssr, theme=None)

# Трансформация колонки в ряд (Series)
series = data["Close"].squeeze()

# Вкладка t5
with t5:
    # Создаем вкладки
    tb7, tb8 = st.tabs(["📶Набор данных",
                        "📈Графики автокорреляции"])
    with tb7:
        # Контейнер для данных series
        with st.container(width=300):
            st.write('📶Набор данных series')
            st.write(series)

    with tb8:
        st.write('📈Графики анализа автокорреляции с matplotlib')
        # Контейнер для графика
        with st.container(width=600, border=True):
            # Графики анализа автокорреляции с matplotlib
            fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
            plot_acf(series, lags=30, ax=ax[0])
            plot_pacf(series, lags=30, ax=ax[1])
            plt.tight_layout()
            st.pyplot(fig, width="content")