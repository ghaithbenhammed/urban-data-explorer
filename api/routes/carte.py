from fastapi import APIRouter
from api.database.mongodb import db

router = APIRouter()

mapping = {

    "qualite-vie": "score_qualite_vie",

    "securite": "score_securite",

    "air": "score_air",

    "transport": "transport",

    "logements-sociaux": "logements_sociaux",

    "vieillissement": "score_vieillissement",

    "accessibilite": "accessibilite",

    "rentabilite": "rentabilite",

    "tension": "tension",

    "prix-median": "prix_median",

    "repartition-parc": "repartition_parc"
}


@router.get("/{indicateur}")
def get_indicateur(indicateur: str):

    collection = mapping.get(indicateur)

    if collection is None:

        return {
            "erreur":
            "Indicateur inconnu"
        }

    return list(
        db[collection].find(
            {},
            {"_id": 0}
        )
    )