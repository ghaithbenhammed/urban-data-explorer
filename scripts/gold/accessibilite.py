import pandas as pd

print("Chargement des données clean...")

dvf = pd.read_csv("data/silver/dvf_clean.csv")
insee = pd.read_csv("data/silver/insee_clean.csv")

# =========================
# CLEAN
# =========================

dvf["arrondissement"] = pd.to_numeric(dvf["arrondissement"], errors="coerce")
insee["arrondissement"] = pd.to_numeric(insee["arrondissement"], errors="coerce")

dvf = dvf.dropna(subset=["arrondissement", "prix_m2"])
insee = insee.dropna(subset=["arrondissement", "revenu_median"])

dvf["arrondissement"] = dvf["arrondissement"].astype(int)
insee["arrondissement"] = insee["arrondissement"].astype(int)

# =========================
# AGRÉGATION DVF
# =========================

print("Calcul prix moyen au m²...")

dvf_grouped = dvf.groupby("arrondissement")["prix_m2"].mean().reset_index()

# =========================
# FUSION
# =========================

print("Fusion DVF + INSEE...")

df_final = dvf_grouped.merge(insee, on="arrondissement")

# =========================
# ACCESSIBILITÉ SIMPLE (VALIDÉE)
# =========================

print("Calcul accessibilité...")

df_final["accessibilite"] = df_final["revenu_median"] / df_final["prix_m2"]

df_final["accessibilite"] = df_final["accessibilite"].round(2)

# =========================
# TRI
# =========================

df_final = df_final.sort_values("accessibilite", ascending=False)

# =========================
# RESULTAT
# =========================

print("Classement accessibilité :")
print(df_final[["arrondissement", "accessibilite"]])

# =========================
# SAVE
# =========================

output_path = "data/gold/accessibilite.csv"

df_final.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")