import pandas as pd

print("Chargement données...")

# =========================
# POPULATION AGEE
# =========================

seniors = pd.read_csv(
    "data/silver/population_agee_clean.csv"
)

# =========================
# ASCENSEURS
# =========================

ascenseurs = pd.read_csv(
    "data/silver/ascenseurs_clean.csv"
)

# =========================
# FUSION
# =========================

df = pd.merge(
    seniors[
        ["arrondissement", "taux_seniors"]
    ],
    ascenseurs[
        ["arrondissement", "taux_sans_ascenseur"]
    ],
    on="arrondissement"
)

# =========================
# INDICE BRUT
# =========================

df["indice_vieillissement"] = (
    df["taux_seniors"]
    *
    df["taux_sans_ascenseur"]
)

# =========================
# NORMALISATION
# ECHELLE 20 -> 80
# =========================

min_val = df[
    "indice_vieillissement"
].min()

max_val = df[
    "indice_vieillissement"
].max()

df["score_inadaptation"] = (
    20
    +
    (
        (
            df["indice_vieillissement"]
            - min_val
        )
        /
        (
            max_val
            - min_val
        )
    ) * 60
)

df["score_inadaptation"] = (
    df["score_inadaptation"]
    .round(2)
)

# =========================
# TRI
# =========================

df = df.sort_values(
    by="score_inadaptation",
    ascending=False
)

# =========================
# RESULTAT
# =========================

print("\nRésultat :")

print(
    df[
        [
            "arrondissement",
            "taux_seniors",
            "taux_sans_ascenseur",
            "indice_vieillissement",
            "score_inadaptation"
        ]
    ]
)

print("\nStatistiques :")

print(
    df["score_inadaptation"]
    .describe()
)

# =========================
# SAVE GOLD
# =========================

output_path = (
    "data/gold/score_vieillissement.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"\nFichier sauvegardé : {output_path}"
)