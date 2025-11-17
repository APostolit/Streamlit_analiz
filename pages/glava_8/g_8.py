import streamlit as st

# Настройка параметров данной страницы
st.set_page_config(
    page_title="Глава 8", # Текст на вкладке браузера
    page_icon='📕',       # Иконка на вкладке браузера
    layout="wide",        # Использовать всю ширину страницы
    initial_sidebar_state="collapsed",  # Развернуть боковую панель
)

# Текст по центру страницы
st.columns(3)[1].header("👩🏻‍💻Листинги главы 8")

# Боковая панель
with st.sidebar:
    # Контейнер
    cont_1 = st.container(width=300)

with cont_1:
    # Раскрывающийся список
    options = st.selectbox("Листинги главы 8",
        ("Листинг 8.1", "Листинг 8.2", "Листинг 8.3", "Листинг 8.4",
         "Листинг 8.5", "Листинг 8.6", "Листинг 8.7", "Листинг 8.8",
         "Листинг 8.9", "Листинг 8.10", "Листинг 8.11", "Листинг 8.12",
         "Листинг 8.13", "Листинг 8.14"),
        index=None,
        placeholder="Выберите листинг..."
    )

# Контейнер
cont_2 = st.container(width=1000)
with cont_2:
    if options is None:
        st.write('Листинг не выбран')
    elif options == "Листинг 8.1":
        st.write('Код листинга 8.1')
        path = 'pages/glava_8/listing_8_1.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_1.py', label='🚀Выполнить код')
    elif options == "Листинг 8.2":
        st.write('Код листинга 8.2')
        path = 'pages/glava_8/listing_8_2.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_2.py', label='🚀Выполнить код')
    elif options == "Листинг 8.3":
        st.write('Код листинга 8.3')
        path = 'pages/glava_8/listing_8_3.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_3.py', label='🚀Выполнить код')
    elif options == "Листинг 8.4":
        st.write('Код листинга 8.4')
        path = 'pages/glava_8/listing_8_4.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_4.py', label='🚀Выполнить код')
    elif options == "Листинг 8.5":
        st.write('Код листинга 8.5')
        path = 'pages/glava_8/listing_8_5.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_5.py', label='🚀Выполнить код')
    elif options == "Листинг 8.6":
        st.write('Код листинга 8.6')
        path = 'pages/glava_8/listing_8_6.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_6.py', label='🚀Выполнить код')
    elif options == "Листинг 8.7":
        st.write('Код листинга 8.7')
        path = 'pages/glava_8/listing_8_7.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_7.py', label='🚀Выполнить код')
    elif options == "Листинг 8.8":
        st.write('Код листинга 8.8')
        path = 'pages/glava_8/listing_8_8.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_8.py', label='🚀Выполнить код')
    elif options == "Листинг 8.9":
        st.write('Код листинга 8.9')
        path = 'pages/glava_8/listing_8_9.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_9.py', label='🚀Выполнить код')
    elif options == "Листинг 8.10":
        st.write('Код листинга 8.10')
        path = 'pages/glava_8/listing_8_10.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_10.py', label='🚀Выполнить код')
    elif options == "Листинг 8.11":
        st.write('Код листинга 8.11')
        path = 'pages/glava_8/listing_8_11.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_11.py', label='🚀Выполнить код')
    elif options == "Листинг 8.12":
        st.write('Код листинга 8.12')
        path = 'pages/glava_8/listing_8_12.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_12.py', label='🚀Выполнить код')
    elif options == "Листинг 8.13":
        st.write('Код листинга 8.13')
        path = 'pages/glava_8/listing_8_13.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_13.py', label='🚀Выполнить код')
    elif options == "Листинг 8.14":
        st.write('Код листинга 8.14')
        path = 'pages/glava_8/listing_8_14.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_8/listing_8_14.py', label='🚀Выполнить код')
