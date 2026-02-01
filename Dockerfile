# Maestro AI Dockerfile
# Multi-stage build for production-ready image

FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY data/ ./data/
COPY pyproject.toml pytest.ini ./

# Create output directory
RUN mkdir -p /app/output

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Set Python path
ENV PYTHONPATH=/app

# Environment variables (can be overridden)
ENV MAESTRO_LLM_BASE_URL=http://host.docker.internal:11434
ENV MAESTRO_LLM_MODEL=mistral-nemo:12b
ENV MAESTRO_API_PORT=8000
ENV MAESTRO_DEBUG=false

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:${MAESTRO_API_PORT}/health')" || exit 1

# Expose port
EXPOSE ${MAESTRO_API_PORT}

# Run application (adjust based on your entry point)
CMD ["python", "-m", "src.adapters.input.api.app"]
