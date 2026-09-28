
import os
import requests
import streamlit as st


# ==========================================
# 1. CONFIGURATION
# ==========================================

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# ==========================================
# 2. PAGE HEADER
# ==========================================

st.title("🎯 Skill Gap Analyzer")

st.write(
    "Compare your skills with a target job "
    "and discover what you need to learn."
)

st.divider()


# ==========================================
# 3. INPUT SECTION
# ==========================================

st.header("Analyze Your Skills")

col1, col2 = st.columns(2)

with col1:

    resume_text = st.text_area(
        "Your Resume / Skills",
        height=250,
        placeholder=(
            "Example: I know Python, Flask, "
            "MySQL and Git."
        )
    )


with col2:

    input_mode = st.radio(
        "Job Description Source",
        [
            "Choose Sample Job",
            "Paste Job Description"
        ]
    )

    job_text = ""

    if input_mode == "Choose Sample Job":

        try:
            response = requests.get(
                f"{API_BASE_URL}/jobs",
                timeout=10
            )

            response.raise_for_status()

            jobs = response.json()

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
                    height=180,
                    disabled=True
                )

            else:

                st.warning(
                    "No sample jobs available."
                )

        except requests.RequestException as error:

            st.error(
                "Could not load sample jobs. "
                "Check your FastAPI server."
            )

            st.caption(str(error))

    else:

        job_text = st.text_area(
            "Paste Job Description",
            height=250,
            placeholder=(
                "Example: We require Python, "
                "FastAPI, MySQL and Docker."
            )
        )


# ==========================================
# 4. ANALYZE BUTTON
# ==========================================

if st.button(
    "Analyze Skills",
    type="primary",
    use_container_width=True
):

    # Validate user input
    if not resume_text.strip():

        st.warning(
            "Please enter your resume or skills."
        )

    elif not job_text.strip():

        st.warning(
            "Please select or enter a job description."
        )

    else:

        # ==================================
        # 5. SEND REQUEST TO FASTAPI
        # ==================================

        try:

            with st.spinner(
                "Analyzing your skills..."
            ):

                response = requests.post(
                    f"{API_BASE_URL}/analyze",
                    json={
                        "resume_text": resume_text,
                        "job_text": job_text
                    },
                    timeout=30
                )

                response.raise_for_status()

                result = response.json()

        except requests.RequestException as error:

            st.error(
                "Unable to analyze your skills. "
                "Make sure the FastAPI server "
                "is running."
            )

            st.caption(str(error))

        else:

            # ==============================
            # 6. EXTRACT API RESULTS
            # ==============================

            matched = result["matched"]
            adjacent = result["adjacent"]
            missing = result["missing"]
            roadmap = result["roadmap"]

            # ==============================
            # 7. RESULTS DASHBOARD
            # ==============================

            st.divider()

            st.header("📊 Your Skill Analysis")

            m1, m2, m3 = st.columns(3)

            m1.metric(
                "Matched Skills",
                len(matched)
            )

            m2.metric(
                "Adjacent Skills",
                len(adjacent)
            )

            m3.metric(
                "Missing Skills",
                len(missing)
            )

            st.divider()

            # ==============================
            # 8. MATCHED SKILLS
            # ==============================

            st.subheader("✅ Matched Skills")

            if matched:

                for skill in matched:
                    st.success(skill)

            else:

                st.info(
                    "No exact skill matches found."
                )

            # ==============================
            # 9. ADJACENT SKILLS
            # ==============================

            st.subheader("🔄 Adjacent Skills")

            if adjacent:

                for item in adjacent:

                    required_skill = item[
                        "required_skill"
                    ]

                    related_skills = item[
                        "related_skills"
                    ]

                    st.warning(
                        f"{required_skill} — "
                        f"Related experience: "
                        f"{', '.join(related_skills)}"
                    )

            else:

                st.info(
                    "No adjacent skills found."
                )

            # ==============================
            # 10. MISSING SKILLS
            # ==============================

            st.subheader("❌ Missing Skills")

            if missing:

                for skill in missing:
                    st.error(skill)

            else:

                st.success(
                    "No missing skills detected "
                    "in the recognized requirements."
                )

            # ==============================
            # 11. LEARNING ROADMAP
            # ==============================

            st.divider()

            st.header("📚 Your Learning Roadmap")

            if roadmap:

                for index, item in enumerate(
                    roadmap,
                    start=1
                ):

                    skill = item["skill"]
                    category = item["category"]
                    priority = item["priority"]
                    description = item["description"]

                    related_skills = item[
                        "related_skills"
                    ]

                    resource_url = item[
                        "resource_url"
                    ]

                    with st.expander(
                        f"{index}. {skill} "
                        f"— Priority {priority}"
                    ):

                        st.write(
                            f"**Category:** {category.title()}"
                        )

                        st.write(description)

                        if related_skills:

                            st.write(
                                "**Your related skills:** "
                                + ", ".join(
                                    related_skills
                                )
                            )

                        if resource_url:

                            st.link_button(
                                "Open Learning Resource",
                                resource_url
                            )

            else:

                st.success(
                    "No learning gaps detected "
                    "in the recognized requirements."
                )


# ==========================================
# 12. FOOTER
# ==========================================

st.divider()

st.caption(
    "Skill Gap Analyzer | "
    "Built with Python, FastAPI, "
    "Streamlit and SQLite"
)
