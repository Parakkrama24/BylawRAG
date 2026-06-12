from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "BAAI/bge-reranker-base"
)


def rerank(question, documents, top_k=3):

    pairs = [
        (question, doc.page_content)
        for doc in documents
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        doc
        for doc, score in ranked[:top_k]
    ]