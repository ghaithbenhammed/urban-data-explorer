import pandas as pd
import sqlite3

print("Chargement des fichiers SILVER...")

# =========================
# 1. LOAD CSV
# =========================

dvf = pd.read_csv("data/silver/dvf_clean.csv")
insee = pd.read_csv("data/silver/insee_clean.csv")
loyers = pd.read_csv("data/silver/loyers_clean.csv")
transport = pd.read_csv("data/silver/transport_clean.csv")
criminalite = pd.read_csv("data/silver/criminalite_clean.csv")
logements = pd.read_csv("data/silver/logements_sociaux_clean.csv")
population = pd.read_csv("data/silver/population_paris.csv")
pollution = pd.read_csv("data/silver/pollution_clean.csv")
population_agee = pd.read_csv("data/silver/population_agee_clean.csv")
ascenseurs = pd.read_csv("data/silver/ascenseurs_clean.csv")


print("Fichiers chargés")

# =========================
# 2. CONNEXION SQLITE
# =========================

conn = sqlite3.connect("data/database.db")

print("Connexion à SQLite OK")

# =========================
# 3. INSERT INTO TABLES
# =========================

print("Insertion dans SQLite...")

dvf.to_sql("dvf_clean", conn, if_exists="replace", index=False)
insee.to_sql("insee_clean", conn, if_exists="replace", index=False)
loyers.to_sql("loyers_clean", conn, if_exists="replace", index=False)
transport.to_sql("transport_clean",conn,if_exists="replace",index=False)
criminalite.to_sql("criminalite_clean",conn,if_exists="replace",index=False)
logements.to_sql("logements_sociaux_clean",conn,if_exists="replace",index=False)
population.to_sql("population_paris",conn,if_exists="replace",index=False)
pollution.to_sql("pollution_clean",conn,if_exists="replace",index=False)
population_agee.to_sql("population_agee_clean",conn,if_exists="replace",index=False)
ascenseurs.to_sql("ascenseurs_clean",conn,if_exists="replace",index=False)

print("Tables créées : dvf_clean, insee_clean, loyers_clean")

# =========================
# 4. TEST
# =========================

query = "SELECT * FROM dvf_clean LIMIT 5"
df_test = pd.read_sql(query, conn)

print("Test lecture :")
print(df_test)

# =========================
# 5. CLOSE
# =========================

conn.close()

print("Base SQLite prête")