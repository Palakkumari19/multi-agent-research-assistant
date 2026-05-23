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
# STYLING
# ==========================================

st.markdown("""
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
""", unsafe_allow_html=True)

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

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Research History")

# ==========================================
# NEW CHAT
# ==========================================

if st.sidebar.button("New Chat"):

    st.session_state.conversation_history = []

    st.session_state.active_chat = None

    st.rerun()

# ==========================================
# HISTORY
# ==========================================

try:

    recent = get_recent_research()

    for item in recent:

        query_title = item["query"]

        research_id = str(item["_id"])

        col1, col2 = st.sidebar.columns([4,1])

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

    st.sidebar.error(str(e))

# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

if st.session_state.conversation_history:

    st.subheader("Research Conversation")

    for idx, interaction in enumerate(

        st.session_state.conversation_history

    ):

        # ==========================================
        # USER PROMPT
        # ==========================================

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
        # SUBQUESTIONS
        # ==========================================

        if interaction.get(
            "subquestions"
        ):

            st.subheader(
                "Research Plan"
            )

            for q in interaction[
                "subquestions"
            ]:

                st.markdown(
                    f"- {q}"
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

                interaction[
                    "search_results"
                ]

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

        st.subheader(
            "Final Research Report"
        )

        st.markdown(
            interaction["final_report"]
        )

        # ==========================================
        # PDF
        # ==========================================

        pdf_filename = (
            f"report_{idx}.pdf"
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
# INPUT
# ==========================================

query = st.text_area(
    "Enter your research query:",
    height=150
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

        previous_context = ""

        improvement_summary = ""

        # ==========================================
        # CONTEXT MEMORY
        # ==========================================

        if st.session_state.conversation_history:

            last_chat = (

                st.session_state
                .conversation_history[-1]

            )

            previous_context = f"""

PREVIOUS REPORT:

{last_chat["final_report"]}

PREVIOUS CRITIC ANALYSIS:

{last_chat["critique"]}
"""

            improvement_summary = """
This response improves the previous report by:
- addressing critic feedback
- refining missing concepts
- increasing completeness
- improving structure
"""

        # ==========================================
        # PROMPT
        # ==========================================

        full_query = f"""
You are an advanced autonomous research assistant.

Generate:

1. Research subquestions
2. Research findings
3. Critic analysis
4. Final structured report

IMPORTANT:
- Use markdown formatting
- Use headings
- Use bullet points
- Keep spacing clean
- Avoid giant paragraphs
- Avoid raw markdown symbols like **

CONTEXT:

{previous_context}

USER REQUEST:

{query}
"""

        # ==========================================
        # STATUS
        # ==========================================

        status = st.empty()

        status.info(
            "Planner Agent Running..."
        )

        initial_state = {

            "query": full_query,

            "subquestions": [],

            "search_results": [],

            "critique": "",

            "final_report": ""

        }

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
        # INTERACTION
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
                improvement_summary
            ),

            "final_report": clean_report

        }

        # ==========================================
        # SAVE MEMORY
        # ==========================================

        st.session_state.conversation_history.append(
            interaction
        )

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
            ],

            conversation_history=(
                st.session_state
                .conversation_history
            )

        )

        st.rerun()

    except Exception as e:

        st.error(
            f"Error occurred: {e}"
        )