import pandas as pd

print("📥 Chargement criminalité clean...")

# =========================
# 1. LOAD SILVER
# =========================

df = pd.read_csv(
    "data/silver/criminalite_clean.csv"
)

# =========================
# 2. CREATION POIDS
# =========================

print("⚖️ Attribution des poids...")

poids = {
    "Violences physiques intrafamiliales": 4,
    "Violences physiques hors cadre familial": 4,
    "Violences sexuelles": 5,
    "Vols avec armes": 5,
    "Vols violents sans arme": 4,
    "Vols sans violence contre des personnes": 2,
    "Cambriolages de logement": 3,
    "Vols de véhicule": 2,
    "Vols dans les véhicules": 2,
    "Vols d'accessoires sur véhicules": 1,
    "Destructions et dégradations volontaires": 2,
    "Usage de stupéfiants": 1,
    "Usage de stupéfiants (AFD)": 1,
    "Trafic de stupéfiants": 3,
    "Escroqueries et fraudes": 2
}

# =========================
# 3. AJOUT POIDS
# =========================

df["poids"] = (
    df["indicateur"]
    .map(poids)
)

# si indicateur absent
df["poids"] = (
    df["poids"]
    .fillna(1)
)

# =========================
# 4. SCORE PONDÉRÉ
# =========================

print("📊 Calcul criminalité pondérée...")

df["score_crime"] = (
    df["taux_pour_mille"] * df["poids"]
)

criminalite = (
    df.groupby("arrondissement")[
        "score_crime"
    ]
    .mean()
    .reset_index()
)

criminalite.columns = [
    "arrondissement",
    "criminalite_ponderee"
]

# =========================
# 5. NORMALISATION
# =========================

print("🛡️ Calcul score sécurité...")

max_val = criminalite[
    "criminalite_ponderee"
].max()

min_val = criminalite[
    "criminalite_ponderee"
].min()

normalized = (
    criminalite["criminalite_ponderee"] - min_val
) / (max_val - min_val)

criminalite["score_securite"] = (
    80 - (normalized * 60)
)

criminalite["score_securite"] = (
    criminalite["score_securite"]
    .round(2)
)

# =========================
# 6. TRI
# =========================

criminalite = criminalite.sort_values(
    by="score_securite",
    ascending=False
)

# =========================
# 7. RESULTAT
# =========================

print("📈 Résultat final :")

print(criminalite)

print(criminalite.info())

# =========================
# 8. SAVE GOLD
# =========================

output_path = (
    "data/gold/score_securite.csv"
)

criminalite.to_csv(
    output_path,
    index=False
)

print(
    f"✅ Fichier sauvegardé : {output_path}"
)