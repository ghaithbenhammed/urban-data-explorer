import json

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_geojson():

    with open(
        "data/bronze/arrondissements.geojson",
        encoding="utf-8"
    ) as f:

        geojson = json.load(f)

    return geojson