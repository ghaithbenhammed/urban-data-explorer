from fastapi import APIRouter
from api.database.mongodb import db

router = APIRouter()

@router.get("/")
def get_all():

    return list(
        db["prix_median"].find(
            {},
            {"_id": 0}
        )
    )

@router.get("/{arrondissement}")
def get_one(arrondissement: int):

    return db["prix_median"].find_one(
        {"arrondissement": arrondissement},
        {"_id": 0}
    )