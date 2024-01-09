# Logs Sports

## Run App Locally

1. Start the docker DB container

```bash
docker compose -f db.compose.yml up --build
```

2. Start the backend

```bash
python manage.py runserver
```

## Run App in Production

1. Make sure that there a file called `.env.prod` in the root directory of the project that contains the environment variables for the production environment, here is an example of the file:

```bash
# DB container envs
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=DB
POSTGRES_PASSWORD='xxx'
POSTGRES_NAME=logs_db

# django container envs
DJANGO_ENV=production
DEBUG=True
SECRET_KEY='xxx'
```

2. Start docker compose

```bash
docker compose up --build
```

## Redeploy App in Production

1. Navigate to the root directory of the project

```bash
cd /var/www/logs-sports
```

2. Stop the docker compose

```bash
docker compose down
```

3. Pull the latest changes from the repository

```bash
git pull
```

4. Start docker compose

```bash
docker compose up --build -d
```
