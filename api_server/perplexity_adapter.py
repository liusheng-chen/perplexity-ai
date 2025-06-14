"""
Adapter to convert between OpenAI format and Perplexity API
"""
import json
import uuid
import time
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator, Generator
import logging

from .models import (
    ChatCompletionRequest, 
    ChatCompletionResponse, 
    ChatCompletionChoice,
    ChatCompletionStreamResponse,
    ChatCompletionStreamChoice,
    ChatMessage,
    ChatCompletionUsage
)
from .config import MODEL_MAPPING, DEFAULT_SOURCES

# Import Perplexity clients
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import perplexity
    import perplexity_async
except ImportError as e:
    logging.error(f"Failed to import perplexity modules: {e}")
    raise

logger = logging.getLogger(__name__)

class PerplexityAdapter:
    """Adapter class to handle conversion between OpenAI and Perplexity formats"""

    def __init__(self, cookies: Optional[Dict] = None, emailnator_cookies: Optional[Dict] = None):
        """
        Initialize the adapter - always uses hardcoded cookies, ignores parameters

        Args:
            cookies: Ignored - always uses hardcoded cookies
            emailnator_cookies: Ignored - not used in this version
        """
        # Always use hardcoded cookies, ignore any passed parameters
        self.cookies = {
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
        self.emailnator_cookies = {}  # Not used in this version
        self.sync_client = None
        self.async_client = None

        logger.info("PerplexityAdapter initialized with hardcoded cookies")
        logger.debug(f"Using {len(self.cookies)} hardcoded Perplexity cookies")

    def _parse_sse_response(self, response) -> str:
        """Parse SSE response stream to extract the final answer"""
        try:
            final_answer = ""

            for line in response.iter_lines():
                if not line:
                    continue

                line_str = line.decode('utf-8')

                if line_str.startswith('event: message'):
                    continue
                elif line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: ' prefix

                    try:
                        data = json.loads(data_str)

                        # Look for text field with answer
                        if 'text' in data:
                            text_content = data['text']

                            # If text is a string, try to parse as JSON
                            if isinstance(text_content, str):
                                try:
                                    parsed_text = json.loads(text_content)
                                    if isinstance(parsed_text, dict) and 'answer' in parsed_text:
                                        answer = parsed_text['answer']
                                        if answer and len(answer) > len(final_answer):
                                            final_answer = answer
                                            logger.debug(f"Found answer: {answer[:100]}...")
                                except json.JSONDecodeError:
                                    pass
                            elif isinstance(text_content, dict) and 'answer' in text_content:
                                answer = text_content['answer']
                                if answer and len(answer) > len(final_answer):
                                    final_answer = answer
                                    logger.debug(f"Found answer: {answer[:100]}...")

                        # Check if this is the final message
                        if data.get('text_completed') == True and data.get('final') == True:
                            logger.info("Found final message marker")
                            break

                    except json.JSONDecodeError:
                        continue
                elif line_str.startswith('event: end_of_stream'):
                    logger.info("Reached end of stream")
                    break

            if final_answer:
                # Decode Unicode escapes
                try:
                    final_answer = final_answer.encode().decode('unicode_escape')
                except:
                    pass
                logger.info(f"Successfully extracted answer: {final_answer[:100]}...")
                return final_answer
            else:
                logger.warning("No answer found in SSE stream")
                return "I apologize, but I couldn't extract a proper response from the stream."

        except Exception as e:
            logger.error(f"Error parsing SSE response: {e}")
            return f"Sorry, I encountered an error while processing the response: {str(e)}"
        
    def _get_sync_client(self) -> perplexity.Client:
        """Get or create synchronous Perplexity client"""
        if self.sync_client is None:
            logger.info("Creating synchronous Perplexity client with hardcoded cookies")
            self.sync_client = perplexity.Client(self.cookies)
            # Create account if emailnator cookies are provided and no perplexity cookies
            if self.emailnator_cookies and not self.cookies:
                try:
                    self.sync_client.create_account(self.emailnator_cookies)
                    logger.info("Created new Perplexity account")
                except Exception as e:
                    logger.warning(f"Failed to create account: {e}")
        return self.sync_client
    
    async def _get_async_client(self) -> perplexity_async.Client:
        """Get or create asynchronous Perplexity client"""
        if self.async_client is None:
            logger.info("Creating asynchronous Perplexity client with hardcoded cookies")
            self.async_client = await perplexity_async.Client(self.cookies)
            # Create account if emailnator cookies are provided and no perplexity cookies
            if self.emailnator_cookies and not self.cookies:
                try:
                    await self.async_client.create_account(self.emailnator_cookies)
                    logger.info("Created new Perplexity account")
                except Exception as e:
                    logger.warning(f"Failed to create account: {e}")
        return self.async_client
    
    def _convert_messages_to_query(self, messages: List[ChatMessage]) -> str:
        """Convert OpenAI messages format to Perplexity query string"""
        # Combine all user messages into a single query
        # System messages can be used as context
        query_parts = []
        
        for message in messages:
            if message.role == "system":
                # Add system message as context
                query_parts.append(f"Context: {message.content}")
            elif message.role == "user":
                query_parts.append(message.content)
            elif message.role == "assistant":
                # For follow-up conversations, we might need to handle this differently
                # For now, we'll skip assistant messages in the query
                pass
        
        return "\n\n".join(query_parts)
    
    def _get_perplexity_params(self, request: ChatCompletionRequest) -> Dict[str, Any]:
        """Convert OpenAI request to Perplexity parameters"""
        model_config = MODEL_MAPPING.get(request.model, MODEL_MAPPING["perplexity-auto"])
        
        params = {
            "mode": model_config["mode"],
            "model": model_config["model"],
            "sources": DEFAULT_SOURCES.get(model_config["mode"], ["web"]),
            "files": {},  # File upload not supported in this version
            "stream": request.stream or False,
            "language": "en-US",  # Default language
            "follow_up": None,  # No follow-up support in this version
            "incognito": False  # Default to non-incognito
        }
        
        return params
    
    def _create_completion_response(
        self, 
        request: ChatCompletionRequest, 
        content: str, 
        completion_id: Optional[str] = None
    ) -> ChatCompletionResponse:
        """Create OpenAI format completion response"""
        if completion_id is None:
            completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
        
        # Estimate token usage (rough approximation)
        prompt_text = self._convert_messages_to_query(request.messages)
        prompt_tokens = len(prompt_text.split()) * 1.3  # Rough token estimation
        completion_tokens = len(content.split()) * 1.3
        
        choice = ChatCompletionChoice(
            index=0,
            message=ChatMessage(role="assistant", content=content),
            finish_reason="stop"
        )
        
        usage = ChatCompletionUsage(
            prompt_tokens=int(prompt_tokens),
            completion_tokens=int(completion_tokens),
            total_tokens=int(prompt_tokens + completion_tokens)
        )
        
        return ChatCompletionResponse(
            id=completion_id,
            model=request.model,
            choices=[choice],
            usage=usage
        )
    
    def _create_stream_chunk(
        self, 
        request: ChatCompletionRequest, 
        content: str, 
        completion_id: str,
        finish_reason: Optional[str] = None
    ) -> ChatCompletionStreamResponse:
        """Create OpenAI format streaming chunk"""
        delta = {"content": content} if content else {}
        if finish_reason:
            delta = {}
        
        choice = ChatCompletionStreamChoice(
            index=0,
            delta=delta,
            finish_reason=finish_reason
        )
        
        return ChatCompletionStreamResponse(
            id=completion_id,
            model=request.model,
            choices=[choice]
        )
    
    def complete_sync(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Synchronous completion"""
        try:
            client = self._get_sync_client()
            query = self._convert_messages_to_query(request.messages)
            params = self._get_perplexity_params(request)
            
            logger.info(f"Perplexity query: {query[:100]}...")
            logger.info(f"Perplexity params: {params}")
            
            # Make the request to Perplexity
            response = client.search(query, **params)

            logger.info(f"Raw Perplexity sync response: {response}")
            logger.info(f"Response type: {type(response)}")

            if response is None:
                logger.warning("Perplexity API returned None - possibly due to expired cookies or API issues")
                content = "I apologize, but I'm currently unable to process your request due to authentication issues. The Perplexity API returned no response."
            elif isinstance(response, dict):
                # Try different possible response formats
                if 'text' in response:
                    text_data = response['text']
                    logger.info(f"Text data type: {type(text_data)}, content: {text_data}")

                    if isinstance(text_data, dict):
                        # If text is a dict, look for answer field
                        if 'answer' in text_data:
                            content = text_data['answer']
                        elif 'content' in text_data:
                            content = text_data['content']
                        else:
                            content = str(text_data)
                    elif isinstance(text_data, str):
                        # If text is a string, try to parse as JSON
                        try:
                            parsed_text = json.loads(text_data)
                            if isinstance(parsed_text, dict) and 'answer' in parsed_text:
                                content = parsed_text['answer']
                            else:
                                content = text_data
                        except json.JSONDecodeError:
                            content = text_data
                    else:
                        content = str(text_data)
                elif 'answer' in response:
                    # Direct answer field
                    content = response['answer']
                else:
                    logger.info(f"Response keys: {list(response.keys())}")
                    content = str(response)
            else:
                content = str(response)

            logger.info(f"Final extracted content: {content[:100]}...")
            
            return self._create_completion_response(request, content)
            
        except Exception as e:
            logger.error(f"Error in sync completion: {e}")
            raise
    
    def complete_stream_sync(self, request: ChatCompletionRequest) -> Generator[str, None, None]:
        """Synchronous streaming completion"""
        try:
            client = self._get_sync_client()
            query = self._convert_messages_to_query(request.messages)
            params = self._get_perplexity_params(request)
            params["stream"] = True
            
            completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
            
            logger.info(f"Perplexity streaming query: {query[:100]}...")
            
            # Get streaming response from Perplexity
            stream = client.search(query, **params)
            
            for chunk in stream:
                if chunk and 'text' in chunk:
                    content = chunk['text']
                    stream_chunk = self._create_stream_chunk(request, content, completion_id)
                    yield f"data: {stream_chunk.model_dump_json()}\n\n"
            
            # Send final chunk
            final_chunk = self._create_stream_chunk(request, "", completion_id, "stop")
            yield f"data: {final_chunk.model_dump_json()}\n\n"
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Error in sync streaming: {e}")
            raise

    async def complete_async(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Asynchronous completion"""
        try:
            client = await self._get_async_client()
            query = self._convert_messages_to_query(request.messages)
            params = self._get_perplexity_params(request)

            logger.info(f"Perplexity async query: {query[:100]}...")
            logger.info(f"Perplexity async params: {params}")

            # Make the request to Perplexity
            response = await client.search(query, **params)

            logger.info(f"Raw Perplexity response: {response}")
            logger.info(f"Response type: {type(response)}")

            if response is None:
                logger.warning("Perplexity API returned None - possibly due to expired cookies or API issues")
                content = "I apologize, but I'm currently unable to process your request due to authentication issues. The Perplexity API returned no response."
            elif isinstance(response, dict):
                # Try different possible response formats
                if 'text' in response:
                    text_data = response['text']
                    logger.info(f"Text data type: {type(text_data)}, content: {text_data}")

                    if isinstance(text_data, dict):
                        # If text is a dict, look for answer field
                        if 'answer' in text_data:
                            content = text_data['answer']
                        elif 'content' in text_data:
                            content = text_data['content']
                        else:
                            content = str(text_data)
                    elif isinstance(text_data, str):
                        # If text is a string, try to parse as JSON
                        try:
                            parsed_text = json.loads(text_data)
                            if isinstance(parsed_text, dict) and 'answer' in parsed_text:
                                content = parsed_text['answer']
                            else:
                                content = text_data
                        except json.JSONDecodeError:
                            content = text_data
                    else:
                        content = str(text_data)
                elif 'answer' in response:
                    # Direct answer field
                    content = response['answer']
                else:
                    logger.info(f"Response keys: {list(response.keys())}")
                    content = str(response)
            else:
                content = str(response)

            logger.info(f"Final extracted content: {content[:100]}...")

            return self._create_completion_response(request, content)

        except Exception as e:
            logger.error(f"Error in async completion: {e}")
            raise

    async def complete_stream_async(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        """Asynchronous streaming completion"""
        try:
            client = await self._get_async_client()
            query = self._convert_messages_to_query(request.messages)
            params = self._get_perplexity_params(request)
            params["stream"] = True

            completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"

            logger.info(f"Perplexity async streaming query: {query[:100]}...")

            # Get streaming response from Perplexity
            stream = await client.search(query, **params)

            async for chunk in stream:
                if chunk and 'text' in chunk:
                    content = chunk['text']
                    stream_chunk = self._create_stream_chunk(request, content, completion_id)
                    yield f"data: {stream_chunk.model_dump_json()}\n\n"

            # Send final chunk
            final_chunk = self._create_stream_chunk(request, "", completion_id, "stop")
            yield f"data: {final_chunk.model_dump_json()}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Error in async streaming: {e}")
            raise
