import pandas as pd

print("Chargement DVF...")

# =========================
# 1. LOAD DATA
# =========================

df = pd.read_csv("data/silver/dvf_clean.csv")

# =========================
# 2. PRÉPARATION
# =========================

# Conversion date
df["date_mutation"] = pd.to_datetime(df["date_mutation"], errors="coerce")

# Supprimer lignes avec dates invalides
df = df.dropna(subset=["date_mutation"])

# Extraire année
df["annee"] = df["date_mutation"].dt.year

# Corriger type arrondissement
df["arrondissement"] = df["arrondissement"].astype(int)

print("Années détectées :", sorted(df["annee"].unique()))

# =========================
# 3. CALCUL MÉDIANE
# =========================

print("Calcul du prix médian...")

df_median = (
    df.groupby(["arrondissement", "annee"])["prix_m2"]
    .median()
    .reset_index()
)

print(df_median.head())

# =========================
# 4. PIVOT (FORMAT LARGE)
# =========================

print("Transformation pour évolution...")

df_pivot = df_median.pivot(
    index="arrondissement",
    columns="annee",
    values="prix_m2"
)

# =========================
# 5. CALCUL ÉVOLUTION
# =========================

print("Calcul de l'évolution...")

# =========================
# ÉVOLUTION GLOBALE
# =========================

df_pivot["evolution_global_%"] = ((df_pivot[2025] - df_pivot[2021]) / df_pivot[2021]) * 100

# =========================
# ÉVOLUTION ANNUELLE
# =========================

df_pivot["evol_21_22"] = ((df_pivot[2022] - df_pivot[2021]) / df_pivot[2021]) * 100
df_pivot["evol_22_23"] = ((df_pivot[2023] - df_pivot[2022]) / df_pivot[2022]) * 100
df_pivot["evol_23_24"] = ((df_pivot[2024] - df_pivot[2023]) / df_pivot[2023]) * 100
df_pivot["evol_24_25"] = ((df_pivot[2025] - df_pivot[2024]) / df_pivot[2024]) * 100

# Arrondi propre
df_pivot = df_pivot.round(2)

# =========================
# 7. RESET INDEX
# =========================

df_pivot = df_pivot.reset_index()

# =========================
# 8. RESULTAT
# =========================

print("Résultat final :")
print(df_pivot)

print(df_pivot.info())

# =========================
# 9. SAVE (GOLD)
# =========================

output_path = "data/gold/prix_median_evolution.csv"

df_pivot.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")