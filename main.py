from fastapi import FastAPI
from api import kb_api, chat_api
from core.model_manager import model_mgr
from config.settings import MODEL_PREHEAT
from core.embedding import init_embedding
from core.rerank import init_rerank
from rag.ocr_parser import init_ocr_engine

app = FastAPI(title="AI Agent 生产级工程化服务")

if MODEL_PREHEAT:
    model_mgr.preheat_all([
        init_embedding,
        init_rerank,
        init_ocr_engine
    ])

# 挂载路由
app.include_router(kb_api.router, prefix="/kb")
app.include_router(chat_api.router, prefix="/chat")

@app.get("/health")
def health():
    return {"status": "ok"}