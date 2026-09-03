from src.llm.router import LLMRouter


def main():

    print("\n" + "=" * 60)
    print("MathMind-AI LLM Router Test")
    print("=" * 60)

    router = LLMRouter()

    print("\nSupported Providers:")

    for provider in (
        router.get_available_providers()
    ):
        print(f"  ✅ {provider}")

    print("\nTesting invalid provider...")

    try:

        router.ask(
            "InvalidProvider",
            "Hello",
        )

    except Exception as error:

        print(
            f"  ✅ Error handled correctly:"
        )

        print(
            f"  {error}"
        )

    print("\nTesting empty prompt...")

    try:

        router.ask(
            "Gemini",
            "",
        )

    except Exception as error:

        print(
            f"  ✅ Error handled correctly:"
        )

        print(
            f"  {error}"
        )

    print("\nTesting provider configuration...")

    for provider in router.get_available_providers():

        try:

            router.ask(
                provider,
                "Hello",
            )

        except Exception as error:

            print(
                f"  ℹ️ {provider}: "
                f"{error}"
            )

    print("\n" + "=" * 60)
    print("LLM Router Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()