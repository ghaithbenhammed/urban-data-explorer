import pandas as pd

# =========================
# 1. CHARGEMENT
# =========================

print("Chargement des données DVF...")
df = pd.read_csv("data/bronze/dvf.csv", low_memory=False)

print(f"Nombre de lignes initial : {df.shape[0]}")

# =========================
# 2. SÉLECTION COLONNES
# =========================

df = df[[
    "valeur_fonciere",
    "surface_reelle_bati",
    "code_postal",
    "date_mutation"
]]

# =========================
# 3. CONVERSION TYPES
# =========================

df["valeur_fonciere"] = pd.to_numeric(df["valeur_fonciere"], errors="coerce")
df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors="coerce")
df["code_postal"] = pd.to_numeric(df["code_postal"], errors="coerce")

# =========================
# 4. DROP NULLS
# =========================

df = df.dropna()

print(f"Après dropna : {df.shape[0]}")

# =========================
# 5. FILTRAGE PARIS
# =========================

df = df[df["code_postal"].between(75001, 75020)]

print(f"Après filtre Paris : {df.shape[0]}")

# =========================
# 6. FILTRAGE QUALITÉ (IMPORTANT 🔥)
# =========================

# surface réaliste
df = df[df["surface_reelle_bati"] > 10]

# valeur réaliste
df = df[df["valeur_fonciere"] < 2000000]  # < 2M€

print(f"Après filtres qualité : {df.shape[0]}")

# =========================
# 7. CALCUL PRIX M²
# =========================

df["prix_m2"] = df["valeur_fonciere"] / df["surface_reelle_bati"]

# enlever prix aberrants
df = df[df["prix_m2"] < 20000]

print(f"Après filtre prix_m2 : {df.shape[0]}")

# =========================
# 8. ARRONDISSEMENT
# =========================

df["arrondissement"] = df["code_postal"] - 75000

# =========================
# 9. RESULTAT
# =========================

print("Données DVF propres :")
print(df.head())

# =========================
# 10. SAVE
# =========================

df.to_csv("data/silver/dvf_clean.csv", index=False)

print("✅ Fichier sauvegardé")