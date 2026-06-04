import pandas as pd

# =========================
# 1. CHARGEMENT DES DONNÉES (BRONZE)
# =========================

print("Chargement des données INSEE...")

df = pd.read_csv("data/bronze/insee.csv", sep=";")

print(f"Nombre de lignes initial : {df.shape[0]}")

# =========================
# 2. SÉLECTION DES COLONNES UTILES
# =========================

print("Sélection des colonnes utiles...")

df = df[[
    "CODGEO",
    "MED17",
    "NBPERSMENFISC17"
]]

# =========================
# 3. SUPPRESSION DES VALEURS MANQUANTES
# =========================

print("Suppression des valeurs nulles...")

df = df.dropna()

print(f"Lignes après suppression des nulls : {df.shape[0]}")

# =========================
# 4. PRÉPARATION CODGEO
# =========================

print("Préparation des codes géographiques...")

# Convertir en string pour éviter erreurs
df["CODGEO"] = df["CODGEO"].astype(str).str.zfill(3)

# =========================
# 5. MAPPING CODGEO → ARRONDISSEMENT
# =========================

print("Transformation en arrondissement...")

mapping = {
    '011':1, '012':2, '013':3, '014':4,
    '021':5, '022':6, '023':7, '024':8, '025':9,
    '031':10, '032':11, '033':12,
    '041':13, '042':14, '043':15, '044':16,
    '051':17, '052':18,
    '061':19, '062':20
}

df["arrondissement"] = df["CODGEO"].map(mapping)

# Supprimer les lignes non correspondantes (sécurité)
df = df.dropna(subset=["arrondissement"])

df["arrondissement"] = df["arrondissement"].astype(int)

# =========================
# 6. RENOMMER LES COLONNES
# =========================

print("Renommage des colonnes...")

df = df[["arrondissement", "MED17","NBPERSMENFISC17"]]
df.columns = ["arrondissement", "revenu_median","population"]

# =========================
# 7. TRI (PROPRE)
# =========================

df = df.sort_values(by="arrondissement")

# =========================
# 8. RÉSULTAT FINAL (SILVER)
# =========================

print("Données INSEE prêtes")

print(df.head())
print(df.info())

# =========================
# 9. SAUVEGARDE
# =========================

output_path = "data/silver/insee_clean.csv"

df.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")