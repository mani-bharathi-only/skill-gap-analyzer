
import requests
import streamlit as st


# Backend API address
API_URL = "http://127.0.0.1:8000/analyze"


# Page configuration
st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="👊",
    layout="wide"
)


# Page header
st.title("Skill Gap Analyzer")

st.write(
    "Compare your skills with a target job "
    "and discover what you need to learn."
)


# Resume and job description inputs
col1, col2 = st.columns(2)

with col1:
    resume_text = st.text_area(
        "Your Resume / Skills",
        placeholder=(
            "Example: I know Python, Flask, "
            "MySQL and Git."
        ),
        height=220
    )

with col2:
    job_text = st.text_area(
        "Target Job Description",
        placeholder=(
            "Example: We require Python, "
            "FastAPI, MySQL and Docker."
        ),
        height=220
    )


# Analyze button
if st.button(
    "Analyze Skills",
    type="primary",
    use_container_width=True
):

    # Validate inputs
    if not resume_text.strip() or not job_text.strip():

        st.warning(
            "Please enter both your resume "
            "and the job description."
        )

    else:

        # Send request to FastAPI
        try:
            with st.spinner("Analyzing your skills..."):

                response = requests.post(
                    API_URL,
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
                "Unable to connect to the API. "
                "Make sure your FastAPI server "
                "is running."
            )

            st.caption(str(error))

        else:

            # Results dashboard
            st.divider()
            st.header("Your Skill Analysis")

            matched = result["matched"]
            adjacent = result["adjacent"]
            missing = result["missing"]
            roadmap = result["roadmap"]

            # Summary metrics
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

            # Matched skills
            st.subheader("Matched Skills")

            if matched:
                for skill in matched:
                    st.success(skill)
            else:
                st.info("No exact skill matches found.")

            # Adjacent skills
            st.subheader("Adjacent Skills")

            if adjacent:
                for item in adjacent:

                    st.warning(
                        f"{item['required_skill']} — "
                        f"Related experience: "
                        f"{', '.join(item['related_skills'])}"
                    )
            else:
                st.info("No adjacent skills found.")

            # Missing skills
            st.subheader("Missing Skills")

            if missing:
                for skill in missing:
                    st.error(skill)
            else:
                st.success(
                    "No missing skills detected "
                    "in the recognized requirements."
                )

            # Learning roadmap
            st.divider()
            st.header("Your Learning Roadmap")

            if roadmap:

                for index, item in enumerate(
                    roadmap,
                    start=1
                ):

                    with st.expander(
                        f"{index}. {item['skill']} "
                        f"— Priority {item['priority']}"
                    ):

                        st.write(
                            f"**Category:** {item['category']}"
                        )

                        st.write(item["description"])

                        if item["related_skills"]:
                            st.write(
                                "**Your related skills:** "
                                + ", ".join(
                                    item["related_skills"]
                                )
                            )

                        if item["resource_url"]:
                            st.link_button(
                                "Open Learning Resource",
                                item["resource_url"]
                            )

            else:
                st.success(
                    "No learning gaps detected "
                    "in the recognized requirements."
                )
