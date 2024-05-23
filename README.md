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
  - Pydantic
  - pytest
    
- event-consumer:
  - FastAPI
  - uvicorn
  - Pydantic
  - SQLAlchemy
  - mysql-connector-python
  - pytest
  - pyjwt

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