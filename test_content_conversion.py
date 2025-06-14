#!/usr/bin/env python3
"""
Test script to verify content conversion from multimodal to string format
"""
import requests
import json
import os

# Disable proxy for localhost
os.environ['no_proxy'] = 'localhost,127.0.0.1'

def test_content_conversion():
    """Test that multimodal content is properly converted to string"""
    
    # Test data with multiple text parts
    test_data = {
        "model": "perplexity-reasoning",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "第一部分：你好"
                    },
                    {
                        "type": "text", 
                        "text": "第二部分：请介绍自己"
                    },
                    {
                        "type": "text",
                        "text": "第三部分：谢谢"
                    }
                ]
            }
        ],
        "stream": False
    }
    
    print("Testing multimodal content conversion...")
    print(f"Original multimodal content:")
    for i, part in enumerate(test_data["messages"][0]["content"]):
        print(f"  Part {i+1}: {part['text']}")
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nResponse status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success! Multimodal content was processed")
            result = response.json()
            
            # The server should have received the content as a single string
            # We can infer this from the token count - if it processed all parts,
            # the token count should reflect the combined content
            usage = result.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            print(f"Prompt tokens: {prompt_tokens}")
            
            if prompt_tokens > 5:  # Should be more than just one part
                print("✅ Content appears to have been properly combined")
            else:
                print("⚠️  Token count seems low - content might not be fully combined")
                
        else:
            print("❌ Failed!")
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_mixed_content():
    """Test mixed content types (should only process text)"""
    
    test_data = {
        "model": "perplexity-reasoning", 
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "这是文本内容"
                    },
                    {
                        "type": "image_url",  # This should be ignored
                        "image_url": {"url": "data:image/jpeg;base64,fake"}
                    },
                    {
                        "type": "text",
                        "text": "这是另一个文本内容"
                    }
                ]
            }
        ],
        "stream": False
    }
    
    print("\n" + "="*50)
    print("Testing mixed content types (text + non-text)...")
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success! Mixed content was processed (non-text parts ignored)")
            result = response.json()
            usage = result.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            print(f"Prompt tokens: {prompt_tokens}")
        else:
            print("❌ Failed!")
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_content_conversion()
    test_mixed_content()
