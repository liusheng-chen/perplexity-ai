#!/usr/bin/env python3
"""
专门测试多模态格式的脚本
"""
import requests
import json
import os

# 禁用代理
os.environ['no_proxy'] = 'localhost,127.0.0.1'

def test_multimodal_request():
    """测试多模态请求（Cline 格式）"""
    
    print("🔄 测试多模态格式（Cline 格式）...")
    
    # Cline 风格的多模态数据
    test_data = {
        "model": "perplexity-reasoning",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请执行以下任务："
                    },
                    {
                        "type": "text",
                        "text": "打印数字 0"
                    }
                ]
            }
        ],
        "stream": False,
        "max_tokens": 50
    }
    
    print(f"📤 发送多模态请求...")
    print(f"内容部分数量: {len(test_data['messages'][0]['content'])}")
    
    for i, part in enumerate(test_data['messages'][0]['content']):
        print(f"  部分 {i+1}: {part}")
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 收到响应，状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ 多模态请求成功!")
            print(f"响应ID: {result.get('id')}")
            print(f"模型: {result.get('model')}")
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"🤖 AI 回复: {content}")
            
            if 'usage' in result:
                usage = result['usage']
                print(f"📊 Token 使用: {usage}")
                
        else:
            print(f"❌ 多模态请求失败!")
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    print("🧪 多模态格式专项测试")
    print("="*50)
    test_multimodal_request()
