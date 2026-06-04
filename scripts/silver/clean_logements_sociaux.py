import pandas as pd

print("Chargement RPLS...")

# =========================
# LOAD BRONZE
# =========================

df = pd.read_csv(
    "data/bronze/logements_sociaux.csv",
    sep=";",
    low_memory=False
)

print("Données chargées")

# =========================
# FILTRE PARIS
# =========================

print("Filtre Paris...")

df = df[
    df["Code Postal"]
    .astype(str)
    .str.startswith("75")
]

df = df.copy()

# =========================
# ARRONDISSEMENT
# =========================

print("Création arrondissement...")

df["arrondissement"] = (
    df["Code Postal"]
    .astype(str)
    .str[-2:]
)

df["arrondissement"] = (
    pd.to_numeric(
        df["arrondissement"],
        errors="coerce"
    )
)

df = df.dropna(
    subset=["arrondissement"]
)

df["arrondissement"] = (
    df["arrondissement"]
    .astype(int)
)

# =========================
# SELECTION COLONNES
# =========================

print("Nettoyage colonnes...")

df = df[[
    "arrondissement",
    "Code Postal"
]]

# =========================
# RESULTAT
# =========================

print(df.head())

print(df["arrondissement"].value_counts())

print(df.info())

# =========================
# SAVE SILVER
# =========================

output_path = (
    "data/silver/logements_sociaux_clean.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"Fichier sauvegardé : {output_path}"
)