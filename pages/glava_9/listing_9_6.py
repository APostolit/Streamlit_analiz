import streamlit as st
import wbdata
from datetime import date, datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import warnings

warnings.filterwarnings("ignore")
# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(indicator, count, s_date, e_date):
    try:
        # Интервал дат - американский формат из строк
        start_d = datetime.strptime(s_date, '%d-%m-%Y')
        end_d = datetime.strptime(e_date, '%d-%m-%Y')
        # Извлечение данных из API Всемирного банка
        dfr = wbdata.get_dataframe(indicator,
                                   country=count,
                                   date=(start_d, end_d),
                                   parse_dates=True)
        # Удалить строки с пустыми значениями NaN
        dfr = dfr.dropna()
        return dfr
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Функция "Окно диалога"
@st.dialog("⚠️ Ошибка выбора страны")
def dialog1(firma):
    if not firma:
        st.write('Не выбрана страна!')
        st.write('Выберите страну из выпадающего списка.')

# Основной модуль -------------------------------------------

st.subheader('🎫 Применение форм для выбора параметров')
st.markdown('##### 🏦 Прогноз экономических показателей стран по данным Всемирного банка')

# Дата начала периода (20 лет назад)
d1 = date.today() - relativedelta(years=20)
# Дата конца периода (сегодня)
d2 = date.today()

# Вложенный список тикеров и названий стран
countries = [['GB', 'Великобритания'], ['DE', 'Германия'],
             ['IT', 'Италия'], ['CN', 'Китай'], ['RU', 'Россия'],
             ['US', 'США'], ['FR', 'Франция']]

# Создать набор данных стран
df_c=pd.DataFrame(countries)
# Выбрать из df_m колонку с названиями стран
df_n = df_c[1]
# Список названий стран для формы
list_name = list(df_n)

# Список кодов экономических индикаторов
kod_indic = [
    "{'NY.GDP.MKTP.KD.ZG': 'GDP growth'}",
    "{'NY.GDP.PCAP.CN': 'GDP per capita (current LCU)'}",
    "{'NE.EXP.GNFS.ZS': 'Exports'}",
    "{'NE.IMP.GNFS.ZS': 'Imports'}",
    "{'GC.DOD.TOTL.GD.ZS': 'Government debt'}",
    "{'SL.UEM.TOTL.ZS': 'Unemployment rate'}",
    "{'FP.CPI.TOTL.ZG': 'Inflation'}",
    "{'NY.GNP.PCAP.CD': 'GNI per capita'}"
]
# Список наименований экономических индикаторов
name_indic = [
    'Рост ВВП', 'ВВП на душу населения', 'Экспорт товаров',
    'Импорт товаров', 'Госдолг', 'Уровень безработицы',
    'Инфляция', 'ВНД на душу населения',
]

# Создать словарь
my_dict = {'kod_indic': kod_indic, 'name_indic': name_indic}
# Создать набор данных с экономическими индикаторами
df_ind=pd.DataFrame(my_dict)

# Выбрать из df_ind колонку с названиями индикаторов
df_n_ind = df_ind['name_indic']
# Список названий индикаторов для формы
list_n_ind = list(df_n_ind)

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
        country = st.multiselect("Выбор страны",
                                 list_name,
                                 default='Великобритания',
                                 help="Выберите страну из предложенного списка",
                                 placeholder='Сделайте выбор')
        indic = st.selectbox(label="Выбор индикатора",
                             options=list_n_ind,
                             index=0)
        # Глубина прогноза
        deep_prog = st.number_input(label='Глубина прогноза',
                                    value=2,
                                    min_value=1,
                                    max_value=10)
        submit_button = st.form_submit_button(label='Отправить')
# Конец боковой панели ---------------------------------------------

# Обработка кнопки выбора в форме ---------------------------
if submit_button:
    if not country:  # Если не выбрана страна
        dialog1(country)
    else:
        # Фильтр на набор данных стран
        filter_c= df_c[df_c[1].isin(country)]
        list_kod_c = list(filter_c[0])

        # Фильтр на выбранный индикатор
        filter_kod_ind = df_ind[df_ind['name_indic'] == indic]
        kod_ind = filter_kod_ind['kod_indic']
        kod_ind = kod_ind.values[0]
        # Преобразовать индикатор в словарь
        kod_ind = eval(kod_ind)

        # Интервал дат в строки - европейский формат
        d1_str = d_start.strftime("%d-%m-%Y")
        d2_str = d_end.strftime("%d-%m-%Y")

        # Использовать круговой спиннер
        with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
            # Загрузка данных из API Всемирного банка
            df = get_data(kod_ind, list_kod_c, d1_str, d2_str)

        # Получить имя колонки с данными из df (наименование индикатора)
        ind_val = df.columns[0]

        # Создаем группы вкладок
        tabs1, tabs2 = st.tabs([
            "📶Данные",
            "📈Графики",
        ])

        # Вкладки с данными
        with tabs1:
            # Создаем вкладки для данных
            t1, t2, tp = st.tabs([
                "📶🏦Исходные данные",
                "📶📝Сводная таблица",
                "📶🔮Данные для Prophet"
            ])

        # Вкладка с данными
        with t1:
            # Контейнер для данных df
            with st.container(width=500):
                st.write('📶🏦Набор данных из API Всемирного банка')
                st.write(df)

        # Менять форму данных, если несколько стран
        if len(list_kod_c) >= 2:
            df = df.reset_index()
            df_pivot = df.pivot(index='date', columns='country', values=ind_val)
            # Колонка с данными для прогноза
            col_predict = df_pivot.columns[0]
        else:
            df_pivot = df
            col_predict = ''

        # Размер контейнера для данных
        n_col = len(list_kod_c)
        w = None
        if n_col == 1:
            w = 400
        elif n_col == 2:
            w = 500
        elif n_col == 3:
            w = 600
        elif n_col == 4:
            w = 800
        elif n_col == 5:
            w = 800

        # Вкладка с данными
        with t2:
            # Контейнер для данных df_pivot
            with st.container(width=w):
                st.write('📶📝Сводная таблица')
                st.write(df_pivot)

        # Вкладки с графиками
        with tabs2:
            # Создаем вкладки для графиков
            t3, t4, t5 = st.tabs([
                "📈🕵️‍♂️Динамика изменения индикатора",
                "📈🔮Прогноз с Prophet",
                "📈❄️Тренд и сезонность"
            ])

        # Формирование графика исторических данных
        fig = df_pivot.plot(title="📈🕵️‍♂️Экономический индикатор: " + indic)
        # Обновить подписи осей
        fig.update_layout(xaxis_title="Годы",
                          yaxis_title=indic)
        # Вкладка с графиком
        with t3:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Готовим данные к прогнозу
        if len(list_kod_c) >= 2:  # Если выбрано более 2-х стран
            # Убрать индекс
            df_pivot.reset_index(level=0, inplace=True)
            # Переименовать колонки по их индексу
            df_pivot.columns.values[[0, 1]] = ['ds', 'y']
            # Выбрать две колонки
            df = df_pivot.take([0, 1], axis=1)
        else:  # Если выбрана одна страна
            # Убрать индекс
            df.reset_index(level=0, inplace=True)
            # Переименовать колонки по их индексу
            df.columns.values[[0, 1]] = ['date', 'value']
            # Переименовать колонки по их именам
            df.rename(columns={'date': 'ds', 'value': 'y'}, inplace=True)

        # Вкладка с данными
        with tp:
            # Контейнер для данных df_pivot
            with st.container(width=300):
                st.write('📶🔮Данные для прогноза с Prophet: ', col_predict)
                st.write(df)

        # Создаем модель
        model = Prophet(yearly_seasonality=False)
        # Обучаем модель
        model.fit(df)

        # Делаем прогноз на заданную глубину
        future = model.make_future_dataframe(periods=deep_prog, freq='YE')
        forecast = model.predict(future)

        # формируем график прогноза
        fig = plot_plotly(model, forecast)
        fig.update_layout(title='📈🔮Прогноз изменения индикатора- ' + ind_val + ', ' + col_predict,
                          xaxis_title='Дата',
                          yaxis_title=indic)
        # Вкладка с графиком
        with t4:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Графики компонент (тренда и сезонности)
        fig = plot_components_plotly(model, forecast)
        fig.update_layout(title='📈❄️Тренд и сезонности временного ряда' + ', ' + col_predict)
        # Вкладка с графиком
        with t5:
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)