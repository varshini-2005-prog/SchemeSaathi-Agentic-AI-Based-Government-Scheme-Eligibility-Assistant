# Multi-stage Dockerfile for SchemeSaathi (FastAPI + React)

# ---------- Build React UI ----------
FROM node:20-alpine AS ui-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
# Build static assets
RUN npm run build

# ---------- Python runtime ----------
FROM python:3.11-slim AS python-base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Final image ----------
FROM python:3.11-slim
WORKDIR /app

# Copy Python packages and app code
COPY --from=python-base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-base /app /app
COPY . .

# Copy built React static files
COPY --from=ui-builder /frontend/dist ./frontend/dist

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI (it will serve the React build as static files)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
