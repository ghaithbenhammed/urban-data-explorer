import pandas as pd

print("Chargement DVF...")

# =========================
# 1. LOAD DATA
# =========================

df = pd.read_csv("data/silver/dvf_clean.csv")

print(f"Nombre de lignes : {df.shape[0]}")
print(df.head())

# =========================
# 2. NETTOYAGE
# =========================

# S'assurer que les colonnes sont bien numériques
df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors="coerce")
df["arrondissement"] = pd.to_numeric(df["arrondissement"], errors="coerce")

# Supprimer les valeurs nulles
df = df.dropna(subset=["surface_reelle_bati", "arrondissement"])

# Convertir arrondissement en int
df["arrondissement"] = df["arrondissement"].astype(int)

# =========================
# 3. CRÉATION CATÉGORIES
# =========================

print("Création des catégories de surface...")

def categorize_surface(x):
    if x < 30:
        return "petit"
    elif x < 70:
        return "moyen"
    else:
        return "grand"

df["categorie_surface"] = df["surface_reelle_bati"].apply(categorize_surface)

print("Répartition globale :")
print(df["categorie_surface"].value_counts())

# =========================
# 4. AGRÉGATION
# =========================

print("Répartition par arrondissement...")

df_grouped = (
    df.groupby(["arrondissement", "categorie_surface"])
    .size()
    .reset_index(name="count")
)

# =========================
# 5. CALCUL POURCENTAGE
# =========================

print("Calcul des pourcentages...")

df_grouped["total"] = df_grouped.groupby("arrondissement")["count"].transform("sum")

df_grouped["pourcentage"] = (df_grouped["count"] / df_grouped["total"]) * 100

# Arrondi propre
df_grouped["pourcentage"] = df_grouped["pourcentage"].round(2)

# =========================
# 6. TRI 
# =========================

df_grouped = df_grouped.sort_values(
    ["arrondissement", "categorie_surface"]
)

# =========================
# 7. RÉSULTAT
# =========================

print("Résultat final :")
print(df_grouped)

print(df_grouped.info())

# =========================
# 8. SAVE (GOLD)
# =========================

output_path = "data/gold/repartition_parc.csv"

df_grouped.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")