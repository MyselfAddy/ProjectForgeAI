from modules.similarity_filter import is_similar
from groq import Groq
import json
import os

# initialize groq client

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

STORAGE_FILE = "storage/generated_ideas.json"


def load_previous_ideas():
    if not os.path.exists(STORAGE_FILE):
        return []

    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def save_idea(new_idea):
    ideas = load_previous_ideas()
    ideas.append(new_idea)

    with open(STORAGE_FILE, "w") as f:
        json.dump(ideas, f, indent=4)


def generate_ai_project(fusion_domains, level, duration, existing_skills="", learning_skills=""):

    domain_description = "\n".join(
        [f"{domain}: {weight}%" for domain, weight in fusion_domains.items()]
    )

    timeline = "\n".join([f"Month {i}:" for i in range(1, duration + 1)])

    prompt = f"""
You are an expert AI mentor helping students find project ideas.

Domain Fusion:
{domain_description}

Project Level: {level}

Maximum Duration: {duration} months

User Skill Profile:

Current Skills:
{existing_skills}

Skills To Learn:
{learning_skills}

Project Skill Constraint Rules:
- The core implementation should primarily use the user's current skills when possible.
- Introduce the requested new skills as a small learning component within the project.
- Ensure the project remains feasible for the user's skill level.

Skill Usage Requirements:

Explicitly include a section called:

Core Skills Used:
<List skills from user's current skills that will be used in the project>

New Skills Introduced:
<List skills from the learning skills input and explain how they will be used>

Ensure the project uses at least one of the user's existing skills.
Ensure the learning skills appear as an extension layer of the project.

STRICT RULES:
- The project MUST strictly fit within {duration} months.
- Do NOT generate months beyond Month {duration}.
- Difficulty must match the project level.
- Respect the domain fusion percentages when designing the system.
- The project idea must be novel and not a commonly suggested student project.
- Avoid generic ideas such as "chatbot", "simple image classifier", or "basic recommendation system".
- Avoid repeating themes such as predictive maintenance, disease prediction, or simple classification systems.
- Prefer unconventional combinations of the selected domains.
- Encourage creative system designs such as simulation platforms, intelligent monitoring tools, autonomous agents, or decision-support systems.
- Ensure each generated idea explores a different application area.


Mini Project:
Small but unique foundational idea.

Mini Project Constraints:
- Must be implementable by 1–2 students
- Must be feasible within the selected duration
- For 1–2 month projects, avoid complex infrastructure such as Kubernetes, large cloud deployments, or multi-platform systems
- Focus on a lightweight prototype, simulation, or small web/mobile demo

Major Research Project:
Academic research focused.

Job-ready Project:
Industry-level engineering project with practical value.

Provide the response EXACTLY in this format:

Project Title:
<one line>

Problem Statement:
<3–4 sentences>

System Architecture:
<short structured explanation>

Tech Stack:
- item
- item
- item

Dataset Suggestions:
- dataset
- dataset

Estimated Timeline:
Follow EXACTLY the months listed below. Do not add any additional months.

{timeline}

Development Plan:
Provide 4–6 key implementation steps that guide the student in building the project.
Do NOT include time estimates here.

Research Paper References:

Provide at least 5 relevant IEEE or peer-reviewed research papers related to this project idea.

Rules:
- Papers must be from 2020 to 2025.
- Prefer IEEE, ACM, Springer, or Elsevier publications.
- Each paper must include:
  - Paper Title
  - Year
  - Short 1-line description of relevance
  - DOI or link if available

Format exactly like this:

Research Papers:

1. <Paper Title> (Year)
   Relevance: <how this paper relates to the project>

2. <Paper Title> (Year)
   Relevance: <short explanation>

3. <Paper Title> (Year)
   Relevance: <short explanation>

4. <Paper Title> (Year)
   Relevance: <short explanation>

5. <Paper Title> (Year)
   Relevance: <short explanation>
"""

    previous_ideas = load_previous_ideas()

    while True:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )

        idea = response.choices[0].message.content

        # keep only first project block
        if "Project Title:" in idea:
            parts = idea.split("Project Title:")
            if len(parts) > 2:
                idea = "Project Title:" + parts[1]

        # duplicate protection
        if idea not in previous_ideas and not is_similar(idea, previous_ideas):
            save_idea(idea)
            return idea