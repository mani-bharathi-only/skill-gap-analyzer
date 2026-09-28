
import os

import requests
import streamlit as st


# ==================================================
# CONFIGURATION
# ==================================================

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #F8FAFC;
        color: #172033;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* Hide default Streamlit decoration */

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }

    /* Header */

    .brand {
        color: #2563EB;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #172033;
        line-height: 1.2;
        margin-bottom: 15px;
    }

    .main-description {
        color: #64748B;
        font-size: 15px;
        line-height: 1.8;
        max-width: 730px;
        margin-bottom: 35px;
    }

    /* Section headings */

    .section-title {
        color: #1E293B;
        font-size: 21px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 7px;
    }

    .section-description {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.7;
        margin-bottom: 23px;
    }

    /* Inputs */

    div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF;
        border: 1px solid #DCE3EC;
        border-radius: 10px;
        color: #1E293B;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        line-height: 1.8;
        padding: 15px;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #2563EB;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.1);
    }

    div[data-testid="stTextArea"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label {
        color: #334155;
        font-size: 13px;
        font-weight: 600;
    }

    /* Buttons */

    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #2563EB;
        border: none;
        border-radius: 9px;
        color: white;
        font-size: 14px;
        font-weight: 600;
        min-height: 48px;
        transition: background-color 0.2s ease;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #1D4ED8;
    }

    /* Metrics */

    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        min-height: 145px;
    }

    .metric-label {
        color: #64748B;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 13px;
    }

    .metric-number {
        color: #172033;
        font-size: 38px;
        font-weight: 800;
        line-height: 1.2;
    }

    .metric-description {
        color: #94A3B8;
        font-size: 11px;
        margin-top: 12px;
    }

    .metric-green {
        border-top: 3px solid #16A34A;
    }

    .metric-blue {
        border-top: 3px solid #2563EB;
    }

    .metric-amber {
        border-top: 3px solid #D97706;
    }

    /* Result sections */

    .result-heading {
        color: #1E293B;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .skill-tag {
        display: inline-block;
        padding: 8px 13px;
        margin: 0 7px 9px 0;
        border-radius: 7px;
        font-size: 12px;
        font-weight: 600;
    }

    .tag-green {
        color: #15803D;
        background-color: #DCFCE7;
    }

    .tag-blue {
        color: #1D4ED8;
        background-color: #DBEAFE;
    }

    .tag-amber {
        color: #92400E;
        background-color: #FEF3C7;
    }

    /* Roadmap */

    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    /* Footer */

    .footer {
        border-top: 1px solid #E2E8F0;
        padding-top: 25px;
        margin-top: 55px;
        color: #94A3B8;
        font-size: 12px;
        text-align: center;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem 1rem;
        }

        .main-title {
            font-size: 29px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_jobs():

    response = requests.get(
        f"{API_BASE_URL}/jobs",
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def analyze_resume(resume_text, job_text):

    response = requests.post(
        f"{API_BASE_URL}/analyze",
        json={
            "resume_text": resume_text,
            "job_text": job_text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()


def show_metric(label, value, description, color):

    st.markdown(
        f"""
        <div class="metric-card {color}">
            <div class="metric-label">
                {label}
            </div>

            <div class="metric-number">
                {value}
            </div>

            <div class="metric-description">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# SESSION STATE
# ==================================================

if "result" not in st.session_state:
    st.session_state.result = None


# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="brand">
        Skill Gap Analyzer
    </div>

    <div class="main-title">
        Find the skills you need to grow.
    </div>

    <div class="main-description">
        Compare your current technical skills with
        the requirements of your target job.
        Identify existing strengths, discover
        potential skill gaps, and receive
        relevant learning recommendations.
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# INPUT SECTION
# ==================================================

st.markdown(
    """
    <div class="section-title">
        Start your analysis
    </div>

    <div class="section-description">
        Enter your experience and choose
        the position you want to pursue.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(
    2,
    gap="large"
)


# Resume input

with col1:

    resume_text = st.text_area(
        "Your Resume / Skills",
        height=260,
        placeholder=(
            "Enter your resume text or list "
            "your technical skills here.\n\n"
            "Example: Python, Flask, MySQL, Git"
        )
    )


# Job description input

with col2:

    input_mode = st.radio(
        "Job Description Source",
        [
            "Choose Sample Job",
            "Paste Job Description"
        ],
        horizontal=True
    )

    job_text = ""

    if input_mode == "Choose Sample Job":

        try:

            jobs = get_jobs()

            if jobs:

                selected_job = st.selectbox(
                    "Select a Job",
                    jobs,
                    format_func=lambda job: job["title"]
                )

                job_text = selected_job["description"]

                st.text_area(
                    "Job Description",
                    value=job_text,
                    height=158,
                    disabled=True
                )

            else:

                st.warning(
                    "No sample jobs are available."
                )

        except requests.RequestException:

            st.error(
                "Unable to load sample jobs. "
                "Please check the backend connection."
            )

    else:

        job_text = st.text_area(
            "Job Description",
            height=205,
            placeholder=(
                "Paste the requirements of "
                "your target job here."
            )
        )


st.write("")

analyze_button = st.button(
    "Analyze Skills",
    type="primary",
    use_container_width=True
)


# ==================================================
# ANALYZE
# ==================================================

if analyze_button:

    st.session_state.result = None

    if not resume_text.strip():

        st.warning(
            "Please enter your resume or skills."
        )

    elif not job_text.strip():

        st.warning(
            "Please select or enter a job description."
        )

    else:

        try:

            with st.spinner(
                "Analyzing your skills..."
            ):

                result = analyze_resume(
                    resume_text,
                    job_text
                )

            st.session_state.result = result

        except requests.Timeout:

            st.error(
                "The request timed out. "
                "The backend may still be starting. "
                "Please try again."
            )

        except requests.RequestException:

            st.error(
                "Unable to complete the analysis. "
                "Please check your backend connection."
            )


# ==================================================
# RESULTS
# ==================================================

result = st.session_state.result

if result is not None:

    matched = result.get("matched", [])
    adjacent = result.get("adjacent", [])
    missing = result.get("missing", [])
    roadmap = result.get("roadmap", [])

    st.write("")
    st.divider()

    st.markdown(
        """
        <div class="section-title">
            Your Skill Analysis
        </div>

        <div class="section-description">
            Here's how your submitted skills
            compare with the selected job.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Summary metrics

    m1, m2, m3 = st.columns(
        3,
        gap="medium"
    )

    with m1:

        show_metric(
            "Matched Skills",
            len(matched),
            "Exact skill matches",
            "metric-green"
        )

    with m2:

        show_metric(
            "Adjacent Skills",
            len(adjacent),
            "Related technical experience",
            "metric-blue"
        )

    with m3:

        show_metric(
            "Potential Skill Gaps",
            len(missing),
            "Skills not identified",
            "metric-amber"
        )

    st.write("")
    st.write("")

    # Matched skills

    st.markdown(
        '<div class="result-heading">Matched Skills</div>',
        unsafe_allow_html=True
    )

    if matched:

        for skill in matched:

            st.markdown(
                f"""
                <span class="skill-tag tag-green">
                    {skill}
                </span>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No exact skill matches were identified."
        )

    st.write("")

    # Adjacent skills

    st.markdown(
        '<div class="result-heading">Adjacent Skills</div>',
        unsafe_allow_html=True
    )

    if adjacent:

        for item in adjacent:

            skill = item["required_skill"]

            related = ", ".join(
                item["related_skills"]
            )

            st.markdown(
                f"""
                <span class="skill-tag tag-blue">
                    {skill}
                </span>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                f"Related experience: {related}"
            )

    else:

        st.info(
            "No adjacent skills were identified."
        )

    st.write("")

    # Missing skills

    st.markdown(
        '<div class="result-heading">Potential Skill Gaps</div>',
        unsafe_allow_html=True
    )

    if missing:

        for skill in missing:

            st.markdown(
                f"""
                <span class="skill-tag tag-amber">
                    {skill}
                </span>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "No missing skills were identified "
            "in the recognized requirements."
        )

    # ==================================================
    # LEARNING ROADMAP
    # ==================================================

    st.write("")
    st.divider()

    st.markdown(
        """
        <div class="section-title">
            Your Learning Roadmap
        </div>

        <div class="section-description">
            Suggested resources to help you
            develop skills relevant to your target role.
        </div>
        """,
        unsafe_allow_html=True
    )

    if roadmap:

        for index, item in enumerate(
            roadmap,
            start=1
        ):

            skill = item["skill"]
            category = item["category"]
            priority = item["priority"]
            description = item["description"]
            related_skills = item["related_skills"]
            resource_url = item["resource_url"]

            with st.expander(
                f"{index}. {skill} — Priority {priority}",
                expanded=(index == 1)
            ):

                st.write(
                    f"**Category:** {category.title()}"
                )

                st.write(description)

                if related_skills:

                    st.write(
                        "**Related experience:** "
                        + ", ".join(related_skills)
                    )

                if resource_url:

                    st.link_button(
                        "View Learning Resource",
                        resource_url
                    )

    else:

        st.success(
            "No additional learning recommendations "
            "were generated."
        )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        Skill Gap Analyzer &nbsp; | &nbsp;
        Built with Python, FastAPI,
        Streamlit and SQLite
    </div>
    """,
    unsafe_allow_html=True
)
