import streamlit as st

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
# STYLING
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
    }

    .stTextArea textarea {

        background-color: #161B22 !important;

        color: white !important;

        border-radius: 10px !important;

        border: 1px solid #2A2F3A !important;
    }

    .report-box {

        background-color: #161B22;

        padding: 25px;

        border-radius: 12px;

        border: 1px solid #1F2937;

        margin-top: 20px;

        margin-bottom: 20px;
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
    "Persistent autonomous research workflow using LangGraph, Groq, Tavily and MongoDB."
)

st.divider()

# ==========================================
# SESSION STATE
# ==========================================

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

if "chat_query" not in st.session_state:
    st.session_state.chat_query = ""

if "chat_report" not in st.session_state:
    st.session_state.chat_report = ""

if "chat_subquestions" not in st.session_state:
    st.session_state.chat_subquestions = []

if "chat_findings" not in st.session_state:
    st.session_state.chat_findings = []

if "chat_critique" not in st.session_state:
    st.session_state.chat_critique = ""

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Research History")

# ==========================================
# NEW CHAT
# ==========================================

if st.sidebar.button("New Chat"):

    st.session_state.active_chat = None

    st.session_state.chat_query = ""

    st.session_state.chat_report = ""

    st.session_state.chat_subquestions = []

    st.session_state.chat_findings = []

    st.session_state.chat_critique = ""

    st.rerun()

# ==========================================
# LOAD HISTORY
# ==========================================

try:

    recent = get_recent_research()

    for item in recent:

        query_title = item["query"]

        research_id = str(item["_id"])

        col1, col2 = st.sidebar.columns([4,1])

        # ==========================================
        # VIEW CHAT
        # ==========================================

        if col1.button(
            query_title,
            key=f"view_{research_id}"
        ):

            st.session_state.active_chat = research_id

            st.session_state.chat_query = item["query"]

            st.session_state.chat_report = item["report"]

            st.session_state.chat_subquestions = item.get(
                "subquestions",
                []
            )

            st.session_state.chat_findings = item.get(
                "search_results",
                []
            )

            st.session_state.chat_critique = item.get(
                "critique",
                ""
            )

            st.rerun()

        # ==========================================
        # DELETE CHAT
        # ==========================================

        if col2.button(
            "✕",
            key=f"delete_{research_id}"
        ):

            delete_research(research_id)

            st.rerun()

except Exception as e:

    st.sidebar.error(str(e))

# ==========================================
# DISPLAY ACTIVE CHAT
# ==========================================

if st.session_state.chat_query:

    st.subheader("Current Session")

    st.markdown(
        f"## {st.session_state.chat_query}"
    )

    # ==========================================
    # SUBQUESTIONS
    # ==========================================

    if st.session_state.chat_subquestions:

        st.subheader(
            "Research Plan"
        )

        for q in st.session_state.chat_subquestions:

            st.markdown(
                f"- {q}"
            )

    # ==========================================
    # FINDINGS
    # ==========================================

    if st.session_state.chat_findings:

        st.subheader(
            "Research Findings"
        )

        for idx, finding in enumerate(

            st.session_state.chat_findings

        ):

            with st.expander(
                f"Finding {idx + 1}"
            ):

                st.markdown(finding)

    # ==========================================
    # CRITIC
    # ==========================================

    if st.session_state.chat_critique:

        st.subheader(
            "Critic Analysis"
        )

        st.warning(
            st.session_state.chat_critique
        )

    # ==========================================
    # FINAL REPORT
    # ==========================================

    if st.session_state.chat_report:

        st.subheader(
            "Final Research Report"
        )

        clean_report = (

            st.session_state.chat_report

            .replace("**", "")

            .replace("```", "")

        )

        st.markdown(clean_report)

        # ==========================================
        # PDF
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

    st.divider()

# ==========================================
# USER INPUT
# ==========================================

query = st.text_area(
    "Enter your research query:",
    height=150,
    placeholder=(
        "Example: Summarize recent AI "
        "research on RAG systems"
    )
)

run_button = st.button(
    "Run Research"
)

# ==========================================
# MAIN WORKFLOW
# ==========================================

if run_button:

    if not query.strip():

        st.warning(
            "Please enter a query."
        )

        st.stop()

    try:

        status = st.empty()

        # ==========================================
        # MEMORY RETRIEVAL
        # ==========================================

        status.info(
            "Checking memory..."
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

                    st.markdown(
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
        # EXECUTION
        # ==========================================

        status.info(
            "Planner Agent Running..."
        )

        result = app.invoke(
            initial_state
        )

        status.success(
            "Research Workflow Completed"
        )

        # ==========================================
        # CLEAN REPORT
        # ==========================================

        clean_report = (

            result["final_report"]

            .replace("**", "")

            .replace("```", "")

        )

        # ==========================================
        # SAVE SESSION
        # ==========================================

        st.session_state.chat_query = query

        st.session_state.chat_report = clean_report

        st.session_state.chat_subquestions = result[
            "subquestions"
        ]

        st.session_state.chat_findings = result[
            "search_results"
        ]

        st.session_state.chat_critique = result[
            "critique"
        ]

        # ==========================================
        # SAVE DATABASE
        # ==========================================

        save_research(

            query=query,

            report=clean_report,

            subquestions=result[
                "subquestions"
            ],

            search_results=result[
                "search_results"
            ],

            critique=result[
                "critique"
            ]

        )

        # ==========================================
        # SAVE VECTOR MEMORY
        # ==========================================

        store_memory(
            query,
            clean_report
        )

        st.rerun()

    except Exception as e:

        st.error(
            f"Error occurred: {e}"
        )