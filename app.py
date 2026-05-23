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
# CLEAN UI
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
    "Persistent autonomous research workflow using LangGraph, Groq, Tavily and MongoDB."
)

st.divider()

# ==========================================
# SESSION STATE
# ==========================================

default_states = {

    "active_chat": None,

    "conversation_history": [],

    "current_query": ""

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

# ==========================================
# LOAD HISTORY
# ==========================================

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

            st.session_state.conversation_history = item.get(
                "conversation_history",
                []
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
# DISPLAY CONVERSATION
# ==========================================

if st.session_state.conversation_history:

    st.subheader("Research Conversation")

    for idx, interaction in enumerate(

        st.session_state.conversation_history

    ):

        st.markdown(
            f"## User Request {idx + 1}"
        )

        st.info(
            interaction["query"]
        )

        # ==========================================
        # IMPROVEMENTS
        # ==========================================

        if interaction.get(
            "improvement_summary"
        ):

            st.subheader(
                "Improvements Added"
            )

            st.success(
                interaction[
                    "improvement_summary"
                ]
            )

        # ==========================================
        # RESEARCH PLAN
        # ==========================================

        if interaction.get(
            "subquestions"
        ):

            st.subheader(
                "Research Plan"
            )

            for i, question in enumerate(

                interaction["subquestions"]

            ):

                st.markdown(
                    f"{i + 1}. {question}"
                )

        # ==========================================
        # FINDINGS
        # ==========================================

        if interaction.get(
            "search_results"
        ):

            st.subheader(
                "Research Findings"
            )

            for i, result_text in enumerate(

                interaction["search_results"]

            ):

                with st.expander(
                    f"Finding {i + 1}"
                ):

                    st.markdown(
                        result_text
                    )

        # ==========================================
        # CRITIC
        # ==========================================

        if interaction.get(
            "critique"
        ):

            st.subheader(
                "Critic Analysis"
            )

            st.warning(
                interaction["critique"]
            )

        # ==========================================
        # FINAL REPORT
        # ==========================================

        if interaction.get(
            "final_report"
        ):

            st.subheader(
                "Final Research Report"
            )

            st.markdown(
                interaction[
                    "final_report"
                ]
            )

            pdf_filename = (
                f"research_report_{idx}.pdf"
            )

            create_pdf(

                interaction["final_report"],

                pdf_filename

            )

            with open(
                pdf_filename,
                "rb"
            ) as pdf_file:

                st.download_button(

                    label=(
                        f"Download PDF "
                        f"{idx + 1}"
                    ),

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
        "Example: "
        "Summarize recent AI "
        "research on RAG systems"
    )
)

run_button = st.button(
    "Run Research"
)

# ==========================================
# EXECUTION STATUS
# ==========================================

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
        # BUILD CONTEXT
        # ==========================================

        previous_context = ""

        if st.session_state.conversation_history:

            last_interaction = (

                st.session_state
                .conversation_history[-1]

            )

            previous_context = f"""

Previous Research Report:

{last_interaction.get('final_report', '')}

Previous Critic Analysis:

{last_interaction.get('critique', '')}
"""

        full_query = f"""
{previous_context}

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

            "final_report": "",

            "improvement_summary": "",

            "conversation_history": (
                st.session_state
                .conversation_history
            )

        }

        # ==========================================
        # EXECUTION STATUS
        # ==========================================

        with timeline_container:

            st.info(
                "Planner Agent Running..."
            )

        result = app.invoke(
            initial_state
        )

        with timeline_container:

            st.success(
                "Research Workflow Completed"
            )

        # ==========================================
        # CLEAN REPORT
        # ==========================================

        clean_report = (

            result["final_report"]

            .replace("**", "")

            .replace("###", "##")

        )

        # ==========================================
        # STREAM REPORT
        # ==========================================

        st.subheader(
            "Generating Final Report"
        )

        report_placeholder = st.empty()

        streamed_text = ""

        for line in clean_report.split("\n"):

            streamed_text += line + "\n"

            report_placeholder.markdown(
                streamed_text
            )

            time.sleep(0.02)

        # ==========================================
        # SAVE INTERACTION
        # ==========================================

        interaction = {

            "query": query,

            "subquestions": (
                result["subquestions"]
            ),

            "search_results": (
                result["search_results"]
            ),

            "critique": (
                result["critique"]
            ),

            "improvement_summary": (
                result.get(
                    "improvement_summary",
                    ""
                )
            ),

            "final_report": clean_report

        }

        # ==========================================
        # APPEND HISTORY
        # ==========================================

        st.session_state.conversation_history.append(

            interaction

        )

        # ==========================================
        # SAVE TO MONGODB
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

        st.success(
            "Research saved successfully."
        )

    except Exception as e:

        st.error(
            f"Error occurred: {e}"
        )