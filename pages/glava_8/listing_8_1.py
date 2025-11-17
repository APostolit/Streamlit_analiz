import streamlit as st
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

# Функция для загрузки данных из CSV файла
@st.cache_data
def get_data():
    # Имя файла
    path_csv = 'csv/passengers.csv'
    # Чтение данных из файла csv
    df1 = pd.read_csv(path_csv)
    # Превратим дату в индекс
    df1.set_index('Month', inplace=True)
    df1.index = pd.to_datetime(df1.index)
    return df1

st.subheader('Авторегрессионная модель (AR) для анализа временных рядов')
st.markdown('##### 🚍👬Данные о пассажиропотоках из файла CSV')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶Набор данных",
     "📶🛠️Анализ данных на модели AR",
     "📈🔮 Прогноз",
     ])

# Запрос данных
df = get_data()
# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶Данные о пассажиропотоках')
        st.write(df)

# Тест Дики-Фуллера
result = adfuller(df["Passengers"])
p_value = result[1]

# Приведение временного ряда к стационарности
if p_value > 0.05:
    df_diff = df["Passengers"].diff().fillna(0)
else:
    df_diff = df

# Вкладка с графиком
with t2:
    st.write('📶🛠️Анализ пассажиропотока на модели AR')
    # Контейнер для графика
    with st.container(width=800, border=True):
        # Графики анализа автокорреляции с matplotlib
        fig, ax = plt.subplots(2, 1, figsize=(10, 6))
        plot_acf(df_diff, lags=36, ax=ax[0])
        plot_pacf(df_diff, lags=36, ax=ax[1])
        plt.tight_layout()
        st.pyplot(fig, width=800)

# Создание обучающей и тестовой выборки
n = len(df_diff)
train_end = int(n * 0.8)
train = df_diff.iloc[:train_end]
test = df_diff.iloc[train_end:]

# Создание модели AR
p = 12
model = AutoReg(train, lags=p, old_names=False)
# Обучение модели на обучающей выборки
model_fit = model.fit()

# Прогноз на тестовой выборке
pred_test = model_fit.predict(start=test.index[0], end=test.index[-1], dynamic=False)
last_train_value = df["Passengers"].iloc[train_end]
forecast_orig = pred_test.cumsum() + last_train_value
forecast_orig.index = test.index

# Формирование графика
fig = plt.figure(figsize=(12, 5))
plt.plot(df["Passengers"], label="Наблюдения", linewidth=1)
plt.plot(forecast_orig, label="AR прогноз", linestyle="--")
plt.axvline(df.index[train_end], alpha=0.5, linestyle=":")
plt.title('Прогноз пассажиропотока на тестовый период')
plt.legend()  # Функция для добавления легенды
plt.xlabel('Дата')
plt.ylabel('Пассажиропоток')

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.write('📈🔮Прогноз на тестовый период на модели AR')
        st.pyplot(fig, width=800)