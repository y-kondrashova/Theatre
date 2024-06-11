# Theatre API

API service for theatre management written on DRF

## Installing using GitHub

Install PostgresSQL and create db

```
    git clone https://github.com/y-kondrashova/Theatre.git
    cd Theatre
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    set POSTGRES_HOST=<your db hostname>
    set POSTGRES_DB=<your db name>
    set POSTGRES_USER=<your db username>
    set POSTGRES_PASSWORD=<your db password>
    set SECRET_KEY=<your secret key>
    python manage.py migrate
    python manage.py runserver
```

## Run with docker

Docker should be installed

```
    docker-compose build
    docker-compose up
```

## Features

 - JWT authentication
 - Admin panel /admin/
 - Documentation is located at:
   - /api/doc/swagger/
   - /api/doc/redoc/
 - Managing tickets
 - Adding performances