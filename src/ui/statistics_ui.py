import streamlit as st

from src.calculator.statistics import *

def show():

    st.header("📊 Statistics & Data Analysis")

    data = st.text_area(
        "Enter Numbers (comma separated)",
        "10,20,30,40,50"
    )

    operation = st.selectbox(
        "Choose Operation",
        [
            "Mean",
            "Median",
            "Mode",
            "Variance",
            "Standard Deviation",
            "Minimum",
            "Maximum",
            "Range",
            "Quartiles",
            "Percentile",
            "IQR",
            "Z Score",
            "Normalize",
            "Standardize"
        ]
    )

    percentile_value = None

    if operation == "Percentile":
        percentile_value = st.number_input(
            "Percentile",
            min_value=0,
            max_value=100,
            value=50
        )

    if st.button("Calculate"):

        try:

            if operation == "Mean":
                result = mean(data)

            elif operation == "Median":
                result = median(data)

            elif operation == "Mode":
                result = mode(data)

            elif operation == "Variance":
                result = variance(data)

            elif operation == "Standard Deviation":
                result = standard_deviation(data)

            elif operation == "Minimum":
                result = minimum(data)

            elif operation == "Maximum":
                result = maximum(data)

            elif operation == "Range":
                result = data_range(data)

            elif operation == "Quartiles":
                result = quartiles(data)

            elif operation == "Percentile":
                result = percentile(data, percentile_value)

            elif operation == "IQR":
                result = iqr(data)

            elif operation == "Z Score":
                result = z_score(data)

            elif operation == "Normalize":
                result = normalize(data)

            elif operation == "Standardize":
                result = standardize(data)

            st.success(result)

            st.subheader("Dataset")

            st.dataframe(dataframe(data))

        except Exception as e:
            st.error(e)