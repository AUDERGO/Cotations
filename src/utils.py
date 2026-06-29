def clean_poste_name(file_name):
    return (
        file_name
        .replace("MEC_", "")
        .replace("VEC_", "")
        .replace(".xlsx", "")
    )
