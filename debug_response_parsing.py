#!/usr/bin/env python3.8
"""
Debug script to test response parsing
"""
import json

# Sample response data from the log
sample_response = '''{"answer": "我背后使用的是Perplexity AI的人工智能大模型。Perplexity AI是一家专注于自然语言处理和信息检索的公司，其模型以大规模语言模型（LLM）为核心，结合了最新的机器学习和深度学习技术，能够理解和生成自然语言文本。该模型经过大量数据训练，具备强大的问答、推理和信息整合能力，能够为用户提供高质量的答案和建议。", "web_results": [], "chunks": ["我背后使用的是Perplexity AI", "的人工智能大模型。Perplexity AI", "是一家专注于自然语言处理和信息检索的公司，其模型以", "大规模语言模型（LLM）为核心，结合了最新的机器学习", "和深度学习技术，能够理解和生成自然语言文本。该模型", "经过大量数据训练，具备强大的问答、推理和信息整合能力", "，能够为用户提供高质量的答案和建议。"], "extra_web_results": [], "structured_answer": []}'''

try:
    parsed = json.loads(sample_response)
    print("Successfully parsed JSON:")
    print(f"Answer: {parsed['answer']}")
    print(f"Chunks: {len(parsed['chunks'])} chunks")
    
    # Test our extraction logic
    if 'answer' in parsed:
        content = parsed['answer']
        print(f"Extracted content: {content}")
    elif 'text' in parsed:
        content = parsed['text']
        print(f"Extracted from text: {content}")
    else:
        print("No answer or text field found")
        print(f"Available keys: {list(parsed.keys())}")
        
except Exception as e:
    print(f"Error parsing JSON: {e}")
