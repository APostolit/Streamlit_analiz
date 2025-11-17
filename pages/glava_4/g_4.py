import streamlit as st

# Настройка параметров данной страницы
st.set_page_config(
    page_title="Глава 4", # Текст на вкладке браузера
    page_icon='📕',       # Иконка на вкладке браузера
    layout="wide",        # Использовать всю ширину страницы
    initial_sidebar_state="collapsed",  # Развернуть боковую панель
)

# Текст по центру страницы
st.columns(3)[1].header("👩🏻‍💻Листинги главы 4")

# Боковая панель
with st.sidebar:
    # Контейнер
    cont_1 = st.container(width=300)

with cont_1:
    # Раскрывающийся список
    options = st.selectbox("Листинги главы 4",
        ("Листинг 4.1", "Листинг 4.2", "Листинг 4.3", "Листинг 4.4",
         "Листинг 4.5", "Листинг 4.6", "Листинг 4.7", "Листинг 4.8",
         "Листинг 4.9", "Листинг 4.10", "Листинг 4.11", "Листинг 4.12",
         "Листинг 4.13", "Листинг 4.14", "Листинг 4.15"),
        index=None,
        placeholder="Выберите листинг..."
    )

# Контейнер
cont_2 = st.container(width=1000)
with cont_2:
    if options is None:
        st.write('Листинг не выбран')
    elif options == "Листинг 4.1":
        st.write('Код листинга 4.1')
        path = 'pages/glava_4/listing_4_1.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_1.py', label='🚀Выполнить код')
    elif options == "Листинг 4.2":
        st.write('Код листинга 4.2')
        path = 'pages/glava_4/listing_4_2.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_2.py', label='🚀Выполнить код')
    elif options == "Листинг 4.3":
        st.write('Код листинга 4.3')
        path = 'pages/glava_4/listing_4_3.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_3.py', label='🚀Выполнить код')
    elif options == "Листинг 4.4":
        st.write('Код листинга 4.4')
        path = 'pages/glava_4/listing_4_4.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_4.py', label='🚀Выполнить код')
    elif options == "Листинг 4.5":
        st.write('Код листинга 4.5')
        path = 'pages/glava_4/listing_4_5.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_5.py', label='🚀Выполнить код')
    elif options == "Листинг 4.6":
        st.write('Код листинга 4.6')
        path = 'pages/glava_4/listing_4_6.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_6.py', label='🚀Выполнить код')
    elif options == "Листинг 4.7":
        st.write('Код листинга 4.7')
        path = 'pages/glava_4/listing_4_7.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_7.py', label='🚀Выполнить код')
    elif options == "Листинг 4.8":
        st.write('Код листинга 4.8')
        path = 'pages/glava_4/listing_4_8.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_8.py', label='🚀Выполнить код')
    elif options == "Листинг 4.9":
        st.write('Код листинга 4.9')
        path = 'pages/glava_4/listing_4_9.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_9.py', label='🚀Выполнить код')
    elif options == "Листинг 4.10":
        st.write('Код листинга 4.10')
        path = 'pages/glava_4/listing_4_10.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_10.py', label='🚀Выполнить код')
    elif options == "Листинг 4.11":
        st.write('Код листинга 4.11')
        path = 'pages/glava_4/listing_4_11.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_11.py', label='🚀Выполнить код')
    elif options == "Листинг 4.12":
        st.write('Код листинга 4.12')
        path = 'pages/glava_4/listing_4_12.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_12.py', label='🚀Выполнить код')
    elif options == "Листинг 4.13":
        st.write('Код листинга 4.13')
        path = 'pages/glava_4/listing_4_13.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_13.py', label='🚀Выполнить код')
    elif options == "Листинг 4.14":
        st.write('Код листинга 4.14')
        path = 'pages/glava_4/listing_4_14.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_14.py', label='🚀Выполнить код')
    elif options == "Листинг 4.15":
        st.write('Код листинга 4.15')
        path = 'pages/glava_4/listing_4_15.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_4/listing_4_15.py', label='🚀Выполнить код')