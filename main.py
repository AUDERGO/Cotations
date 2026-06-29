from pathlib import Path
import pandas as pd
from config import MEC_PATH, VEC_PATH, ENGINS_FILE, OUTPUT_FILE
from src.engine import process_poste, load_engins


def run():

    engins_df = load_engins(ENGINS_FILE)
    results = []

    for folder in [MEC_PATH, VEC_PATH]:
        for file in Path(folder).glob("*.xlsx"):
            try:
                res = process_poste(file, engins_df)
                results.append(res)
            except Exception as e:
                print(f"Erreur sur {file.name}: {e}")

    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    run()

