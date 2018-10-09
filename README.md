# Project Title: Web Portal for Concentration and Flux of CO<sub>2</sub> in Global Inland Waters

## Introduction
Observational data, especially *in situ* CO<sub>2</sub> concentration and flux measurements, are essential for correctly modeling CO<sub>2</sub> evasions from global inland waters. However, these measurements were collected and published separately by different research groups and there is a lack of a cohesive synthesis of direct measurements, hampering our ability to accurately model CO<sub>2</sub> emissions from inland waters. We believe that a global synthesis of direct CO<sub>2</sub> measurements would greatly enhance our understanding of the role that inland water plays in contributing CO<sub>2</sub> to the atmosphere. The aim of this project is to develop a publically accessible, easy-to-use web portal for inland water greenhouse gas researchers to easily input, visualize and download data from the portal. See this impressive web portal from Global Ocean Acidification Network for visualizing ocean field campaigns as an exmple: http://portal.goa-on.org/Explorer.

Refer to the project's [phase 1](phase1.md) development for a general description of the CO<sub>2</sub>web project.

Refer to [phase 2](phase2.md) development of the project for detailed description of phase 2 development of the CO<sub>2</sub>web project.

## Docker compose spin up
The project uses docker as the development environment. Make sure to have docker and docker-compose installed on your local machine then run the following command to build and spin up the application.

```bash
docker-compose -f infra/docker-compose.yml -p co2web up
```
Now the container should be running.

To have a Jupyter Notebook running from the Docker Container, run the command:

```bash
docker-compose -f infra/docker-compose.yml -p co2web run --rm --no-deps -p 8888:8888 django-web-server bash -c "source activate backend && jupyter notebook --allow-root --notebook-dir=./notebooks --ip=0.0.0.0 --port=8888"
```

To stop your work session, run `ctrl + c`

```bash
docker-compose -f infra/docker-compose.yml -p co2web down
```

To re-start your work session repeat the first two steps.

To Access Django Admin Page,use web browser to visit localhost:8000/admin

* user: co2master
* password: *************

Rebuild the Docker Instance, run:

```bash
docker-compose -f infra/docker-compose.yml -p co2web down --volumes
```  

```bash
docker-compose -f infra/docker-compose.yml -p co2web up
```