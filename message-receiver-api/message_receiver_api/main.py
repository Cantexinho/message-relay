from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ready/")
async def ready_check():
    return Response(status_code=status.HTTP_200_OK, content="ok")
