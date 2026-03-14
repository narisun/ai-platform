import os
from openai import AsyncOpenAI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

class EnterpriseLLMClient:
    def __init__(self):
        self.base_url = os.getenv("LITELLM_BASE_URL", "http://localhost:4000/v1")
        self.api_key = os.getenv("INTERNAL_API_KEY", "sk-enterprise-local-dev")
        
        self.client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        self._initialize_telemetry()

    def _initialize_telemetry(self):
        """Sets up OpenTelemetry to export traces to the local OTel Collector."""
        # Only initialize if a provider hasn't been set yet
        if not isinstance(trace.get_tracer_provider(), TracerProvider):
            # 1. Define the service name that will show up in Dynatrace
            resource = Resource(attributes={"service.name": "ai-platform-local-agent"})
            provider = TracerProvider(resource=resource)
            
            # 2. Point the exporter to our local Docker OTel Collector
            otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
            processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otel_endpoint))
            provider.add_span_processor(processor)
            
            trace.set_tracer_provider(provider)

        # 3. Instrument the OpenAI client
        instrumentor = OpenAIInstrumentor()
        if not instrumentor.is_instrumented_by_opentelemetry:
            instrumentor.instrument()

    async def generate_response(self, model_routing: str, messages: list, **kwargs):
        return await self.client.chat.completions.create(
            model=model_routing,
            messages=messages,
            **kwargs
        )