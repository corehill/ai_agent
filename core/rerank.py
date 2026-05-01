from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from core.model_manager import model_mgr

def init_rerank():
    return HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")

rerank_model = model_mgr.get_model("bge_rerank", init_rerank)