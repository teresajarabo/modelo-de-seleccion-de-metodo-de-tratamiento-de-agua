import streamlit as st
import pandas as pd

df_comparativa = pd.read_csv('tabla_comparativa.csv')

st.header('Tabla comparativa')
st.table(df_comparativa)
st.caption('El caudal está en litros por minuto')