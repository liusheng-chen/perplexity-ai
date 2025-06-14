#!/usr/bin/env python3
"""
简单的 Cline 测试脚本
"""
import requests
import json
import os

# 禁用代理
os.environ['no_proxy'] = 'localhost,127.0.0.1'

def test_simple_request():
    """测试简单的请求"""
    
    print("🚀 开始测试 Cline 与 Perplexity API 服务器的交互...")
    
    # 简单的测试数据
    test_data = {
        "model": "perplexity-reasoning",
        "messages": [
            {
                "role": "user",
                "content": "请打印数字 0"
            }
        ],
        "stream": False,
        "max_tokens": 100
    }
    
    print(f"📤 发送请求到服务器...")
    print(f"请求内容: {test_data['messages'][0]['content']}")
    
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
            
            print("✅ 请求成功!")
            print(f"模型: {result.get('model', 'unknown')}")
            print(f"响应ID: {result.get('id', 'unknown')}")
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"🤖 AI 回复: {content}")
            
            if 'usage' in result:
                usage = result['usage']
                print(f"📊 Token 使用情况:")
                print(f"  - 输入 tokens: {usage.get('prompt_tokens', 0)}")
                print(f"  - 输出 tokens: {usage.get('completion_tokens', 0)}")
                print(f"  - 总计 tokens: {usage.get('total_tokens', 0)}")
                
        else:
            print(f"❌ 请求失败!")
            print(f"错误响应: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时")
    except requests.exceptions.ConnectionError:
        print("🔌 连接错误 - 请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

def test_multimodal_request():
    """测试多模态请求（Cline 格式）"""
    
    print("\n" + "="*50)
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
        "max_tokens": 100
    }
    
    print(f"📤 发送多模态请求...")
    print(f"内容部分数量: {len(test_data['messages'][0]['content'])}")
    
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
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"🤖 AI 回复: {content}")
                
        else:
            print(f"❌ 多模态请求失败!")
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 发生错误: {e}")

def check_server_status():
    """检查服务器状态"""
    
    print("🔍 检查服务器状态...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器正在运行")
            server_info = response.json()
            print(f"服务器信息: {server_info.get('message', 'unknown')}")
            return True
        else:
            print(f"⚠️ 服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Cline 兼容性测试")
    print("="*50)
    
    # 检查服务器状态
    if check_server_status():
        # 测试简单请求
        test_simple_request()
        
        # 测试多模态请求
        test_multimodal_request()
        
        print("\n🎉 测试完成!")
    else:
        print("\n❌ 请先启动 Perplexity API 服务器")
        print("运行命令: python -m api_server.main")
