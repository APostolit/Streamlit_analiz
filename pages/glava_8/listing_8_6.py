import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pandas_datareader.data as web
from pmdarima.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import time
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Подключить matplotlib к pandas
pd.options.plotting.backend = 'matplotlib'
# Игнорировать предупреждения
warnings.filterwarnings("ignore")

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
        data = web.DataReader(firm, sours, start=d1, end=d2)
        # Добавляем пропущенные дни
        df_1 = data["Close"].resample("1D").mean().ffill()
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🛠️ Поиск оптимальных параметров модели ARMA')
st.markdown('##### 💹 Данные Stooq о котировках акций')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    df = get_data()

# Разбивка данных на обучающие и тестовые
test_size = int(len(df) * 0.2)
train_size = len(df) - test_size
train, test = train_test_split(df, train_size=train_size)

# Расчет средней цены и базовой ошибки
train_mean = train.mean()
pred_baseline = [train_mean] * len(train)
mae_baseline = mean_absolute_error(train, pred_baseline)
m_price = round(train_mean, 2)
base_mae = round(mae_baseline, 2)

# Задание сетки параметров
p_params = range(0, 15, 5)
q_params = range(0, 3, 1)

# Создать словарь для хранения данных MAEs
mae_grid = dict()

st.toast("Ждите, идет подготовка модели...", icon="😍")

# Использовать круговой спиннер
with st.spinner(text="Ждите, идет подбор параметров модели...", show_time=True):
    # Внешний цикл: перебор возможных значений для `p`
    for p in p_params:
        # Словарь ключ-значение. Ключ-`p`, значение-пустой список
        mae_grid[p] = list()
        # Внутренний цикл: перебор возможных значений для `q`
        for q in q_params:
            # Комбинация параметров для модели
            order = (p, 0, q)
            # Отметка времени начала обучения
            start_time = time.time()
            # Создание и обучение модели
            model = ARIMA(train, order=order).fit()
            # Расчет времени обучения
            elapsed_time = round(time.time() - start_time, 2)
            # print(f"Время обучения ARIMA {order} - {elapsed_time} секунд")
            # Сформировать прогноз на основе обучающей выборки
            pred = model.predict()
            # Расчет ошибки обучения MAE
            mae = mean_absolute_error(train, pred)
            # Добавить MAE в словарь
            mae_grid[p].append(mae)

# Создать набор данных из ошибок обучения
mae_df = pd.DataFrame(mae_grid)
mae_df = mae_df.round(4)

with st.spinner(text="Идет обучение модели...", show_time=True):
    order = (5, 0, 0)
    # Создание модели с оптимальными параметрами
    model = ARIMA(train, order=order)
    # обучение модели
    result = model.fit()

st.toast("Обучения модели завершено!", icon="😍")

# Создаем вкладки
t1, t2, t3, t4  = st.tabs(
    ["📶🧹Очищенные данные",
     "📈️График",
     "🛠️Параметры модели",
     "📈Диагностика модели"])

# Вкладка
with t1:
    # Контейнер для данных df
    with st.container(width=250):
        st.write('📶Исходный набор данных df')
        st.write(df)

# Вкладка
with t2:
    # Контейнер для данных df
    with st.container(width=800, border=True):
        fig_1 = px.line(df,
                        title="📈 Котировки акций компании Microsoft")
        st.plotly_chart(fig_1, theme=None)

# Вкладка
with t3:
    with st.container(width=300, border=True):
        st.write('Средняя цена акции:', m_price)
        st.write('Базовая ошибка MAE:', base_mae)
        st.write('Сетка параметров модели ARMA:', mae_df)

# Вкладка
with t4:
    # Контейнер для графика
    with st.container(width=600, border=True):
        st.write('📈Параметры диагностики модели ARMA')
        # График из result методом plot библиотеки statsmodels
        fig_d = result.plot_diagnostics(figsize=(10, 11))
        # Вывод графика в streamlit c matplotlib
        st.pyplot(fig_d, width="content")