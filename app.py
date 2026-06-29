import streamlit as st
import pandas as pd
from src.engine import run_from_folders
import os
import tempfile

st.title("🧠 Cotation ergonomique")

# -------------------------
# INPUT UTILISATEUR
# -------------------------

st.header("1. Sélection des données")

mec_files = st.file_uploader(
    "📂 Charger fichiers MEC",
    accept_multiple_files=True
)

vec_files = st.file_uploader(
    "📂 Charger fichiers VEC",
    accept_multiple_files=True
)

engins_file = st.file_uploader(
    "📄 Charger fichier cotations_engins.xlsx",
    type=["xlsx"]
)

# -------------------------
# EXECUTION
# -------------------------

if st.button("🚀 Lancer le calcul"):

    if not mec_files or not vec_files or not engins_file:
        st.error("⚠️ Charger tous les fichiers nécessaires")
    else:

        with tempfile.TemporaryDirectory() as tmpdir:

            mec_dir = os.path.join(tmpdir, "MEC")
            vec_dir = os.path.join(tmpdir, "VEC")

            os.makedirs(mec_dir, exist_ok=True)
            os.makedirs(vec_dir, exist_ok=True)

            # sauvegarde fichiers MEC
            for file in mec_files:
                with open(os.path.join(mec_dir, file.name), "wb") as f:
                    f.write(file.read())

            # sauvegarde fichiers VEC
            for file in vec_files:
                with open(os.path.join(vec_dir, file.name), "wb") as f:
                    f.write(file.read())

            # sauvegarde engins
            engins_path = os.path.join(tmpdir, "engins.xlsx")
            with open(engins_path, "wb") as f:
                f.write(engins_file.read())

            # run engine
            df = run_from_folders(
                mec_dir,
                vec_dir,
                engins_path,
                os.path.join(tmpdir, "output.xlsx")
            )

            st.success("✅ Calcul terminé")

            st.dataframe(df)

            # DOWNLOAD
            st.download_button(
                "⬇️ Télécharger résultat",
                df.to_csv(index=False),
                file_name="cotations_bilan.csv"
            )
