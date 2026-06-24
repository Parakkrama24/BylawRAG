query_cache = {}


def get_cached_answer(session_id, question):

    cache_key = f"{session_id}:{question.strip().lower()}"

    return query_cache.get(cache_key)


def cache_answer(session_id, question, answer):

    cache_key = f"{session_id}:{question.strip().lower()}"

    query_cache[cache_key] = answer