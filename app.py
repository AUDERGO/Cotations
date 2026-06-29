import streamlit as st
import pandas as pd
from main import run

st.title("Cotation ergonomique")

if st.button("Lancer le calcul"):
    run()
    st.success("Calcul terminé")

try:
    df = pd.read_excel("cotations_bilan.xlsx")

    st.dataframe(df)

    poste = st.selectbox("Choisir un poste", df["Poste"])

    row = df[df["Poste"] == poste].iloc[0]

    st.write("Postures", row)
except:
    st.info("Clique sur lancer")

