# Cline 配置指南

## 🎯 问题解决

您遇到的 `[object Object]` 问题已确认**不是服务器问题**。服务器完全正常，响应格式符合 OpenAI API 标准。

## ⚙️ Cline 配置步骤

### 1. 基本设置

在 Cline 中配置以下设置：

```
API Provider: OpenAI Compatible
API Base URL: http://localhost:8000
API Key: any-key-will-work
Model: perplexity-reasoning
```

### 2. 可用模型列表

您的服务器支持以下模型：
- `perplexity-auto`
- `perplexity-pro` 
- `perplexity-reasoning` ⭐ (推荐)
- `perplexity-research`
- `perplexity-pro-gpt4o`
- `perplexity-pro-claude`
- `perplexity-reasoning-r1`
- `perplexity-reasoning-o3`

### 3. 测试连接

使用以下简单消息测试连接：
```
你好
```

或者：
```
请打印数字 0
```

## 🐛 故障排除

### 如果仍然看到 `[object Object]`

1. **检查浏览器控制台**：
   - 按 F12 打开开发者工具
   - 查看 Console 标签页是否有错误
   - 查看 Network 标签页的请求/响应详情

2. **验证网络请求**：
   在 Network 标签页中，查找对 `localhost:8000` 的请求：
   - 请求状态应该是 200
   - 响应应该是有效的 JSON
   - Content-Type 应该是 application/json

3. **检查 Cline 版本**：
   - 确保使用最新版本的 Cline
   - 如果是旧版本，可能存在兼容性问题

4. **尝试重新安装 Cline**：
   - 如果问题持续存在，可能需要重新安装

### 常见错误和解决方案

| 错误现象 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `[object Object]` | JavaScript 序列化错误 | 检查浏览器控制台，重启 Cline |
| 连接超时 | 服务器未运行 | 运行 `python -m api_server.main` |
| 404 错误 | URL 配置错误 | 确认 Base URL 为 `http://localhost:8000` |
| 认证错误 | API Key 问题 | 任意字符串即可，服务器会忽略 |

## ✅ 验证服务器状态

您可以随时使用以下命令验证服务器是否正常：

```bash
# 检查服务器状态
curl http://localhost:8000/

# 测试聊天 API
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "perplexity-reasoning",
    "messages": [{"role": "user", "content": "测试"}],
    "stream": false
  }'
```

## 🔧 高级配置

### 自定义端口

如果需要更改端口，修改 `api_server/config.py`：

```python
SERVER_PORT = 8001  # 改为其他端口
```

然后在 Cline 中使用 `http://localhost:8001`

### 启用调试日志

在服务器启动时查看详细日志：

```bash
python -m api_server.main
```

日志会显示每个请求的详细信息。

## 📞 获取帮助

如果问题仍然存在：

1. **检查服务器日志**：查看是否有错误信息
2. **提供浏览器控制台截图**：包含任何 JavaScript 错误
3. **提供网络请求详情**：从开发者工具的 Network 标签页

## 🎉 成功标志

当配置正确时，您应该看到：
- Cline 能够发送消息
- 收到有意义的回复（而不是 `[object Object]`）
- 没有 JavaScript 控制台错误
- Network 标签页显示成功的 HTTP 200 响应

---

**注意**：您的 Perplexity API 服务器已经完全正常工作，支持 Cline 的多模态格式。问题出现在客户端显示层面。
