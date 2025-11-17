import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
import warnings
# Игнорировать предупреждения
warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Путь к исходному csv файлу
        name_csv = 'csv/oil_exports.csv'
        # Запрос данных в БД
        ser = pd.read_csv(name_csv, header=0, delimiter=',')
        ser = ser.loc[ser['Oil Type'] == 'Total'].filter(['Period', 'Volume (bbl/d)'])
        ser['Period'] = ser['Period'].transform(lambda x: datetime.strptime(x, '%m/%d/%Y'))
        ser.set_index(keys='Period', drop=True, inplace=True)
        ser = ser.squeeze(axis=1)
        return ser
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🔮️ Прогнозирование временного ряда с моделью ARIMA')
st.markdown('##### 🛢️ Данные CSV-файла (динамика экспорта нефти)')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    series = get_data()
    # Преобразовать Series в DataFrame
    df_1 = series.to_frame(name='volume')
    df = series.to_frame(name='volume')

# Оптимальные параметры модели (рассчитаны заранее)
p, d, q = 2, 1, 2

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Создание модели
    model = ARIMA(series, order=(p, d, q))
    # обучение модели
    results = model.fit()
    st.toast("Обучения модели завершено!", icon="😍")

# Даты предсказания на исторической выборке
start_date = '2010-01-01'
end_date = '2025-08-01'
# Оценка модели на исторической выборке
df['prediction'] = results.predict(start=start_date, end=end_date)

# Количество месяцев предсказания на будущий период
forecast_steps = 12
# Создание дат будущего периода (индексы)
predict_index = pd.date_range(start=df['volume'].index[-1], periods=forecast_steps + 1, freq='M')[1:]

# Создать DataFrame с будущим периодом
df_ind = pd.DataFrame({'Date': predict_index})
# Прогноз на будущий период (Series)
forecast = results.forecast(steps=forecast_steps)
# Создание из серии df c прогнозом на будущий период
df_predict = forecast.to_frame().reset_index()
# Извлечение колонки с прогнозом из DF
extracted_col = df_predict["predicted_mean"]
# Объединение колонки с прогнозом с датами будущего периода
df_ind = pd.concat([df_ind, extracted_col.rename("prog_noz")], axis=1)

# Создаем вкладки
t1, t2, t3, t4 = st.tabs(
    ["📶🧹Очищенные данные",
     "📶🔮Расчет прогноза",
     "📈🔮Прогноз с plotly",
     "📈🔮Прогноз с matplotlib"
     ])

# Вкладка с графиком
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🧹Исходный набор очищенных данных')
        st.write(df_1)

# Вкладка с графиком
with t2:
    # Контейнер для данных df
    with st.container(width=600):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write('🛠Оптимальные параметры модели')
            st.write('p=', p, ' d=', d, ' q=', q)
        with col2:
            # Контейнер для данных df
            with st.container(width=300):
                st.write('📶🔮Прогноз на будущие периоды')
                st.write(df_ind)

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=800, border=True):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['volume'], name="Объем экспорта"))
        fig.add_trace(go.Scatter(x=df.index, y=df['prediction'], name="Модель ARIMA"))
        fig.add_trace(go.Scatter(x=df_ind['Date'], y=df_ind['prog_noz'], name="Прогноз"))
        # Обновить подписи осей
        fig.update_layout(xaxis_title="Дата",
                          yaxis_title="Объем экспорта",
                          title='📈🔮Динамика и прогноз объема экспорта нефти (с plotly)🛢',
                          xaxis_rangeslider_visible=True)
        st.plotly_chart(fig, theme=None)

# Прогноз и доверительный интервал с библиотекой matplotlib
pred = results.get_prediction(start='2010-01-01', end='2025-08-01', dynamic=False)
pred_ci = pred.conf_int()

# Вкладка с графиком
with t4:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.write('📈🔮Динамика и прогноз объема экспорта нефти с matplotlib🛢')
        # График прогноза с matplotlib
        fig = plt.figure()
        ax = series['2010':].plot(label='История', figsize=(10, 7))
        pred.predicted_mean.plot(ax=ax, label='Прогноз', alpha=.7)
        ax.fill_between(pred_ci.index,
                        pred_ci.iloc[:, 0],
                        pred_ci.iloc[:, 1], color='k', alpha=.2)
        ax.set_xlabel('Дата')
        ax.set_ylabel('Средний объем экспорта нефти (баррелей в день)')
        plt.legend()
        st.pyplot(plt, width="content")