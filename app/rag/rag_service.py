from app.rag.vector_store import similarity_search
from app.rag.llm import llm
from app.rag.prompts import RAG_PROMPT


def ask_question(question: str):

    docs = similarity_search(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    answer = llm.invoke(prompt)

    sources = []

    for doc in docs:

        sources.append({
            "document": doc.metadata.get("document"),
            "page": doc.metadata.get("page")
        })

    return {
        "answer": answer,
        "sources": sources
    }