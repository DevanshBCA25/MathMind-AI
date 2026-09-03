from fastapi import FastAPI

from src.api.routes import router


app = FastAPI(
    title="MathMind AI API",
    description=(
        "API layer for the MathMind AI "
        "mathematical reasoning platform."
    ),
    version="1.0.0",
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(
    router,
    prefix="/api",
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "application": "MathMind AI",
        "status": "running",
        "version": "1.0.0",
        "message": "MathMind AI API is running successfully.",
    }