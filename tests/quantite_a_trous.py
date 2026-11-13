"""TP 4 : la règle « une commande compte de 1 à 4 billets » (verifier_quantite).

Remplacez les ___ (modèle : slide « Un test unitaire et un test d'intégration »), puis renommez ce fichier en test_quantite.py :
    git mv tests/quantite_a_trous.py tests/test_quantite.py
Puis lancez pytest.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app, verifier_quantite


def test_quantite_trop_grande_refusee_unitaire():
    with pytest.raises(ValueError):
        verifier_quantite(___)


def test_quantite_trop_grande_refusee_integration():
    client = TestClient(app)
    reponse = client.post("/billets", json={"categorie": "Pass 1 jour", "quantite": ___})
    assert reponse.status_code == ___
