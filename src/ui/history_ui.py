import pandas as pd
import streamlit as st

from src.ui.common import page_header

from src.utils.history import (
    latest_records,
    clear_history,
)


def show():

    page_header(
        "📜",
        "My History",
        "Your recent work in this session",
    )

    records = latest_records(limit=50)

    if len(records) == 0:
        st.info(
            "No history yet. Use any calculator or the AI pages "
            "and your work will show up here."
        )
        return

    table = pd.DataFrame(list(reversed(records)))

    st.dataframe(
        table,
        width="stretch",
        hide_index=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "⬇ Download as CSV",
            data=table.to_csv(index=False),
            file_name="mathmind_history.csv",
            mime="text/csv",
            width="stretch",
        )

    with col2:

        if st.button("🗑 Clear History", width="stretch"):

            clear_history()

            st.rerun()
