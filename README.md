# esiva.it

## Requirements
Docker installed and running.

## Build repo
`docker-compose build`<br>
Images and dockerfiles will take care of DB creation, requirements installation.

### DB not created
In case the DB has not been created you can access it through `docker exec -it postgres_1 /bin/sh`, then:

1) make sure the postgres container is up and running `docker-compose up postgres`;
2) su postgres;
3) psql;
4) exec any functionality, eg. created new table and give your user privileges.

## Run the project
`docker-compose up`
