Overall:
 + good readme
 + recent Python versions (3.12)
 + using recent Poetry (1.8.3)
 + use DB as a storage (MySQL)
 + using docker-compose
 + using Makefile (`make up` and all good)
 + using auth (Oauth2 JWT), though it was not required
 + using SQLAlchemy
 + there are unit tests


Code:
 * DB calls a sync and they are called from an async function (FastAPI)
 * it would be nice to have some unified prefix set to configure consumer and propagator
 * in propagator HTTP post URL better as const or settings (nit-picking)
 + try-excepts are trying to be explicit (not except Exeption: ...)


Unit tests:
 * could be more negative tests (for failures)


Questions / topics to discuss:
 * architecture choice (why async)?
