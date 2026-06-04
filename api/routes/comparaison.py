from fastapi import APIRouter
from api.database.mongodb import db

router = APIRouter()

@router.get("/{arr1}/{arr2}")
def compare(arr1: int, arr2: int):

    a1 = db["score_qualite_vie"].find_one(
        {"arrondissement": arr1},
        {"_id": 0}
    )

    a2 = db["score_qualite_vie"].find_one(
        {"arrondissement": arr2},
        {"_id": 0}
    )

    return {
        "arrondissement_1": a1,
        "arrondissement_2": a2
    }