from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_documents(pages, filename):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120
    )

    docs = []

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk in chunks:

            docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "document": filename,
                        "page": page["page"]
                    }
                )
            )

    return docs