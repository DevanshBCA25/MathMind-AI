FROM python:3.11-slim

# ==========================================================
# ENVIRONMENT
# ==========================================================

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV PIP_NO_CACHE_DIR=1

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
# NON-ROOT USER (required by Hugging Face Spaces)
# ==========================================================

RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# ==========================================================
# PYTHON DEPENDENCIES
# CPU-only PyTorch keeps the image several GB smaller.
# ==========================================================

COPY --chown=user requirements.txt .

RUN pip install --user --upgrade pip \
    && pip install --user \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        -r requirements.txt

# ==========================================================
# PROJECT FILES
# ==========================================================

COPY --chown=user . .

# ==========================================================
# START APPLICATION (NiceGUI)
# ==========================================================

ENV PORT=7860

EXPOSE 7860

CMD ["python", "main.py"]
