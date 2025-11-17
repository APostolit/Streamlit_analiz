import streamlit as st
import pandas as pd

# Генератор данных
period = 6
rng = pd.date_range(start="1-1-2025", periods=period, freq="2D")

# Объект Series (6 строк, с датами через день)
s6 = pd.Series(data=range(period), index=rng)

# Объект Series (11 строк, без заполнения строк данными)
s11 = s6.asfreq(freq="1D")

# Объект Series (11 строк, c заполнением пустот методом ffill)
s11_fill = s6.asfreq(method="ffill", freq="1D")

# Объект Series (11 строк c заполнением пустот методом pad)
s11_pad = s6.asfreq(method="pad", freq="1D")

# Объект Series (11 строк c заполнением пустот методом bfill)
s11_bfill = s6.asfreq(method="bfill", freq="1D")

# Объект Series (11 строк c заполнением пустот методом fill_value)
s11_val = s6.asfreq(fill_value=10.0, freq="1D")

# Преобразовать Series в df
s6 = s6.to_frame()
s11 = s11.to_frame()
s11_fill = s11_fill.to_frame()
s11_pad = s11_pad.to_frame()
s11_bfill = s11_bfill.to_frame()
s11_val = s11_val.to_frame()

st.subheader('⬆️ Увеличение частоты временного ряда')
st.markdown('##### ☝Метод asfreq')

# Контейнер для вывода данных
with st.container(width=600):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('6 дней (через день)')
        st.write(s6)
    with col2:
        st.write('11 дней (пустой)')
        st.write(s11)
    with col3:
        st.write('11 дней (fill)')
        st.write(s11_fill)

# Контейнер для вывода данных
with st.container(width=600):
    col4, col5, col6 = st.columns(3)
    with col4:
        st.write('11 дней (pad)')
        st.write(s11_pad)
    with col5:
        st.write('11 дней (bfill)')
        st.write(s11_bfill)
    with col6:
        st.write('11 дней (val)')
        st.write(s11_val)