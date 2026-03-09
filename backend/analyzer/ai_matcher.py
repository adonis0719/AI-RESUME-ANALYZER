"""
AI Semantic Similarity Module using Sentence Transformers.
Uses all-MiniLM-L6-v2 for embeddings and cosine similarity.
"""


def semantic_similarity(resume_text, job_text):
    """
    Compute semantic similarity between resume and job description text.
    Returns a score from 0 to 100.
    """
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        return None

    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")

        resume_embedding = model.encode([resume_text or ""])
        job_embedding = model.encode([job_text or ""])

        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return round(float(similarity) * 100, 2)
    except Exception:
        return None
