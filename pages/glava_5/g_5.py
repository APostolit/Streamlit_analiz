import streamlit as st

# Настройка параметров данной страницы
st.set_page_config(
    page_title="Глава 5", # Текст на вкладке браузера
    page_icon='📕',       # Иконка на вкладке браузера
    layout="wide",        # Использовать всю ширину страницы
    initial_sidebar_state="collapsed",  # Развернуть боковую панель
)

# Текст по центру страницы
st.columns(3)[1].header("👩🏻‍💻Листинги главы 5")

# Боковая панель
with st.sidebar:
    # Контейнер
    cont_1 = st.container(width=300)

with cont_1:
    # Раскрывающийся список
    options = st.selectbox("Листинги главы 5",
        ("Листинг 5.1", "Листинг 5.2", "Листинг 5.3", "Листинг 5.4",
         "Листинг 5.5", "Листинг 5.6"),
        index=None,
        placeholder="Выберите листинг..."
    )

# Контейнер
cont_2 = st.container(width=1000)
with cont_2:
    if options is None:
        st.write('Листинг не выбран')
    elif options == "Листинг 5.1":
        st.write('Код листинга 5.1')
        path = 'pages/glava_5/listing_5_1.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_5/listing_5_1.py', label='🚀Выполнить код')
    elif options == "Листинг 5.2":
        st.write('Код листинга 5.2')
        path = 'pages/glava_5/listing_5_2.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_5/listing_5_2.py', label='🚀Выполнить код')
    elif options == "Листинг 5.3":
        st.write('Код листинга 5.3')
        path = 'pages/glava_5/listing_5_3.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_5/listing_5_3.py', label='🚀Выполнить код')
    elif options == "Листинг 5.4":
        st.write('Код листинга 5.4')
        path = 'pages/glava_5/listing_5_4.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_5/listing_5_4.py', label='🚀Выполнить код')
    elif options == "Листинг 5.5":
        st.write('Код листинга 5.5')
        path = 'pages/glava_5/listing_5_5.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_5/listing_5_5.py', label='🚀Выполнить код')
    elif options == "Листинг 5.6":
        st.write('Код листинга 5.6')
        path = 'pages/glava_5/listing_5_6.py'
        file = open(path, 'r')
        code = file.read()
        st.code(code, language="python", line_numbers=True)
        st.divider()  # Разделитель
        st.page_link('pages/glava_5/listing_5_6.py', label='🚀Выполнить код')