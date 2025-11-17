import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.stattools import adfuller

# Функция для загрузки данных из CSV файла
@st.cache_data
def get_data():
    # Имя файла
    path_csv = 'csv/passengers.csv'
    # Чтение данных из файла csv
    data = pd.read_csv(path_csv)
    return data

st.subheader('🌊﹏ Приведение временного ряда к стационарности')
st.markdown('##### 🚍👬Данные о пассажиропотоках из файла CSV')

# Создаем вкладки
t1, t2 = st.tabs(
    ["📶🛠️ Обработанные данные",
     "📈 График",
     ])

# Получение данных
df = get_data()
# Превратим дату в индекс
df.set_index('Month', inplace=True)
df.index = pd.to_datetime(df.index)

# Приведение к стационарности дифференцированием
df['Pass_diff'] = df['Passengers'].diff()

# Замена значения NaN на 0
df['Pass_diff'] = df['Pass_diff'].fillna(0)
# Тест на стационарность
adf_test = adfuller(df['Pass_diff'])
p_test = adf_test[1]
if p_test <= 0.05:
    stat_txt = '🙂👍Временной ряд является стационарным'
else:
    stat_txt = '🙁👎Временной ряд не является стационарным'

# Вкладка с данными
with t1:
    with st.container(width=900):
        col1, col2 = st.columns([1,2])
        with col1:
            st.write('📶🛠️Набор данных после дифференцирования')
            st.write(df)
        with col2:
            st.write('🧪Тест Дики-Фуллера -', p_test)
            st.write(stat_txt)

# Формируем график
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Pass_diff'], name="Пассажиропоток"))
fig.update_layout(title='📈🛠️Приведение временного ряда к стационарности - дифференцирование',
                  xaxis_title="Дата",
                  yaxis_title="Пассажиропоток, тыс.чел.",
                  autosize=False,
                  width=800,
                  height=600,
                  hoverlabel=dict(font_size=20))

# Вкладка с графиком
with t2:
    # Контейнер для графика
     with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)