import pandas as pd

print("Chargement transport clean...")

df = pd.read_csv("data/silver/transport_clean.csv")

# =========================
# CALCUL INDICATEUR
# =========================

transport = (
    df.groupby("arrondissement")
    .size()
    .reset_index(name="nb_arrets")
)

# =========================
# TRI
# =========================

transport = transport.sort_values(
    by="nb_arrets",
    ascending=False
)

print(transport)

# =========================
# SAVE GOLD
# =========================

output_path = "data/gold/transport_access.csv"

transport.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")