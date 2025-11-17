import streamlit as st
import plotly.graph_objects as go
from statsmodels.tsa.stattools import adfuller
import yfinance as yf

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    # Загрузка данных из Yahoo Finance о продаже нефти
    try:
        tick = 'CL=F'
        ticker = yf.Ticker(tick)
        # Загрузка данных
        df_1 = ticker.history(period='5y')
        # Оставляем одну колонку - объем продаж
        df_1 = df_1[['Volume']]
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Использовать круговой спиннер
with st.spinner(text="Ждите, идет загрузка данных...", show_time=True):
    # Получение данных
    df = get_data()

st.subheader('🌊﹏ Оценка стационарности временного ряда')
st.markdown('##### 🛢Данные об объемах продажи нефти от Yahoo Finance')

# Создаем вкладки
t1, t2 = st.tabs(
    ["📶🧹 Очищенные данные",
     "📈 График",
     ])

# Тест на стационарность
adf_test = adfuller(df['Volume'])
p_test = adf_test[1]
if p_test <= 0.05:
    stat_txt = '🙂👍Временной ряд является стационарным'
else:
    stat_txt = '🙁👎Временной ряд не является стационарным'

# Вкладка с данными
with t1:
    with st.container(width=800):
        col1, col2 = st.columns([1,2])
        with col1:
            st.write('📶🧹Очищенные данные')
            st.write(df)
        with col2:
            st.write('🧪Тест Дики-Фуллера -', p_test)
            st.write(stat_txt)

# Формируем график
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Volume'], name="Объем продаж"))
fig.update_layout(title='📈Динамика объема продаж нефти из API Yahoo Finance',
                    xaxis_title="Дата",
                    yaxis_title="Объем продаж",
                    autosize=False,
                    width=800,
                    height=600,
                    hoverlabel=dict(font_size=15))

# Вкладка с графиком
with t2:
    # Контейнер для графика
     with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)