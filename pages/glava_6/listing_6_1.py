import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Функция для загрузки данных
@st.cache_data
def get_data():
    # Имя файла
    name_file = 'csv/oil_exports.csv'
    # Чтение данных из файла csv
    df_1 = pd.read_csv(name_file, header=0, delimiter=',')
    series = df_1
    series = series.loc[series['Oil Type'] == 'Total'].filter(['Period', 'Volume (bbl/d)'])
    series['Period'] = series['Period'].transform(lambda x: datetime.strptime(x, '%m/%d/%Y'))
    series.set_index(keys='Period', drop=True, inplace=True)
    series = series.squeeze(axis=1)
    return df_1, series

# Получение данных
df, ser = get_data()

st.subheader('📥🧹Загрузка и очистка данных из CSV файла')
# Создаем вкладки
t1, t2, t3, t4 = st.tabs(
    ["📶 Сырые данные из CSV",
     "🔎Типы данных из CSV",
     "🧹📶 Очищенные данные",
     "📈 График",
     ])

# Вкладка с данными
with t1:
    # Контейнер для данных из CSV файла
    with st.container(width=600):
        st.write('📶Набор сырых данных DataFrame из файла CSV')
        st.write(df)

# Вкладка с данными
with t2:
    # Контейнер для типов данных
    with st.container(width=250,  border=True):
        st.write('🔎Типы данных DataFrame')
        st.text(df.dtypes)

with t3:
    # Контейнер для данных после очистки - series
    with st.container(width=300):
        st.write('🧹📶Набор данных после очистки')
        st.write(ser)

with t4:
    # Контейнер для графика
    with st.container(width=800, border=True):
        fig = px.line(ser, title="📈Объем продаж нефти")
        fig.update_layout(xaxis_title='Годы', yaxis_title='Объем продаж')
        st.plotly_chart(fig, theme=None)