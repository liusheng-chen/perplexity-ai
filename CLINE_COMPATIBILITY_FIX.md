# Cline 兼容性修复

## 问题描述

在使用 Cline 测试 Perplexity API 服务器时，遇到了以下验证错误：

```
Validation error: [{'type': 'string_type', 'loc': ('body', 'messages', 1, 'content'), 'msg': 'Input should be a valid string', 'input': [{'type': 'text', 'text': '...'}, {'type': 'text', 'text': '...'}]}]
```

## 根本原因

Cline 使用 OpenAI 的新多模态消息格式，其中 `content` 字段可以是一个包含多个内容部分的数组：

```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "<task>\n测试\n</task>"},
    {"type": "text", "text": "<environment_details>\n# VSCode Visible Files\ntest.py\n</environment_details>"}
  ]
}
```

而我们的 API 服务器只支持简单的字符串格式：

```json
{
  "role": "user", 
  "content": "简单的字符串内容"
}
```

## 解决方案

修改了 `api_server/models.py` 中的 `ChatMessage` 模型，添加了对多模态内容的支持：

### 1. 更新类型定义

```python
class TextContent(BaseModel):
    """Text content part for multimodal messages"""
    type: Literal["text"] = Field(..., description="Content type")
    text: str = Field(..., description="Text content")

class ChatMessage(BaseModel):
    """Chat message model - supports both string and multimodal content"""
    role: Literal["system", "user", "assistant"] = Field(..., description="Role of the message sender")
    content: Union[str, List[TextContent]] = Field(..., description="Content of the message")
```

### 2. 添加内容转换验证器

```python
@field_validator('content', mode='before')
@classmethod
def normalize_content(cls, v):
    """Convert multimodal content to simple string if needed"""
    if isinstance(v, list):
        # Extract text from multimodal content
        text_parts = []
        for item in v:
            if isinstance(item, dict) and item.get('type') == 'text':
                text_parts.append(item.get('text', ''))
            elif isinstance(item, TextContent):
                text_parts.append(item.text)
        return '\n'.join(text_parts)
    return v
```

### 3. 使用 Pydantic v2 语法

将 `@validator` 更新为 `@field_validator`，以兼容 Pydantic v2。

## 功能特性

修复后的服务器现在支持：

1. **向后兼容**：仍然支持原有的简单字符串格式
2. **多模态支持**：支持 Cline 使用的多模态内容格式
3. **内容合并**：将多个文本部分合并为单个字符串，用换行符分隔
4. **类型过滤**：只处理 `type: "text"` 的内容，忽略其他类型（如图片）

## 测试结果

创建了测试脚本验证修复效果：

### 基本兼容性测试 (`test_cline_format.py`)
- ✅ Cline 多模态格式：成功处理
- ✅ 简单字符串格式：仍然正常工作

### 内容转换测试 (`test_content_conversion.py`)
- ✅ 多文本部分合并：正确将多个文本部分合并为单个字符串
- ✅ 混合内容类型：正确忽略非文本内容，只处理文本部分

## 示例

### Cline 发送的请求格式
```json
{
  "model": "perplexity-reasoning",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "<task>\n测试\n</task>"},
        {"type": "text", "text": "<environment_details>\n# VSCode Visible Files\ntest.py\n</environment_details>"}
      ]
    }
  ]
}
```

### 服务器内部处理后的内容
```
<task>
测试
</task>
<environment_details>
# VSCode Visible Files
test.py
</environment_details>
```

## 部署说明

修复已应用到生产环境，无需额外配置。服务器会自动检测并处理两种格式的消息内容。

## 相关文件

- `api_server/models.py` - 主要修改文件
- `test_cline_format.py` - 基本兼容性测试
- `test_content_conversion.py` - 内容转换测试
- `CLINE_COMPATIBILITY_FIX.md` - 本文档
