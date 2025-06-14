#!/usr/bin/env python3.8
"""
Debug script to test sync client directly
"""
import sys
sys.path.append('.')

from api_server.perplexity_adapter import PerplexityAdapter
from api_server.models import ChatCompletionRequest, ChatMessage

# Create a test request
request = ChatCompletionRequest(
    model="perplexity-auto",
    messages=[ChatMessage(role="user", content="Hello, what is 2+2?")]
)

print("Testing PerplexityAdapter with sync client...")

# Create adapter
adapter = PerplexityAdapter()

try:
    # Test sync completion
    print("Calling sync completion...")
    response = adapter.complete_sync(request)
    print(f"Success! Response: {response}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
