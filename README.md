# Kelvia — billetterie en ligne de festivals

> Cas fictif, exercice pédagogique.

Kelvia vend en ligne les billets de festivals. Le jour de l'ouverture des ventes, le site est tombé et ce sont les festivaliers qui ont prévenu l'équipe.
Vous êtes la nouvelle équipe DevOps : ce dépôt est votre point de départ pour tous les TP.

- `app/main.py` : l'API (page `/`, `/health`, `/billets`) ; `tests/` : les tests pytest.
- `.devcontainer/` : l'environnement du codespace, décrit en code.
- `infra/` : Terraform et Ansible (TP 3) ; `Dockerfile`, `compose.yaml`, `monitoring/`, `charge.sh` : TP 4.
- `CHANGELOG.md` : les versions livrées (TP 2).

**Bloqué ?** 5 minutes : ouvrez le bloc **Indice** de l'étape ; 10 minutes : le bloc **Solution**, puis un message privé au formateur sur Discord. Une erreur : [Erreurs fréquentes](#erreurs-fréquentes).

## Livrer : commit et push

Un commit par livrable, avec le bouton **Source Control** (barre de gauche) : message, **Commit**, puis **Sync Changes**.
Depuis le TP 2, `main` est protégée : passez par une branche et une pull request.

<details><summary>Solution</summary>

```bash
git switch -c tp3                 # une branche par livrable (depuis le TP 2)
git add -A
git commit -m "TP 3 : inventaire"
git push -u origin tp3            # puis, sur GitHub : Compare & pull request, Create, Merge
git switch main && git pull       # revenir sur main à jour
```
</details>

## TP 0 — Votre billetterie en ligne

### 1. Votre page de billetterie est ouverte (slide « On fait ensemble : GitHub et votre codespace »).

```bash
uvicorn app.main:app --reload
```

**Vous devez voir** : la page de billetterie.

<details><summary>Indice</summary>

Page du dépôt : **Code → Codespaces**. Le port 8000 est dans l'onglet **Ports**, à côté du terminal (icône globe).
</details>

<details><summary>Solution</summary>

**Code → Codespaces → Create codespace on main** (ou ouvrir celui créé à J-2). Dans le terminal : `uvicorn app.main:app --reload`.
Onglet **Ports** → ligne 8000 → **Open in Browser**. Laissez la visibilité du port à **Private**.
</details>

### 2. Changer le nom du festival dans app/main.py.

**Vous devez voir** : le nouveau nom.

<details><summary>Indice</summary>

La variable `FESTIVAL`, en haut du fichier. Grâce à `--reload`, l'API redémarre seule : rechargez la page.
</details>

<details><summary>Solution</summary>

```python
FESTIVAL = "Festival de Mon Binôme"
```
Enregistrez (Ctrl+S), puis rechargez la page du port 8000.
</details>

### 3. Inviter votre binôme, activer la protection au push.

**Vous devez voir** : la protection activée.

<details><summary>Indice</summary>

Tout est dans **Settings**, sur la page du dépôt.
</details>

<details><summary>Solution</summary>

**Settings → Collaborators → Add people** : le compte GitHub de votre binôme.
**Settings → Advanced Security** (ou **Code security**) **→ Push protection → Enable** : GitHub refusera un push qui contient un secret.
</details>

### 4. Commit et push avec le bouton Source Control.

**Vous devez voir** : le commit sur GitHub.

<details><summary>Indice</summary>

Barre de gauche, icône des branches : message du commit, **Commit**, puis **Sync Changes**.
</details>

<details><summary>Solution</summary>

```bash
git commit -am "TP 0 : nom du festival"
git push
```
Postez le lien de votre dépôt dans le chat.
</details>

## TP 2 — Du commit à la release

### 1. Recopier ci.yml et la ligne du badge (README) sur une branche, pull request, fusion.

Fichier `.github/workflows/ci.yml` :

```yaml
name: ci
on:
  push: {branches: [main]}
  pull_request:
# moindre privilège pour le jeton
permissions: {contents: read}
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with: {python-version: "3.12"}
      - run: pip install -r requirements.txt
      - run: pytest
```

Ligne du badge, à coller sous le titre de ce `README.md` (remplacez `<votre-compte>` par votre compte GitHub) :

```markdown
![ci](https://github.com/<votre-compte>/kelvia-api/actions/workflows/ci.yml/badge.svg)
```

**Vous devez voir** : la pastille verte, puis le badge vert.

<details><summary>Indice</summary>

Créez la branche avec le nom de branche en bas à gauche de l'éditeur (**Create new branch**). Après le push, GitHub propose **Compare & pull request**. Le badge affiche l'état du pipeline sur `main` : il passe au vert après la fusion.
</details>

<details><summary>Solution</summary>

```bash
git switch -c ajout-ci
mkdir -p .github/workflows       # puis créer ci.yml dans ce dossier, et coller la ligne du badge dans README.md
git add .github/workflows/ci.yml README.md
git commit -m "TP 2 : pipeline d'intégration continue et badge"
git push -u origin ajout-ci
```
Sur GitHub : **Compare & pull request → Create pull request**, attendre la pastille verte, **Merge pull request**. Puis `git switch main && git pull`.
</details>

### 2. Ruleset (slide « Protéger main avec un ruleset »), changer un prix, pull request.

**Vous devez voir** : la fusion bloquée. Remettre le prix.

<details><summary>Indice</summary>

**Settings → Rules → Rulesets**. Le check à exiger est le nom du job : `tests`. Le test `test_prix_pass_1_jour` vérifie le prix du Pass 1 jour.
</details>

<details><summary>Solution</summary>

1. **Settings → Rules → Rulesets → New ruleset → New branch ruleset** ; cible : **Include default branch** ; cocher **Require a pull request before merging** (0 approbation) et **Require status checks to pass before merging**, ajouter `tests` ; **Enforcement status : Active** ; **Create**.
2. Changer un prix :
   ```bash
   git switch -c prix                 # puis, dans app/main.py : "prix": 59 devient "prix": 65
   git commit -am "Nouveau prix du Pass 1 jour"
   git push -u origin prix
   ```
   Ouvrir la pull request : pastille rouge, **Merge** grisé.
3. Remettre `59`, puis `git commit -am "Prix remis" && git push` : pastille verte, fusion.
</details>

### 3. Sur une branche : livraison.yml à trous (README) et CHANGELOG.md v1.0.0 ; pull request, fusion ; puis tag v1.0.0.

1. Sur une nouvelle branche, dans `CHANGELOG.md`, ajoutez au-dessus de v0.1.0 une section v1.0.0 qui résume les TP 0 à 2 (même format que v0.1.0).
2. Créez `.github/workflows/livraison.yml` à partir de ce modèle et remplacez A, B, C et D.
   ```yaml
   name: livraison
   on: {push: {___A___: ["v*"]}}
   permissions:
     contents: ___B___
   jobs:
     release:
       runs-on: ___C___
       steps:
         - uses: actions/checkout@v7
           with: {persist-credentials: false}
         - uses: actions/setup-python@v7
           with: {python-version: "3.12"}
         - run: pip install -r requirements.txt
         - run: pytest
         - run: gh release create "$GITHUB_REF_NAME" -F CHANGELOG.md
           env:
             ___D___: ${{ secrets.GITHUB_TOKEN }}
   ```
3. Pull request, fusion (main est protégée), puis :
   ```
   git switch main
   git pull
   git tag v1.0.0
   git push origin v1.0.0
   ```
   **Vous devez voir** : la release v1.0.0 dans l'onglet Releases, avec le texte de votre CHANGELOG.

<details><summary>Indice</summary>

A : quand se déclenche le workflow ? B : la release écrit dans le dépôt. C : la même machine que ci.yml. D : la variable d'environnement que lit gh.
</details>

<details><summary>Solution</summary>

A `tags`, B `write`, C `ubuntu-latest`, D `GH_TOKEN`. Section du CHANGELOG, par exemple :

```markdown
## v1.0.0 — 2026-11-18
### Ajouté
- Nom du festival sur la page de billetterie
- Pipeline d'intégration continue (ci.yml) et badge d'état
- Protection de main par un ruleset
- Livraison sur tag (livraison.yml)
```
```bash
git switch -c livraison
git add CHANGELOG.md .github/workflows/livraison.yml
git commit -m "TP 2 : livraison v1.0.0"
git push -u origin livraison
```
Puis la pull request, la fusion et les 4 commandes du point 3. Onglet **Actions** : le workflow `livraison` tourne, puis la release apparaît.
</details>

## TP 3 — L'infrastructure de Kelvia en code

Dans `infra/` : `main.tf` (Terraform), `inventaire.yaml` et `site.yaml` (Ansible). Livrable : un commit de `infra/inventaire.yaml`.

### 1. Dans infra/ : terraform init, plan, apply.

```bash
cd infra
terraform init
terraform plan
terraform apply      # répondez yes
```

**Vous devez voir** : deux pages, ports 8081 et 8082.

<details><summary>Indice</summary>

Lisez le plan avant l'apply : chaque `+` est une ressource créée. Les pages s'ouvrent dans l'onglet **Ports**, ou avec `curl localhost:8081`.
</details>

<details><summary>Solution</summary>

Plan : `Plan: 4 to add, 0 to change, 0 to destroy.` (image, réseau, vm-web-1, vm-web-2). Les ports 8081 et 8082 affichent « Directory listing for / » : le dossier `/srv` est encore vide.
</details>

### 2. Lancer le playbook.

```bash
ansible-playbook -i inventaire.yaml site.yaml
```

**Vous devez voir** : RECETTE sur 8081, PRODUCTION sur 8082.

<details><summary>Indice</summary>

Lancez la commande depuis `infra/`. Rechargez les deux pages.
</details>

<details><summary>Solution</summary>

`changed=1` pour vm-web-1 et vm-web-2. `curl localhost:8081` affiche `<h1>RECETTE</h1>`, `curl localhost:8082` affiche `<h1>PRODUCTION</h1>`.
</details>

### 3. maintenance: true pour la production (inventaire.yaml), relancer.

**Vous devez voir** : seule la production en maintenance.

<details><summary>Indice</summary>

Une seule valeur change, dans le groupe `production`. Relancez le playbook.
</details>

<details><summary>Solution</summary>

```yaml
  vars: {environnement: PRODUCTION,
         maintenance: true}
```
Puis `ansible-playbook -i inventaire.yaml site.yaml` : `changed=1` pour vm-web-2 seulement ; le port 8082 affiche « Maintenance en cours ».
</details>

### 4. Remettre false, tout relancer deux fois.

```bash
terraform apply
ansible-playbook -i inventaire.yaml site.yaml
```

**Vous devez voir** : « No changes » et changed=0.

<details><summary>Indice</summary>

Le premier passage remet la page de production ; le second ne trouve plus rien à changer : c'est l'idempotence.
</details>

<details><summary>Solution</summary>

Remettez `maintenance: false`. Premier passage : `No changes.` pour Terraform, `changed=1` pour vm-web-2. Second passage : `No changes.` et `changed=0` partout.
</details>

## TP 4 — Partie 1 : conteneuriser l'API

Livrable : un commit de `compose.yaml`.

### 1. Lire le Dockerfile, décommenter le service api de compose.yaml, docker compose up -d.

```bash
docker compose up -d
docker compose ps
```

**Vous devez voir** : api healthy.

<details><summary>Indice</summary>

Arrêtez d'abord uvicorn (Ctrl+C) : il occupe le port 8000. Pour décommenter : sélectionnez les lignes du service `api`, puis Ctrl+/. La vérification de santé a lieu toutes les 10 s.
</details>

<details><summary>Solution</summary>

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment: {SERVIE_PAR: docker}
    healthcheck:
      test: >-
        python -c "import urllib.request as u;
        u.urlopen('http://localhost:8000/health')"
      interval: 10s
```
`docker compose ps` : `Up … (healthy)` sur la ligne api (après « health: starting », 10 à 20 s).
</details>

### 2. Ouvrir le port 8000.

**Vous devez voir** : « Servie par un conteneur Docker ».

<details><summary>Indice</summary>

Onglet **Ports**, ligne 8000. La phrase s'affiche quand la variable `SERVIE_PAR` vaut `docker`.
</details>

<details><summary>Solution</summary>

Onglet **Ports** → 8000 → **Open in Browser** (ou `curl localhost:8000`). La variable vient de `environment` dans `compose.yaml`.
</details>

### 3. Changer un texte de la page, docker compose up -d --build.

```bash
docker compose up -d --build
```

**Vous devez voir** : la modification.

<details><summary>Indice</summary>

Sans `--build`, l'ancienne image tourne toujours.
</details>

<details><summary>Solution</summary>

Dans `app/main.py`, changez par exemple `FESTIVAL` ou la phrase « Billetterie Kelvia… », puis `docker compose up -d --build` et rechargez la page.
</details>

## TP 4 — Observer Kelvia, provoquer une panne

Livrables : un commit pour l'instrumentation, un commit pour le test des quantités. La latence et l'hypothèse se votent sur l'outil de sondage.

### 1. Décommenter l'instrumentation, up -d --build, Grafana, ./charge.sh puis ./charge.sh rush.

```bash
docker compose up -d --build
./charge.sh          # Ctrl+C, puis ./charge.sh rush
```

**Vous devez voir** : les courbes monter.

<details><summary>Indice</summary>

Les deux lignes marquées « TP 4 » dans `app/main.py`. Grafana : port 3000, tableau de bord « Kelvia ». Les courbes se mettent à jour toutes les 5 s.
</details>

<details><summary>Solution</summary>

```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app, latency_lowr_buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1)).expose(app)
```
`curl -s localhost:8000/metrics | head` affiche des mesures. Sous `./charge.sh`, environ 5 requêtes par seconde ; sous `./charge.sh rush`, le trafic et la latence montent pendant 60 s.
</details>

### 2. Lire la latence au 95e centile au pic de ./charge.sh rush.

```bash
./charge.sh rush
```

**Vous devez voir** : la valeur ; votez-la : sous les 500 ms ou non (slide « SLI, SLO et error budget »).

<details><summary>Indice</summary>

Panneau « Latence 95e centile /billets », pendant les 60 s du rush : survolez le point le plus haut de la courbe.
</details>

<details><summary>Solution</summary>

La valeur dépend du codespace (environ 0,5 s mesuré en 2 cœurs). Sous 500 ms : le SLO est tenu au pic ; au-dessus : il ne l'est pas. Votez sur l'outil de sondage.
</details>

### 3. Compléter et renommer le test à trous (README), limite à 6.

Fichier `tests/quantite_a_trous.py` :

```bash
git mv tests/quantite_a_trous.py tests/test_quantite.py
pytest
```

**Vous devez voir** : le test rouge. Remettre 4.

<details><summary>Indice</summary>

Une quantité refusée est hors de 1 à 4. Code HTTP d'une donnée refusée : 422. Puis `QUANTITE_MAX = 6` dans `app/main.py` et relancez `pytest`.
</details>

<details><summary>Solution</summary>

Trous : `verifier_quantite(5)`, `"quantite": 5`, `== 422`. `pytest` : vert. Avec `QUANTITE_MAX = 6`, 5 devient acceptée : `2 failed`. Remettez `QUANTITE_MAX = 4` : vert.
</details>

### 4. Votez votre hypothèse : en combien de temps « API joignable » passe à 0 ? Puis docker compose stop api 2 minutes, et start.

```bash
docker compose stop api      # attendre 2 minutes
docker compose start api
```

**Vous devez voir** : la panne, puis le retour.

<details><summary>Indice</summary>

Votez sur l'outil de sondage avant d'arrêter quoi que ce soit. Gardez `./charge.sh` dans un autre terminal et le tableau de bord ouvert.
</details>

<details><summary>Solution</summary>

`./charge.sh` affiche `000` (pas de réponse) ; « API joignable » passe à 0 en une dizaine de secondes ; les panneaux de trafic et de latence montrent un trou. Après `start` : « API joignable » revient à 1, `200` revient.
</details>

## En avance ?

- Ajoutez `pip install pip-audit` et `pip-audit -r requirements.txt` au pipeline.
- Passez `nombre_vm` à 3 dans `infra/main.tf`, puis `terraform apply` : une troisième page.
- Dans Grafana, une alerte sur « API joignable » à 0.

## Erreurs fréquentes

Copiez le message exact avant de demander de l'aide.

| Message ou symptôme | Cause et correction |
|---|---|
| `push declined due to repository rule violations` | `main` est protégée depuis le TP 2 : passez par une branche et une pull request. |
| `Interrupted: 1 error during collection` | `pytest.ini` a disparu de la racine : restaurez-le. |
| `StarletteDeprecationWarning` | Un avertissement sans effet : les tests passent. |
| Cible Prometheus en erreur (`no such host`), « API joignable » à 0 | Le service `api` est encore en commentaire dans `compose.yaml` (TP 4, partie 1). |
| Panneaux de requêtes et de latence vides pendant l'arrêt de l'API | Normal : une API arrêtée n'envoie plus de mesures. Seul « API joignable » (et `charge.sh`) voit la panne. |
| `port is already allocated` sur le port 8000 | Un conteneur ou uvicorn tourne encore : Ctrl+C, ou `docker ps` puis `docker stop`. |
| `timeout while waiting for state to become 'removed'` | Une ressource remplacée (`-/+` dans le plan) est encore utilisée par une autre. |
| `env: 'bash\r': No such file or directory` ou `detected dubious ownership` | Vous travaillez hors de Codespaces : repassez sur votre codespace. |
| Aucune release après `git push origin v1.0.0` | Le tag a été poussé avant la fusion de `livraison.yml` : `git push origin :v1.0.0` et `git tag -d v1.0.0`, puis recommencez après la fusion. |
