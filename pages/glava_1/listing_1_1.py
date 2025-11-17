import streamlit as st
import pandas as pd

st.subheader('🐼Создание объектов Series в Pandas')
# Создаем вкладки для данных
t1, t2 = st.tabs(["📃Series из списка",
                  "📖Series из словаря"])

# Вкладка с данными
with t1:
    st.subheader('📃Создание Series из списка')
    # Создать контейнер
    cont = st.container(width=200)
    with cont:
        # Series из списка
        data = [100, 300, 800, 500, 400]
        index = ["A", "B", "C", "D", "E"]
        s_list = pd.Series(data, index)
        st.write(s_list)
        st.write('B=', s_list['B'])
        st.write('C=', s_list.loc['C'])
        st.write('Срез C-E')
        st.write(s_list['C':'E'])

# Вкладка с данными
with t2:
    st.subheader('📖Создание Series из словаря')
    # Создать контейнер
    cont = st.container(width=200)
    with cont:
        # Series из словаря
        dic = {"A": 10.1, "B": 20.2, "C": 30.3, "D": 40.4, "E": 50.5}
        s_dic = pd.Series(data=dic)
        st.write(s_dic)
        st.write('Строки с индексами A, D, E')
        st.write(s_dic[['A', 'D', 'E']])
        st.write('Строка с индексом A')
        st.write(s_dic['A'])