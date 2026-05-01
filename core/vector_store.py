from langchain_chroma import Chroma
from langchain_core.embeddings import HuggingFaceEmbeddings
from config.settings import CHROMA_DIR

embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
def get_kb_vdb(kb_id: str):
    return Chroma(
        embedding_function=embedding,
        persist_directory=CHROMA_DIR,
        collection_name=kb_id,
    )