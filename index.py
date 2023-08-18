from fastapi import FastAPI
from routes.user_route import user_router
from routes.transaction_route import transaction_router

app = FastAPI()
app.include_router(user_router, prefix="/api")
app.include_router(transaction_router, prefix="/api")
