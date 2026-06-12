query_cache = {}


def get_cached_answer(question):

    return query_cache.get(question)


def cache_answer(question, answer):

    query_cache[question] = answer