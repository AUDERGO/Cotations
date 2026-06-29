from src.rules_mec import safe_check


def compute_postures_vec(df):

    membres_inf = int(safe_check(df, 4) or safe_check(df, 1))
    poignet = safe_check(df, 5)
    epaule = safe_check(df, 6)
    dos = int(safe_check(df, 7) or safe_check(df, 3))
    cervicales = int(safe_check(df, 8) or safe_check(df, 2))

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
