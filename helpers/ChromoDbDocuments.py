import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def RankingChunks(items, query_embedding, top_k):
    ranked = sorted(
        items,
        key=lambda x: cosine_similarity(query_embedding, x["embedding"]),
        reverse=True
    )
    return [item["text"] for item in ranked[:top_k]]


