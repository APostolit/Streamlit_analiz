import streamlit as st
import pandas as pd

st.subheader('🐼Манипуляция данными DataFrame в Pandas')
# Создаем вкладки для данных
t1, t2 = st.tabs(["📶Набор данных DataFrame",
                  "↕️Сортировка данных по колонке"
                  ])

# Создаем DataFrame
df = pd.DataFrame({'А': [3, 2, 1],
                   'Б': [6, 5, 4],
                   'В': [9, 8, 7]})

# Вкладка с данными
with t1:
    st.subheader('📶Созданный набор данных - df')
    # Создать контейнер
    with st.container(width=500):
        st.dataframe(df)

# Вкладка с данными
with t2:
    st.subheader('↕️Сортировка по столбцу "A"')
    # Создать контейнер
    with st.container(width=500):
        df_sorted = df.sort_values(by='А')
        st.write(df_sorted)