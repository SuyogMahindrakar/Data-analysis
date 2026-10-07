import streamlit as st
import pandas as pd

from dataframe_tools import load_dataframe, get_dataframe_info
from ai import generate_python_code, explain_result
from chart_tools import execute_python_code, format_result

# -------------------------
# Streamlit Configuration
# -------------------------

st.set_page_config(
    page_title="Excel AI Agent",
    layout="wide"
)

st.title("📊 Data Analysis AI Agent")
st.caption("Ask questions about your CSV or Excel file using AI.")

# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.header("Configuration")

    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"]
    )

# -------------------------
# Load Dataset
# -------------------------

if uploaded_file is not None:

    if st.session_state.df is None:

        df = load_dataframe(uploaded_file)

        st.session_state.df = df

        st.success("Dataset Loaded Successfully")

# -------------------------
# Dataset Preview
# -------------------------

if st.session_state.df is not None:

    df = st.session_state.df

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Missing Values", int(df.isna().sum().sum()))

# -------------------------
# Chat History
# -------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant":

            st.markdown(msg["text"])

            if msg.get("table") is not None:
                st.dataframe(msg["table"])

            if msg.get("chart") is not None:
                st.pyplot(msg["chart"])

        else:

            st.markdown(msg["text"])

# -------------------------
# User Question
# -------------------------

if st.session_state.df is not None:

    question = st.chat_input(
        "Ask anything about your data..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "text": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):
                dataset_info = get_dataframe_info(df)
                python_code = generate_python_code(
                    api_key,
                    dataset_info,
                    question
                    )
                execution = execute_python_code(
                    python_code,
                    df
                    )
                display = format_result(execution)
                explanation = explain_result(
                    api_key,
                    question,
                    execution["result"]
                    )
                st.markdown(explanation)
                if display["text"]:
                    st.write(display["text"])
                if display["table"] is not None:
                    st.dataframe(display["table"], use_container_width=True)
                if display["chart"] is not None:
                    st.pyplot(display["chart"])
                with st.expander("Generated Python"):
                    st.code(python_code, language="python")       
              
             


        st.session_state.messages.append(
            {
                "role": "assistant",
                "text": explanation,
                "table": display["table"],
                "chart": display["chart"]
            }
        )