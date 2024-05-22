# message-relay
Two service project where one service sends payload, second receives and stores it.

Stack:
- FastAPI for services as they are small with little functionality
- MySQL database because only need simple operations
- Docker for containerization and encapsulation of services and database
- Poetry for dependency management

Dependencies:
- event-propagator:
  - FastAPI
  - uvicorn
  - Pydantic
  - pytest
    
- event-consumer:
  - FastAPI
  - uvicorn
  - Pydantic
  - SQLAlchemy
  - mysql-connector-python
  - pytest

Docker-compose:
- event-propagator (python:3.12-slim-bookworm)
- event-consumer (python:3.12-slim-bookworm)
- MySQL database (mysql:8.4)


Workflow:
- event-propagator:
  - service starts
  - time(seconds) start running
  - time reaches requested value (pydantic BaseSettings)
  - JSON object is selected randomly from predefined JSON objects file (location of file: pydantic BaseSettings)
  - service sends request to provided endpoint (pydantic BaseSettings)
 
- event-consumer:
  - service starts
  - endpoint start to accept incoming POST requests on the path `/event`
  - request received
  - request matches required payload => store to database / request doesn`t match required payload => return 400 Bad Request
  - store good request to database (database config in pydantic BaseSettings)
