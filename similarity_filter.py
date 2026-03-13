from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = None
SIMILARITY_THRESHOLD = 0.85


def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def is_similar(new_idea, previous_ideas):

    if len(previous_ideas) == 0:
        return False

    model = get_model()

    new_embedding = model.encode([new_idea])
    previous_embeddings = model.encode(previous_ideas)

    similarities = cosine_similarity(new_embedding, previous_embeddings)

    max_similarity = np.max(similarities)

    if max_similarity > SIMILARITY_THRESHOLD:
        return True

    return False