from fastapi import APIRouter

from app.services.llm_service import LLMService


router = APIRouter()

llm_service = LLMService()


@router.get("/models")
def get_models():
    return {
        "models": llm_service.get_available_models()
    }