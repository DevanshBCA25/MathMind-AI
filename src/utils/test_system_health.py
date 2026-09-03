from src.utils.system_health import (
    SystemHealth,
)


def main():

    print()
    print("==============================")
    print("MathMind-AI System Health")
    print("==============================")

    health = SystemHealth()

    report = health.run()

    # --------------------------------------------------
    # Documents
    # --------------------------------------------------

    documents = report["documents"]

    print()
    print("📚 Documents")
    print(
        "Status:",
        documents["status"],
    )

    print(
        "Count:",
        documents["count"],
    )

    # --------------------------------------------------
    # Vector Database
    # --------------------------------------------------

    vector_db = (
        report["vector_database"]
    )

    print()
    print("🗄️ Vector Database")
    print(
        "Status:",
        vector_db["status"],
    )

    print(
        "FAISS index:",
        vector_db["index_exists"],
    )

    print(
        "Metadata:",
        vector_db["metadata_exists"],
    )

    # --------------------------------------------------
    # Environment
    # --------------------------------------------------

    environment = (
        report["environment"]
    )

    print()
    print("🔑 Provider Configuration")

    for provider, configured in (
        environment["providers"].items()
    ):

        status = (
            "CONFIGURED"
            if configured
            else "NOT CONFIGURED"
        )

        print(
            f"{provider}: {status}"
        )

    print()
    print("==============================")
    print("✅ System Health Check Complete")
    print("==============================")


if __name__ == "__main__":
    main()