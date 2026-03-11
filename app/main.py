from fastapi import FastAPI
from app.routers import timestamp
from mangum import Mangum

app = FastAPI()
app.include_router(timestamp.router)


@app.get("/")
async def root():
    return {"message": "Hello World from Root!"}


handler = Mangum(app)
