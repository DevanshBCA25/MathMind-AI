from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Dict, Optional


# ============================================================
# LOG DIRECTORY
# ============================================================

LOG_DIR = Path("logs")

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


LOG_FILE = LOG_DIR / "mathmind.log"


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger(
    "MathMindAI"
)

logger.setLevel(
    logging.INFO
)


if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )


# ============================================================
# ERROR CLASSIFICATION
# ============================================================

def classify_error(
    error: Exception,
) -> str:
    """
    Classify application errors.
    """

    message = str(error).lower()

    api_keywords = [
        "api key",
        "api_key",
        "authentication",
        "unauthorized",
        "invalid api",
        "quota",
        "rate limit",
        "permission denied",
        "401",
        "403",
        "429",
    ]

    connection_keywords = [
        "connection",
        "connect",
        "timeout",
        "timed out",
        "network",
        "ollama",
    ]

    import_keywords = [
        "importerror",
        "modulenotfounderror",
        "cannot import",
        "no module named",
    ]

    file_keywords = [
        "filenotfound",
        "no such file",
        "index.faiss",
        "vector database",
    ]

    if any(
        keyword in message
        for keyword in api_keywords
    ):
        return "API_ERROR"

    if any(
        keyword in message
        for keyword in connection_keywords
    ):
        return "CONNECTION_ERROR"

    if any(
        keyword in message
        for keyword in import_keywords
    ):
        return "IMPORT_ERROR"

    if any(
        keyword in message
        for keyword in file_keywords
    ):
        return "FILE_ERROR"

    return "APPLICATION_ERROR"


# ============================================================
# SAFE ERROR MESSAGE
# ============================================================

def user_friendly_error(
    error: Exception,
) -> str:
    """
    Convert technical exceptions into
    user-friendly messages.
    """

    error_type = classify_error(
        error
    )

    if error_type == "API_ERROR":

        return (
            "AI provider/API is unavailable. "
            "Please check the API key, quota, "
            "or provider configuration."
        )

    if error_type == "CONNECTION_ERROR":

        return (
            "Connection to the selected service "
            "failed. Please check whether the "
            "service is running."
        )

    if error_type == "IMPORT_ERROR":

        return (
            "A required project module or "
            "dependency could not be loaded."
        )

    if error_type == "FILE_ERROR":

        return (
            "A required project file or vector "
            "database could not be found."
        )

    return (
        "The operation could not be completed. "
        "Please check the application logs."
    )


# ============================================================
# LOG ERROR
# ============================================================

def log_exception(
    error: Exception,
    context: Optional[str] = None,
) -> None:
    """
    Log an exception with optional context.
    """

    if context:

        logger.error(
            "%s | %s",
            context,
            str(error),
            exc_info=True,
        )

    else:

        logger.error(
            "%s",
            str(error),
            exc_info=True,
        )


# ============================================================
# LOG INFO
# ============================================================

def log_info(
    message: str,
) -> None:

    logger.info(
        message
    )


# ============================================================
# LOG WARNING
# ============================================================

def log_warning(
    message: str,
) -> None:

    logger.warning(
        message
    )


# ============================================================
# SAFE EXECUTION
# ============================================================

def safe_execute(
    function: Callable,
    *args: Any,
    context: Optional[str] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Execute a function safely.

    Returns a standard response dictionary.
    """

    try:

        result = function(
            *args,
            **kwargs,
        )

        return {
            "status": "SUCCESS",
            "result": result,
        }

    except Exception as error:

        log_exception(
            error,
            context=context,
        )

        return {
            "status": classify_error(
                error
            ),
            "result": None,
            "error": user_friendly_error(
                error
            ),
            "technical_error": str(
                error
            ),
        }


# ============================================================
# STANDARD RESPONSE
# ============================================================

def success_response(
    result: Any = None,
    message: str = "Operation completed successfully.",
) -> Dict[str, Any]:

    return {
        "status": "SUCCESS",
        "message": message,
        "result": result,
    }


def error_response(
    error: Exception,
    context: Optional[str] = None,
) -> Dict[str, Any]:

    log_exception(
        error,
        context=context,
    )

    return {
        "status": classify_error(
            error
        ),
        "message": user_friendly_error(
            error
        ),
        "technical_error": str(
            error
        ),
    }