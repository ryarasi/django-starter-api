## About

This repo contains the Dockerized Django-based Graphql API as a starter project. This README file details everything you need to know about this project.

## Versions

- Python 3.8.5
- pip 20.0.2 (Python 3.8)
- PostgreSQL 12
- Docker 20.10.6, build 370c289
- Docker Compose 1.29.1, build c34c88b2

## Environment Setup

The following instructions assumes that you are attempting to setup the project on an Ubuntu 20.04 machine or Windows WSL with an Ubuntu image. The responsibility of making necessary adjustments to the steps below rests on the follower of these instructions.

1. [Setup Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
2. [Setup Docker Compose](https://docs.docker.com/compose/install/)
3. [Setup Python](https://www.python.org/downloads/)
4. [Setup PostgreSQL](https://www.postgresql.org/download/)

## Starting Project

1. Ensure that you are in the `dev` branch.
2. cd into the api repo.
3. Duplicate the `sample.env` file and rename it to `.env`
4. Setup the database with these commands
   1. In the terminal execute `psql -U postgres` to enter psql.
   2. `CREATE DATABASE starterdb;`
   3. `CREATE USER starteradmin WITH PASSWORD 'password';`
   4. `ALTER ROLE starteradmin SET client_encoding TO 'utf8';`
   5. `ALTER ROLE starteradmin SET default_transaction_isolation TO 'read committed';`
   6. `ALTER ROLE starteradmin SET timezone TO 'UTC';`
   7. `GRANT ALL PRIVILEGES ON DATABASE starterdb TO starteradmin;`
   8. `\q`
   9. `exit`
5. If this is the first time you are running the project, do the following:-
   1. Run `npm run build`
   2. Run `npm run start`
   3. Create an administrative user for the project with `docker-compose run web python manage.py createsuperuser` in a new terminal window
      1. Choose your username and password.
      2. Now you can go to `localhost:8000/admin` to log into the console
   4. Run migrations with `npm run makemigrations` and then `npm run migrate`
   5. Populate the database using fixtures by executing this `docker-compose run web python manage.py loaddata ./starter/fixtures/initial_data.json`.
6. If this is not the first time, then you can simply execute `npm start` to start the project inside docker

## Project recreation instructions

The instructions are helpful if you wish to recreate this project from the scratch. Not needed if you wish to just run the project locally.

1. Create a new folder for the project and copy over the following files from this reop:-
   1. `.gitignore`
   2. `Dockerfile`
   3. `docker-compose.yml`
   4. `requirements.txt`
2. Create a new isolated virtual python environment
   `python -m venv venv`
3. Activate the virtual environment
   `source venv/bin/activate`
4. Install all the requirements in the virtual environment with `pip install -r requirements.txt`
5. Create a new Django project `django-admin startproject starter .`
6. Create a new app called starter inside the base project folder with `django-admin startapp app`
7. Update the `DATABASES` variable in `settings.py` file with the contents of that variable from the `settings.py` file in this repo.
8. Create a postgres database and a database user inside Docker with the following commands:-
   1. `docker pull postgres:alpine` to create postgres docker image. We use the alipne version because its lighter.
   2. `docker images` to check if it shows the newly created docker image.
   3. `docker run --name starter-db -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine` to create a docker container named starter-db with the docker image we just pulled.
   4. `docker ps` should list the newly created container.
   5. `docker exec -it starter-db bash` to enter the container.
   6. `psql -U postgres` to enter psql.
   7. `CREATE DATABASE starterdb;`
   8. `CREATE USER starteradmin WITH PASSWORD 'password';`
   9. `ALTER ROLE starteradmin SET client_encoding TO 'utf8';`
   10. `ALTER ROLE starteradmin SET default_transaction_isolation TO 'read committed';`
   11. `ALTER ROLE starteradmin SET timezone TO 'UTC';`
   12. `GRANT ALL PRIVILEGES ON DATABASE starterdb TO starteradmin;`
   13. `\q`
   14. `exit`
9. Create a new file called `database.env` with the following content (feel free to use your own values if needed):-
   1. POSTGRES_USER='starteradmin'
   2. POSTGRES_PASSWORD='password'
   3. POSTGRES_DB='starterdb'
10. Create a new .env file with the following values listed for local env:-

```
DJANGO_SECRET_KEY='django-insecure-)3@2sm6lgn_p83_t(l-44hd16ou5-qbk=rso!$b1#$fu*n2^rq'
ENABLED_AUTOMATED_TESTING=true
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0
DJANGO_CORS_ORIGIN_ALLOW_ALL=true
REDIS_URL="Needs to be set on Redis to go on heroku"
FRONTEND_DOMAIN_URL=localhost:4200
ENV_DEFAULT_FROM_EMAIL=mail@email.com
ENV_EMAIL_HOST_USER=11b14065118c386fee370e61df2c748e
ENV_EMAIL_HOST_PASSWORD=fffdbe9cdd900098103c4efae521db75
ENV_EMAIL_PORT=587
ENV_EMAIL_USE_TLS=true
ENV_EMAIL_USE_SSL=false
PORT=8080
APP_PORT=8001
```

11. Create your superuser in django (different from the db user created above) that will be used for the admin console in the backend with `docker-compose run web python manage.py createsuperuser` and follow prompts to setup username and password. You can use the credentials to login to the admin console at `http://localhost:8000/admin/login/`.
12. Test setup type in the following commands:-
    1. Start the postgres docker container with `docker start starter-db`
    2. If this says that ports are already in use, then shut down postgres and try again `sudo service postgresql stop`
    3. Once the postgres container is up and running, start the docker for the project with `docker-compose up`
    4. Visit `localhost:8000` or `localhost:8000/graphql` to check if setup has worked.
13. In order to run `makemigrations` and `migrate` commands on the project, we must now do it inside the docker container by adding `docker-compose run web` before whichever command you wish to execute on the project. Eg `docker-compose run web python manage.py migrate`

## Docker adaptations of regular Django commands:-

1. Create an administrative user for the project with `docker-compose run web python manage.py createsuperuser`
   1. Choose your username and password.
   2. Now you can go to `localhost:8000/admin` to log into the console
2. While installing new packages follow these steps:-
   1. Make sure you've activated the virtual environment with `source venv/bin/activate`
   2. Install the package with `pip install <package_name>`
   3. Update the `requirements.txt` file with `pip freeze > requirements.txt`
   4. If the docker doesn't recognize the newly installed package, ensure that the docker container is rebuilt and try again.

## Using pgAdmin:-

1.  During first time set up, add a new server with the hostname `db` and port `5432` and username and password as given in the `database.env` file.
2.  The database can be explored and modified by visiting `localhost:5000` in the browser.
3.  The email and password are available in the `docker-compose.yml` file under `environment` in `pgadmin4`.

## Deployment:-

1. Heroku deployment requires the `heroku.yml` file and some modifications in the `Dockerfile`, `docker-compose.yml` and `settings.py`, all of which are already taken care of in this repo.
2. Get setup with the [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. User `heroku create` to set up a new heroku project. From the GUI add the following addons to the Heroku project:-
   1. **Heroku Postgres** - For the database (This automatically adds the DATABASE_URL to the project's config variables)
   2. **Heroku Redis** - For the redis server (This automatically adds the REDIS_URL to the project's config variables)
4. Add all essential ENV variables in `settings > config`. Refer to the .env file locally or in the information above in this readme for complete list of all essentail environment variables.
   1. Make sure to set `DJANGO_DEBUG` to false
5. Set the heroku stack to container with `heroku stack:set container -a <heroku_app_name>`
6. Use automatic deployment through git so that pushing to the production branch will automatically build and deploy. But pushing to heroku git by default also works.
7. [Some tips for setting up the Dockerfile and troubleshooting tips](https://stackoverflow.com/a/46229012/7981162)

## Initial Setup Post deployment:-

1. First step after deployment and testing that the build succeeded is to make migrations - `heroku run python manage.py makemigrations -a <heroku_app_name>`
2. Second step is to migrate the database - `heroku run python manage.py migrate -a <heroku_app_name>`
3. The migrations automatically load some essential initial data. The next step is to create a super user - `heroku run python manage.py createsuperuser -a <heroku_app_name>`. Make sure to set a very secure password. Also select a functional email ID in order to be able to receive activation email.
4. Once the super user is created, go to the Django admin console and set the institution, role and update thes status to approved.
5. Login to the app from the front end to receive the activation email and once activated, it should complete the initial setup.

## Troubleshooting:-

1. If docker-compose up keeps crashing, [rebuild the container](https://vsupalov.com/docker-compose-runs-old-containers/#the-quick-workaround)
   1. Use `docker-compose down && docker-compose build && docker-compose up`
   2. or use `docker-compose rm -f && docker-compose pull && docker-compose up`
   3. Not recommended, but last resort => `docker-compose rm -f && sudo docker-compose build`
2. If there are issues with migration conflicts, and simple solutions fail, reset the migrations with these commands:-
   1. Delete all files inside the `migrations` folder except `__init__.py`
   2. Delete the database file, in our case `./data`
   3. Run `docker-compose up`
3. If you have issues with connecting to the docker database on pgadmin, try the following step:-
   1. Stop docker and start it again with `docker-compose down && docker-compose up`
   2. If the above step doesn't help, try restarting postgresql. First stop it with `sudo service postgresql stop` and then start it up again with `sudo service postgresql start`
4. If you remove the docker images and reset it all, the database should still be intact because we have static volumes of the database in ./data. If the build fails while rebuilding the database, change the permissions of the folder with this `sudo chmod -R a+rwx ./data`
5. While creating migrations if the migration file is being created inside the container, as a temporary fix we can copy the file from the container onto the local machine using `sudo docker cp <docker_container_id>:/<path_to_file> <local_path>`. Example - `sudo docker cp 60939c395609:/app/starter/migrations ~/code/migrations`. For details see [here](https://www.geeksforgeeks.org/copying-files-to-and-from-docker-containers/)

## Useful PGAdmin commands:-

1. If you wish to delete the rows in a table and have it cascade to dependent tables, use this:-

   `TRUNCATE public.user RESTART IDENTITY CASCADE;`

2. When you experience the error ERROR: duplicate key value violates unique constraint Key already exists, use this following command on pgadmin to set the latest PK to the highest pk + 1. (Replace the table name accordingly)

   `SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('"tablename_pkey"', 'id')), (SELECT (MAX("id") + 1) FROM public.tablename), FALSE);`

3. When trying to query for rows where a certain field is empty:-

   `SELECT * FROM public.tablename WHERE COALESCE(invitecode, '') = '';`

4. Update some rows based on a condition:-

   `UPDATE public.tablename SET points = 0, remarks = 'The correct answer is "Because IP address are hard to remember"' WHERE option != 'Because IP address are hard to remember';`

## Useful Links:-

1. [Docker & Django](https://docs.docker.com/samples/django/)
2. [Docker & PostgreSQL](https://www.youtube.com/watch?v=aHbE3pTyG-Q)
3. [Autogenerate the requirements.txt file](https://stackoverflow.com/a/33468993/7981162)
4. [Implementing authentication using JWT in Django/Graphene GraphQL API](https://www.youtube.com/watch?v=pyV2_F9wlk8)
5. [Connect to the postgres table in the Docker container with pgAdmin](https://stackoverflow.com/a/62749875/7981162)
6. [How to uninstall all packages in a python project](https://stackoverflow.com/a/67379806/7981162)
7. [Setting up secure 12factor Django app with Docker and Environ, for different environemnts](https://medium.com/swlh/setting-up-a-secure-django-project-repository-with-docker-and-django-environ-4af72ce037f0)
8. [Documentation for JWT tokens and various associated configuration](https://readthedocs.org/projects/django-graphql-jwt/downloads/pdf/latest/)
