from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

import os
resource = Resource(attributes={"service.name": os.environ.get("MICROSENSE_SERVICE_NAME",default="Microsense")}) 


tracer = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer)

# Use the OTLPSpanExporter to send traces to Tempo
tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint= os.environ.get("MICROSENSE_SERVICE_NAME",default="http://tempo:4317"))))

def init_tracer(app:FastAPI):
    LoggingInstrumentor().instrument()
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)