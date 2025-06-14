#!/usr/bin/env python3
"""
调试 Cline 响应格式的脚本
"""
import requests
import json
import os

# 禁用代理
os.environ['no_proxy'] = 'localhost,127.0.0.1'

def test_response_format():
    """测试响应格式是否符合 OpenAI 标准"""
    
    print("🔍 调试 Cline 响应格式...")
    
    # 简单的测试请求
    test_data = {
        "model": "perplexity-reasoning",
        "messages": [
            {
                "role": "user",
                "content": "0"  # 最简单的请求
            }
        ],
        "stream": False,
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 HTTP 状态码: {response.status_code}")
        print(f"📋 响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            # 获取原始响应文本
            raw_text = response.text
            print(f"📄 原始响应文本长度: {len(raw_text)} 字符")
            
            try:
                # 尝试解析 JSON
                result = response.json()
                print("✅ JSON 解析成功")
                
                # 检查必需的字段
                required_fields = ['id', 'object', 'created', 'model', 'choices']
                missing_fields = [field for field in required_fields if field not in result]
                
                if missing_fields:
                    print(f"⚠️ 缺少必需字段: {missing_fields}")
                else:
                    print("✅ 所有必需字段都存在")
                
                # 详细检查响应结构
                print("\n📊 响应结构分析:")
                print(f"  - ID: {result.get('id', 'MISSING')}")
                print(f"  - Object: {result.get('object', 'MISSING')}")
                print(f"  - Model: {result.get('model', 'MISSING')}")
                print(f"  - Created: {result.get('created', 'MISSING')}")
                
                if 'choices' in result:
                    choices = result['choices']
                    print(f"  - Choices 数量: {len(choices)}")
                    
                    if len(choices) > 0:
                        choice = choices[0]
                        print(f"    - Choice 0 index: {choice.get('index', 'MISSING')}")
                        print(f"    - Choice 0 finish_reason: {choice.get('finish_reason', 'MISSING')}")
                        
                        if 'message' in choice:
                            message = choice['message']
                            print(f"    - Message role: {message.get('role', 'MISSING')}")
                            print(f"    - Message content: {repr(message.get('content', 'MISSING'))}")
                        else:
                            print("    - ❌ Message 字段缺失")
                else:
                    print("  - ❌ Choices 字段缺失")
                
                if 'usage' in result:
                    usage = result['usage']
                    print(f"  - Usage: {usage}")
                else:
                    print("  - ⚠️ Usage 字段缺失")
                
                # 生成标准格式的响应示例
                print("\n📝 标准 OpenAI 格式示例:")
                standard_response = {
                    "id": "chatcmpl-123",
                    "object": "chat.completion",
                    "created": 1677652288,
                    "model": "gpt-3.5-turbo",
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "0"
                        },
                        "finish_reason": "stop"
                    }],
                    "usage": {
                        "prompt_tokens": 1,
                        "completion_tokens": 1,
                        "total_tokens": 2
                    }
                }
                print(json.dumps(standard_response, indent=2, ensure_ascii=False))
                
                # 比较我们的响应与标准格式
                print("\n🔍 格式兼容性检查:")
                
                # 检查 object 字段
                if result.get('object') == 'chat.completion':
                    print("✅ object 字段正确")
                else:
                    print(f"❌ object 字段错误: {result.get('object')}")
                
                # 检查 choices 结构
                if 'choices' in result and len(result['choices']) > 0:
                    choice = result['choices'][0]
                    if 'message' in choice and 'role' in choice['message'] and 'content' in choice['message']:
                        print("✅ choices 结构正确")
                    else:
                        print("❌ choices 结构错误")
                else:
                    print("❌ choices 为空或缺失")
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析失败: {e}")
                print(f"原始响应: {raw_text[:500]}...")
                
        else:
            print(f"❌ HTTP 错误: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

def test_streaming_response():
    """测试流式响应格式"""
    
    print("\n" + "="*50)
    print("🌊 测试流式响应格式...")
    
    test_data = {
        "model": "perplexity-reasoning",
        "messages": [
            {
                "role": "user",
                "content": "0"
            }
        ],
        "stream": True,
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=test_data,
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=30
        )
        
        print(f"📥 流式响应状态码: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            print("📡 接收流式数据...")
            chunk_count = 0
            
            for line in response.iter_lines():
                if line:
                    chunk_count += 1
                    line_str = line.decode('utf-8')
                    print(f"  Chunk {chunk_count}: {line_str[:100]}...")
                    
                    if chunk_count >= 5:  # 只显示前5个chunk
                        print("  ... (更多数据)")
                        break
            
            print(f"✅ 流式响应正常，共接收 {chunk_count} 个数据块")
        else:
            print(f"❌ 流式响应失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 流式请求失败: {e}")

if __name__ == "__main__":
    print("🐛 Cline 响应格式调试工具")
    print("="*50)
    
    test_response_format()
    test_streaming_response()
    
    print("\n💡 如果 Cline 显示 [object Object]，可能的原因:")
    print("1. Cline 的 JavaScript 代码没有正确处理 JSON 响应")
    print("2. 响应的 Content-Type 不正确")
    print("3. 响应格式与 OpenAI API 不完全兼容")
    print("4. Cline 期望特定的字段或格式")
    
    print("\n🔧 建议的解决方案:")
    print("1. 检查 Cline 的网络请求日志")
    print("2. 确认 Content-Type 为 application/json")
    print("3. 验证响应格式完全符合 OpenAI API 规范")
    print("4. 检查是否有额外的响应头或字段要求")
