from rank_bm25 import BM25Okapi


def bm25_search(documents, query, top_k=5):

    corpus = [
        doc.page_content
        for doc in documents
    ]

    tokenized_corpus = [
        doc.lower().split()
        for doc in corpus
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        doc
        for doc, score in ranked[:top_k]
    ]