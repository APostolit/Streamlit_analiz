import pandas as pd
import streamlit as st
from datetime import datetime
import pandas_datareader.data as web
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Игнорировать предупреждения
warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Даты запрашиваемого периода
        d1 = '20-06-2024'
        d2 = '20-06-2025'
        d1 = datetime.strptime(d1, "%d-%m-%Y")
        d2 = datetime.strptime(d2, "%d-%m-%Y")
        # Фирма
        firm = ['MSFT']
        # Источник данных
        sours = 'stooq'
        # Загрузка данных
        data = web.DataReader(firm, sours, start=d1, end=d2)
        # Выбор колонки Close и добавление пропущенных дней
        df_1 = data["Close"].resample("1D").mean().ffill()
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🔮 Прогнозирование временного ряда с моделью ARMA')
st.markdown('##### 💹 Данные Stooq о котировках акций')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    df = get_data()

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🧹Очищенные данные",
     "📶🔮Расчет прогноза",
     "📈🔮Прогноз на модели ARMA"])

# Вкладка
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶Исходный набор данных df с колонкой Close (цена акций Microsoft)')
        st.write(df)

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Параметры модели
    order = (5, 0, 0)
    # Создание модели с оптимальными параметрами
    model = ARIMA(endog=df['MSFT'], order=order)
    # Обучение модели
    results = model.fit()

st.toast("Обучения модели завершено!", icon="😍")

# Даты предсказания на исторической выборке
start_date = '2024-06-20'
end_date = '2025-06-20'
# Оценка модели на исторической выборке
df['prediction'] = results.predict(start=start_date, end=end_date)

# Вкладка
with t2:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🔮Исходный набор данных df с колонкой Close и прогнозом')
        st.write(df)

# Количество дней предсказания на будущий период
forecast_steps = 15
# Создание дат будущего периода (индексы)
predict_index = pd.date_range(start=df['MSFT'].index[-1], periods=forecast_steps + 1, freq='D')[1:]
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

# Формируем график котировок акций и прогнозом
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['MSFT'], name="Акции Microsoft"))
fig.add_trace(go.Scatter(x=df.index, y=df['prediction'], name="Модель ARMA"))
fig.add_trace(go.Scatter(x=df_ind['Date'], y=df_ind['prog_noz'], name="Прогноз"))
# Обновить подписи осей
fig.update_layout(xaxis_title="Дата",
                  yaxis_title="Стоимость акций, $",
                  title='📈🔮Котировки акций Microsoft от Stooq с прогнозом',
                  xaxis_rangeslider_visible=True)

# Вкладка
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)