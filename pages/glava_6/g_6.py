import streamlit as st

# Настройка параметров данной страницы
st.set_page_config(
    page_title="Глава 6", # Текст на вкладке браузера
    page_icon='📕',       # Иконка на вкладке браузера
    layout="wide",        # Использовать всю ширину страницы
    initial_sidebar_state="collapsed",  # Развернуть боковую панель
)

# Текст по центру страницы
st.columns(3)[1].header("👩🏻‍💻Листинги главы 6")

# Боковая панель
with st.sidebar:
    # Контейнер
    cont_1 = st.container(width=300)

with cont_1:
    # Раскрывающийся список
    options = st.selectbox("Листинги главы 6",
        ("Листинг 6.1", "Листинг 6.2", "Листинг 6.3", "Листинг 6.4",
         "Листинг 6.5", "Листинг 6.6", "Листинг 6.7", "Листинг 6.8",
         "Листинг 6.9", "Листинг 6.10", "Листинг 6.11"),
        index=None,
        placeholder="Выберите листинг..."
    )

# Контейнер
cont_2 = st.container(width=1000)
with cont_2:
    if options is None:
        st.write('Листинг не выбран')
    elif options == "Листинг 6.1":
        st.write('Код листинга 6.1')
        path = 'pages/glava_6/listing_6_1.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_1.py', label='🚀Выполнить код')
    elif options == "Листинг 6.2":
        st.write('Код листинга 6.2')
        path = 'pages/glava_6/listing_6_2.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_2.py', label='🚀Выполнить код')
    elif options == "Листинг 6.3":
        st.write('Код листинга 6.3')
        path = 'pages/glava_6/listing_6_3.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_3.py', label='🚀Выполнить код')
    elif options == "Листинг 6.4":
        st.write('Код листинга 6.4')
        path = 'pages/glava_6/listing_6_4.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_4.py', label='🚀Выполнить код')
    elif options == "Листинг 6.5":
        st.write('Код листинга 6.5')
        path = 'pages/glava_6/listing_6_5.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_5.py', label='🚀Выполнить код')
    elif options == "Листинг 6.6":
        st.write('Код листинга 6.6')
        path = 'pages/glava_6/listing_6_6.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_6.py', label='🚀Выполнить код')
    elif options == "Листинг 6.7":
        st.write('Код листинга 6.7')
        path = 'pages/glava_6/listing_6_7.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_7.py', label='🚀Выполнить код')
    elif options == "Листинг 6.8":
        st.write('Код листинга 6.8')
        path = 'pages/glava_6/listing_6_8.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_8.py', label='🚀Выполнить код')
    elif options == "Листинг 6.9":
        st.write('Код листинга 6.9')
        path = 'pages/glava_6/listing_6_9.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_9.py', label='🚀Выполнить код')
    elif options == "Листинг 6.10":
        st.write('Код листинга 6.10')
        path = 'pages/glava_6/listing_6_10.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_10.py', label='🚀Выполнить код')
    elif options == "Листинг 6.11":
        st.write('Код листинга 6.11')
        path = 'pages/glava_6/listing_6_11.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_6/listing_6_11.py', label='🚀Выполнить код')
