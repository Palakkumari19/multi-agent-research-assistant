import streamlit as st
import time

from graph.workflow import app

from memory.mongo_store import (
    save_research,
    get_recent_research,
    delete_research
)

from utils.pdf_generator import create_pdf

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# CLEAN MINIMAL UI
# ==========================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }

    .stTextArea textarea {

        background-color: #161B22 !important;

        color: white !important;

        border: 1px solid #2A2F3A !important;

        border-radius: 10px !important;

        font-size: 16px !important;
    }

    .stButton button {

        background-color: #1F2937 !important;

        color: white !important;

        border: 1px solid #374151 !important;

        border-radius: 8px !important;

        padding: 0.5rem 1rem !important;

        font-weight: 500 !important;
    }

    .stButton button:hover {

        background-color: #273244 !important;
    }

    .stDownloadButton button {

        background-color: #1F2937 !important;

        color: white !important;

        border: 1px solid #374151 !important;

        border-radius: 8px !important;
    }

    hr {
        border-color: #1F2937;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# TITLE
# ==========================================

st.title("Multi-Agent Research Assistant")

st.caption(
    "AI-powered autonomous research workflow using LangGraph, Groq, Tavily and MongoDB."
)

st.divider()

# ==========================================
# SESSION STATE
# ==========================================

default_states = {

    "active_chat": None,

    "chat_query": "",

    "chat_report": "",

    "chat_subquestions": [],

    "chat_results": [],

    "chat_critique": ""

}

for key, value in default_states.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Research History")

# NEW CHAT

if st.sidebar.button("New Chat"):

    for key, value in default_states.items():

        st.session_state[key] = value

    st.rerun()

# LOAD HISTORY

try:

    recent = get_recent_research()

    for item in recent:

        query_title = item["query"]

        research_id = str(item["_id"])

        col1, col2 = st.sidebar.columns([4, 1])

        # VIEW CHAT

        if col1.button(
            query_title,
            key=f"view_{research_id}"
        ):

            st.session_state.active_chat = research_id

            st.session_state.chat_query = item.get(
                "query",
                ""
            )

            st.session_state.chat_report = item.get(
                "report",
                ""
            )

            st.session_state.chat_subquestions = item.get(
                "subquestions",
                []
            )

            st.session_state.chat_results = item.get(
                "search_results",
                []
            )

            st.session_state.chat_critique = item.get(
                "critique",
                ""
            )

            st.rerun()

        # DELETE CHAT

        if col2.button(
            "✕",
            key=f"delete_{research_id}"
        ):

            delete_research(research_id)

            st.rerun()

except Exception as e:

    st.sidebar.error(
        f"Could not load history: {e}"
    )

# ==========================================
# DISPLAY SAVED CHAT
# ==========================================

if st.session_state.chat_query:

    st.subheader("Current Session")

    st.markdown(
        f"## {st.session_state.chat_query}"
    )

    # ==========================================
    # RESEARCH PLAN
    # ==========================================

    if st.session_state.chat_subquestions:

        st.subheader("Research Plan")

        for idx, question in enumerate(
            st.session_state.chat_subquestions
        ):

            st.markdown(
                f"{idx + 1}. {question}"
            )

    # ==========================================
    # RESEARCH FINDINGS
    # ==========================================

    if st.session_state.chat_results:

        st.subheader("Research Findings")

        for idx, result_text in enumerate(
            st.session_state.chat_results
        ):

            with st.expander(
                f"Research Result {idx + 1}"
            ):

                st.markdown(result_text)

    # ==========================================
    # CRITIC ANALYSIS
    # ==========================================

    if st.session_state.chat_critique:

        st.subheader("Critic Analysis")

        st.info(
            st.session_state.chat_critique
        )

    # ==========================================
    # FINAL REPORT
    # ==========================================

    if st.session_state.chat_report:

        st.subheader("Final Research Report")

        clean_saved_report = (
            st.session_state.chat_report
            .replace("**", "")
        )

        st.markdown(clean_saved_report)

        pdf_filename = "research_report.pdf"

        create_pdf(
            clean_saved_report,
            pdf_filename
        )

        with open(
            pdf_filename,
            "rb"
        ) as pdf_file:

            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name=pdf_filename,
                mime="application/pdf"
            )

    st.divider()

# ==========================================
# USER INPUT
# ==========================================

query = st.text_area(
    "Enter your research query:",
    height=150,
    placeholder="Example: Summarize recent AI research on RAG systems"
)

run_button = st.button(
    "Run Research"
)

# ==========================================
# EXECUTION TIMELINE
# ==========================================

st.subheader("Execution Timeline")

timeline_container = st.container()

# ==========================================
# MAIN WORKFLOW
# ==========================================

if run_button:

    if not query.strip():

        st.warning(
            "Please enter a research query."
        )

        st.stop()

    try:

        # ==========================================
        # CONTEXT MEMORY
        # ==========================================

        full_query = query

        if st.session_state.chat_report:

            full_query = f"""
Previous Research Report:

{st.session_state.chat_report[:3000]}

Previous Critic Analysis:

{st.session_state.chat_critique}

New User Request:

{query}
"""

        # ==========================================
        # INITIAL STATE
        # ==========================================

        initial_state = {

            "query": full_query,

            "subquestions": [],

            "search_results": [],

            "critique": "",

            "final_report": ""

        }

        # ==========================================
        # EXECUTION STATUS
        # ==========================================

        with timeline_container:

            st.success(
                "Planner Agent Running..."
            )

        result = app.invoke(initial_state)

        with timeline_container:

            st.success(
                "Researcher Agent Completed"
            )

            st.success(
                "Critic Agent Completed"
            )

            st.success(
                "Writer Agent Completed"
            )

        # ==========================================
        # RESEARCH PLAN
        # ==========================================

        st.subheader("Research Plan")

        for idx, question in enumerate(
            result["subquestions"]
        ):

            st.markdown(
                f"{idx + 1}. {question}"
            )

        # ==========================================
        # RESEARCH FINDINGS
        # ==========================================

        st.subheader("Research Findings")

        for idx, result_text in enumerate(
            result["search_results"]
        ):

            with st.expander(
                f"Research Result {idx + 1}"
            ):

                st.markdown(result_text)

        # ==========================================
        # CRITIC ANALYSIS
        # ==========================================

        st.subheader("Critic Analysis")

        st.info(
            result["critique"]
        )

        # ==========================================
        # FINAL REPORT
        # ==========================================

        final_report = result[
            "final_report"
        ]

        clean_report = (
            final_report
            .replace("**", "")
        )

        st.subheader(
            "Final Research Report"
        )

        report_placeholder = st.empty()

        streamed_text = ""

        for line in clean_report.split("\n"):

            streamed_text += line + "\n"

            report_placeholder.markdown(
                streamed_text
            )

            time.sleep(0.03)

        # ==========================================
        # SAVE SESSION STATE
        # ==========================================

        st.session_state.chat_query = query

        st.session_state.chat_report = clean_report

        st.session_state.chat_subquestions = result[
            "subquestions"
        ]

        st.session_state.chat_results = result[
            "search_results"
        ]

        st.session_state.chat_critique = result[
            "critique"
        ]

        # ==========================================
        # PDF DOWNLOAD
        # ==========================================

        pdf_filename = "research_report.pdf"

        create_pdf(
            clean_report,
            pdf_filename
        )

        with open(
            pdf_filename,
            "rb"
        ) as pdf_file:

            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name=pdf_filename,
                mime="application/pdf"
            )

        # ==========================================
        # SAVE TO MONGODB
        # ==========================================

        save_research(

            query=query,

            report=clean_report,

            subquestions=result["subquestions"],

            search_results=result["search_results"],

            critique=result["critique"]

        )

    except Exception as e:

        st.error(
            f"Error occurred: {e}"
        )