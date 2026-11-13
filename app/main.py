"""Kelvia, billetterie en ligne de festivals (cas fictif, exercice pédagogique)."""
import asyncio
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

FESTIVAL = "Festival de Mon Binôme"
QUANTITE_MAX = 4
# Catégories de billets, en mémoire : prix en euros et stock.
CATEGORIES = {
    "Pass 1 jour": {"prix": 65, "stock": 5000},
    "Pass 3 jours": {"prix": 149, "stock": 2000},
    "Camping": {"prix": 25, "stock": 1000},
}

app = FastAPI(title="Kelvia")

# TP 4 : décommentez les deux lignes suivantes pour exposer /metrics à Prometheus.
# from prometheus_fastapi_instrumentator import Instrumentator
# Instrumentator().instrument(app, latency_lowr_buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1)).expose(app)


class Commande(BaseModel):
    categorie: str
    quantite: int


def verifier_quantite(quantite):
    """Règle métier : une commande compte de 1 à QUANTITE_MAX billets."""
    if not 1 <= quantite <= QUANTITE_MAX:
        raise ValueError(f"une commande compte de 1 à {QUANTITE_MAX} billets")
    return quantite


# Latence simulée : chaque requête en cours ajoute 20 ms d'attente (elle monte sous ./charge.sh rush).
en_cours = 0


async def latence_simulee():
    global en_cours
    en_cours += 1
    try:
        await asyncio.sleep(min(0.003 + 0.02 * (en_cours - 1), 0.9))
    finally:
        en_cours -= 1


@app.get("/", response_class=HTMLResponse)
def accueil():
    lignes = "".join(f"<li>{nom} : {c['prix']} €, {c['stock']} en stock</li>" for nom, c in CATEGORIES.items())
    docker = "<p>Servie par un conteneur Docker</p>" if os.environ.get("SERVIE_PAR") == "docker" else ""
    return f"""<!doctype html><meta charset="utf-8"><title>Kelvia</title>
<h1>{FESTIVAL}</h1>
<p>Billetterie Kelvia : jusqu'à {QUANTITE_MAX} billets par commande.</p>
<ul>{lignes}</ul>
{docker}"""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/billets")
async def lister_billets():
    await latence_simulee()
    return CATEGORIES


@app.post("/billets", status_code=201)
async def commander(commande: Commande):
    await latence_simulee()
    try:
        verifier_quantite(commande.quantite)
    except ValueError as erreur:
        raise HTTPException(status_code=422, detail=str(erreur))
    if commande.categorie not in CATEGORIES:
        raise HTTPException(status_code=404, detail="catégorie inconnue")
    CATEGORIES[commande.categorie]["stock"] -= commande.quantite
    return commande
