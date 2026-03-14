import os
from openai import AsyncOpenAI
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

class EnterpriseLLMClient:
    """
    Standardized client routing traffic through the internal LiteLLM proxy.
    Automatically instruments OpenTelemetry traces for every agent call.
    """
    def __init__(self):
        # Point the OpenAI SDK to our internal LiteLLM service, not public OpenAI
        self.base_url = os.getenv("LITELLM_BASE_URL", "http://litellm-service.ai-platform.svc.cluster.local:4000")
        
        # In a real enterprise setup, this would fetch a short-lived internal JWT
        self.api_key = os.getenv("INTERNAL_API_KEY", "sk-enterprise-local-dev")
        
        self.client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        # Auto-instrument the client to capture token costs and latency [cite: 209-210]
        OpenAIInstrumentor().instrument_clients(clients=[self.client])

    async def generate_response(self, model_routing: str, messages: list, **kwargs):
        """
        model_routing options: 'claude-3-haiku' or 'claude-3-sonnet'
        """
        response = await self.client.chat.completions.create(
            model=model_routing,
            messages=messages,
            **kwargs
        )
        return response