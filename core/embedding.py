from langchain_community.embeddings import HuggingFaceEmbeddings
from core.model_manager import model_mgr


def init_embedding():
    return HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

embedding = model_mgr.get_model("bge_embedding", init_embedding)