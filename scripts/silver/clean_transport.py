import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

print("Chargement transport...")

# =========================
# 1. LOAD CSV
# =========================

df = pd.read_csv(
    "data/bronze/arrets-lignes.csv",
    sep=None,
    engine="python",
    on_bad_lines="skip"
)

# =========================
# 2. FILTRE PARIS
# =========================

df = df[df["Nom_commune"] == "Paris"]

# =========================
# 3. COLONNES UTILES
# =========================

df = df[[
    "stop_name",
    "stop_lat",
    "stop_lon",
    "mode"
]]

df.columns = [
    "nom_arret",
    "lat",
    "lon",
    "transport"
]

df = df.dropna()

print("Données transport prêtes")

# =========================
# 4. CREATE GEODATAFRAME
# =========================

geometry = [
    Point(xy) for xy in zip(df["lon"], df["lat"])
]

gdf_transport = gpd.GeoDataFrame(
    df,
    geometry=geometry,
    crs="EPSG:4326"
)

# =========================
# 5. LOAD ARRONDISSEMENTS
# =========================

print("Chargement GeoJSON arrondissements...")

gdf_arr = gpd.read_file(
    "data/bronze/arrondissements.geojson"
)

print(gdf_arr.head())

# =========================
# 6. SPATIAL JOIN
# =========================

print("Spatial join...")

gdf_join = gpd.sjoin(
    gdf_transport,
    gdf_arr,
    how="inner",
    predicate="within"
)

# =========================
# 7. EXTRACTION ARRONDISSEMENT
# =========================

# ⚠ adapte le nom si besoin
print(gdf_join.columns)

# souvent :
# "c_ar"

gdf_join["arrondissement"] = gdf_join["c_ar"]

# =========================
# 8. CLEAN FINAL
# =========================

final_df = gdf_join[[
    "nom_arret",
    "lat",
    "lon",
    "transport",
    "arrondissement"
]]

print(final_df.head())

print(final_df["arrondissement"].value_counts())

# =========================
# SAVE SILVER
# =========================

output_path = "data/silver/transport_clean.csv"

final_df.to_csv(output_path, index=False)

print(f"Fichier sauvegardé : {output_path}")