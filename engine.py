import pandas as pd

def extract_charges(file, is_mec):

    df = pd.read_excel(file, sheet_name="Evaluation ergonomique", header=None)

    if is_mec:
        mapping = {
            "3_6_KG": (27, 9),
            "6_9_KG": (28, 9),
            "9_12_KG": (29, 9),
            "12+_KG": (30, 9),
            "materiel": (31, 9),
            "specifique": (32, 9)
        }
    else:
        mapping = {
            "3_6_KG": (23, 9),
            "6_9_KG": (24, 9),
            "9_12_KG": (25, 9),
            "12+_KG": (26, 9),
            "materiel": (27, 9),
            "specifique": (28, 9)
        }

    result = {}

    for key, (row, col) in mapping.items():
        try:
            value = df.iloc[row, col]
            result[key] = float(value) if pd.notna(value) else 0
        except:
            result[key] = 0

    return result

def safe_check(df, crit):

    # nettoyage colonnes
    df.columns = df.columns.str.strip().str.lower()

    # mapping colonnes
    if "item" not in df.columns:
        raise ValueError("❌ Colonne ITEM absente")

    # noms exacts dans ton fichier
    col_j = "points jaunes"
    col_r = "points rouges"

    if col_j not in df.columns or col_r not in df.columns:
        raise ValueError("❌ Colonnes points jaunes / rouges absentes")

    # sécurisation valeurs
    df[col_j] = df[col_j].fillna(0)
    df[col_r] = df[col_r].fillna(0)

    # filtrage
    row = df[df["item"] == crit]

    if row.empty:
        return 0

    return int((row[col_j].values[0] + row[col_r].values[0]) > 0)


# -------- MEC --------
def compute_postures_mec(df):
    membres_inf = safe_check(df, 3)
    poignet = safe_check(df, 8)
    epaule = safe_check(df, 9)
    dos = safe_check(df, 10)
    cervicales = safe_check(df, 11)

    posture = int(membres_inf or poignet or epaule or dos or cervicales)

    return membres_inf, poignet, epaule, dos, cervicales, posture


# -------- VEC --------
def compute_postures_vec(df):
    membres_inf = int(safe_check(df, 4) or safe_check(df, 1))
    poignet = safe_check(df, 5)
    epaule = safe_check(df, 6)
    dos = int(safe_check(df, 7) or safe_check(df, 3))
    cervicales = int(safe_check(df, 8) or safe_check(df, 2))

    posture = int(membres_inf or poignet or epaule or dos or cervicales)

    return membres_inf, poignet, epaule, dos, cervicales, posture


# -------- MAIN --------
def process_files(mec_files, vec_files, engins_file):

    engins_df = pd.read_excel(engins_file)

    results = []

    # MEC
    for file in mec_files:

        name = file.name.replace(".xlsx", "")

        df = pd.read_excel(file, sheet_name="Résultats")

        membres_inf, poignet, epaule, dos, cervicales, posture = compute_postures_mec(df)

        match = engins_df.loc[engins_df["Poste"] == name]

        if match.empty:
            st.error(f"❌ Poste absent fichier engins : {name}")
            continue

        engin_row = match.iloc[0]

        results.append({
            "Poste": name,
            "Engin": engin_row["Engin"],
            "engin_debout": engin_row["engin_debout"],
            "engin_frontal": engin_row["engin_frontal"],
            "engin_retract": engin_row["engin_retract"],
            "engin_tous": int(
                engin_row["engin_debout"] == 1 and
                engin_row["engin_frontal"] == 1 and
                engin_row["engin_retract"] == 1
            ),
            "membres_inf": membres_inf,
            "poignet": poignet,
            "epaule": epaule,
            "dos": dos,
            "cervicales": cervicales,
            "posture": posture
        })

    # VEC
    for file in vec_files:

        name = file.name.replace(".xlsx", "")

        df = pd.read_excel(file, sheet_name="Résultats")

        membres_inf, poignet, epaule, dos, cervicales, posture = compute_postures_vec(df)

        match = engins_df.loc[engins_df["Poste"] == name]

        if match.empty:
            st.error(f"❌ Poste absent fichier engins : {name}")
            continue

        engin_row = match.iloc[0]
        
        results.append({
            "Poste": name,
            "Engin": engin_row["Engin"],
            "engin_debout": engin_row["engin_debout"],
            "engin_frontal": engin_row["engin_frontal"],
            "engin_retract": engin_row["engin_retract"],
            "engin_tous": int(
                engin_row["engin_debout"] == 1 and
                engin_row["engin_frontal"] == 1 and
                engin_row["engin_retract"] == 1
            ),
            "membres_inf": membres_inf,
            "poignet": poignet,
            "epaule": epaule,
            "dos": dos,
            "cervicales": cervicales,
            "posture": posture
        })

    return pd.DataFrame(results)
