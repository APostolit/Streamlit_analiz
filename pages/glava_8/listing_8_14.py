import streamlit as st
from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Путь к исходному csv файлу
        path_csv = 'csv/passengers.csv'
        # Загрузка данных из CSV файла
        df_1 = pd.read_csv(path_csv)
        # Превратим дату в индекс
        df_1.set_index('Month', inplace=True)
        df_1.index = pd.to_datetime(df_1.index)
        # Экзогенная переменная
        df_1['month_index'] = df_1.index.month
        return df_1
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🛠🔮 Прогнозирование временного ряда с моделью SARIMAX')
st.markdown('##### 🚍👬Данные о пассажиропотоках из файла CSV')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    df = get_data()

# Создаем вкладки
t1, t2, t3 = st.tabs(
    ["📶🧹Очищенные данные",
     "📈🔮Прогноз с plotly",
     "📈🔮Прогноз с matplotlib"])

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=350):
        st.write('📶🧹Исходный набор с экзогенными данными')
        st.dataframe(df)

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Параметры модели
    p, d, q = 1, 1, 0
    P, D, Q, S = 0, 1, 0, 12
    # создадим объект модели SARIMAX
    model = SARIMAX(df['Passengers'], exogenous=df['month_index'],
                    order=(p, d, q),
                    seasonal_order=(P, D, Q, S))
    # Применим метод .fit() - обучение
    results = model.fit()
    st.toast("Обучения модели завершено!", icon="😍")

# Количество месяцев предсказания на будущий период
forecast_steps = 24
# Создание дат будущего периода (индексы)
predict_index = pd.date_range(start=df['Passengers'].index[-1],
                              periods=forecast_steps + 1, freq='M')[1:]
# Создать DataFrame с будущим периодом
df_ind = pd.DataFrame({'Month': predict_index})
# Добавить колонку с экзогенными данными
df_ind.insert(1, "month_index", 1)

# Превратить дату в индекс
df_ind.set_index(keys='Month', inplace=True)
# Добывать колонку с экзогенными данными
df_ind['month_index'] = df_ind.index.month
# Прогноз на будущий период (Series)
forecast = results.forecast(steps=forecast_steps,
                            exog=df_ind['month_index'],
                            dynamic=False)
# Создание из Series набора df c прогнозом на будущий период
df_predict = forecast.to_frame().reset_index()
df_predict.set_index(keys='index', inplace=True)
df_predict.index.name = 'Month'

# Формируем график прогноза на будущий период
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Passengers'], name="История"))
fig.add_trace(go.Scatter(x=df_predict.index, y=df_predict['predicted_mean'], name="Прогноз"))
fig.update_layout(title='📈🔮Прогноз на будущий период (с plotly)',
                  xaxis_title="Дата",
                  yaxis_title="Пассажиропоток, тыс.чел.",
                  autosize=False,
                  xaxis_rangeslider_visible=True,
                  width=800,
                  height=500,
                  hoverlabel=dict(font_size=15))

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)

# Прогноз с интервалом прогнозирования для графика с matplotlib
pred = results.get_prediction(start=pd.to_datetime('2025-01-31'),
                              end=pd.to_datetime('2026-12-31'),
                              exog=df_ind['month_index'],
                              dynamic=False)
# Интервал прогнозирования
pred_ci = pred.conf_int()

fig = plt.figure()
# Линия с историческими данными
ax = df.plot(label='Наблюдения')
# Линия с прогнозом
pred.predicted_mean.plot(ax=ax, label='Прогноз')
# Область с доверительным интервалом
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
# Подписи к осям
ax.set_xlabel('Дата')
ax.set_ylabel('Пассажиропоток')
plt.legend(['Пассажиры', 'Месяцы', 'Прогноз'])

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=700, border=True):
        st.write('📈🔮Прогноз на будущий период (с matplotlib)')
        st.pyplot(plt, clear_figure=True, width="content")