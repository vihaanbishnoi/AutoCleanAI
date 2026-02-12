from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize

def cluster_embeddings(file_paths, embeddings):
    embeddings = normalize(embeddings)

    model = DBSCAN(
        eps=0.15,
        min_samples=2,
        metric='cosine'
    )

    labels = model.fit_predict(embeddings)

    cluster_map = {}

    for label, path, emb in zip(labels, file_paths, embeddings):
        if label == -1:
            continue
        cluster_map.setdefault(label, []).append((path, emb))

    return cluster_map
