from langchain_community.vectorstores import Chroma
from app.rag.embedding import get_embedding_model
from langchain_chroma import Chroma

embedding_model = get_embedding_model()

VECTOR_DB_PATH = "data/vectordb"


def create_vector_store(documents):

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=VECTOR_DB_PATH
    )

    return vector_store


def load_vector_store():

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embedding_model
    )

    return vector_store


def similarity_search(query: str, k: int = 5):

    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )

    return results