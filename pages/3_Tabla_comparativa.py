import streamlit as st
import pandas as pd

df_comparativa = pd.read_csv('tabla_comparativa.csv')

st.header('Tabla comparativa')
st.table(df_comparativa.style.format(subset=['Caudal'], formatter="{:.2f}"))
st.caption('El caudal está en litros por día')