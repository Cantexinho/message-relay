# message-relay
Two service project where one service sends payload, second receives and stores it.

Stack:
- FastAPI for event-consumer service as it is small with little functionality
- APScheduler for event-propagator, its light and does what this service require
- MySQL database because only need simple operations
- Docker for containerization and encapsulation of services and database
- Poetry for dependency management

Dependencies:
- event-propagator:
  - APScheduler
  - Aiohttp
  - Pydantic
  - Pydantic-settings
  - Pytest
  - Aioresponses
  - Pytest-asyncio
  - Requests
  - flake8
    
- event-consumer:
  - FastAPI
  - uvicorn
  - Pydantic
  - Pydantic-settings
  - SQLAlchemy
  - mysql-connector-python
  - pytest
  - pyjwt
  - flake8

Docker-compose:
- event-propagator (python:3.12-slim-bookworm)
- event-consumer (python:3.12-slim-bookworm)
- MySQL database (mysql:8.4)


Workflow:
- event-propagator:
  - service starts
  - service sends auth request to get auth token from event-consumer
  - time(seconds) start running
  - time reaches requested value (pydantic BaseSettings)
  - JSON object is selected randomly from predefined JSON objects file (location of file: pydantic BaseSettings)
  - service sends request to provided endpoint (pydantic BaseSettings)
 
- event-consumer:
  - service starts
  - payload endpoint start to accept incoming POST requests on the path `/event`
  - request received
  - request matches required payload => store to database / request doesn`t match required payload => return 400 Bad Request
  - store good request to database (database config in pydantic BaseSettings)

Endpoints:
- event-propagator:
  - None
- event-consumer:
  - `/token` `POST` generates auth token and refresh token when passed credentials
  - `/event` `POST` uploads received payload to database
  - `/event` `GET` lists events uploaded to database

Auth:
- Oauth2 JWT authentication for callin event-consumer. Storing username and password of event-propagator in env variables as it is the only service we want to authenticate.

Notes:
- Due to docker-compose context limitation we can only take data.json with the use of volumes. 
  I have placed data.json in event-propagator context for testing purposes, but if needed I have commented how we can pull data using absolute path in docker-compose

Installation and startup:
- Install docker to your pc
- Install make (you can use `choco install make`)
- Configure .env using .env.example as an example
- Use `make up` 
- After docker-compose finished building use `make status` to follow the logs
- Other make commads are provided in Makefile
