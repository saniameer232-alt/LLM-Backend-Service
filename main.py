from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.models import router as models_router


app = FastAPI(title="LLM Backend Service")


@app.get("/")
def root():
    return {"message": "LLM Backend Service is running"}


app.include_router(chat_router)
app.include_router(models_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )