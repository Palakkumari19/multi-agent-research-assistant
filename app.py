import streamlit as st
import time

from graph.workflow import app

from memory.mongo_store import (
    save_research,
    get_recent_research,
    delete_research
)

from memory.faiss_store import (
    store_memory,
    retrieve_similar
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
# MINIMAL CLEAN UI
# ==========================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: #FFFFFF;
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

        transition: 0.2s ease;
    }

    .stButton button:hover {

        background-color: #273244 !important;

        border: 1px solid #4B5563 !important;
    }

    .stDownloadButton button {

        background-color: #1F2937 !important;

        color: white !important;

        border-radius: 8px !important;

        border: 1px solid #374151 !important;
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

st.divider()

# ==========================================
# WORKFLOW
# ==========================================


# ==========================================
# SESSION STATE
# ==========================================

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

if "chat_query" not in st.session_state:
    st.session_state.chat_query = ""

if "chat_report" not in st.session_state:
    st.session_state.chat_report = ""

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Research History")

# NEW CHAT BUTTON

if st.sidebar.button("New Chat"):

    st.session_state.active_chat = None

    st.session_state.chat_query = ""

    st.session_state.chat_report = ""

    st.rerun()

try:

    recent = get_recent_research()

    for item in recent:

        query_title = item["query"]

        report_text = item["report"]

        research_id = str(item["_id"])

        col1, col2 = st.sidebar.columns([4, 1])

        # VIEW CHAT

        if col1.button(
            query_title,
            key=f"view_{research_id}"
        ):

            st.session_state.active_chat = research_id

            st.session_state.chat_query = query_title

            st.session_state.chat_report = report_text

            st.rerun()

        # DELETE CHAT

        if col2.button(
            "✕",
            key=f"delete_{research_id}"
        ):

            delete_research(research_id)

            if (
                st.session_state.active_chat
                == research_id
            ):

                st.session_state.active_chat = None

                st.session_state.chat_query = ""

                st.session_state.chat_report = ""

            st.rerun()

except Exception as e:

    st.sidebar.error(
        f"Could not load history: {e}"
    )

# ==========================================
# ACTIVE CHAT
# ==========================================

if st.session_state.chat_query:

    st.subheader("Current Session")

    st.markdown(
        f"### {st.session_state.chat_query}"
    )

    if st.session_state.chat_report:

        st.markdown(
            st.session_state.chat_report
        )

        # PDF DOWNLOAD

        pdf_filename = "research_report.pdf"

        create_pdf(
            st.session_state.chat_report,
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
    value=st.session_state.chat_query,
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
        # MEMORY RETRIEVAL
        # ==========================================

        with timeline_container:

            st.success(
                "Memory Retrieval Completed"
            )

        similar_memories = retrieve_similar(query)

        if similar_memories:

            st.subheader(
                "Similar Past Research"
            )

            for memory in similar_memories:

                with st.expander(
                    memory["query"]
                ):

                    st.write(
                        memory["report"]
                    )

        # ==========================================
        # INITIAL STATE
        # ==========================================

        initial_state = {
            "query": query,
            "subquestions": [],
            "search_results": [],
            "critique": "",
            "final_report": ""
        }

        # ==========================================
        # EXECUTE GRAPH
        # ==========================================

        with timeline_container:

            st.success(
                "Planner Agent Completed"
            )

        result = app.invoke(initial_state)

        with timeline_container:

            st.success(
                "Researcher Agent Completed"
            )

        with timeline_container:

            st.success(
                "Critic Agent Completed"
            )

        with timeline_container:

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
        # SEARCH RESULTS
        # ==========================================

        st.subheader("Research Findings")

        for idx, result_text in enumerate(
            result["search_results"]
        ):

            with st.expander(
                f"Research Result {idx + 1}"
            ):

                st.write(result_text)

        # ==========================================
        # FINAL REPORT
        # ==========================================

        final_report = result[
            "final_report"
        ]

        # SAVE ACTIVE CHAT

        st.session_state.chat_query = query

        st.session_state.chat_report = final_report

        st.subheader("Final Research Report")

        report_placeholder = st.empty()

        streamed_text = ""

        words = final_report.split()

        for word in words:

            streamed_text += word + " "

            report_placeholder.markdown(
                streamed_text
            )

            time.sleep(0.02)

        # ==========================================
        # PDF DOWNLOAD
        # ==========================================

        pdf_filename = "research_report.pdf"

        create_pdf(
            final_report,
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
        # SAVE MEMORY
        # ==========================================

        save_research(
            query,
            final_report
        )

        store_memory(
            query,
            final_report
        )

        st.divider()

    except Exception as e:

        st.error(
            f"Error occurred: {e}"
        )