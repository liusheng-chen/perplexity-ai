#!/bin/bash
# Curl 测试命令，用于验证 API 服务器

echo "🧪 使用 curl 测试 Perplexity API 服务器"
echo "================================================"

# 设置服务器地址
SERVER_URL="http://localhost:8000"

echo "1️⃣ 测试服务器状态..."
curl -s "$SERVER_URL/" | jq '.' 2>/dev/null || curl -s "$SERVER_URL/"

echo -e "\n2️⃣ 测试简单聊天请求..."
curl -s -X POST "$SERVER_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "perplexity-reasoning",
    "messages": [
      {
        "role": "user",
        "content": "请打印数字 0"
      }
    ],
    "stream": false,
    "max_tokens": 50
  }' | jq '.' 2>/dev/null || echo "JSON 解析失败，显示原始响应:"

echo -e "\n3️⃣ 测试多模态请求（Cline 格式）..."
curl -s -X POST "$SERVER_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "perplexity-reasoning",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "请执行任务："
          },
          {
            "type": "text",
            "text": "打印数字 0"
          }
        ]
      }
    ],
    "stream": false,
    "max_tokens": 50
  }' | jq '.' 2>/dev/null || echo "JSON 解析失败，显示原始响应:"

echo -e "\n4️⃣ 测试模型列表..."
curl -s "$SERVER_URL/v1/models" | jq '.' 2>/dev/null || curl -s "$SERVER_URL/v1/models"

echo -e "\n✅ curl 测试完成！"
echo "如果以上测试都正常，说明服务器工作正常，问题在 Cline 客户端。"
