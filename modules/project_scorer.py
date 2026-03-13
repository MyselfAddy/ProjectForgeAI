import random

def score_project(idea_text):

    innovation_keywords = [
        "novel", "autonomous", "adaptive", "intelligent",
        "simulation", "decision", "optimization"
    ]

    research_keywords = [
        "analysis", "framework", "model", "algorithm",
        "prediction", "detection"
    ]

    implementation_keywords = [
        "robot", "sensor", "system", "platform",
        "interface", "integration"
    ]

    text = idea_text.lower()

    innovation = sum(word in text for word in innovation_keywords)
    research = sum(word in text for word in research_keywords)
    implementation = sum(word in text for word in implementation_keywords)

    innovation_score = min(10, 6 + innovation)
    research_score = min(10, 6 + research)
    feasibility_score = min(10, 7 + implementation)

    if feasibility_score >= 9:
        difficulty = "Medium"
    elif feasibility_score >= 7:
        difficulty = "Medium-Hard"
    else:
        difficulty = "Hard"

    return {
        "innovation": round(innovation_score,1),
        "research": round(research_score,1),
        "feasibility": round(feasibility_score,1),
        "difficulty": difficulty
    }