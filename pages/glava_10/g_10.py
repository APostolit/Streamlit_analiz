import streamlit as st

# Настройка параметров данной страницы
st.set_page_config(
    page_title="Глава 10", # Текст на вкладке браузера
    page_icon='📕',       # Иконка на вкладке браузера
    layout="wide",        # Использовать всю ширину страницы
    initial_sidebar_state="collapsed",  # Развернуть боковую панель
)

# Текст по центру страницы
st.columns(3)[1].header("👩🏻‍💻Листинги главы 10")

# Боковая панель
with st.sidebar:
    # Контейнер
    cont_1 = st.container(width=300)

with cont_1:
    # Раскрывающийся список
    options = st.selectbox("Листинги главы 10",
        ("Листинг 10.1", "Листинг 10.2", "Листинг 10.3", "Листинг 10.4",
         "Листинг 10.5", "Листинг 10.6", "Листинг 10.7"),
        index=None,
        placeholder="Выберите листинг..."
    )

# Контейнер
cont_2 = st.container(width=1000)
with cont_2:
    if options is None:
        st.write('Листинг не выбран')
    elif options == "Листинг 10.1":
        st.write('Код листинга 10.1')
        path = 'pages/glava_10/listing_10_1.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_10/listing_10_1.py', label='🚀Выполнить код')
    elif options == "Листинг 10.2":
        st.write('Код листинга 10.2')
        path = 'pages/glava_10/listing_10_2.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_10/listing_10_2.py', label='🚀Выполнить код')
    elif options == "Листинг 10.3":
        st.write('Код листинга 10.3')
        path = 'pages/glava_10/listing_10_3.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_10/listing_10_3.py', label='🚀Выполнить код')
    elif options == "Листинг 10.4":
        st.write('Код листинга 10.4')
        path = 'pages/glava_10/listing_10_4.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_10/listing_10_4.py', label='🚀Выполнить код')
