import pandas as pd

print("Chargement population âgée...")

df = pd.read_csv(
    "data/bronze/population_agee.csv",
    sep=";",
    low_memory=False
)

# =========================
# FILTRE PARIS
# =========================

df = df[
    df["CODGEO"]
    .astype(str)
    .str.startswith("751")
]

# =========================
# SENIORS
# 65-79 ans + 80 ans et +
# =========================

df = df[
    df["AGEMEN7"].isin([65, 80])
]

# =========================
# ARRONDISSEMENT
# =========================

df["arrondissement"] = (
    df["CODGEO"]
    .astype(str)
    .str[-2:]
    .astype(int)
)

# =========================
# POPULATION ÂGÉE
# =========================

seniors = (
    df.groupby("arrondissement")["NB"]
    .sum()
    .reset_index()
)

seniors.columns = [
    "arrondissement",
    "population_agee"
]

# =========================
# POPULATION TOTALE PARIS
# =========================

print("Chargement population Paris...")

population = pd.read_csv(
    "data/silver/population_paris.csv"
)

population = population[
    ["arrondissement", "population"]
]

# =========================
# FUSION
# =========================

seniors = pd.merge(
    seniors,
    population,
    on="arrondissement",
    how="left"
)

# =========================
# TAUX SENIORS
# =========================

seniors["taux_seniors"] = (
    seniors["population_agee"]
    /
    seniors["population"]
) * 100

seniors["taux_seniors"] = (
    seniors["taux_seniors"]
    .round(2)
)

# =========================
# TRI
# =========================

seniors = seniors.sort_values(
    by="arrondissement"
)

# =========================
# RESULTAT
# =========================

print("\nRésultat :")
print(seniors)

print("\nStatistiques :")
print(
    seniors["taux_seniors"]
    .describe()
)

# =========================
# SAVE
# =========================

output_path = (
    "data/silver/population_agee_clean.csv"
)

seniors.to_csv(
    output_path,
    index=False
)

print(
    f"\nFichier sauvegardé : {output_path}"
)