from app.rag.memory.chat_memory import get_chat_history


def build_prompt(
        session_id,
        question,
        docs,
        prompt_template):

    history = get_chat_history(session_id)

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in history
        ]
    )

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

    return prompt_template.format(
        history=history_text,
        context=context,
        question=question
    )