import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

# ==================================
# SILVER
# ==================================

silver_scripts = [
    "clean_dvf.py",
    "clean_insee.py",
    "clean_loyers.py",
    "clean_transport.py",
    "clean_criminalite.py",
    "clean_logements_sociaux.py",
    "clean_pollution.py",
    "clean_population_agee.py",
    "clean_ascenseurs.py"
]

# ==================================
# SQLITE
# ==================================

sqlite_scripts = [
    "load_to_sqlite.py"
]

# ==================================
# GOLD
# ==================================

gold_scripts = [
    "prix_median.py",
    "rentabilite.py",
    "tension.py",
    "repartition_parc.py",
    "accessibilite.py",
    "transport_indicator.py",
    "score_securite.py",
    "score_air.py",
    "logements_sociaux.py",
    "score_vieillissement.py",
    "score_qualite_vie.py"
]

# ==================================
# MONGODB
# ==================================

mongo_scripts = [
    "load_to_mongodb.py"
]

# ==================================
# EXECUTION
# ==================================

def run_script(folder, script):

    path = ROOT / folder / script

    print("\n" + "=" * 70)
    print(f"▶ {script}")
    print("=" * 70)

    result = subprocess.run(
        ["python", str(path)]
    )

    if result.returncode != 0:
        raise Exception(
            f"Erreur dans {script}"
        )

# ==================================
# PIPELINE
# ==================================

print("\nPIPELINE URBAN DATA\n")

print("\nSILVER")
for script in silver_scripts:
    run_script("silver", script)

print("\nSQLITE")
for script in sqlite_scripts:
    run_script("database", script)

print("\nGOLD")
for script in gold_scripts:
    run_script("gold", script)

print("\nMONGODB")
for script in mongo_scripts:
    run_script("database", script)

print("\nPIPELINE TERMINÉ")