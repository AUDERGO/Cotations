import pandas as pd
from openpyxl import load_workbook


# =========================
# LECTURE TABLE1 (Résultats)
# =========================
def read_table1(file):

    from io import BytesIO

    content = file.read()
    file.seek(0)

    wb = load_workbook(
        filename=BytesIO(content),
        data_only=True,
        read_only=True
    )

    ws = wb["Résultats"]

    table = ws.tables["Table1"]
    data = ws[table.ref]

    rows = list(data)

    columns = [cell.value for cell in rows[0]]
    values = [[cell.value for cell in row] for row in rows[1:]]

    df = pd.DataFrame(values, columns=columns)

    df.columns = df.columns.str.strip().str.lower()
    df = df[df["item"].notna()]

    return df


# =========================
# SAFE CHECK POSTURE
# =========================
def safe_check(df, crit):

    col_j = None
    col_r = None

    for col in df.columns:
        if "jaune" in col:
            col_j = col
        if "rouge" in col:
            col_r = col

    if col_j is None or col_r is None:
        raise ValueError("Colonnes jaunes / rouges introuvables")

    df[col_j] = pd.to_numeric(df[col_j], errors="coerce").fillna(0)
    df[col_r] = pd.to_numeric(df[col_r], errors="coerce").fillna(0)

    row = df[df["item"] == crit]

    if row.empty:
        return 0

    return int((row[col_j].values[0] + row[col_r].values[0]) > 0)


# =========================
# POSTURES MEC / VEC
# =========================
def compute_postures_mec(df):
    return {
        "membres_inf": safe_check(df, 3),
        "poignet": safe_check(df, 8),
        "epaule": safe_check(df, 9),
        "dos": safe_check(df, 10),
        "cervicales": safe_check(df, 11)
    }


def compute_postures_vec(df):
    return {
        "membres_inf": int(safe_check(df, 4) or safe_check(df, 1)),
        "poignet": safe_check(df, 5),
        "epaule": safe_check(df, 6),
        "dos": int(safe_check(df, 7) or safe_check(df, 3)),
        "cervicales": int(safe_check(df, 8) or safe_check(df, 2))
    }


# =========================
# CHARGES (Evaluation ergonomique)
# =========================
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

    for key, (r, c) in mapping.items():
        try:
            val = df.iloc[r, c]
            result[key] = float(val) if pd.notna(val) else 0
        except:
            result[key] = 0

    return result


# =========================
# FONCTION PRINCIPALE
# =========================
def process_files(mec_files, vec_files, engins_file):

    engins_df = pd.read_excel(engins_file)

    engins_df["Poste"] = engins_df["Poste"].str.strip()

    results = []

    # ---------- MEC ----------
    for file in mec_files:

        name = file.name.replace(".xlsx", "")
        
        file.seek(0)
        df = read_table1(file)
        postures = compute_postures_mec(df)
        file.seek(0)
        charges = extract_charges(file, True)

        match = engins_df[engins_df["Poste"] == name]
        if match.empty:
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
            "Charge": 0,
            **charges,
            **postures,
            "posture": int(any(postures.values()))
        })

    # ---------- VEC ----------
    for file in vec_files:

        name = file.name.replace(".xlsx", "")
        
        file.seek(0)
        df = read_table1(file)
        postures = compute_postures_vec(df)
        file.seek(0)
        charges = extract_charges(file, False)

        match = engins_df[engins_df["Poste"] == name]
        if match.empty:
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
            "Charge": 0,
            **charges,
            **postures,
            "posture": int(any(postures.values()))
        })

    return pd.DataFrame(results)
