import streamlit as st
import statsmodels.api as sm
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Функция загрузки данных с кэшированием
@st.cache_data
def get_data():
    try:
        # Получение временного ряда из тестового набора данных
        data = sm.datasets.co2.load_pandas()
        df = data.data
        # Параметр 'MS' группирует данные по началу месяца
        df = df['co2'].resample('MS').mean()
        # Заполняем пропуски значениями перед пропущенными значениями
        ser = df.fillna(df.bfill())
        return ser
    except Exception as e:
        st.error(f'Ошибка загрузки данных: {e}', icon="🚨")

st.markdown('### 🔮 Прогнозирование временного ряда с моделью SARIMA')
st.markdown('##### 🚗💨 Данные из Statmodels (содержание в воздухе CO2)')

# Использовать круговой спиннер
with st.spinner(text="📥Ждите, идет загрузка данных...", show_time=True):
    # Загрузка данных
    series = get_data()

with st.spinner(text="Идет обучение модели...", show_time=True):
    # Параметры модели
    p, d, q = 1, 1, 1
    P, D, Q, S = 1, 0, 1, 12
    # Создание модели
    model = sm.tsa.statespace.SARIMAX(series,
                                      order=(p, d, q),
                                      seasonal_order=(P, D, Q, S),
                                      enforce_stationarity=False,
                                      enforce_invertibility=False)
    # обучение модели
    results = model.fit()
    st.toast("Обучения модели завершено!", icon="😍")

# Оценка модели по историческим данным - статический прогноз
pred = results.get_prediction(start=pd.to_datetime('1990-01-01'),
                                  dynamic=False)
pred_ci = pred.conf_int()

# Прогнозируемые и истинные значения из временного ряда
y_forecasted = pred.predicted_mean
y_truth = series['1998-01-01':]
# Среднеквадратичная ошибка
mse_stat = ((y_forecasted - y_truth) ** 2).mean()

# Создаем вкладки
t1, t2, t3, t4, t5 = st.tabs(
    ["📶🧹Данные",
     "📈🚗💨График СО2",
     "📈🔮Статический прогноз",
     "📈🔮Динамический прогноз",
     "📈🔮Прогноз на 10 лет"])

# Вкладка с данными
with t1:
    # Контейнер для данных df
    with st.container(width=300):
        st.write('📶🧹Очищенные данные🚗💨')
        st.write(series)

# Формируем график динамики изменения временного ряда
fig = go.Figure()
fig.add_trace(go.Scatter(x=series.index, y=series.values))
# Обновить подписи осей
fig.update_layout(xaxis_title="Дата",
                  yaxis_title="Уровень загрязнения",
                  title='📈🚗💨Динамика загрязнения воздуха',
                  xaxis_rangeslider_visible=True)

# Вкладка с графиком
with t2:
    # Контейнер для графика
    with st.container(width=800, border=True):
        st.plotly_chart(fig, theme=None)

# График статического прогноза
ax = series['1990':].plot(label='Наблюдения')
pred.predicted_mean.plot(ax=ax, label='Модель', alpha=.5)
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Дата')
ax.set_ylabel('Уровень CO2')
plt.legend()

# Вкладка с графиком
with t3:
    # Контейнер для графика
    with st.container(width=700, border=True):
        st.write('📈🔮Статический прогноз с matplotlib')
        st.write('☹️Среднеквадратичная ошибка прогноза', mse_stat)
        st.pyplot(plt, width="content")

# Оценка модели по историческим данным - динамический прогноз
pred_dynamic = results.get_prediction(start=pd.to_datetime('1998-01-01'),
                                        dynamic=True,
                                        full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()

# Прогнозируемые и истинные значения из временного ряда
y_forecasted = pred_dynamic.predicted_mean
y_truth = series['1998-01-01':]
# Вычислить среднеквадратичную ошибку
mse_din = ((y_forecasted - y_truth) ** 2).mean()

# Вывод графика динамического прогноза
fig = plt.figure()
ax = series['1990':].plot(label='Наблюдения')
pred_dynamic.predicted_mean.plot(ax=ax, label='Динамический прогноз')
ax.fill_between(pred_dynamic_ci.index,
                pred_dynamic_ci.iloc[:, 0],
                pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)
ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('1998-01-01'),
                 series.index[-1],
                 alpha=.1, zorder=-1)
ax.set_xlabel('Дата')
ax.set_ylabel('Уровень CO2')
plt.legend()

# Вкладка с графиком
with t4:
    # Контейнер для графика
    with st.container(width=700, border=True):
        st.write('📈🔮Динамический прогноз с matplotlib')
        st.write('Среднеквадратичная ошибка прогноза', mse_din)
        st.pyplot(plt, width="content")

# Прогноз на ближайшие 10 лет
pred_uc = results.get_forecast(steps=10 * 12)
# Получение доверительных интервалов прогнозов
pred_ci = pred_uc.conf_int()

# Вывод графика прогноза на будущий период
fig = plt.figure()
ax = series.plot(label='Наблюдения')
pred_uc.predicted_mean.plot(ax=ax, label='Прогноз на 10 лет')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Дата')
ax.set_ylabel('Уровень CO2')
plt.legend()

# Вкладка с графиком
with t5:
    # Контейнер для графика
    with st.container(width=700, border=True):
        st.write('📈🔮Прогноз на 10 лет с matplotlib')
        st.pyplot(plt, clear_figure=True, width="content")