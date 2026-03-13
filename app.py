from modules.llm_generator import generate_ai_project
import streamlit as st
from modules.pdf_generator import generate_pdf
from modules.project_scorer import score_project
from modules.llm_generator import load_previous_ideas
from ui_style import apply_ui

st.set_page_config(page_title="ProjectForge AI", layout="wide")
st.markdown("""
# 🚀 ProjectForge AI

### Discover AI Project Ideas Instantly
Generate unique projects using **AI + Domain Fusion + Skill Intelligence**
""")

apply_ui()

def extract_keywords(idea_text):

    lines = idea_text.split("\n")

    title_line = [l for l in lines if "Project Title" in l]

    if title_line:
        title = title_line[0].replace("Project Title:", "").strip()

        stopwords = {"using","for","in","with","and","of"}

        keywords = [w for w in title.split() if w.lower() not in stopwords]

        return " ".join(keywords[:4])

    return ""


st.write("Generate unique project ideas using weighted domain fusion.")

# Alphabetical domain list
domains = sorted([
"Artificial Intelligence",
"Augmented Reality",
"Bioinformatics",
"Blockchain",
"Cloud Computing",
"Computer Vision",
"Cybersecurity",
"Data Science",
"DevOps",
"Edge Computing",
"Finance Technology",
"Healthcare Informatics",
"Human Computer Interaction",
"Internet of Things",
"Machine Learning",
"Natural Language Processing",
"Quantum Computing",
"Robotics",
"Smart Cities",
"Software Engineering"
])

st.markdown("### Domain Fusion (Up to 3 Domains)")

with st.sidebar:

    st.header("⚙️ Project Configuration")

    domain1 = st.selectbox("Domain 1", domains)
    weight1 = st.number_input("Domain 1 %", min_value=0, max_value=100, value=40)

    domain2 = st.selectbox("Domain 2", domains)
    weight2 = st.number_input("Domain 2 %", min_value=0, max_value=100, value=30)

    domain3 = st.selectbox("Domain 3", domains)
    weight3 = st.number_input("Domain 3 %", min_value=0, max_value=100, value=30)

    # ADD THIS LINE
    total_weight = weight1 + weight2 + weight3

    level = st.selectbox(
        "Project Level",
        ["Mini Project", "Major Research Project", "Job-ready Project"]
    )

    duration = st.selectbox(
        "Project Duration (months)",
        [1,2,3,4,5,6]
    )

    st.markdown("### Skill Preferences")

    existing_skills = st.text_input(
        "Your Current Skills",
        placeholder="Python, ML, Flask"
    )

    learning_skills = st.text_input(
        "Skills to Learn",
        placeholder="Computer Vision, Docker"
    )

st.write("Domain Fusion:")
st.write(f"{domain1}: {weight1}%")
st.write(f"{domain2}: {weight2}%")
st.write(f"{domain3}: {weight3}%")
if domain1 == domain2 or domain1 == domain3 or domain2 == domain3:
    st.error("Please select three different domains.")


if st.button("Generate Project Idea"):

    if total_weight != 100:
        st.error("Please ensure domain weights total 100%")
    else:

        fusion_domains = {
            domain1: weight1,
            domain2: weight2,
            domain3: weight3
        }

        with st.spinner("Generating AI project idea...Almost Found something great for you..☺️ just a few more second"):
            idea = generate_ai_project(fusion_domains, level, duration)

        st.session_state["idea"] = idea


if "idea" in st.session_state:

    st.markdown("## Current Idea")
    st.markdown("""
    <div style="
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    "
    """, unsafe_allow_html=True)

    st.markdown(st.session_state["idea"])

    st.markdown("</div>", unsafe_allow_html=True)

    # ----- Project Evaluation -----
    scores = score_project(st.session_state["idea"])

    st.markdown("### Project Evaluation")

    st.write(f"Innovation Score: {scores['innovation']}/10")
    st.write(f"Research Novelty: {scores['research']}/10")
    st.write(f"Feasibility Score: {scores['feasibility']}/10")
    st.write(f"Implementation Difficulty: {scores['difficulty']}")

    # ----- Add evaluation into PDF -----
    idea_with_scores = f"""{st.session_state["idea"]}

Project Evaluation

Innovation Score: {scores['innovation']}/10
Research Novelty: {scores['research']}/10
Feasibility Score: {scores['feasibility']}/10
Implementation Difficulty: {scores['difficulty']}
"""

    pdf_file = generate_pdf(idea_with_scores)

    st.download_button(
        label="Download Idea as PDF",
        data=pdf_file,
        file_name="project_idea.pdf",
        mime="application/pdf"
    )


if st.button("Refresh Idea"):

    fusion_domains = {
        domain1: weight1,
        domain2: weight2,
        domain3: weight3
    }

    idea = generate_ai_project(
    fusion_domains,
    level,
    duration,
    existing_skills,
    learning_skills
)

    st.session_state["idea"] = idea

    st.markdown("## Refreshed Idea")
    st.markdown(idea)


# ----- Idea History -----
st.markdown("### Previous Generated Ideas")

previous_ideas = load_previous_ideas()

if previous_ideas:

    for i, idea_item in enumerate(previous_ideas[::-1][:5]):

        # Extract project title
        title_line = None
        for line in idea_item.split("\n"):
            if "Project Title" in line:
                title_line = line.replace("Project Title:", "").strip()
                break

        if not title_line:
            title_line = "Generated Project Idea"

        col1, col2 = st.columns([4,1])

        with col1:
            st.write(title_line)

        with col2:
            if st.button("View", key=f"history_{i}"):

                st.session_state["idea"] = idea_item

                st.markdown("## Current Idea")
                st.markdown(st.session_state["idea"])

else:
    st.write("No previous ideas found.")