from fastapi import FastAPI
from routers import user_router, category_router, product_router, order_router, restock_router, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(user_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(restock_router.router)

@app.get("/")
def get_root():
    return {"greet": "Hello this is smartshop"}
