import pandas as pd

print("Chargement des données...")

dvf = pd.read_csv("data/silver/dvf_clean.csv")
insee = pd.read_csv("data/silver/insee_clean.csv")

# =========================
# 1. NOMBRE DE TRANSACTIONS
# =========================

print("Calcul nombre de transactions...")

transactions = (
    dvf.groupby("arrondissement")
    .size()
    .reset_index(name="nb_transactions")
)

print(transactions.head())

# =========================
# 2. FUSION AVEC INSEE
# =========================

print("Fusion DVF + INSEE...")

df = transactions.merge(insee, on="arrondissement")

# =========================
# 3. CALCUL TENSION
# =========================

print("Calcul tension immobilière...")

df["tension"] = df["population"] / df["nb_transactions"]

# =========================
# 4. TRI
# =========================

df = df.sort_values("tension", ascending=False)

# =========================
# 5. RESULTAT
# =========================

print("Résultat final :")
print(df)

# =========================
# 6. SAVE (GOLD)
# =========================

output_path = "data/gold/tension_immobiliere.csv"

df.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")