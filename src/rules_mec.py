def safe_check(df, crit):
    row = df[df["N°"] == crit]
    if row.empty:
        return 0
    return int((row["J"].values[0] + row["R"].values[0]) > 0)


def compute_postures_mec(df):

    membres_inf = safe_check(df, 3)
    poignet = safe_check(df, 8)
    epaule = safe_check(df, 9)
    dos = safe_check(df, 10)
    cervicales = safe_check(df, 11)

    posture = int(
        membres_inf or poignet or epaule or dos or cervicales
    )

    return {
        "membres_inf": membres_inf,
        "poignet": poignet,
        "epaule": epaule,
        "dos": dos,
        "cervicales": cervicales,
        "posture": posture
    }

