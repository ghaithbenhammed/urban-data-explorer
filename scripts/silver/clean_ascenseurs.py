import pandas as pd

print("Chargement ascenseurs...")

df = pd.read_csv(
    "data/bronze/ascenseurs_logements.csv",
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
# APPARTEMENTS UNIQUEMENT
# =========================

df = df[
    df["TYPLR"] == 2
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
# LOGEMENTS AVEC ASCENSEUR
# =========================

avec_ascenseur = (
    df[df["ASCEN"] == 1]
    .groupby("arrondissement")["NB"]
    .sum()
    .reset_index()
)

avec_ascenseur.columns = [
    "arrondissement",
    "logements_avec_ascenseur"
]

# =========================
# LOGEMENTS SANS ASCENSEUR
# =========================

sans_ascenseur = (
    df[df["ASCEN"] == 2]
    .groupby("arrondissement")["NB"]
    .sum()
    .reset_index()
)

sans_ascenseur.columns = [
    "arrondissement",
    "logements_sans_ascenseur"
]

# =========================
# FUSION
# =========================

ascenseurs = pd.merge(
    avec_ascenseur,
    sans_ascenseur,
    on="arrondissement",
    how="outer"
)

ascenseurs = ascenseurs.fillna(0)

# =========================
# TOTAL LOGEMENTS
# =========================

ascenseurs["total_logements"] = (
    ascenseurs["logements_avec_ascenseur"]
    +
    ascenseurs["logements_sans_ascenseur"]
)

# =========================
# TAUX SANS ASCENSEUR
# =========================

ascenseurs["taux_sans_ascenseur"] = (
    ascenseurs["logements_sans_ascenseur"]
    /
    ascenseurs["total_logements"]
) * 100

ascenseurs["taux_sans_ascenseur"] = (
    ascenseurs["taux_sans_ascenseur"]
    .round(2)
)

# =========================
# TRI
# =========================

ascenseurs = ascenseurs.sort_values(
    by="arrondissement"
)

# =========================
# RESULTAT
# =========================

print("\nRésultat :")
print(ascenseurs)

print("\nStatistiques :")
print(
    ascenseurs[
        "taux_sans_ascenseur"
    ].describe()
)

# =========================
# SAVE
# =========================

output_path = (
    "data/silver/ascenseurs_clean.csv"
)

ascenseurs.to_csv(
    output_path,
    index=False
)

print(
    f"\nFichier sauvegardé : {output_path}"
)