# Эмодзи
# https://emojidb.org/web-emojis
import streamlit as st

# Сделать доступной всю ширину страницы
st.set_page_config(layout="wide")
st.set_page_config(initial_sidebar_state="collapsed")

# Иконка приложения
with st.sidebar:
    st.logo(image='favicon.ico', icon_image='favicon.ico', size="large")

# Создание страниц в виде объектов -------------------------------
# Глава 1
g_1 = st.Page(page="pages/glava_1/g_1.py", title="📝 Листинги главы 1")
pg_1_1 = st.Page('pages/glava_1/listing_1_1.py', title="🚀Выполнить 1.1")
pg_1_2 = st.Page('pages/glava_1/listing_1_2.py', title="🚀Выполнить 1.2")
pg_1_3 = st.Page('pages/glava_1/listing_1_3.py', title="🚀Выполнить 1.3")
pg_1_4 = st.Page('pages/glava_1/listing_1_4.py', title="🚀Выполнить 1.4")
pg_1_5 = st.Page('pages/glava_1/listing_1_5.py', title="🚀Выполнить 1.5")
pg_1_6 = st.Page('pages/glava_1/listing_1_6.py', title="🚀Выполнить 1.6")
pg_1_7 = st.Page('pages/glava_1/listing_1_7.py', title="🚀Выполнить 1.7")
pg_1_8 = st.Page('pages/glava_1/listing_1_8.py', title="🚀Выполнить 1.8")
pg_1_9 = st.Page('pages/glava_1/listing_1_9.py', title="🚀Выполнить 1.9")
pg_1_10 = st.Page('pages/glava_1/listing_1_10.py', title="🚀Выполнить 1.10")
pg_1_11 = st.Page('pages/glava_1/listing_1_11.py', title="🚀Выполнить 1.11")
pg_1_12 = st.Page('pages/glava_1/listing_1_12.py', title="🚀Выполнить 1.12")
pg_1_13 = st.Page('pages/glava_1/listing_1_13.py', title="🚀Выполнить 1.13")
pg_1_14 = st.Page('pages/glava_1/listing_1_14.py', title="🚀Выполнить 1.14")

# Глава 3
g_3 = st.Page(page="pages/glava_3/g_3.py", title="📝 Листинги главы 3")
pg_3_1 = st.Page('pages/glava_3/listing_3_1.py', title="🚀Выполнить 3.1")
pg_3_2 = st.Page('pages/glava_3/listing_3_2.py', title="🚀Выполнить 3.2")
pg_3_3 = st.Page('pages/glava_3/listing_3_3.py', title="🚀Выполнить 3.3")
pg_3_4 = st.Page('pages/glava_3/listing_3_4.py', title="🚀Выполнить 3.4")
pg_3_5 = st.Page('pages/glava_3/listing_3_5.py', title="🚀Выполнить 3.5")
pg_3_6 = st.Page('pages/glava_3/listing_3_6.py', title="🚀Выполнить 3.6")
pg_3_7 = st.Page('pages/glava_3/listing_3_7.py', title="🚀Выполнить 3.7")
pg_3_8 = st.Page('pages/glava_3/listing_3_8.py', title="🚀Выполнить 3.8")


# Глава 4
g_4 = st.Page(page="pages/glava_4/g_4.py", title="📝 Листинги главы 4")
pg_4_1 = st.Page('pages/glava_4/listing_4_1.py', title="🚀Выполнить 4.1")
pg_4_2 = st.Page('pages/glava_4/listing_4_2.py', title="🚀Выполнить 4.2")
pg_4_3 = st.Page('pages/glava_4/listing_4_3.py', title="🚀Выполнить 4.3")
pg_4_4 = st.Page('pages/glava_4/listing_4_4.py', title="🚀Выполнить 4.4")
pg_4_5 = st.Page('pages/glava_4/listing_4_5.py', title="🚀Выполнить 4.5")
pg_4_6 = st.Page('pages/glava_4/listing_4_6.py', title="🚀Выполнить 4.6")
pg_4_7 = st.Page('pages/glava_4/listing_4_7.py', title="🚀Выполнить 4.7")
pg_4_8 = st.Page('pages/glava_4/listing_4_8.py', title="🚀Выполнить 4.8")
pg_4_9 = st.Page('pages/glava_4/listing_4_9.py', title="🚀Выполнить 4.9")
pg_4_10 = st.Page('pages/glava_4/listing_4_10.py', title="🚀Выполнить 4.10")
pg_4_11 = st.Page('pages/glava_4/listing_4_11.py', title="🚀Выполнить 4.11")
pg_4_12 = st.Page('pages/glava_4/listing_4_12.py', title="🚀Выполнить 4.12")
pg_4_13 = st.Page('pages/glava_4/listing_4_13.py', title="🚀Выполнить 4.13")
pg_4_14 = st.Page('pages/glava_4/listing_4_14.py', title="🚀Выполнить 4.14")
pg_4_15 = st.Page('pages/glava_4/listing_4_15.py', title="🚀Выполнить 4.15")

# Глава 5
g_5 = st.Page(page="pages/glava_5/g_5.py", title="📝 Листинги главы 5")
pg_5_1 = st.Page('pages/glava_5/listing_5_1.py', title="🚀Выполнить 5.1")
pg_5_2 = st.Page('pages/glava_5/listing_5_2.py', title="🚀Выполнить 5.2")
pg_5_3 = st.Page('pages/glava_5/listing_5_3.py', title="🚀Выполнить 5.3")
pg_5_4 = st.Page('pages/glava_5/listing_5_4.py', title="🚀Выполнить 5.4")
pg_5_5 = st.Page('pages/glava_5/listing_5_5.py', title="🚀Выполнить 5.5")
pg_5_6 = st.Page('pages/glava_5/listing_5_6.py', title="🚀Выполнить 5.6")

# Глава 6
g_6 = st.Page(page="pages/glava_6/g_6.py", title="📝 Листинги главы 6")
pg_6_1 = st.Page('pages/glava_6/listing_6_1.py', title="🚀Выполнить 6.1")
pg_6_2 = st.Page('pages/glava_6/listing_6_2.py', title="🚀Выполнить 6.2")
pg_6_3 = st.Page('pages/glava_6/listing_6_3.py', title="🚀Выполнить 6.3")
pg_6_4 = st.Page('pages/glava_6/listing_6_4.py', title="🚀Выполнить 6.4")
pg_6_5 = st.Page('pages/glava_6/listing_6_5.py', title="🚀Выполнить 6.5")
pg_6_6 = st.Page('pages/glava_6/listing_6_6.py', title="🚀Выполнить 6.6")
pg_6_7 = st.Page('pages/glava_6/listing_6_7.py', title="🚀Выполнить 6.7")
pg_6_8 = st.Page('pages/glava_6/listing_6_8.py', title="🚀Выполнить 6.8")
pg_6_9 = st.Page('pages/glava_6/listing_6_9.py', title="🚀Выполнить 6.9")
pg_6_10 = st.Page('pages/glava_6/listing_6_10.py', title="🚀Выполнить 6.10")
pg_6_11 = st.Page('pages/glava_6/listing_6_11.py', title="🚀Выполнить 6.11")

# Глава 7
g_7 = st.Page(page="pages/glava_7/g_7.py", title="📝 Листинги главы 7")
pg_7_1 = st.Page('pages/glava_7/listing_7_1.py', title="🚀Выполнить 7.1")
pg_7_2 = st.Page('pages/glava_7/listing_7_2.py', title="🚀Выполнить 7.2")
pg_7_3 = st.Page('pages/glava_7/listing_7_3.py', title="🚀Выполнить 7.3")
pg_7_4 = st.Page('pages/glava_7/listing_7_4.py', title="🚀Выполнить 7.4")
pg_7_5 = st.Page('pages/glava_7/listing_7_5.py', title="🚀Выполнить 7.5")
pg_7_6 = st.Page('pages/glava_7/listing_7_6.py', title="🚀Выполнить 7.6")
pg_7_7 = st.Page('pages/glava_7/listing_7_7.py', title="🚀Выполнить 7.7")
pg_7_8 = st.Page('pages/glava_7/listing_7_8.py', title="🚀Выполнить 7.8")
pg_7_9 = st.Page('pages/glava_7/listing_7_9.py', title="🚀Выполнить 7.9")
pg_7_10 = st.Page('pages/glava_7/listing_7_10.py', title="🚀Выполнить 7.10")

# Глава 8
g_8 = st.Page(page="pages/glava_8/g_8.py", title="📝 Листинги главы 8")
pg_8_1 = st.Page('pages/glava_8/listing_8_1.py', title="🚀Выполнить 8.1")
pg_8_2 = st.Page('pages/glava_8/listing_8_2.py', title="🚀Выполнить 8.2")
pg_8_3 = st.Page('pages/glava_8/listing_8_3.py', title="🚀Выполнить 8.3")
pg_8_4 = st.Page('pages/glava_8/listing_8_4.py', title="🚀Выполнить 8.4")
pg_8_5 = st.Page('pages/glava_8/listing_8_5.py', title="🚀Выполнить 8.5")
pg_8_6 = st.Page('pages/glava_8/listing_8_6.py', title="🚀Выполнить 8.6")
pg_8_7 = st.Page('pages/glava_8/listing_8_7.py', title="🚀Выполнить 8.7")
pg_8_8 = st.Page('pages/glava_8/listing_8_8.py', title="🚀Выполнить 8.8")
pg_8_9 = st.Page('pages/glava_8/listing_8_9.py', title="🚀Выполнить 8.9")
pg_8_10 = st.Page('pages/glava_8/listing_8_10.py', title="🚀Выполнить 8.10")
pg_8_11 = st.Page('pages/glava_8/listing_8_11.py', title="🚀Выполнить 8.11")
pg_8_12 = st.Page('pages/glava_8/listing_8_12.py', title="🚀Выполнить 8.12")
pg_8_13 = st.Page('pages/glava_8/listing_8_13.py', title="🚀Выполнить 8.13")
pg_8_14 = st.Page('pages/glava_8/listing_8_14.py', title="🚀Выполнить 8.14")

# Глава 9
g_9 = st.Page(page="pages/glava_9/g_9.py", title="📝 Листинги главы 9")
pg_9_1 = st.Page('pages/glava_9/listing_9_1.py', title="🚀Выполнить 9.1")
pg_9_2 = st.Page('pages/glava_9/listing_9_2.py', title="🚀Выполнить 9.2")
pg_9_3 = st.Page('pages/glava_9/listing_9_3.py', title="🚀Выполнить 9.3")
pg_9_4 = st.Page('pages/glava_9/listing_9_4.py', title="🚀Выполнить 9.4")
pg_9_5 = st.Page('pages/glava_9/listing_9_5.py', title="🚀Выполнить 9.5")
pg_9_6 = st.Page('pages/glava_9/listing_9_6.py', title="🚀Выполнить 9.6")
pg_9_7 = st.Page('pages/glava_9/listing_9_7.py', title="🚀Выполнить 9.7")

# Глава 10
g_10 = st.Page(page="pages/glava_10/g_10.py", title="📝 Листинги главы 10")
pg_10_1 = st.Page('pages/glava_10/listing_10_1.py', title="🚀Выполнить 10.1")
pg_10_2 = st.Page('pages/glava_10/listing_10_2.py', title="🚀Выполнить 10.2")
pg_10_3 = st.Page('pages/glava_10/listing_10_3.py', title="🚀Выполнить 10.3")
pg_10_4 = st.Page('pages/glava_10/listing_10_4.py', title="🚀Выполнить 10.4")

# Создание навигатора страниц (главное меню)
pages = {
    "Глава 1": [g_1, pg_1_1, pg_1_2, pg_1_3, pg_1_4, pg_1_5, pg_1_6, pg_1_7,
                pg_1_8, pg_1_9, pg_1_10, pg_1_11, pg_1_12, pg_1_13, pg_1_14],
    "Глава 3": [g_3, pg_3_1, pg_3_2, pg_3_3, pg_3_4, pg_3_5, pg_3_6, pg_3_7,
                pg_3_8],
    "Глава 4": [g_4, pg_4_1, pg_4_2, pg_4_3, pg_4_4, pg_4_5, pg_4_6, pg_4_7,
                pg_4_8, pg_4_9, pg_4_10, pg_4_11, pg_4_12, pg_4_13, pg_4_14,
                pg_4_15],
    "Глава 5": [g_5, pg_5_1, pg_5_2, pg_5_3, pg_5_4, pg_5_5, pg_5_6],
    "Глава 6": [g_6, pg_6_1, pg_6_2, pg_6_3, pg_6_4, pg_6_5, pg_6_6,
                pg_6_7, pg_6_8, pg_6_9, pg_6_10, pg_6_11],
    "Глава 7": [g_7, pg_7_1, pg_7_2, pg_7_3, pg_7_4, pg_7_5, pg_7_6,
                pg_7_7, pg_7_8, pg_7_9, pg_7_10],
    "Глава 8": [g_8, pg_8_1, pg_8_2, pg_8_3, pg_8_4, pg_8_5, pg_8_6,
                pg_8_7, pg_8_8, pg_8_9, pg_8_10, pg_8_11, pg_8_12,
                pg_8_13, pg_8_14],
    "Глава 9": [g_9, pg_9_1, pg_9_2, pg_9_3, pg_9_4, pg_9_5, pg_9_6, pg_9_7],
    "Глава 10": [g_10, pg_10_1, pg_10_2, pg_10_3, pg_10_4],
}
pg = st.navigation(pages=pages, position="top", expanded=False)

# Запуск навигатора страниц
pg.run()