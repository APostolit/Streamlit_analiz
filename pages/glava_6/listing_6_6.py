import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(firma, start, end):
    try:
        url_mb = 'http://iss.moex.com/iss/engines/stock/markets/shares/securities/'
        cand = '/candles.json?from='
        till = '&till='
        interval = '&interval=24'
        url = url_mb + firma + cand + start + till + end + interval
        # Получить данные формата json
        j = requests.get(url).json()
        data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]
        # Трансформировать данные в df
        data_1 = pd.DataFrame(data)
        # Создать индекс
        data = data_1.set_index('end')
        return data_1, data
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.subheader('📥🧹Загрузка и очистка данных из API Московской биржи🏛️')
st.markdown('##### 💨🔥 Цены на акции Газпрома')

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🔥 Сырые данные",
     "📶🧹 Очищенные данные",
     "📈🔥 График",
     ])

# Формирование интервала дат
firm = 'GAZP'
d1 = '2024/01/01'
d2 = '2025-05-17'

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Запрос данных через API
    df_g, df = get_data(firm, d1, d2)

# Вкладка с данными
with t1:
    # Контейнер для данных df_1
    with st.container(width=700):
        st.write('🔥Сырые данные из API Московской биржи')
        st.write(df_g)

# Вкладка с данными
with t2:
    # Контейнер для данных df_1
    with st.container(width=700):
        st.write('🔥🧹Очищенные данные из API Московской биржи')
        st.write(df)

# Создать объект - График (фигура)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='Газпром'))
tit = '🔥Динамика стоимости акций Газпрома с ' + d1 + ' по ' + d2
fig.update_layout(title=tit,
                  xaxis_title="Дата",
                  yaxis_title="Цена, руб.",
                  xaxis_rangeslider_visible=True)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)