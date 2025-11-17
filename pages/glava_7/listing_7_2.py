import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Функция для загрузки данных из CSV файла
@st.cache_data
def get_data():
    # Имя файла
    path_csv = 'csv/passengers.csv'
    # Чтение данных из файла csv
    data = pd.read_csv(path_csv)
    return data

st.subheader('🏂Скользящее среднее временного ряда')
st.markdown('##### 🚍👬Данные о пассажиропотоках из файла CSV')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶 Сырые данные",
     "🏂 Скользящие средние",
     "📈 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных из CSV файла
    with st.container(width=300):
        df = get_data()
        st.write('📶Набор сырых данных из файла CSV')
        st.write(df)

# Превратим дату в индекс
df.set_index('Month', inplace=True)
df.index = pd.to_datetime(df.index)

# Простое скользящее среднее (SMA)
df['SMA'] = df['Passengers'].rolling(window=12).mean()
# Экспоненциальное скользящее среднее
df['EMA'] = df['Passengers'].ewm(span=12).mean()
# Кумулятивное скользящее среднее (CMA)
df['CMA'] = df['Passengers'].expanding().mean()

# Вкладка с данными
with t2:
    # Контейнер для данных из CSV файла
    with st.container(width=500):
        st.write('🏂 Расчет средних скользящих')
        st.write(df)

# Формируем график
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Passengers'], name="Пассажиропоток"))
fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], name="Простое-SMA"))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], name="Экспоненциальное-EMA"))
fig.add_trace(go.Scatter(x=df.index, y=df['CMA'], name="Кумулятивное-CMA"))
# Обновить подписи осей
fig.update_layout(xaxis_title="Дата",
                    yaxis_title="Пассажиропоток, тыс.чел.",
                    title='Скользящие средние пассажиропотока')

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)