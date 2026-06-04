from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from api.routes.qualite_vie import router as qualite_router
from api.routes.securite import router as securite_router
from api.routes.air import router as air_router
from api.routes.transport import router as transport_router
from api.routes.logements_sociaux import router as social_router
from api.routes.vieillissement import router as vieillissement_router
from api.routes.dashboard import router as dashboard_router
from api.routes.comparaison import router as comparaison_router
from api.routes.accessibilite import router as accessibilite_router
from api.routes.rentabilite import router as rentabilite_router
from api.routes.tension import router as tension_router
from api.routes.repartition_parc import router as parc_router
from api.routes.prix_median import router as prix_router
from api.routes.geojson import router as geojson_router
from api.routes.carte import router as carte_router


app = FastAPI(
    title="Urban Data Explorer API"
)
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)
app.include_router(
    qualite_router,
    prefix="/qualite-vie",
    tags=["Qualité de vie"]
)

app.include_router(
    securite_router,
    prefix="/securite",
    tags=["Sécurité"]
)

app.include_router(
    air_router,
    prefix="/air",
    tags=["Pollution"]
)

app.include_router(
    transport_router,
    prefix="/transport",
    tags=["Transport"]
)

app.include_router(
    social_router,
    prefix="/logements-sociaux",
    tags=["Logements sociaux"]
)

app.include_router(
    vieillissement_router,
    prefix="/vieillissement",
    tags=["Vieillissement"]
)

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    comparaison_router,
    prefix="/comparaison",
    tags=["Comparaison"]
)

app.include_router(
    accessibilite_router,
    prefix="/accessibilite",
    tags=["Accessibilité"]
)

app.include_router(
    rentabilite_router,
    prefix="/rentabilite",
    tags=["Rentabilité"]
)

app.include_router(
    tension_router,
    prefix="/tension",
    tags=["Tension immobilière"]
)

app.include_router(
    parc_router,
    prefix="/repartition-parc",
    tags=["Répartition parc"]
)
app.include_router(
    prix_router,
    prefix="/prix-median",
    tags=["Prix médian"]
)
app.include_router(
    geojson_router,
    prefix="/geojson",
    tags=["Carte"]
)
app.include_router(
    carte_router,
    prefix="/carte",
    tags=["Carte Interactive"]
)
@app.get("/")
def root():

    return {
        "message":
        "Urban Data Explorer API"
    }