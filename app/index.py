from fastapi import FastAPI
from app.routes.user_route import user_router
from app.routes.transaction_route import transaction_router

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "To view the documentations @ http://127.0.0.1:8000/docs"}


@app.get("/api")
async def root():
    return {"msg": "To view the documentations @ http://127.0.0.1:8000/docs"}


app.include_router(user_router, prefix="/api")
app.include_router(transaction_router, prefix="/api")
