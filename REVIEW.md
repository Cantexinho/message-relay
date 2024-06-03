## Task review by Ignas

The task review is composed of two parts - a general overview here and comments in the code.

## Pros

1. Previewed good knowledge of Python tooling, such as Poetry, Pydantic, FastAPI.

2. Code is generally well structured, pretty clear naming of submodules, methods and classes.

3. Code is covered with tests.

4. Task requirements fulfilled and the services are working as expected.

5. Showed good practise knowledge by implementing a readyness check endpoint.

6. Clean Dockerfile and docker-compose setup.

7. Kudos for going the extra mile to implement authentication. :prayge:



## Cons

1. Inconsistent use of typing. Some methods have declared types, while others are missing them. Usage of type hints should be consistant through the whole project.

2. Lacking knowledge in sync/async context management. Synchronous I/O methods shouldn't be used in an async context, as it defeats the purpose of having async completely. 

3. Missed some important edge cases in error handling (F.E. `Propagator.get_events()`), that would break the application in an unexpected way.

4. Code could be more readable in some places. There were a few cases where there were more nested layers than there should be.

5. Packaging of the services isn't perfect. Ideally, the services should be bundled in a `src/` folder and have a `__main__.py` file, which would allow for the services to be run as a module. F.E. `python -m event_propagator` instead of `python event_propagator/main.py` 