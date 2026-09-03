# Stage 1: build the React demonstration UI.
FROM node:20-alpine AS ui
WORKDIR /ui
COPY src/frontend/package.json src/frontend/package-lock.json* src/frontend/.npmrc ./
RUN npm install --no-audit --no-fund
COPY src/frontend/ ./
RUN npm run build

# Stage 2: Python runtime serving both the API and the built UI.
FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

COPY src/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src/backend/app ./app
COPY data ./data

COPY --from=ui /ui/dist ./app/static

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
