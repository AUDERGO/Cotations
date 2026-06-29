import streamlit as st
from engine import process_files
from datetime import datetime
import io

st.title("🧠 Cotation ergonomique")

st.markdown("### 📂 Charger les fichiers")

mec_files = st.file_uploader(
    "Fichiers MEC",
    accept_multiple_files=True,
    type=["xlsx"]
)

vec_files = st.file_uploader(
    "Fichiers VEC",
    accept_multiple_files=True,
    type=["xlsx"]
)

engins_file = st.file_uploader(
    "Fichier cotations_engins.xlsx",
    type=["xlsx"]
)

# -------- bouton --------
if st.button("🚀 Lancer le calcul"):

    if not mec_files or not vec_files or not engins_file:
        st.error("⚠️ Merci de charger tous les fichiers")
    else:

        df = process_files(mec_files, vec_files, engins_file)

        st.success("✅ Calcul terminé")

        st.write("📊 Résultats")
        st.dataframe(df)

        st.write(f"Nombre de postes traités : {len(df)}")

        # ✅ EXPORT EXCEL (AU BON ENDROIT)

        now = datetime.now()
        filename = now.strftime("bilan_cotations_%Y-%m-%d_%H-%M.xlsx")

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)

        st.download_button(
            label="⬇️ Télécharger résultats (Excel)",
            data=buffer,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
