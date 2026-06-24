from app.log.retrieval_logger import log_question
from app.rag.retrieval import hybrid_search
from app.rag.llm import llm
from app.rag.prompts import RAG_PROMPT
from app.rag.cache import (
    get_cached_answer,
    cache_answer
)



def ask_question(question: str):
    cached = get_cached_answer(question)

    if cached:
        print("CACHE HIT")
        return cached

    docs = hybrid_search(question)

    if not docs:
        return {
            "answer": "I could not find this information in the university regulations.",
            "sources": []
        }

    # Debug
    print("\n===== Retrieved Documents =====")

    for doc in docs:
        print(doc.metadata)

    print("==============================\n")

    # Build Context
    context = "\n\n".join(
        [
            f"""
Document: {doc.metadata.get('document')}
Page: {doc.metadata.get('page')}

{doc.page_content}
"""
            for doc in docs
        ]
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
            "page": doc.metadata.get("page"),
            "snippet": doc.page_content[:200]
        })

    response = {
        "answer": answer,
        "sources": sources
    }

    cache_answer(
        question,
        response
    )

    log_question(
        question,
        sources
    )

    return response

def stream_answer(prompt):

    for chunk in llm.stream(prompt):
        yield chunk