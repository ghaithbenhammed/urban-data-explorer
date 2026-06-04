from fastapi import APIRouter
from api.database.mongodb import db

router = APIRouter()

@router.get("/")
def dashboard():

    return {
        "qualite_vie": list(
            db["score_qualite_vie"].find(
                {},
                {"_id": 0}
            )
        ),
        "securite": list(
            db["score_securite"].find(
                {},
                {"_id": 0}
            )
        ),
        "air": list(
            db["score_air"].find(
                {},
                {"_id": 0}
            )
        ),
        "transport": list(
            db["transport"].find(
                {},
                {"_id": 0}
            )
        )
    }