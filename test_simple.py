#!/usr/bin/env python3.8
import perplexity

# Test without cookies (will use free tier)
perplexity_cli = perplexity.Client()

try:
    # Simple test query
    resp = perplexity_cli.search('What is 2+2?', mode='auto', stream=False)
    print("Response type:", type(resp))
    print("Response content:", resp)
    
    if isinstance(resp, dict):
        print("Response keys:", list(resp.keys()))
        if 'text' in resp:
            print("Text content:", resp['text'])
    
except Exception as e:
    print("Error:", e)
    print("Error type:", type(e))
