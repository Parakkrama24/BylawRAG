from app.log.retrieval_logger import log_question
from app.rag.retrival.retrieval import hybrid_search
from app.rag.llm.llm import llm
from app.rag.llm.prompts import RAG_PROMPT

from app.rag.memory.cache import (
    get_cached_answer,
    cache_answer
)

from app.rag.memory.chat_memory import (
    get_chat_history,
    add_message
)
from app.services.chat_session_service import update_session_title


def ask_question(session_id: str, question: str):

    # Cache Check
    cached = get_cached_answer(session_id,question)

    if cached:
        print("CACHE HIT")
        return cached

    # Retrieve Documents
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

    # Get Chat History
    history = get_chat_history(session_id)

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in history
        ]
    )

    # Build Retrieval Context
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

    # Build Prompt
    prompt = RAG_PROMPT.format(
        history=history_text,
        context=context,
        question=question
    )

    update_session_title(
        session_id,
        question
    )

    # Generate Answer
    answer = llm.invoke(prompt)

    # Save Conversation Memory
    add_message(
        session_id,
        "user",
        question
    )

    add_message(
        session_id,
        "assistant",
        answer
    )

    # Build Sources
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

    # Cache
    cache_answer(
        session_id,
        question,
        response
    )

    # Log Retrieval
    log_question(
        question,
        sources
    )

    return response


def stream_answer(prompt):

    for chunk in llm.stream(prompt):
        yield chunk