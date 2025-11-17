import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objects as go

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Загрузка данных из Yahoo Finance
        tick = 'BZ=F'
        ticker = yf.Ticker(tick)
        df_1 = ticker.history(start="2022-01-01", end="2025-05-21", interval="1d")
        # Оставляем одну колонку
        df_1 = df_1[['Close']]
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🔮 Прогнозирование временных рядов с библиотекой Prophet')
st.markdown('##### 🛢️ Цены на нефть из API Yahoo Finance')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    df = get_data()

# Создаем вкладки
t1, t2, t3, t4, t5 = st.tabs(
    ["📶🧹Очищенные данные",
     "📈🛢️Цены на нефть",
     "📶🛢️Данные для Prophet",
     "📈🔮Прогноз с Prophet",
     "📈❄️Тренд и сезонность"
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🧹🛢️Очищенные данные')
        st.write(df)

 # Создать объект - График (фигура)
fig = go.Figure()
# Добавить на график элемент (линию)
fig.add_trace(go.Scatter(x=df.index, y=df['Close']))
# Обновить макет
fig.update_layout(title='📈🛢 Динамика изменения цены на нефть',
                  xaxis_title='Дата',
                  yaxis_title='Цена, $')

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)

# Сбрасываем индекс
df = df.reset_index()
# Задаем имена колонок под требования Prophet
df.columns = ['ds', 'y']
# Из колонки с датой убираем время
df['ds'] = pd.to_datetime(df['ds']).dt.date

# Вкладка с данными
with t3:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🛢️Набор данных для Prophet')
        st.write(df)

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Создаем модель
    model = Prophet(yearly_seasonality=True)
    # Обучаем модель
    model.fit(df)
    st.toast("Обучения модели завершено!", icon="😍")

# Делаем прогноз на 30 дней
predict = 30
future = model.make_future_dataframe(periods=predict, freq='D')
forecast = model.predict(future)

# Вкладка с графиком
with t4:
    # Контейнер для графика
    with st.container(width=800, border=True):
        # формируем график
        fig = plot_plotly(model, forecast)
        fig.update_layout(title='📈🔮 Динамика и прогноз изменения цены на нефть',
                          xaxis_title='Дата',
                          yaxis_title='Цена, $')
        st.plotly_chart(fig, theme=None)

# Вкладка с графиком
with t5:
    # Контейнер для графика
    with st.container(width=800, border=True):
        # Графики компонент (тренда и сезонности)
        fig = plot_components_plotly(model, forecast)
        fig.update_layout(title_text='📈❄️ Тренд и сезонность')
        st.plotly_chart(fig, theme=None)