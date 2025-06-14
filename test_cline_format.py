#!/usr/bin/env python3
"""
Test script to verify Cline multimodal format support
"""
import requests
import json
import os

# Disable proxy for localhost
os.environ['no_proxy'] = 'localhost,127.0.0.1'

def test_cline_format():
    """Test the multimodal content format that Cline uses"""
    
    # Test data mimicking Cline's format
    test_data = {
        "model": "perplexity-reasoning",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "<task>\n测试\n</task>"
                    },
                    {
                        "type": "text", 
                        "text": "<environment_details>\n# VSCode Visible Files\ntest.py\n\n# Current Time\n2025/6/14 上午0:30:00\n</environment_details>"
                    }
                ]
            }
        ],
        "stream": False
    }
    
    print("Testing Cline multimodal format...")
    print(f"Request data: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nResponse status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Success! Cline format is now supported")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print("❌ Failed!")
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_simple_format():
    """Test the simple string format for comparison"""
    
    test_data = {
        "model": "perplexity-reasoning",
        "messages": [
            {
                "role": "user",
                "content": "你好，请简单介绍一下自己"
            }
        ],
        "stream": False
    }
    
    print("\n" + "="*50)
    print("Testing simple string format...")
    print(f"Request data: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nResponse status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success! Simple format still works")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print("❌ Failed!")
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_cline_format()
    test_simple_format()
