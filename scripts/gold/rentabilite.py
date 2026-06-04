import pandas as pd

# =========================
# 1. CHARGEMENT
# =========================

print("Chargement des données...")

dvf = pd.read_csv("data/silver/dvf_clean.csv")
loyers = pd.read_csv("data/silver/loyers_clean.csv")

# =========================
# 2. PRÉPARATION
# =========================

# Corriger type arrondissement
dvf["arrondissement"] = dvf["arrondissement"].astype(int)
loyers["arrondissement"] = loyers["arrondissement"].astype(int)

# =========================
# 3. AGRÉGATION DVF
# =========================

print("Agrégation DVF...")

dvf_grouped = (
    dvf.groupby("arrondissement")["prix_m2"]
    .mean()
    .reset_index()
)

# =========================
# 4. MERGE
# =========================

print("Fusion des données...")

df = pd.merge(dvf_grouped, loyers, on="arrondissement")

# =========================
# 5. CALCUL RENTABILITÉ
# =========================

print("Calcul de la rentabilité...")

df["rentabilite"] = (df["loyer_m2"] * 12 / df["prix_m2"]) * 100

# =========================
# 6. TRI 
# =========================

df = df.sort_values(by="rentabilite", ascending=False)

# =========================
# 7. RESULTAT
# =========================

print("Résultat final :")
print(df)

print(df.info())

# =========================
# 8. SAUVEGARDE (GOLD)
# =========================

output_path = "data/gold/rentabilite.csv"

df.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")