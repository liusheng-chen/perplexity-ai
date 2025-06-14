"""
OpenAI Compatible API Server for Perplexity AI
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import uvicorn

from .models import (
    ChatCompletionRequest,
    ChatCompletionResponse, 
    ModelsResponse,
    ModelInfo,
    ErrorResponse
)
from .perplexity_adapter import PerplexityAdapter
from .config import (
    MODEL_MAPPING,
    SERVER_HOST,
    SERVER_PORT,
    API_VERSION,
    DEFAULT_MODEL
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global adapter instance
adapter: Optional[PerplexityAdapter] = None

# Security scheme
security = HTTPBearer(auto_error=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global adapter
    logger.info("Starting Perplexity API Server...")
    
    # Initialize adapter (will be configured per request based on API key)
    adapter = PerplexityAdapter()
    
    yield
    
    logger.info("Shutting down Perplexity API Server...")

# Create FastAPI app
app = FastAPI(
    title="Perplexity AI - OpenAI Compatible API",
    description="OpenAI Compatible API Server for Perplexity AI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_hardcoded_cookies() -> Dict[str, Any]:
    """
    Return hardcoded cookies - ignores any external API key
    """
    cookies = {
        'pplx.visitor-id': 'a708621e-c83b-4453-8763-f0d7f075986a',
        'pplx.session-id': '69312f60-388b-4c15-94da-d9ce9ca1a292',
        '__cflb': '02DiuDyvFMmK5p9jVbVnMNSKYZhUL9aGmKaa5e4DZaVd6',
        'cf_clearance': 'I0cjtmC5xF.702gN0DBjUeJl_FNJI6h37FBkI8_IDlI-1749821658-1.2.1.1-BTClaKezyACtLYwRJ8.1RAXwWbz7o2arWCoghHLHX.U.Zrzg6Fc9hi6JVv7Q3TRvQG9YvzkNJr6exiaP6ybjpEnDYk5SU67KaADWsFHyTpdRzJmhz28AGIIQmxiLmfpqM7c2GikaU4j.Xh87ged..K1k7CDZaMVmeP49gUxVcJO4dPgJG08h5dZvUexArdld5cIzTaxl5CNqbcu7wM.zuAmd8iKlkq6023OqE9ApAMpyObIwY8YgSRH3_vkjyc7OP.titWFbOpkstGGw.kBAHf4u9I.bcS3h1B7U3B80rquk82hl7A6sK9cXQaSYqsAi7SgpvnJdWSeLozFMXc9F4YXf49fgBiZcVaHis2TuccE_rHTIFmguPG603uJ6P7iI',
        'next-auth.csrf-token': '016caa3f88438bee1fd806d0c0108763eb3cb81871dc4d77120581c1d7bd7cb3%7C7e1ea93d7b2f2f1be609b9e3d71623557d0aca785065a6be987238956a6eeab0',
        'sidebarHiddenHubs': '[]',
        'voice-mode-activation-tooltip': '1',
        '_gcl_au': '1.1.1607421484.1749821661',
        'next-auth.callback-url': 'https%3A%2F%2Fwww.perplexity.ai%2Fapi%2Fauth%2Fsignin-callback%3Fredirect%3Dhttps%253A%252F%252Fwww.perplexity.ai%252F%253Flogin-source%253DfloatingSignup',
        'pplx.metadata': '{%22qc%22:0%2C%22qcu%22:280%2C%22qcm%22:79%2C%22qcc%22:274%2C%22qcr%22:0%2C%22qcdr%22:0%2C%22qcs%22:0%2C%22qcd%22:0%2C%22hli%22:true%2C%22hcga%22:false%2C%22hcds%22:false%2C%22hso%22:false%2C%22hfo%22:false}',
        'AWSALB': 'Ny2UV2ifO+O7KoyNiAEvUTfMPm2jGgTuyT4jFgCr0dnEctI9cWYmWwArqdkuU89MHWjoCbvkSrPTWa85bf0/dt4vtDL3MQ9Ej6GrgNTe1WPXV3ZFIQzTP5D3pBPd',
        'AWSALBCORS': 'Ny2UV2ifO+O7KoyNiAEvUTfMPm2jGgTuyT4jFgCr0dnEctI9cWYmWwArqdkuU89MHWjoCbvkSrPTWa85bf0/dt4vtDL3MQ9Ej6GrgNTe1WPXV3ZFIQzTP5D3pBPd',
        '__Secure-next-auth.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..On1BQ0DqJs6b2jhz.6YfeepB0p6mEATHaagXE0qlR_yc5rKTnBsU2hIeK7Wty9wa91StuKjK5cES-dhUjiACBHl1-vk8wJz0CfqrVzI2b7mT9MnZYCNGwZTizNw8CIDqJkdIwDK8zvHjqxD3VildNdKnfoRxjmASZurAOi9xarUFWFTWw-eirGAADWZzYMTkK4tJYmRIGRMZJ2e5Yk_Rz2fng9ZW5N90Kb-cdCltpOC7oE_-fhSgmiHlCm37OTwS0QjeJtyOidCwyOBNu24wtpQ.97Kq8E6MO3uh0ClLc72plw',
        '_rdt_uuid': '1749821752527.90917331-65cc-4955-ad75-9c3bd3793e50',
        '__podscribe_perplexityai_referrer': 'https://accounts.google.co.jp/',
        '__podscribe_perplexityai_landing_url': 'https://www.perplexity.ai/?login-source=floatingSignup&login-new=false',
        '__cf_bm': 'HE3GzvB5nyL9mBSrpC9sbxjDuWupqqDgRTFS6gCqEKM-1749821760-1.0.1.1-wngYpOQvZgBQI8AlyslKfiEt50_upcMZOLN5DmhJU3AMvFDF5wRhzIuZfYTz4xqTdQdJRJ6MNnZR3Xi.t_Drb3M0OIycQxOR0N8GljzMaI8',
        '_fbp': 'fb.1.1749821759753.831608165429360035',
        '_dd_s': 'aid=cb614a2c-b942-4cb5-97f3-4d4453a1fb63&rum=0&expire=1749822667984&logs=0',
    }
    emailnator_cookies = {}

    logger.info("Using hardcoded Perplexity cookies (ignoring any external API key)")
    logger.debug(f"Hardcoded cookies count: {len(cookies)} cookies")

    return {"cookies": cookies, "emailnator_cookies": emailnator_cookies}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Perplexity AI - OpenAI Compatible API Server",
        "version": "1.0.0",
        "endpoints": {
            "models": f"/{API_VERSION}/models",
            "chat_completions": f"/{API_VERSION}/chat/completions"
        }
    }

@app.get(f"/{API_VERSION}/models")
async def list_models() -> ModelsResponse:
    """List available models"""
    models = []
    for model_id, config in MODEL_MAPPING.items():
        model_info = ModelInfo(
            id=model_id,
            owned_by="perplexity"
        )
        models.append(model_info)
    
    return ModelsResponse(data=models)

@app.post(f"/{API_VERSION}/chat/completions")
async def create_chat_completion(
    raw_request: Request,
    request: ChatCompletionRequest,
    auth_data: Dict[str, Any] = Depends(get_hardcoded_cookies)
):
    """Create chat completion"""
    try:
        # 首先打印原始请求体
        try:
            raw_body = await raw_request.body()
            raw_json = json.loads(raw_body.decode('utf-8'))
            logger.info("="*60)
            logger.info("📥 RAW REQUEST BODY (before Pydantic validation):")
            logger.info(json.dumps(raw_json, indent=2, ensure_ascii=False))
            logger.info("="*60)
        except Exception as e:
            logger.warning(f"Could not parse raw request body: {e}")

        logger.info("="*60)
        logger.info("📥 PARSED REQUEST DETAILS (after Pydantic validation):")
        logger.info(f"Model: {request.model}")
        logger.info(f"Messages count: {len(request.messages)}")
        logger.info(f"Stream: {request.stream}")
        logger.info(f"Max tokens: {request.max_tokens}")
        logger.info(f"Temperature: {request.temperature}")

        # 打印消息内容
        for i, message in enumerate(request.messages):
            logger.info(f"Message {i+1}:")
            logger.info(f"  Role: {message.role}")
            logger.info(f"  Content type: {type(message.content)}")
            if isinstance(message.content, str):
                logger.info(f"  Content (string): {repr(message.content[:200])}...")
            elif isinstance(message.content, list):
                logger.info(f"  Content (list with {len(message.content)} parts):")
                for j, part in enumerate(message.content):
                    if hasattr(part, 'type') and hasattr(part, 'text'):
                        logger.info(f"    Part {j+1}: type={part.type}, text={repr(part.text[:100])}...")
                    else:
                        logger.info(f"    Part {j+1}: {part}")
            else:
                logger.info(f"  Content (other): {message.content}")

        logger.info("="*60)

        # Validate model
        if request.model not in MODEL_MAPPING:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{request.model}' not found. Available models: {list(MODEL_MAPPING.keys())}"
            )
        
        # Create adapter with cookies from API key
        request_adapter = PerplexityAdapter(
            cookies=auth_data["cookies"],
            emailnator_cookies=auth_data["emailnator_cookies"]
        )
        
        logger.info(f"Processing request for model: {request.model}, stream: {request.stream}")
        
        if request.stream:
            # Streaming response
            logger.info("🌊 Starting streaming response...")

            async def generate_stream():
                chunk_count = 0
                try:
                    async for chunk in request_adapter.complete_stream_async(request):
                        chunk_count += 1
                        logger.info(f"📡 Stream chunk {chunk_count}: {chunk[:100]}...")
                        yield chunk
                except Exception as e:
                    logger.error(f"Streaming error: {e}")
                    error_chunk = f"data: {json.dumps({'error': str(e)})}\n\n"
                    logger.info(f"📡 Error chunk: {error_chunk}")
                    yield error_chunk
                    yield "data: [DONE]\n\n"
                    logger.info("📡 Stream ended with [DONE]")

                logger.info(f"🌊 Streaming completed, total chunks: {chunk_count}")

            return StreamingResponse(
                generate_stream(),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/plain; charset=utf-8"
                }
            )
        else:
            # Non-streaming response - try sync first to debug
            try:
                response = request_adapter.complete_sync(request)

                # 详细打印响应内容用于调试
                logger.info("="*60)
                logger.info("📤 RESPONSE DETAILS FOR DEBUGGING:")
                logger.info(f"Response type: {type(response)}")

                if hasattr(response, 'dict'):
                    response_dict = response.dict()
                    logger.info(f"Response as dict: {json.dumps(response_dict, indent=2, ensure_ascii=False)}")
                elif hasattr(response, '__dict__'):
                    logger.info(f"Response attributes: {response.__dict__}")
                else:
                    logger.info(f"Response content: {response}")

                # 打印 JSON 序列化后的内容
                try:
                    if hasattr(response, 'dict'):
                        json_str = json.dumps(response.dict(), ensure_ascii=False)
                        logger.info(f"JSON serialized length: {len(json_str)} characters")
                        logger.info(f"JSON content preview: {json_str[:200]}...")
                        logger.info(f"JSON content full: {json_str}")
                    else:
                        json_str = json.dumps(response, default=str, ensure_ascii=False)
                        logger.info(f"Fallback JSON: {json_str}")
                except Exception as json_error:
                    logger.error(f"JSON serialization error: {json_error}")

                logger.info("="*60)

                return response
            except Exception as sync_error:
                logger.warning(f"Sync completion failed: {sync_error}, trying async...")
                response = await request_adapter.complete_async(request)

                # 同样为异步响应添加调试日志
                logger.info("="*60)
                logger.info("📤 ASYNC RESPONSE DETAILS FOR DEBUGGING:")
                logger.info(f"Async response type: {type(response)}")

                if hasattr(response, 'dict'):
                    response_dict = response.dict()
                    logger.info(f"Async response as dict: {json.dumps(response_dict, indent=2, ensure_ascii=False)}")
                    json_str = json.dumps(response_dict, ensure_ascii=False)
                    logger.info(f"Async JSON content: {json_str}")

                logger.info("="*60)

                return response
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": {"message": str(exc), "type": "validation_error", "details": exc.errors()}}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": {"message": str(exc), "type": "internal_error"}}
    )

def main():
    """Main entry point"""
    logger.info(f"Starting server on {SERVER_HOST}:{SERVER_PORT}")
    uvicorn.run(
        "api_server.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
