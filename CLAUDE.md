# Email Generator — instructions Claude Code

Projet full-stack H'appi. **Lire ce fichier avant toute modification.**
Règles communes : Happi Brain (`~/workspace/happi-brain`, plugin `happi`).

## Démarrage

```bash
make install        # venv backend + dépendances de dev, npm install
make db-init        # base development_db et tables (provisoire, voir « Écarts connus »)
make seed           # données de démo
make dev-backend    # uvicorn sur le port 8001
make dev-frontend   # vite sur le port 5173
make check          # ruff + oxlint + pytest + build : à lancer avant de dire « c'est fini »
```

## Stack

| Couche | Techno |
|---|---|
| Backend | FastAPI · SQLAlchemy 2.1 · psycopg 3 · PostgreSQL 16 |
| Frontend | React 19 · Vite 8 · TypeScript 7 · Tailwind 4 · axios · oxlint |
| Python | `backend/venv/` (3.12), toujours passer par `./venv/bin/…` ou `make` |

## Règles non négociables

1. **Port backend = 8001.** Jamais 8000 (bloqué sous WSL2) : uvicorn, `VITE_API_URL`, repli de
   `frontend/src/api/client.ts`, `.vscode/launch.json`.
2. **Soft delete** : `is_deleted = True`, jamais de `DELETE` SQL sur une entité métier ; toute
   lecture filtre `is_deleted`.
3. **Routes statiques avant les routes paramétrées** (`/templates/export` avant `/templates/{id}`).
4. **Aucun secret en dur.** Tout passe par `.env` ; toute nouvelle variable va dans `.env.example`.
   **Ce dépôt est public** : relire chaque diff avant de pousser.
5. **Schéma par Alembic uniquement**, une seule tête (`alembic heads`).
6. **Index** sur les clés étrangères et composite `(is_deleted, <colonne filtrée>)`.
7. **`GET /health` renvoie `{"status": "ok"}`** (test `backend/tests/test_smoke.py`).
8. **try/except autour de tout appel externe** (Anthropic, OpenAI, SMTP, webhooks).
9. **Adresse e-mail normalisée à l'entrée** : `.strip().lower()`.
10. Une tâche n'est finie que si `make check` passe.

## Écarts connus (à corriger, dans cet ordre)

- **Pas d'Alembic** : le schéma vit dans `database/scripts/init.sql`. À convertir en modèles
  SQLAlchemy et migration initiale ; `init.sql` disparaît ensuite.
- **Pas de soft delete** : les tables ont `is_active` mais pas `is_deleted`, et
  `generated_emails.partner_id` est en `ON DELETE CASCADE`. À reprendre dans la migration initiale.
- **Pas de docker-compose** : modèle dans `happi-template` et dans l'ancien dépôt
  `email-generator-app` (Postgres conteneurisé sur 5433, migrations au démarrage, healthchecks).
- **Pas de test de base de données** : seul le test de fumée existe.

## Pièges connus

- `import.meta.env.VITE_*` n'est lu qu'au démarrage de Vite : le relancer après édition de `frontend/.env`.
- SQLAlchemy 2.1 utilise psycopg 3 : l'URL commence par `postgresql+psycopg://`.
- Ne pas passer `--exclude` à ruff en ligne de commande : il remplace celui de `backend/pyproject.toml`.
