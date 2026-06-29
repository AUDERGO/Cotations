import pandas as pd

def read_resultats(file_path):
    return pd.read_excel(file_path, sheet_name="Résultats")

def read_ergo(file_path):
    return pd.read_excel(file_path, sheet_name="Evaluation ergonomique")
