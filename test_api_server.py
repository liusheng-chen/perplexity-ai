#!/usr/bin/env python3.8
"""
Test script for the OpenAI Compatible API Server
"""
import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:8000"
API_VERSION = "v1"

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Server health check: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Server health check failed: {e}")
        return False

def test_models_endpoint():
    """Test the models endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/{API_VERSION}/models")
        print(f"✓ Models endpoint: {response.status_code}")
        data = response.json()
        print(f"  Available models: {len(data['data'])}")
        for model in data['data']:
            print(f"    - {model['id']}")
        return True
    except Exception as e:
        print(f"✗ Models endpoint failed: {e}")
        return False

def test_chat_completion(api_key="test-key"):
    """Test chat completion endpoint"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "perplexity-auto",
            "messages": [
                {"role": "user", "content": "What is 2+2? Please give a very short answer."}
            ],
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        print(f"Testing chat completion with API key: '{api_key}'")
        response = requests.post(
            f"{BASE_URL}/{API_VERSION}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"✓ Chat completion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Model: {data['model']}")
            print(f"  Response: {data['choices'][0]['message']['content'][:100]}...")
            print(f"  Usage: {data['usage']}")
        else:
            print(f"  Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Chat completion failed: {e}")
        return False

def test_streaming_completion(api_key="test-key"):
    """Test streaming chat completion"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "perplexity-auto",
            "messages": [
                {"role": "user", "content": "Count from 1 to 5"}
            ],
            "stream": True,
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        print(f"Testing streaming completion with API key: '{api_key}'")
        response = requests.post(
            f"{BASE_URL}/{API_VERSION}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        print(f"✓ Streaming completion: {response.status_code}")
        
        if response.status_code == 200:
            chunks_received = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove 'data: ' prefix
                        if data_str == '[DONE]':
                            print("  Stream completed")
                            break
                        try:
                            chunk_data = json.loads(data_str)
                            chunks_received += 1
                            if chunks_received <= 3:  # Show first 3 chunks
                                print(f"  Chunk {chunks_received}: {chunk_data}")
                        except json.JSONDecodeError:
                            pass
            print(f"  Total chunks received: {chunks_received}")
        else:
            print(f"  Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Streaming completion failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing OpenAI Compatible API Server")
    print("=" * 50)
    
    # Test with different API keys to confirm they're ignored
    test_keys = [
        "dummy-key",
        "test-123", 
        "any-string-works",
        '{"some": "json"}',  # Even JSON should be ignored now
        ""  # Empty string
    ]
    
    # Basic tests
    if not test_server_health():
        print("Server is not running. Please start it first:")
        print("python -m api_server.main")
        return
    
    print()
    test_models_endpoint()
    
    # Test with different API keys
    for i, key in enumerate(test_keys):
        print(f"\n--- Test {i+1}: API Key = '{key}' ---")
        test_chat_completion(key)
        
        # Only test streaming for first key to save time
        if i == 0:
            print()
            test_streaming_completion(key)
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("Check the server logs to confirm hardcoded cookies are being used.")
    print("=" * 50)

if __name__ == "__main__":
    main()
