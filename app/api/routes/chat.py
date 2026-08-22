import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from groq import APIConnectionError
from groq import APITimeoutError
from groq import AuthenticationError
from groq import NotFoundError
from groq import RateLimitError

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import LLMService


router = APIRouter()

llm_service = LLMService()

logger = logging.getLogger("LLM_BACKEND_CHAT")


# -----------------------------------
# Normal Chat Endpoint
# -----------------------------------

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    print("🔥 CHAT ENDPOINT CALLED")
    logger.info(
        "🔥 Chat request received | model=%s",
        request.model,
    )

    try:

        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ]

        logger.info(
            "Chat request received | model=%s",
            request.model,
        )

        result = await llm_service.generate_response(
            message=request.message,
            system_prompt=request.system_prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            history=history,
        )

        logger.info(
            "Chat request completed | model=%s | tokens=%s | latency_ms=%s",
            result["model"],
            result["tokens_used"],
            result["latency_ms"],
        )

        return ChatResponse(**result)

    except AuthenticationError as exc:

        logger.error("Groq authentication failed")

        raise HTTPException(
            status_code=401,
            detail={
                "error": "Authentication failed",
                "message": "Invalid or missing Groq API key.",
            },
        ) from exc

    except RateLimitError as exc:

        logger.warning("Groq rate limit reached")

        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
            },
        ) from exc

    except NotFoundError as exc:

        logger.error(
            "Groq model not found | model=%s",
            request.model,
        )

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Model not found",
                "message": f"Model '{request.model}' is not available.",
            },
        ) from exc

    except APITimeoutError as exc:

        logger.error("Groq request timed out")

        raise HTTPException(
            status_code=504,
            detail={
                "error": "Request timeout",
                "message": "The LLM provider took too long to respond.",
            },
        ) from exc

    except APIConnectionError as exc:

        logger.error("Unable to connect to Groq")

        raise HTTPException(
            status_code=503,
            detail={
                "error": "LLM provider unavailable",
                "message": "Unable to connect to the Groq API.",
            },
        ) from exc

    except Exception as exc:

        logger.exception("Unexpected chat error")

        raise HTTPException(
            status_code=500,
            detail={
                "error": "LLM request failed",
                "message": "An unexpected error occurred.",
            },
        ) from exc


# -----------------------------------
# Streaming Chat Endpoint
# -----------------------------------

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in request.history
    ]

    async def generate():

        try:

            logger.info(
                "Streaming request received | model=%s",
                request.model,
            )

            async for chunk in llm_service.stream_response(
                message=request.message,
                system_prompt=request.system_prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                history=history,
            ):

                yield chunk

        except AuthenticationError:

            logger.error("Streaming authentication failed")

            yield "\n\n[Error: Invalid or missing Groq API key.]"

        except RateLimitError:

            logger.warning("Streaming rate limit reached")

            yield "\n\n[Error: Rate limit exceeded. Please try again later.]"

        except NotFoundError:

            logger.error(
                "Streaming model not found | model=%s",
                request.model,
            )

            yield f"\n\n[Error: Model '{request.model}' is not available.]"

        except APITimeoutError:

            logger.error("Streaming request timed out")

            yield "\n\n[Error: LLM request timed out.]"

        except APIConnectionError:

            logger.error("Streaming connection failed")

            yield "\n\n[Error: Unable to connect to Groq.]"

        except Exception:

            logger.exception(
                "Unexpected streaming error"
            )

            yield "\n\n[Error: An unexpected error occurred.]"

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )