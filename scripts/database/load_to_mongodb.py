import pandas as pd
from pymongo import MongoClient

print("Chargement données GOLD...")

# =========================
# 1. LOAD CSV GOLD
# =========================
prix_median = pd.read_csv("data/gold/prix_median_evolution.csv")
access = pd.read_csv("data/gold/accessibilite.csv")
rent = pd.read_csv("data/gold/rentabilite.csv")
parc = pd.read_csv("data/gold/repartition_parc.csv")
tension = pd.read_csv("data/gold/tension_immobiliere.csv")
transport = pd.read_csv("data/gold/transport_access.csv")
securite = pd.read_csv("data/gold/score_securite.csv")
social = pd.read_csv("data/gold/logements_sociaux.csv")
air = pd.read_csv("data/gold/score_air.csv")
qualite_vie = pd.read_csv("data/gold/score_qualite_vie.csv")
score_vieillissement = pd.read_csv("data/gold/score_vieillissement.csv")

print("CSV chargés")

# =========================
# 2. CONNEXION MONGODB
# =========================

client = MongoClient("mongodb://localhost:27017/")
db = client["urban_data"]

print("Connexion MongoDB OK")

# =========================
# 3. RESET COLLECTIONS (IMPORTANT)
# =========================
db["prix_median"].delete_many({})
db["accessibilite"].delete_many({})
db["rentabilite"].delete_many({})
db["repartition_parc"].delete_many({})
db["tension"].delete_many({})
db["transport"].delete_many({})
db["score_securite"].delete_many({})
db["logements_sociaux"].delete_many({})
db["score_air"].delete_many({})
db["score_qualite_vie"].delete_many({})
db["score_vieillissement"].delete_many({})


print("Collections nettoyées")

# =========================
# 4. INSERTION
# =========================
db["prix_median"].insert_many(prix_median.to_dict("records"))
db["accessibilite"].insert_many(access.to_dict("records"))
db["rentabilite"].insert_many(rent.to_dict("records"))
db["repartition_parc"].insert_many(parc.to_dict("records"))
db["tension"].insert_many(tension.to_dict("records"))
db["transport"].insert_many(transport.to_dict("records"))
db["score_securite"].insert_many(securite .to_dict("records"))
db["logements_sociaux"].insert_many(social.to_dict("records"))
db["score_air"].insert_many(air.to_dict("records"))
db["score_qualite_vie"].insert_many(qualite_vie.to_dict("records"))
db["score_vieillissement"].insert_many(score_vieillissement.to_dict("records"))

print("Données insérées dans MongoDB")

# =========================
# 5. TEST
# =========================

print("Exemple tension :")
print(db["tension"].find_one())