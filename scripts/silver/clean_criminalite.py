import pandas as pd

print("Chargement criminalité parquet...")

# =========================
# LOAD PARQUET
# =========================

df = pd.read_parquet(
    "data/bronze/criminalite.parquet"
)

# =========================
# FILTRE PARIS
# =========================

print("Filtre Paris...")

df = df[
    df["CODGEO_2025"].astype(str).str.startswith("751")
]

# =========================
# DERNIÈRE ANNÉE
# =========================

print("Filtre dernière année...")

last_year = df["annee"].max()

df = df[df["annee"] == last_year]

print(f"Année utilisée : {last_year}")

# =========================
# SUPPRESSION NAN
# =========================

df = df.dropna(subset=["taux_pour_mille"])

# =========================
# EXTRACTION ARRONDISSEMENT
# =========================

df["arrondissement"] = (
    df["CODGEO_2025"]
    .astype(str)
    .str[-2:]
    .astype(int)
)

# =========================
# COLONNES UTILES
# =========================

df = df[[
    "arrondissement",
    "indicateur",
    "nombre",
    "taux_pour_mille"
]]

# =========================
# RESULTAT
# =========================

print(df.head())

print(df.info())

# =========================
# SAVE SILVER
# =========================

output_path = "data/silver/criminalite_clean.csv"

df.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")