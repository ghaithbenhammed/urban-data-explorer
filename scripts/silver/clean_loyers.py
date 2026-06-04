import pandas as pd

print("Chargement des loyers...")

df = pd.read_csv("data/bronze/loyers.csv", sep=";", encoding="latin1")

print("Lignes initiales :", df.shape[0])

# =========================
# 1. SÉLECTION COLONNES
# =========================

df = df[["INSEE_C", "loypredm2"]]

# =========================
# 2. CONVERSION NUMÉRIQUE
# =========================

df["loypredm2"] = df["loypredm2"].astype(str)
df["loypredm2"] = df["loypredm2"].str.replace(",", ".")
df["loypredm2"] = pd.to_numeric(df["loypredm2"], errors="coerce")

# =========================
# 3. SUPPRESSION VALEURS NULL
# =========================

df = df.dropna()

print("Après nettoyage :", df.shape[0])

# =========================
# 4. FILTRAGE PARIS
# =========================

df["INSEE_C"] = df["INSEE_C"].astype(str)

df = df[df["INSEE_C"].str.startswith("75")]

print("Après filtre Paris :", df.shape[0])

# =========================
# 5. EXTRACTION ARRONDISSEMENT
# =========================

df["arrondissement"] = df["INSEE_C"].str[-2:].astype(int)

# =========================
# 6. AGRÉGATION
# =========================

df = df.groupby("arrondissement")["loypredm2"].mean().reset_index()

# =========================
# 7. RENOMMER
# =========================

df.columns = ["arrondissement", "loyer_m2"]

# =========================
# 8. RÉSULTAT
# =========================

print("Données finales :")
print(df)

print(df.info())

# =========================
# 9. SAUVEGARDE
# =========================

output_path = "data/silver/loyers_clean.csv"

df.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")