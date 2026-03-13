from fastapi import FastAPI
from app.routers import hello, dynamo
from mangum import Mangum

app = FastAPI()
app.include_router(hello.router)
app.include_router(dynamo.router)


@app.get("/")
async def root():
    return {"message": "Hello World from Root!"}


handler = Mangum(app)
