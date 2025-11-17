import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import warnings

warnings.filterwarnings("ignore")
# Подключение plotly к pandas
pd.options.plotting.backend = "plotly"

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data(indicator_id, group_ids=None, years=None):
    try:
        # Значения параметров по умолчанию
        if years is None:
            years = []
        if group_ids is None:
            group_ids = []

        # Фрагмент заголовка URL адреса
        head_url = "https://www.imf.org/external/datamapper/api/v1"
        # Фрагментов URL адреса с географической группой
        list_groups = "/".join(group_ids)
        # Фрагментов URL адреса с периодом
        list_period = "?periods=" + ",".join(years)
        # Полный URL адрес запроса
        url = f"{head_url}/{indicator_id}/{list_groups}{list_period}"

        # Запрос к API
        response = requests.get(url=url)

        # Извлечение текста из формата JSON
        resp_txt = json.loads(response.text)

        # Разбор полученных данных
        response_values = resp_txt.get("values")
        if not response_values:
            return pd.DataFrame()

        # Создание DateFrame
        indicator_df = pd.DataFrame.from_records(
            resp_txt["values"][indicator_id]).sort_index()
        return indicator_df
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

# Функция "Окно диалога"
@st.dialog("⚠️ Ошибка выбора страны")
def dialog1(firma):
    if not firma:
        st.write('Не выбрана страна!')
        st.write('Выберите страну из выпадающего списка.')

# Основной модуль -------------------------------------------

st.subheader('🎫 Применение форм для выбора параметров из API МВФ')

# Вложенный список id и названий стран
countries = [['DEU', 'Германия'], ['GBR', 'Великобритания'],
             ['CHN', 'Китай'], ['RUS', 'Россия'],
             ['FRA', 'Франция'], ['USA', 'США']]

# Создать набор данных стран
df_c=pd.DataFrame(countries)
# Выбрать из df_c колонку с названиями стран
df_n = df_c[1]
# Список названий стран для формы
list_name_c = list(df_n)

# Вложенный список id и индикаторов
indicators = [['LP', 'Население'], ['NGDPD', 'ВВП'],
             ['rltir', 'Доходность гособлигаций'],
             ['LUR', 'Безработица'], ['GDP', 'Номинальный ВВП'],
             ['GG_DEBT_GDP', 'Государственный долг']]

# Создать набор данных индикаторов
df_i=pd.DataFrame(indicators)
# Выбрать из df_m колонку с названиями индикаторов
df_ni = df_i[1]
# Список названий индикаторов для формы
list_name_i = list(df_ni)

# Боковая панель-------------------------------------
with st.sidebar:
    # Создать форму
    with st.form(key='my_form'):
        # Даты периода
        range_years = st.slider("Диапазон (годы)", 2000, 2024,
                                (2010, 2024))
        country = st.multiselect("Выбор страны",
                                 list_name_c,
                                 default='Германия',
                                 help="Выберите страну из предложенного списка",
                                 placeholder='Сделайте выбор')
        indic = st.selectbox(label="Выбор индикатора",
                             options=list_name_i,
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
        # Фильтр на набор стран
        filter_c= df_c[df_c[1].isin(country)]
        list_kod_c = list(filter_c[0])

        # Из интервала создать список дат
        d1 = range_years[0]
        d2 = range_years[1]
        list_year = list(range(d1, d2+1))
        list_year = [str(x) for x in list_year]

        # Строка с выбранным индикатором
        row_ind = df_i[df_i[1] == indic]
        # Код индикатора
        kod_ind = row_ind.values[0][0]
        # Имя индикатора
        name_ind = row_ind.values[0][1]

        st.markdown('##### 🏦 Динамика и прогноз изменения индикатора - ' + name_ind)

        # Использовать круговой спиннер
        with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
            # Загрузка данных из API МВФ
            df = get_data(kod_ind, list_kod_c, list_year)

        # Создаем группы вкладок
        tabs1, tabs2 = st.tabs([
            "📶Данные",
            "📈Графики",
        ])

        # Вложенные вкладки с данными
        with tabs1:
            # Создаем вкладки для данных
            t1, t2 = st.tabs([
                "📶🏦Исходные данные",
                "📶🔮Данные для Prophet"
            ])

        # Вложенные вкладки с графиками
        with tabs2:
            # Создаем вкладки для графиков
            t3, t4, t5 = st.tabs([
                "📈🕵️‍♂️Динамика изменения индикатора",
                "📈🔮Прогноз с Prophet",
                "📈❄️Тренд и сезонность"
            ])

        # Размер контейнера для данных
        n_col = len(list_kod_c)
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
        elif n_col == 6:
            w = 700

        # Вкладка с данными
        with t1:
            # Контейнер для данных df
            with st.container(width=w):
                st.write('📶🏦Набор данных из API МВФ')
                st.write(df)

        # Имя первой колонки c кодом страны df
        col_name = df.columns[0]
        # Фильтр на код станы
        df_f = df_c.loc[df_c[0] == col_name]
        # Получение названия страны прогноза
        prog_c = df_f.values[0][1]

        # Формирование графика исторических данных
        fig = go.Figure()
        # Цикл по выбранным странам
        for kod_c in list_kod_c:
            # Фильтр на код станы
            df_f = df_c.loc[df_c[0] == kod_c]
            # Наименование станы
            name_c = df_f[1].iloc[0]
            # Добавить на график элементы (линии)
            fig.add_trace(go.Scatter(x=df.index, y=df[kod_c], name=name_c))

        title = 'Экономический показатель - ' + indic + ', за период с ' + str(d1) + ' по ' + str(d2)
        fig.update_layout(xaxis_title='Годы',
                          yaxis_title=indic,
                          title=title)

         # Вкладка с графиком
        with t3:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Готовим данные к прогнозу
        if len(list_kod_c) >= 2:  # Если выбрано более 2-х стран
            # Убрать индекс
            df.reset_index(level=0, inplace=True)
            # Переименовать колонки по их индексу
            df.columns.values[[0, 1]] = ['ds', 'y']
            # Выбрать две колонки
            df = df.take([0, 1], axis=1)
            col_predict = df.columns[0]
        else:  # Если выбрана одна страна
            # Убрать индекс
            df.reset_index(level=0, inplace=True)
            # Переименовать колонки по их индексу
            df.columns.values[[0, 1]] = ['date', 'value']
            # Переименовать колонки по их именам
            df.rename(columns={'date': 'ds', 'value': 'y'}, inplace=True)
            col_predict = ''

        # Вкладка с данными
        with t2:
            # Контейнер для данных df_pivot
            with st.container(width=300):
                # st.write('📶🔮Данные для прогноза с Prophet: ', df.columns)
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
        fig.update_layout(title='📈🔮Прогноз изменения индикатора- ' + indic + ', ' + prog_c,
                          xaxis_title='Дата',
                          yaxis_title=indic)
        # Вкладка с графиком
        with t4:
            # Контейнер для графика
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)

        # Графики компонент (тренда и сезонности)
        fig = plot_components_plotly(model, forecast)
        fig.update_layout(title='📈❄️Тренд и сезонности временного ряда' + ', ' + prog_c)
        # Вкладка с графиком
        with t5:
            with st.container(width=800, border=True):
                st.plotly_chart(fig, theme=None)