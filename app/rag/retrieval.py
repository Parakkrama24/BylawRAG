from app.rag.vector_store import similarity_search
from app.rag.bm25_retriever import bm25_search
from app.rag.reranker import rerank


def hybrid_search(question):

    vector_results = similarity_search(
        question,
        k=5
    )

    docs = [
        doc
        for doc, score in vector_results
    ]

    bm25_results = bm25_search(
        docs,
        question,
        top_k=3
    )

    merged = docs + bm25_results

    unique_docs = []

    seen = set()

    for doc in merged:

        content = doc.page_content

        if content not in seen:

            seen.add(content)

            unique_docs.append(doc)

    reranked_docs = rerank(
        question,
        unique_docs,
        top_k=3
    )

    return reranked_docs