import streamlit as st

from src.utils.history import (
    latest_records,
    clear_history,
)


def show():

    st.header("📜 History")

    records = latest_records()

    if len(records) == 0:
        st.info("No history found.")
        return

    for record in reversed(records):

        st.json(record)

    if st.button("Clear History"):

        clear_history()

        st.success("History Cleared")