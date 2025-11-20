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