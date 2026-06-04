import pandas as pd

print("Chargement pollution clean...")

# =========================
# 1. LOAD SILVER
# =========================

df = pd.read_csv(
    "data/silver/pollution_clean.csv"
)

# =========================
# 2. NORMALISATION
# =========================

print("Calcul score air...")

max_val = df[
    "pollution_no2"
].max()

min_val = df[
    "pollution_no2"
].min()

normalized = (
    df["pollution_no2"] - min_val
) / (max_val - min_val)

# score qualité air
df["score_air"] = (
    80 - (normalized * 60)
)

df["score_air"] = (
    df["score_air"]
    .round(2)
)

# =========================
# 3. TRI
# =========================

df = df.sort_values(
    by="score_air",
    ascending=False
)

# =========================
# 4. RESULTAT
# =========================

print("\nScore air :\n")

print(df)

print("\n")

print(df.info())

# =========================
# 5. SAVE GOLD
# =========================

output_path = (
    "data/gold/score_air.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"\nFichier sauvegardé : {output_path}"
)