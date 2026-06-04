import pandas as pd

print("Chargement données...")

# =========================
# LOAD SILVER
# =========================

logements = pd.read_csv(
    "data/silver/logements_sociaux_clean.csv"
)

population = pd.read_csv(
    "data/silver/population_paris.csv"
)

# =========================
# NOMBRE LOGEMENTS SOCIAUX
# =========================

print("Calcul logements sociaux...")

social = (
    logements.groupby("arrondissement")
    .size()
    .reset_index(name="nb_logements_sociaux")
)

# =========================
# FUSION POPULATION
# =========================

print("Fusion population...")

df = social.merge(
    population,
    on="arrondissement"
)

# =========================
# TAUX LOGEMENTS SOCIAUX
# =========================

print("Calcul taux logements sociaux...")

df["taux_logement_social"] = (
    df["nb_logements_sociaux"]
    / df["population"]
) * 100

df["taux_logement_social"] = (
    df["taux_logement_social"]
    .round(2)
)

# =========================
# TRI
# =========================

df = df.sort_values(
    by="taux_logement_social",
    ascending=False
)

# =========================
# RESULTAT
# =========================

print(df)

# =========================
# SAVE GOLD
# =========================

output_path = (
    "data/gold/logements_sociaux.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"Fichier sauvegardé : {output_path}"
)