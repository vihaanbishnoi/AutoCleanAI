from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(vec1, vec2):
    similarity = cosine_similarity([vec1], [vec2])[0][0]
    return similarity * 100
