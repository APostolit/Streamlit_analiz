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
def get_data(d_11, d_22):
    try:
        # Формируем URL адрес запроса в ЦБ
        url_cb = 'http://www.cbr.ru/scripts/xml_metall.asp?'
        date_req1 = 'date_req1='
        date_req2 = '&date_req2='
        url = url_cb + date_req1 + d_11 + date_req2 + d_22
        # Загрузка данных из БД ЦБ
        dat = pd.read_xml(url)

        # Заменяем запятые на точки в столбце с ценой продажи
        dat['Sell'] = dat['Sell'].str.replace(',', '.')
        # Преобразуем строки в числа в столбце с ценой продажи
        dat['Sell'] = dat['Sell'].astype(float)

        # Заменяем запятые на точки в столбце с ценой покупки
        dat['Buy'] = dat['Buy'].str.replace(',', '.')
        # Преобразуем строки в числа в столбце с ценой покупки
        dat['Buy'] = dat['Buy'].astype(float)

        # В дате заменяем точки на "-"
        dat['Date'] = dat['Date'].str.replace('.', '-')
        # Заменяем строковый столбец с датой на тип datetime
        dat['Date'] = pd.to_datetime(dat['Date'], format='%d-%m-%Y', errors='coerce')
        return dat
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Функция "Окно диалога"
@st.dialog("⚠️ Ошибка выбора драгметалла")
def dialog1(firma):
    if not firma:
        st.write('Не выбран драгметалл!')
        st.write('Выберите драгметалл из выпадающего списка.')

# Основной модуль -------------------------------------------

st.subheader('🎫 Применение форм для выбора параметров')
st.markdown('##### 💍👑️ Цены на драгоценные металлы от Центрального банка России🏛️')

# Дата начала периода (5 лет назад)
d1 = date.today() - relativedelta(years=5)
# Дата конца периода (сегодня)
d2 = date.today()

# Вложенный список драгметаллов
list_met = [['1', 'Золото'], ['2', 'Серебро'],
        ['3', 'Платина'], ['4', 'Палладий']]

# Создать набор данных металлов
df_m=pd.DataFrame(list_met)
# Выбрать из df колонку с названиями металлов
df_n = df_m[1]
# Список названий металлов для формы
list_name = list(df_n)

# Боковая панель ---------------------------------
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
        met = st.multiselect("Выбор металла",
                               list_name,
                               default='Золото',
                               help="Выберите драгметалл из предложенного списка",
                               placeholder='Сделайте выбор')
        # Глубина прогноза
        deep_prog = st.number_input(label='Глубина прогноза',
                                    value=30,
                                    min_value=1,
                                    max_value=365)
        submit_button = st.form_submit_button(label='Отправить')

# Обработка кнопки выбора в форме ------------------------
if submit_button:
    if not met:  # Если не выбран драгметалл
        dialog1(met)
    else:
        # Фильтр на набор данных металлов
        filter_met= df_m[df_m[1].isin(met)]
        list_kod = list(filter_met[0])

        # Интервал дат в строки - европейский формат
        d1_str = d_start.strftime("%d-%m-%Y")
        d2_str = d_end.strftime("%d-%m-%Y")

        # Использовать круговой спиннер
        with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
            # Загрузка данных от ЦБ
            date = get_data(d1_str, d2_str)

        # Формируем график
        fig = go.Figure()
        name = None
        name_met = []
        df = None
        # Цикл по выбранным металлам
        for k_met in list_kod:
            if k_met == '1':
                name = 'Золото'
                name_met.append(name)
            elif k_met == '2':
                name = 'Серебро'
                name_met.append(name)
            elif k_met == '3':
                name = 'Платина'
                name_met.append(name)
            elif k_met == '4':
                name = 'Палладий'
                name_met.append(name)

            # Фильтрация данных на код металла
            df = date[date['Code'] == int(k_met)]
            # Формирование линии на графике
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Sell'], name=name))

        # Создаем вкладки для графиков
        t1, t2, t3 = st.tabs(["📈💍 Цены на драгметаллы от ЦБ",
                              "📈🔮Прогноз с Prophet",
                              "📈❄️Тренд и сезонность"])

        # Формируем параметры надписей к графику
        fig.update_layout(title='📈💍Динамика цены на драгметаллы за период: c ' + d1_str + ' по ' + d2_str,
                          xaxis_title="Дата",
                          yaxis_title="Цена, руб.",
                          hoverlabel=dict(font_size=12))
        # Вкладка с графиком
        with t1:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Выбрать из полученных данных только две колонки
        df = df[['Date', 'Sell']]
        # Переименовать колонки по их именам
        df.rename(columns={'Date': 'ds', 'Sell': 'y'}, inplace=True)

        # Создаем модель
        model = Prophet(yearly_seasonality=True)
        # Обучаем модель
        model.fit(df)

        # Делаем прогноз на заданную глубину
        future = model.make_future_dataframe(periods=deep_prog, freq='D')
        forecast = model.predict(future)

        # формируем график прогноза
        fig = plot_plotly(model, forecast)
        fig.update_layout(title='📈🔮Прогноз цен на драгметаллы- ' + name,
                          xaxis_title='Дата',
                          yaxis_title='Цена')
        # Вкладка с графиком
        with t2:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Графики компонент (тренда и сезонности)
        fig = plot_components_plotly(model, forecast)
        fig.update_layout(title='📈❄️Тренд и сезонности временного ряда')
        # Вкладка с графиком
        with t3:
            # Контейнер для графика
            with st.container(width=800,border=True):
                st.plotly_chart(fig, theme=None)