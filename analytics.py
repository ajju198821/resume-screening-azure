from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text: str, job_desc: str) -> float:
    documents = [resume_text, job_desc]

    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform(documents)

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])

    score = similarity[0][0] * 100
    return round(score, 2)