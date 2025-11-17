import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(start, end, firma):
    try:
        # Загрузка данных из Yahoo Finance
        df_1 = yf.download(firma, start=start, end=end)
        # Оставляем одну колонку
        df_1 = df_1[['Close']]
        # Добавляем пропущенные дни
        df_1 = df_1["Close"].resample("1D").mean().ffill()
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Функция "Окно диалога"
@st.dialog("⚠️ Ошибка выбора фирм")
def dialog1(firma):
    if not firma:
        st.write('Не выбрана фирма!')
        st.write('Выберите фирму из выпадающего списка.')

# Функция отображения результатов ###############################
def result(start, end, df, my_firm, d_prog):
    # Интервал дат в строки - европейский формат
    d1_str = start.strftime("%d-%m-%Y")
    d2_str = end.strftime("%d-%m-%Y")

    # Размер контейнера для данных
    n_col = len(df.columns)
    w = None
    if n_col == 1:
        w = 200
    elif n_col == 2:
        w = 300
    elif n_col == 3:
        w = 400
    elif n_col == 4:
        w = 500
    elif n_col == 5:
        w = 600

    # Создаем вкладки
    t1, t2, t3, t4, t5 = st.tabs(
        ["📶🧹Очищенные данные",
         "📈💰️Котировка акций",
         "📶💰️Данные для Prophet",
         "📈🔮Прогноз с Prophet",
         "📈❄️Тренд и сезонность"
         ])

    # Вкладка с данными
    with t1:
        # Контейнер для данных df
        with st.container(width=w):
            st.write('📶🧹Очищенные данные от Yahoo Finance')
            st.write(df)

    # Вкладка с графиком
    with t2:
        # Контейнер для графика
        with st.container(width=800, border=True):
            # Формирование фигуры (графика)
            fig = df.plot()
            # Формирование параметров графика
            fig.update_layout(
                xaxis=dict(title="Даты"),
                yaxis=dict(title="Стоимость акций, $"),
                title='📈💰️Котировка акций за период: c ' + d1_str + ' по ' + d2_str,
                hoverlabel=dict(font_size=12))
            st.plotly_chart(fig, theme=None)

    # Убрать индекс
    df.reset_index(level=0, inplace=True)
    # Переименовать колонки по их индексу
    df.columns.values[[0, 1]] = ['ds', 'y']
    # Вкладка с данными
    with t3:
        # Контейнер для данных df
        with st.container(width=260):
            st.write('📶💰️Данные для Prophet')
            st.write(df)

    with st.spinner(text="Идет обучение модели...", show_time=True):
        # Создаем модель
        model = Prophet(yearly_seasonality=True)
        # Обучаем модель
        model.fit(df)
        # Делаем прогноз на заданную глубину
        future = model.make_future_dataframe(periods=d_prog, freq='D')
        forecast = model.predict(future)
        st.toast("Обучения модели завершено!", icon="😍")

    # Вкладка с графиком
    with t4:
        # Контейнер для графика
        with st.container(width=800, border=True):
            # формируем график
            firm = my_firm[0]
            fig = plot_plotly(model, forecast)
            fig.update_layout(title='📈🔮Прогноз изменения цен на акции фирмы ' + firm + ' с Prophet',
                              xaxis_title='Дата',
                              yaxis_title='Цена, $')
            st.plotly_chart(fig, theme=None)

    # Вкладка с графиком
    with t5:
        # Контейнер для графика
        with st.container(width=800, border=True):
            # Графики компонент (тренда и сезонности)
            fig = plot_components_plotly(model, forecast)
            fig.update_layout(title='📈❄️Тренд и сезонность временного ряда')
            st.plotly_chart(fig, theme=None)

# Основной модуль -------------------------------------------

st.markdown('### 🎫 Применение форм для выбора параметров')
st.markdown('##### 💰️ Котировка акций из API Yahoo Finance')

# Дата начала периода (5 лет назад)
d1 = date.today() - relativedelta(years=5)
# Дата конца периода (сегодня)
d2 = date.today()

# Вложенный список тикеров и названий фирм
list_tik = [["Apple", 'AAPL'], ["Google", 'GOOGL'], ["Intel", 'INTC'],
          ["Microsoft", 'MSFT'], ["Nvidia", 'NVDA']]
# Создать набор данных фирм
df_f=pd.DataFrame(list_tik)
# выбрать из df колонку с названиями фирм
df_n = df_f[0]
# Список названий фирм
list_name_f = list(df_n)

# Боковая панель ------------------------------------
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
        firms = st.multiselect("Выбор фирм",
                               list_name_f,
                               default='Apple',
                               help="Выберите фирмы из предложенного списка",
                               placeholder='Сделайте выбор')
        # Глубина прогноза
        deep_prog = st.number_input(label='Глубина прогноза',
                                    value=30,
                                    min_value=1,
                                    max_value=365)
        submit_button = st.form_submit_button(label='Отправить')

# Обработка клавиши выбора в форме ----------------------------
if submit_button:
    if not firms:  # Если не выбрана фирма
        dialog1(firms)
    else:
        # Фильтр на набор данных фирм - df_f
        filter_df = df_f[df_f[0].isin(firms)]
        # Получение списка тикеров фирм из фильтрованного filter_df
        list_firms = list(filter_df[0])
        list_tik = list(filter_df[1])
        # Использовать круговой спиннер
        with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
            # Загрузка данных от Yahoo Finance
            df_yf = get_data(d_start, d_end, list_tik)
            result(d_start, d_end, df_yf, list_firms, deep_prog)