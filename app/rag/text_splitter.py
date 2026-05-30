from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(text: str):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_text(text)

    return chunks