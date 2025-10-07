create network
docker network create spdtnet

create postgis
docker run -d --name postgis --network=spdtnet -e POSTGRES_PASSWORD=tempPassword -e POSTGRES_DB=spdtDB -p 5432:5432 postgis/postgis

create pgadmin4
docker run -d -p 8080:80 --network=spdtnet -e PGADMIN_DEFAULT_EMAIL=admin@gmail.com -e PGADMIN_DEFAULT_PASSWORD=tempPassword dpage/pgadmin4

connect both
In pgadmin:
Add new Server
name: postgis
hostname: postgis
username: postgres
password: tempPassword

create pg_tileserve:
docker run --network=spdtnet  -dt -e DATABASE_URL=postgresql://postgres:tempPassword@postgis/spdtDB -p 7800:7800 pramsey/pg_tileserv:latest


---
# Docker version of readme

## Quick start
1. Ensure that `docker` and `docker compose` (or the [older](https://stackoverflow.com/questions/66514436/difference-between-docker-compose-and-docker-compose) `docker-compose`) are both installed
Ensure Node.js is installed
2. Create a new docker volume named `RedisDB'. This can be done in docker desktop or using the command:
```bash 
docker volume create RedisDB
```
3. Build the app image from the dockerfile
```bash
docker build -t spdt -f Dockerfile  .
```
4. Run the `compose.yaml` file
```bash
docker compose up 
```
5. To access the Mimick MVP App, in a web browser, go to [localhost](localhost)
## House keeping

This file structure is temporary and is likely to change as the project evolves. For now:
1. Anything concerning modelling should go into /modelling
2. Functionality for the digital twin should go into /other
3. Any static data (e.g. images, datasets, maps etc. that will be the same every time) should go into static. Keep like with like in subfolders, creating new folders as needed
4. Anything without a home should go into /other. We should try and kee this folder as empty as possible, if it gets too full we should reorganise
5. Anything that shouldn't be uploaded to Github should be added to the .gitignore. Any passwords/ user credentials etc. should be filed under /other/private