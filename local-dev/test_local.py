import sys
import os
import asyncio
import traceback

# --- Force Local Environment Variables for Testing ---
os.environ["LITELLM_BASE_URL"] = "http://localhost:4000/v1"
os.environ["INTERNAL_API_KEY"] = "sk-enterprise-local-dev"

# Dynamically add the SDK path to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sdk_path = os.path.join(current_dir, '..', 'shared_sdk', 'python')
sys.path.append(os.path.abspath(sdk_path))

from platform_sdk.llm_client import EnterpriseLLMClient

async def main():
    print("Initializing Enterprise SDK (LiteLLM Proxy Mode)...")
    client = EnterpriseLLMClient()
    
    print("Sending request via local LiteLLM Proxy -> Local Ollama...")
    try:
        response = await client.generate_response(
            model_routing="fast-routing",
            messages=[{"role": "user", "content": "Explain Agentic AI in one short sentence."}]
        )
        print("\n✅ Success! Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("\n❌ Failed to connect. Detailed Stacktrace:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())