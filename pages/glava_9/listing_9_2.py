import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from prophet.serialize import model_to_json, model_from_json
import plotly.graph_objects as go

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Загрузка данных из Yahoo Finance
        # Фирмы
        firma = ['AAPL']
        # Загрузка данных
        df_1 = yf.download(firma, start="2022-01-01", end="2025-06-01")
        # Оставляем одну колонку
        df_1 = df_1[['Close']]
        # Добавляем пропущенные дни
        df_1 = df_1["Close"].resample("1D").mean().ffill()
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🔮 Прогнозирование временных рядов с библиотекой Prophet')
st.markdown('##### 💰️ Котировка акций из API Yahoo Finance')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных от Yahoo Finance
    df_yf = get_data()

# Создаем вкладки
t1, t2, t3, t4, t5 = st.tabs(
    ["📶🧹Очищенные данные",
     "📈💰️Котировка акций",
     "📶💰️Данные для Prophet",
     "📈🔮Прогноз с Prophet",
     "📈❄️Тренд и сезонность"
     ])

# Сбрасываем индекс и формируем df для Prophet
df = df_yf.reset_index()
# Задаем имена колонок под требования Prophet
df.columns = ['ds', 'y']
# Из колонки с датой убираем время
df['ds'] = pd.to_datetime(df['ds']).dt.date

# Вкладка с данными
with t1:
    # Контейнер для данных df_yf
    with st.container(width=300):
        st.write('📶🧹💰️ Очищенные данные')
        st.write(df_yf)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        # Создать объект - График (фигура)
        fig = go.Figure()
        # Добавить на график элемент (линию)
        fig.add_trace(go.Scatter(x=df_yf.index, y=df_yf['AAPL']))
        # Обновить макет
        fig.update_layout(title='📈💰️ Динамика изменения цен на акции Apple',
                          xaxis_title='Дата',
                          yaxis_title='Цена, $')
        st.plotly_chart(fig, theme=None)

# Вкладка с данными
with t3:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶💰️Данные для Prophet')
        st.write(df)

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Создаем модель
    model = Prophet(yearly_seasonality=True)
    # Обучаем модель
    model.fit(df)
    # Создаем модель
    model = Prophet(yearly_seasonality=True)
    # Обучаем модель
    model.fit(df)
    # Сохраняем обученную модель
    family = 'mod'
    with open(f'prophet_{family}.json', 'w') as f:
        f.write(model_to_json(model))
    st.toast("Обучения модели завершено!", icon="😍")

# Загружаем обученную модель
with open(f'prophet_{family}.json', 'r') as f:
    model = model_from_json(f.read())

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
        fig.update_layout(title='📈🔮Прогноз изменения цен на акции Apple',
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