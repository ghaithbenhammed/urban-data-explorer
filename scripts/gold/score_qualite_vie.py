import pandas as pd

print("Chargement datasets GOLD...")

# =========================
# 1. LOAD GOLD
# =========================

securite = pd.read_csv(
    "data/gold/score_securite.csv"
)

air = pd.read_csv(
    "data/gold/score_air.csv"
)

transport = pd.read_csv(
    "data/gold/transport_access.csv"
)

logements = pd.read_csv(
    "data/gold/logements_sociaux.csv"
)

print("Fichiers chargés")

# =========================
# 2. NORMALISATION TRANSPORT
# =========================

max_transport = transport[
    "nb_arrets"
].max()

min_transport = transport[
    "nb_arrets"
].min()

transport["score_transport"] = (
    (
        transport["nb_arrets"]
        - min_transport
    )
    /
    (
        max_transport
        - min_transport
    )
) * 60 + 20

transport["score_transport"] = (
    transport["score_transport"]
    .round(2)
)

# =========================
# 3. NORMALISATION MIXITE
# =========================

max_mixite = logements[
    "taux_logement_social"
].max()

min_mixite = logements[
    "taux_logement_social"
].min()

logements["score_mixite"] = (
    (
        logements[
            "taux_logement_social"
        ]
        - min_mixite
    )
    /
    (
        max_mixite
        - min_mixite
    )
) * 40 + 40

logements["score_mixite"] = (
    logements["score_mixite"]
    .round(2)
)

# =========================
# 4. MERGE
# =========================

df = securite.merge(
    air[
        ["arrondissement", "score_air"]
    ],
    on="arrondissement"
)

df = df.merge(
    transport[
        [
            "arrondissement",
            "score_transport"
        ]
    ],
    on="arrondissement"
)

df = df.merge(
    logements[
        [
            "arrondissement",
            "score_mixite"
        ]
    ],
    on="arrondissement"
)

# =========================
# 5. SCORE FINAL
# =========================

print("Calcul score qualité de vie...")

df["score_qualite_vie"] = (
    df["score_securite"] * 0.30
    +
    df["score_air"] * 0.30
    +
    df["score_transport"] * 0.30
    +
    df["score_mixite"] * 0.10
)

df["score_qualite_vie"] = (
    df["score_qualite_vie"]
    .round(2)
)

# =========================
# 6. TRI
# =========================

df = df.sort_values(
    by="score_qualite_vie",
    ascending=False
)

# =========================
# 7. RESULTAT
# =========================

print("\nScore qualité de vie :\n")

print(df)

print("\n")

print(df.info())

# =========================
# 8. SAVE GOLD
# =========================

output_path = (
    "data/gold/score_qualite_vie.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"\nFichier sauvegardé : {output_path}"
)