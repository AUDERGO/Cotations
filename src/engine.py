import pandas as pd
from src.reader import read_resultats, read_ergo
from src.rules_mec import compute_postures_mec
from src.rules_vec import compute_postures_vec
from src.utils import get_poste_name
from src.controls import check_poste_engins


def process_poste(file_path, engins_df):

    name = get_poste_name(file_path.name)

    is_mec = file_path.name.startswith("MEC")

    resultats = read_resultats(file_path)
    ergo = read_ergo(file_path)

    print(f"Traitement : {name}")

    check_poste_engins(name, engins_df)

    if is_mec:
        postures = compute_postures_mec(resultats)
    else:
        postures = compute_postures_vec(resultats)

    engin_row = engins_df.loc[
        engins_df["Poste"] == name
    ].iloc[0]

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


def run_from_folders(mec_folder, vec_folder, engins_file, output_file):

    engins_df = pd.read_excel(engins_file)

    results = []

    from pathlib import Path

    for folder in [mec_folder, vec_folder]:
        for file in Path(folder).glob("*.xlsx"):
            try:
                res = process_poste(file, engins_df)
                results.append(res)
            except Exception as e:
                print(f"Erreur sur {file.name}: {e}")

    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)

    return df
