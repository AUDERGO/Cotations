def check_poste_engins(name, engins_df):
    if name not in engins_df["Poste"].values:
        raise ValueError(f"Poste absent du fichier engins : {name}")


def check_output(row):
    warnings = []

    if all(v == 0 for v in [
        row["epaule"], row["dos"], row["cervicales"],
        row["membres_inf"], row["poignet"]
    ]):
        warnings.append("Toutes les postures à 0")

    return warnings
