# Importing necessary modules
# re: Regular expressions for pattern matching
# sys: System-specific parameters and functions
# json: JSON parsing and serialization
# random: Random number generation
# mimetypes: Guessing MIME types of files
# uuid: Generating unique identifiers
# curl_cffi: HTTP requests and multipart form data handling
import re
import sys
import json
import random
import mimetypes
from uuid import uuid4
from curl_cffi import requests, CurlMime

# Importing Emailnator class for email generation
from .emailnator import Emailnator

class Client:
    '''
    A client for interacting with the Perplexity AI API.
    '''

    def __init__(self, cookies={}):
        # Initialize an HTTP session with default headers and optional cookies
        self.session = requests.Session(headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"128.0.6613.120"',
            'sec-ch-ua-full-version-list': '"Not;A=Brand";v="24.0.0.0", "Chromium";v="128.0.6613.120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }, cookies=cookies, impersonate='chrome')

        # Flags and counters for account and query management
        self.own = bool(cookies)  # Indicates if the client uses its own account
        self.copilot = 0 if not cookies else float('inf')  # Remaining pro queries
        self.file_upload = 0 if not cookies else float('inf')  # Remaining file uploads

        # Regular expression for extracting sign-in links
        self.signin_regex = re.compile(r'"(https://www\\.perplexity\\.ai/api/auth/callback/email\\?callbackUrl=.*?)"')

        # Unique timestamp for session identification
        self.timestamp = format(random.getrandbits(32), '08x')

        # Initialize session by making a GET request
        self.session.get('https://www.perplexity.ai/api/auth/session')

    def create_account(self, cookies):
        '''
        Creates a new account using Emailnator cookies.
        '''
        while True:
            try:
                # Initialize Emailnator client
                emailnator_cli = Emailnator(cookies)

                # Send a POST request to initiate account creation
                resp = self.session.post('https://www.perplexity.ai/api/auth/signin/email', data={
                    'email': emailnator_cli.email,
                    'csrfToken': self.session.cookies.get_dict()['next-auth.csrf-token'].split('%')[0],
                    'callbackUrl': 'https://www.perplexity.ai/',
                    'json': 'true'
                })

                # Check if the response is successful
                if resp.ok:
                    # Wait for the sign-in email to arrive
                    new_msgs = emailnator_cli.reload(wait_for=lambda x: x['subject'] == 'Sign in to Perplexity', timeout=20)

                    if new_msgs:
                        break
                else:
                    print('Perplexity account creating error:', resp)

            except Exception:
                pass

        # Extract the sign-in link from the email
        msg = emailnator_cli.get(func=lambda x: x['subject'] == 'Sign in to Perplexity')
        new_account_link = self.signin_regex.search(emailnator_cli.open(msg['messageID'])).group(1)

        # Complete the account creation process
        self.session.get(new_account_link)

        # Update query and file upload limits
        self.copilot = 5
        self.file_upload = 10

        return True

    def extract_answer(self, response_data):
        '''
        Extract the final answer text from Perplexity response data.
        '''
        if not response_data:
            return None

        # 尝试从不同字段提取答案
        text_content = response_data.get('text', [])

        if isinstance(text_content, list):
            # 查找包含答案的步骤
            for step in text_content:
                if isinstance(step, dict):
                    step_type = step.get('step_type')
                    if step_type in ['ANSWER', 'FINAL_ANSWER', 'RESPONSE']:
                        content = step.get('content', {})
                        if isinstance(content, dict) and 'text' in content:
                            return content['text']
                        elif isinstance(content, str):
                            return content

            # 如果没有找到特定的答案步骤，查找最后一个有内容的步骤
            for step in reversed(text_content):
                if isinstance(step, dict):
                    content = step.get('content', {})
                    if isinstance(content, dict) and 'text' in content:
                        text = content['text']
                        if text and len(text.strip()) > 10:  # 过滤掉太短的内容
                            return text
                    elif isinstance(content, str) and len(content.strip()) > 10:
                        return content

        # 如果text是字符串，直接返回
        elif isinstance(text_content, str):
            return text_content

        # 尝试其他可能的字段
        for field in ['answer', 'response', 'result', 'output']:
            if field in response_data:
                value = response_data[field]
                if isinstance(value, str) and value.strip():
                    return value

        return None

    def search(self, query, mode='auto', model=None, sources=['web'], files={}, stream=False, language='en-US', follow_up=None, incognito=False):
        '''
        Executes a search query on Perplexity AI.

        Parameters:
        - query: The search query string.
        - mode: Search mode ('auto', 'pro', 'reasoning', 'deep research').
        - model: Specific model to use for the query.
        - sources: List of sources ('web', 'scholar', 'social').
        - files: Dictionary of files to upload.
        - stream: Whether to stream the response.
        - language: Language code (ISO 639).
        - follow_up: Information for follow-up queries.
        - incognito: Whether to enable incognito mode.
        '''
        # Validate input parameters
        assert mode in ['auto', 'pro', 'reasoning', 'deep research'], 'Invalid search mode.'
        assert model in {
            'auto': [None],
            'pro': [None, 'sonar', 'gpt-4.5', 'gpt-4o', 'claude 3.7 sonnet', 'gemini 2.0 flash', 'grok-2'],
            'reasoning': [None, 'r1', 'o3-mini', 'claude 3.7 sonnet'],
            'deep research': [None]
        }[mode] if self.own else True, 'Invalid model for the selected mode.'
        assert all([source in ('web', 'scholar', 'social') for source in sources]), 'Invalid sources.'
        assert self.copilot > 0 if mode in ['pro', 'reasoning', 'deep research'] else True, 'No remaining pro queries.'
        assert self.file_upload - len(files) >= 0 if files else True, 'File upload limit exceeded.'

        # Update query and file upload counters
        self.copilot = self.copilot - 1 if mode in ['pro', 'reasoning', 'deep research'] else self.copilot
        self.file_upload = self.file_upload - len(files) if files else self.file_upload

        # Upload files and prepare the query payload
        uploaded_files = []
        for filename, file in files.items():
            file_type = mimetypes.guess_type(filename)[0]
            file_upload_info = (self.session.post(
                'https://www.perplexity.ai/rest/uploads/create_upload_url?version=2.18&source=default',
                json={
                    'content_type': file_type,
                    'file_size': sys.getsizeof(file),
                    'filename': filename,
                    'force_image': False,
                    'source': 'default',
                }
            )).json()

            # Upload the file to the server
            mp = CurlMime()
            for key, value in file_upload_info['fields'].items():
                mp.addpart(name=key, data=value)
            mp.addpart(name='file', content_type=file_type, filename=filename, data=file)

            upload_resp = self.session.post(file_upload_info['s3_bucket_url'], multipart=mp)

            if not upload_resp.ok:
                raise Exception('File upload error', upload_resp)

            # Extract the uploaded file URL
            if 'image/upload' in file_upload_info['s3_object_url']:
                uploaded_url = re.sub(
                    r'/private/s--.*?--/v\\d+/user_uploads/',
                    '/private/user_uploads/',
                    upload_resp.json()['secure_url']
                )
            else:
                uploaded_url = file_upload_info['s3_object_url']

            uploaded_files.append(uploaded_url)

        # Prepare the JSON payload for the query
        json_data = {
            'query_str': query,
            'params': {
                'attachments': uploaded_files + follow_up['attachments'] if follow_up else uploaded_files,
                'frontend_context_uuid': str(uuid4()),
                'frontend_uuid': str(uuid4()),
                'is_incognito': incognito,
                'language': language,
                'last_backend_uuid': follow_up['backend_uuid'] if follow_up else None,
                'mode': 'concise' if mode == 'auto' else 'copilot',
                'model_preference': {
                    'auto': { None: 'turbo' },
                    'pro': {
                        None: 'pplx_pro',
                        'sonar': 'experimental',
                        'gpt-4.5': 'gpt45',
                        'gpt-4o': 'gpt4o',
                        'claude 3.7 sonnet': 'claude2',
                        'gemini 2.0 flash': 'gemini2flash',
                        'grok-2': 'grok'
                    },
                    'reasoning': {
                        None: 'pplx_reasoning',
                        'r1': 'r1',
                        'o3-mini': 'o3mini',
                        'claude 3.7 sonnet': 'claude37sonnetthinking'
                    },
                    'deep research': { None: 'pplx_alpha' }
                }[mode][model],
                'source': 'default',
                'sources': sources,
                'version': '2.18'
            }
        }

        # Send the query request and handle the response
        resp = self.session.post('https://www.perplexity.ai/rest/sse/perplexity_ask', json=json_data, stream=True, timeout=60)
        # print(f"Response object received: {resp}") # Debug print
        chunks = []

        def stream_response(resp):
            '''
            Generator for streaming responses.
            '''
            for chunk in resp.iter_lines(delimiter=b'\r\n\r\n'):
                # print(f"Streamed chunk: {chunk}") # Debug print
                content = chunk.decode('utf-8')

                if content.startswith('event: message\r\n'):
                    content_json = json.loads(content[len('event: message\r\ndata: '):])
                    content_json['text'] = json.loads(content_json['text'])

                    chunks.append(content_json)
                    yield chunks[-1]

                elif content.startswith('event: end_of_stream\r\n'):
                    return

        if stream:
            return stream_response(resp)

        # print("Entering non-stream mode iteration.") # Debug print
        final_answer = None

        for chunk in resp.iter_lines(delimiter=b'\r\n\r\n'):
            # print(f"Non-stream chunk: {chunk}") # Debug print
            content = chunk.decode('utf-8')

            if content.startswith('event: message\r\n'):
                try:
                    content_json = json.loads(content[len('event: message\r\ndata: '):])
                    content_json['text'] = json.loads(content_json['text'])
                    chunks.append(content_json)

                    # 检查是否包含最终答案
                    if content_json.get('text_completed', False) or content_json.get('status') == 'completed':
                        final_answer = content_json
                        # print(f"Found final answer: {final_answer.get('text', 'No text field')}")

                except json.JSONDecodeError as e:
                    # print(f"JSON decode error: {e}")
                    continue

            elif content.startswith('event: end_of_stream\r\n'):
                # print("End of stream detected.")
                break

        # print("Exiting non-stream mode iteration.") # Debug print

        # 返回最终答案，如果没有找到则返回最后一个chunk
        result_data = final_answer if final_answer else (chunks[-1] if chunks else None)

        if result_data:
            # 尝试提取可读的答案文本
            extracted_answer = self.extract_answer(result_data)
            if extracted_answer:
                # print(f"Extracted answer: {extracted_answer[:200]}...")
                return {
                    'answer': extracted_answer,
                    'raw_data': result_data,
                    'status': 'success'
                }
            else:
                # print("Could not extract readable answer, returning raw data")
                return {
                    'answer': None,
                    'raw_data': result_data,
                    'status': 'no_answer_extracted'
                }
        else:
            # print("No chunks received!")
            return {
                'answer': None,
                'raw_data': None,
                'status': 'no_response'
            }