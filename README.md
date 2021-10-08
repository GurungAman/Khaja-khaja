## Khaja-khaja
API for a Food Ordering Management System.

### How to run:
- Install docker from [here](https://docs.docker.com/get-docker/) and docker-compose from [here](https://docs.docker.com/compose/install/).
- Run: ```docker-compose up --build```
- To make migrations and create dummy data: ```docker exec -it <container_name> ./seeder.sh```
- Open ```localhost:8000/api``` to view api documentation.
