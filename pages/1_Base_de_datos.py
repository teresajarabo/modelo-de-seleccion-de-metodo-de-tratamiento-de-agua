import streamlit as st
import pandas as pd

st.subheader('Base de datos del modelo')
df = pd.read_csv('model_data.csv') # Base de datos

st.table(df.style.format(subset=['Caudal'], formatter="{:.2f}"))
st.caption('El caudal está en litros por día')