FROM python:3.11-slim

# ==========================================================
# ENVIRONMENT
# ==========================================================

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV PIP_NO_CACHE_DIR=1

# ==========================================================
# WORKING DIRECTORY
# ==========================================================

WORKDIR /app

# ==========================================================
# SYSTEM DEPENDENCIES
# ==========================================================

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ==========================================================
# PYTHON DEPENDENCIES
# ==========================================================

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ==========================================================
# PROJECT FILES
# ==========================================================

COPY . .

# ==========================================================
# STREAMLIT
# ==========================================================

EXPOSE 8501

# ==========================================================
# START APPLICATION
# ==========================================================

CMD [
    "streamlit",
    "run",
    "app.py",
    "--server.address=0.0.0.0",
    "--server.port=8501",
    "--server.headless=true"
]