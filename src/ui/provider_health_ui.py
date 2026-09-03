import streamlit as st

from src.llm.provider_health import (
    SUPPORTED_PROVIDERS,
    check_provider_configuration,
    check_all_providers,
)


def show():

    st.title(
        "🩺 LLM Provider Health Check"
    )

    st.caption(
        "Check provider configuration and "
        "model availability."
    )

    st.info(
        "🔐 API keys are never displayed."
    )

    st.divider()

    # ========================================================
    # ALL PROVIDERS
    # ========================================================

    st.subheader(
        "🤖 Provider Configuration"
    )

    results = check_all_providers()

    for provider in SUPPORTED_PROVIDERS:

        result = results.get(
            provider,
            {},
        )

        status = result.get(
            "status",
            "UNKNOWN",
        )

        model = result.get(
            "model",
            "N/A",
        )

        if status == "CONFIGURED":

            icon = "🟢"

        elif status == "MISSING_API_KEY":

            icon = "🟡"

        elif status == "UNSUPPORTED":

            icon = "🔴"

        else:

            icon = "⚪"

        with st.expander(
            f"{icon} {provider}",
            expanded=True,
        ):

            col1, col2, col3 = (
                st.columns(3)
            )

            with col1:

                st.metric(
                    "Status",
                    status,
                )

            with col2:

                st.metric(
                    "Model",
                    model,
                )

            with col3:

                configured = result.get(
                    "configured",
                    False,
                )

                st.metric(
                    "Configured",
                    "YES"
                    if configured
                    else "NO",
                )

            st.write(
                result.get(
                    "message",
                    "",
                )
            )

            if provider == "Ollama":

                st.caption(
                    "Ollama does not require an API key."
                )

                if result.get(
                    "base_url"
                ):

                    st.code(
                        result[
                            "base_url"
                        ]
                    )

    st.divider()

    # ========================================================
    # SINGLE PROVIDER CHECK
    # ========================================================

    st.subheader(
        "🔍 Check Individual Provider"
    )

    selected_provider = st.selectbox(
        "Select Provider",
        SUPPORTED_PROVIDERS,
    )

    if st.button(
        "🔄 Check Provider",
        use_container_width=True,
    ):

        result = (
            check_provider_configuration(
                selected_provider
            )
        )

        status = result.get(
            "status",
            "UNKNOWN",
        )

        if status == "CONFIGURED":

            st.success(
                f"✅ {selected_provider} "
                "is configured."
            )

        elif status == "MISSING_API_KEY":

            st.warning(
                f"⚠️ {selected_provider} "
                "API key is missing."
            )

        else:

            st.error(
                result.get(
                    "message",
                    "Provider check failed.",
                )
            )

        st.json(
            result
        )

    st.divider()

    # ========================================================
    # REFRESH
    # ========================================================

    if st.button(
        "🔄 Refresh All Providers",
        use_container_width=True,
    ):

        st.rerun()