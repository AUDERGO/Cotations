import pandas as pd
from src.reader import read_resultats, read_ergo
from src.rules_mec import compute_postures_mec
from src.rules_vec import compute_postures_vec
from src.utils import clean_poste_name
from src.controls import check_poste_engins


def load_engins(path):
    return pd.read_excel(path)


def process_poste(file_path, engins_df):

    name = clean_poste_name(file_path.name)
    is_mec = "MEC" in file_path.name

    resultats = read_resultats(file_path)
    ergo = read_ergo(file_path)

    print(f"Traitement : {name}")

    check_poste_engins(name, engins_df)

    if is_mec:
        postures = compute_postures_mec(resultats)
    else:
        postures = compute_postures_vec(resultats)

    engin_row = engins_df.loc[engins_df["Poste"] == name].iloc[0]

    return {
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
        **postures,
        "Temps": 0
    }
