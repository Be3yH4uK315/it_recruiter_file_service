from fastapi import FastAPI
from app.api.v1.files import router

app = FastAPI(title="Files Service")
app.include_router(router, prefix="/v1/files")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Files Service"}
