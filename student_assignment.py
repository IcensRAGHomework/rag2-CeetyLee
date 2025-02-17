from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import (CharacterTextSplitter,
                                      RecursiveCharacterTextSplitter)

q1_pdf = "OpenSourceLicenses.pdf"
q2_pdf = "勞動基準法.pdf"


def hw02_1(q1_pdf):
    q1_loader = PyPDFLoader(q1_pdf)
    q1_docs = q1_loader.load()
    q1_spliter = CharacterTextSplitter(chunk_overlap = 0)
    q1_docs_chunks = q1_spliter.split_documents(q1_docs)
    print(f"docs count: {len(q1_docs_chunks)}")
    last_chunk = q1_docs_chunks[-1]
    print(f"last chunk: {last_chunk.metadata}")
    return last_chunk

def hw02_2(q2_pdf):
    q2_loader = PyPDFLoader(q2_pdf)
    q2_docs = q2_loader.load()
    q2_text = ""
    for doc in q2_docs:
        q2_text = q2_text + doc.page_content + "\n"
    
    chapter_sepatators = [r"(?:\n|^|\s*)第\s+(?:[一二三四五六七八九十百千萬]+|零)\s+章.*\n"]
    chapter_spliter = RecursiveCharacterTextSplitter(
        separators = chapter_sepatators,
        keep_separator = 'start',
        chunk_size = 500,
        chunk_overlap = 0,
        is_separator_regex = True
    )
    chapters = chapter_spliter.split_text(q2_text)

    q2_chunks = []
    session_separators = [r"(?:\n|^)第\s+[0-9]+(?:-[0-9]+)?\s+條.*\n"]
    session_spliter = RecursiveCharacterTextSplitter(
        separators = session_separators,
        keep_separator = 'start',
        chunk_size = 0,
        chunk_overlap = 0,
        is_separator_regex = True
    )
    for chapter in chapters:
        session_chunks = session_spliter.split_text(chapter)
        q2_chunks.extend(session_chunks)
    
    q2_chunks_count = len(q2_chunks)
    print("chunk_count={}".format(q2_chunks_count))

    return q2_chunks_count


#hw02_1(q1_pdf)
hw02_2(q2_pdf)