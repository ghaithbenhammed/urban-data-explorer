import pandas as pd
import re

print("Chargement pollution...")

# =========================
# 1. LOAD BRONZE
# =========================

df = pd.read_csv(
    "data/bronze/pollution.csv",
    sep=";"
)

print("Données chargées")

# =========================
# 2. FILTRE ANNEE
# =========================

print("Filtre année 2019...")

# 2019 = année complète
df = df[
    df["Année"] == 2019
]

print("Année utilisée : 2019")

# =========================
# 3. EXTRACTION NO2
# =========================

print("🧹 Extraction pollution NO2...")

data = []

for col in df.columns:

    # garder colonnes arrondissements
    if (
        "ardt soumis à dépassement VR NO2"
        in col
    ):

        # extraction numéro arrondissement
        match = re.search(
            r"du\s?(\d+)",
            col
        )

        if match:

            arrondissement = int(
                match.group(1)
            )

            valeur = df.iloc[0][col]

            data.append({
                "arrondissement": arrondissement,
                "pollution_no2": valeur
            })

# =========================
# 4. DATAFRAME FINAL
# =========================

pollution = pd.DataFrame(data)

# suppression NaN
pollution = pollution.dropna()

# tri
pollution = pollution.sort_values(
    by="arrondissement"
)

# reset index
pollution = pollution.reset_index(
    drop=True
)

# =========================
# 5. RESULTAT
# =========================

print("\nPollution clean :\n")

print(pollution)

print("\n")

print(pollution.info())

# =========================
# 6. SAVE SILVER
# =========================

output_path = (
    "data/silver/pollution_clean.csv"
)

pollution.to_csv(
    output_path,
    index=False
)

print(
    f"\nFichier sauvegardé : {output_path}"
)