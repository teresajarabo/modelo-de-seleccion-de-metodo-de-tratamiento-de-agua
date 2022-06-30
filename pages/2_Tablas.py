import streamlit as st
import pandas as pd

df_fuente = pd.read_csv('fuente_agua.csv')
df_suelos = pd.read_csv('uso_suelos.csv')
df_color_sabor = pd.read_csv('color_sabor.csv')
df_pH = pd.read_csv('pH_agua.csv')

st.header('La calidad del agua')
st.markdown('A continuación se muestran las tablas empleadas en el modelo de selección para averiguar la calidad del agua.')

st.subheader('Fuente de agua')
st.table(df_fuente)

st.subheader('Uso de los suelos')
st.table(df_suelos)

st.subheader('Color y sabor del agua')
st.table(df_color_sabor)

st.subheader('pH del agua')
st.table(df_pH)