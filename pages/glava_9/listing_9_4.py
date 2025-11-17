import streamlit as st
from datetime import date
import plotly.graph_objs as go
import pandas as pd
from dateutil.relativedelta import relativedelta
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(d_11, d_22, kod_val):
    try:
        # Формируем URL адрес запроса в ЦБ
        url_cb = 'https://www.cbr.ru/scripts/XML_dynamic.asp?'
        date_req1 = 'date_req1='
        date_req2 = '&date_req2='
        VAL_NM_RQ = '&VAL_NM_RQ='
        url = url_cb + date_req1 + d_11 + date_req2 + d_22 + VAL_NM_RQ + kod_val
        # Загрузка данных из БД ЦБ
        dat = pd.read_xml(url)

        # Заменяем запятые на точки в столбце с валютой
        dat['Value'] = dat['Value'].str.replace(',', '.')
        # Преобразуем строки в числа в столбце с валютой
        dat['Value'] = dat['Value'].astype(float)

        # В дате заменяем точки на "-"
        dat['Date'] = dat['Date'].str.replace('.', '-')
        # Заменяем строковый столбец с датой на тип datetime
        dat['Date'] = pd.to_datetime(dat['Date'], format='%d-%m-%Y', errors='coerce')
        return dat
    except Exception as e:
         st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Функция "Окно диалога"
@st.dialog("⚠️ Ошибка выбора валют")
def dialog1(firma):
    if not firma:
        st.write('Не выбрана валюта!')
        st.write('Выберите валюту из выпадающего списка.')

# Основной модуль -------------------------------------------

st.subheader('🎫 Применение форм для выбора параметров')
st.markdown('##### 💰️ Курсы валют от Центрального банка России🏛️')

# Дата начала периода (5 лет назад)
d1 = date.today() - relativedelta(years=5)
# Дата конца периода (сегодня)
d2 = date.today()

# Вложенный список названий валют и их кодов
list_tik = [['Доллар', 'R01235'], ['Евро', 'R01239'],
        ['Фунт', 'R01035'], ['Юань', 'R01375']]

# Создать набор данных валют
df_f=pd.DataFrame(list_tik)
# выбрать из df колонку с названиями валют
df_n = df_f[0]
# Список названий валют
list_name_val = list(df_n)

# Боковая панель-------------------------------------
with st.sidebar:
    # Создать форму
    with st.form(key='my_form'):
        # Дата начала периода
        d_start = st.date_input(label="Начало периода",
                                value=d1,
                                format='DD/MM/YYYY')
        # Дата конца периода
        d_end = st.date_input(label="Конец периода",
                              value=d2,
                              format='DD/MM/YYYY')
        firms = st.multiselect("Выбор валют",
                               list_name_val,
                               default='Доллар',
                               help="Выберите валюту из предложенного списка",
                               placeholder='Сделайте выбор')
        # Глубина прогноза
        deep_prog = st.number_input(label='Глубина прогноза',
                                    value=30,
                                    min_value=1,
                                    max_value=365)
        submit_button = st.form_submit_button(label='Отправить')

# Обработка кнопки выбора в форме----------------------------
if submit_button:
    if not firms:  # Если не выбрана валюта
        dialog1(firms)
    else:
        # Фильтр на набор данных валют - df_f
        filter_df = df_f[df_f[0].isin(firms)]
        # Получение списка кодов валют из фильтрованного filter_df
        list_tik = list(filter_df[1])

        # Интервал дат в строки - европейский формат
        d1_str = d_start.strftime("%d-%m-%Y")
        d2_str = d_end.strftime("%d-%m-%Y")

        # Формируем график
        fig = go.Figure()
        name = None
        df = None
        name_val = []
        # Цикл по выбранным валютам
        for k_val in list_tik:
            if k_val == 'R01235':
                name = 'Доллар'
                name_val.append(name)
            elif k_val == 'R01239':
                name = 'Евро'
                name_val.append(name)
            elif k_val == 'R01035':
                name = 'Фунт'
                name_val.append(name)
            elif k_val == 'R01375':
                name = 'Юань'
                name_val.append(name)

            # Использовать круговой спиннер
            with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
                # Загрузка данных от ЦБ
                df = get_data(d1_str, d2_str, k_val)

            fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], name=name))

        # Создаем вкладки для графиков
        t1, t2, t3 = st.tabs(["📈💰Курс валют ЦБ",
                              "📈🔮Прогноз с Prophet",
                              "📈❄️Тренд и сезонность"])

        fig.update_layout(title='📈💰Динамика курса за период: c ' + d1_str + ' по ' + d2_str,
                          xaxis_title="Дата",
                          yaxis_title="Курс, руб.",
                          hoverlabel=dict(font_size=15))

        # Вкладка с графиком
        with t1:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Выбрать из полученных данных только две колонки
        df = df[['Date', 'Value']]
        # Переименовать колонки по их именам
        df.rename(columns={'Date': 'ds', 'Value': 'y'}, inplace=True)
        # Создаем модель
        model = Prophet(yearly_seasonality=True)
        # Обучаем модель
        model.fit(df)
        # Делаем прогноз на заданную глубину
        future = model.make_future_dataframe(periods=deep_prog, freq='D')
        forecast = model.predict(future)

        # формируем график прогноза
        fig = plot_plotly(model, forecast)
        fig.update_layout(title='📈🔮Прогноз изменения курса валюты- ' + name,
                          xaxis_title='Дата',
                          yaxis_title='Курс, $')

        # Вкладка с графиком
        with t2:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Графики компонент (тренда и сезонности)
        fig = plot_components_plotly(model, forecast)
        fig.update_layout(title='📈❄️Тренд и сезонности временного ряда- '+ name)

        # Вкладка с графиком
        with t3:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)