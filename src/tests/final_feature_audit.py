from __future__ import annotations

import importlib
from pathlib import Path

from src.config.settings import (
    PROJECT_ROOT,
)


# ============================================================
# MODULES THAT SHOULD EXIST
# ============================================================

REQUIRED_MODULES = {

    "Configuration":
        "src.config",

    "Calculator":
        "src.calculator",

    "Unified Solver":
        "src.core.unified_solver",

    "LLM Router":
        "src.llm",

    "Provider Health":
        "src.llm.provider_health",

    "Planner Agent":
        "src.agents.planner",

    "Solver Agent":
        "src.agents.solver",

    "Reviewer Agent":
        "src.agents.reviewer",

    "Teacher Agent":
        "src.agents.teacher",

    "Agent Graph":
        "src.agents.agent_graph",

    "RAG Pipeline":
        "src.rag.pipeline",

    "Vector Database":
        "src.rag.vector_store",

    "Document Loader":
        "src.rag.document_loader",

    "RAG Chunking":
        "src.rag.chunking",

    "Vision Processing":
        "src.vision.image_processing",

    "Vision Preprocessing":
        "src.vision.preprocessing",

    "Vision Filters":
        "src.vision.filters",

    "Vision Edge Detection":
        "src.vision.edge_detection",

    "Vision Morphology":
        "src.vision.morphology",

    "Vision Contours":
        "src.vision.contours",

    "Vision Histogram":
        "src.vision.histogram",

    "Math OCR":
        "src.vision.math_ocr",

    "Vision Solver":
        "src.vision.vision_solver",

    "Analytics":
        "src.analytics.analytics_engine",
}


# ============================================================
# IMPORTANT FILES
# ============================================================

REQUIRED_FILES = [

    "app.py",

    ".env.example",

    ".gitignore",

    "requirements.txt",

    "README.md",

]


def check_modules():

    results = {}

    for name, module_name in (
        REQUIRED_MODULES.items()
    ):

        try:

            importlib.import_module(
                module_name
            )

            results[name] = True

        except Exception:

            results[name] = False

    return results


def check_files():

    results = {}

    for filename in REQUIRED_FILES:

        path = (
            Path(PROJECT_ROOT)
            / filename
        )

        results[filename] = (
            path.exists()
        )

    return results


def calculate_score(
    module_results,
    file_results,
):

    total = (
        len(module_results)
        + len(file_results)
    )

    passed = (
        sum(module_results.values())
        + sum(file_results.values())
    )

    if total == 0:

        return 0.0

    return round(
        (
            passed
            / total
        )
        * 100,
        2,
    )


def run_audit():

    print()
    print(
        "=============================================="
    )

    print(
        "        MathMind AI Final Feature Audit"
    )

    print(
        "=============================================="
    )

    print()

    module_results = (
        check_modules()
    )

    print(
        "MODULE AUDIT"
    )

    print(
        "----------------------------------------------"
    )

    for name, passed in (
        module_results.items()
    ):

        print(
            f"{'✅' if passed else '❌'} "
            f"{name}"
        )

    print()

    file_results = (
        check_files()
    )

    print(
        "PROJECT FILE AUDIT"
    )

    print(
        "----------------------------------------------"
    )

    for name, passed in (
        file_results.items()
    ):

        print(
            f"{'✅' if passed else '❌'} "
            f"{name}"
        )

    print()

    score = calculate_score(
        module_results,
        file_results,
    )

    print(
        "=============================================="
    )

    print(
        f"Feature Audit Score: {score}%"
    )

    print(
        "=============================================="
    )

    if score == 100:

        print(
            "🎉 All audited features are present."
        )

    else:

        print(
            "⚠️ Some audited items are missing."
        )

    print()

    return (
        module_results,
        file_results,
        score,
    )


if __name__ == "__main__":

    run_audit()