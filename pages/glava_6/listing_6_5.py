import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(d_start, d_end):
    try:
        # Перевод дат в строки европейский формат
        d1_str = d_start.strftime("%d-%m-%Y")
        d2_str = d_end.strftime("%d-%m-%Y")

        # Формирование URL адреса
        url_cb = 'http://www.cbr.ru/scripts/xml_metall.asp?'
        date_req1 = 'date_req1='
        date_req2 = '&date_req2='
        url = url_cb + date_req1 + d1_str + date_req2 + d2_str

        # Запрос к данным БД Центробанка о стоимости драгметаллов
        df = pd.read_xml(url)
        # Заменяем запятые на точки в столбце с валютой
        df['Sell'] = df['Sell'].str.replace(',', '.')
        # Преобразуем строки в числа в столбце с валютой
        df['Sell'] = df['Sell'].astype(float)

        # В дате заменяем точки на "-"
        df['Date'] = df['Date'].str.replace('.', '-')
        # Заменяем строковый столбец с датой на datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')

         # Создание сводной таблицы
        df_pivot = df.pivot(index='Date', columns='Code', values="Sell")
        df_pivot.columns = ['Золото', 'Серебро', 'Платина', 'Палладий']
        return df, df_pivot
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('📥🧹Загрузка и очистка данных из API Центрального банка🏛️')
st.markdown('##### 👑💍 Цены на драгоценные металлы')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶💍 Сырые данные",
     "📶💍 Очищенные данные",
     "📈💍 График",
     ])

# Формирование интервала дат
d1 = date.today() - relativedelta(years=5)
d2 = date.today()
# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Запрос данных через API
    df_1, df_p = get_data(d1, d2)

# Вкладка с данными
with t1:
    # Контейнер для данных df_1
    with st.container(width=600):
        st.write('👑💍Сырые данные о стоимости драгметаллов')
        st.write(df_1)

# Вкладка с данными
with t2:
    # Контейнер для данных df_1
    with st.container(width=600):
        st.write('👑💍Очищенные данные о стоимости драгметаллов')
        st.write(df_p)


# Создать объект - График (фигура)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_p.index, y=df_p['Золото'], name='Золото'))
fig.add_trace(go.Scatter(x=df_p.index, y=df_p['Серебро'], name='Серебро'))
fig.add_trace(go.Scatter(x=df_p.index, y=df_p['Платина'], name='Платина'))
fig.add_trace(go.Scatter(x=df_p.index, y=df_p['Палладий'], name='Палладий'))
tit = '👑💍Динамика стоимости драгоценных металлов с ' + str(d1) + ' по ' + str(d2)
fig.update_layout(title=tit,
                  xaxis_title="Дата",
                  yaxis_title="Цена, руб.",
                  )

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)