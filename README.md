# Theatre API

API service for theatre management written on DRF

## Installing using GitHub

Install PostgresSQL and create db

```shell
  git clone https://github.com/y-kondrashova/Theatre.git
```
```shell
  cd Theatre
```
```shell
  python -m venv venv
```
```shell
  source venv/bin/activate
```
```shell
  pip install -r requirements.txt
```
   Add .env file to the project
```
   In .env:
   
   set POSTGRES_HOST=<your db hostname>
   set POSTGRES_DB=<your db name>
   set POSTGRES_USER=<your db username>
   set POSTGRES_PASSWORD=<your db password>
   set SECRET_KEY=<your secret key>
```

```shell
  python manage.py migrate
```
```shell
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