import pandas as pd

def safe_check(df, crit):
    row = df[df["N°"] == crit]
    if row.empty:
        return 0
    return int((row["J"].values[0] + row["R"].values[0]) > 0)


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

        df = pd.read_excel(file, sheet_name="Evaluation ergonomique")

        membres_inf, poignet, epaule, dos, cervicales, posture = compute_postures_mec(df)

        engin_row = engins_df.loc[engins_df["Poste"] == name].iloc[0]

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

        df = pd.read_excel(file, sheet_name="Evaluation ergonomique")

        membres_inf, poignet, epaule, dos, cervicales, posture = compute_postures_vec(df)

        engin_row = engins_df.loc[engins_df["Poste"] == name].iloc[0]

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
