import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf
import warnings

warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Тикер компании
        tick = yf.Ticker("AMD")
        # Получение набора данных от Yahoo Finance
        df_1 = tick.history(start="2023-01-01", end="2025-06-30")
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('##### 🔮 Модель скользящего среднего (MA) для прогнозирования временных рядов')
st.markdown('##### 💹 Данные Yahoo Finance о котировках акций')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    df = get_data()

# Обучение модели с отображением спиннера
with st.spinner(text="Обучение модели...", show_time=True):
    st.toast("Ждите, идет обучения модели...", icon="😍")
    # Создание модели
    model = ARIMA(endog=df['Close'], order=(0, 0, 15))
    # Обучение модели
    results = model.fit()
    st.toast("Обучения модели завершено!", icon="😍")

# Даты предсказания на исторической выборке
start_date = '2023-12-15'
end_date = '2025-06-20'
# Оценка модели на исторической выборке
df['prediction'] = results.predict(start=start_date, end=end_date)

# Количество дней предсказания на будущий период
forecast_steps = 30
# Создание дат будущего периода (индексы)
predict_index = pd.date_range(start=df['Close'].index[-1], periods=forecast_steps + 1, freq='D')[1:]

# Создать DataFrame с будущим периодом
df_ind = pd.DataFrame({'Date': predict_index})
# Прогноз на будущий период (Series)
forecast = results.forecast(steps=forecast_steps)
# Создание из серии df c прогнозом на будущий период
df_predict = forecast.to_frame().reset_index()
# Извлечение колонки с прогнозом из DF
extracted_col = df_predict["predicted_mean"]
# Объединение колонки с прогнозом с датами будущего периода
df_ind = pd.concat([df_ind, extracted_col.rename("prog_noz")], axis=1)

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶 Сырые данные",
     "📶🔮 Данные прогноза",
     "📈 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=500):
        st.write('📶Набор сырых данных от Yahoo Finance')
        st.write(df)

# Формируем график котировок акций и прогнозом
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Акции AMD"))
fig.add_trace(go.Scatter(x=df.index, y=df['prediction'], name="Модель MA"))
fig.add_trace(go.Scatter(x=df_ind['Date'], y=df_ind['prog_noz'], name="Прогноз"))
# Обновить подписи осей
fig.update_layout(xaxis_title="Дата",
                  yaxis_title="Стоимость акций, $",
                  title='📈💹Котировки акций от Yahoo Finance',
                  xaxis_rangeslider_visible=True)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)

# Вкладка с данными
with t2:
    # Удаление из колонки с датами элемента "время"
    df_ind['date'] = pd.to_datetime(df_ind['Date']).dt.date
    df_ind = df_ind.drop(columns=['Date'])
    # Контейнер для данных df_ind
    with st.container(width=300):
        st.write('Набор данных df_ind')
        st.write(df_ind)