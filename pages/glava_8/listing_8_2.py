import streamlit as st
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
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

st.subheader('🔮 Авторегрессионные модели (AR) для прогнозирования')
st.markdown('##### 🚍👬Данные о пассажиропотоках из файла CSV')

# Создаем вкладки
t1, t2 = st.tabs(
    ["📶Набор данных",
     "📈🔮 Прогноз",
     ])

# Запрос данных
df = get_data()

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('🚍👬 Данные о пассажиропотоках')
        st.write(df)

# Создание модели
model = AutoReg(df, lags=20)
# Обучение модели на исторических данных
model_fit = model.fit()
# Прогноз на 2 года
forecast = model_fit.forecast(steps=24)

# Вкладка с графиком
with t2:
    st.write('🔮Прогноз пассажиропотока на модели AR')
    # Контейнер для графика
    with st.container(width=800, border=True):
        # График прогноза с matplotlib
        fig = plt.figure(figsize=(12, 5))
        plt.plot(df, label='Наблюдения')
        plt.plot(forecast, label='Прогноз')
        plt.title('Прогноз пассажиропотока на 2 года')
        plt.legend()  # Функция для добавления легенды
        plt.xlabel('Дата')
        plt.ylabel('Пассажиропоток')
        st.pyplot(fig, width=800)