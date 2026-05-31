from app.rag.vector_store import similarity_search
from app.rag.llm import llm
from app.rag.prompts import RAG_PROMPT


def ask_question(question: str):
    results = similarity_search(question)

    results = similarity_search(question)

    if not results:
        return {
            "answer": "I could not find this information in the university regulations.",
            "sources": []
        }

    best_score = results[0][1]

    print(f"Best Score: {best_score}")

    if best_score > 1.2:
        return {
            "answer": "I could not find this information in the university regulations.",
            "sources": []
        }
    # Debug retrieval results
    for doc, score in results:
        print(f"Score: {score}")
        print(doc.metadata)

    context = "\n\n".join(
        [
            f"""
            Document: {doc.metadata.get('document')}
            Page: {doc.metadata.get('page')}

            {doc.page_content}
            """
            for doc, score in results
        ]
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    answer = llm.invoke(prompt)

    sources = []

    for doc, score in results:
        sources.append({
            "document": doc.metadata.get("document"),
            "page": doc.metadata.get("page"),
            "score": round(score, 3),
            "snippet": doc.page_content[:200]
        })

    return {
        "answer": answer,
        "sources": sources
    }