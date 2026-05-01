from fastapi import APIRouter, UploadFile, File, Query
import os
from datetime import datetime
from common.logger import logger
from common.auth import check_api_key
from rag.parser import load_document
from rag.splitter import splitter
from core.vector_store import get_kb_vdb
from config.settings import CHROMA_DIR

router = APIRouter()

# 临时目录确保存在
os.makedirs("./tmp", exist_ok=True)

@router.post("/upload")
async def upload_file(kb_id: str =Query(...),
                      file: UploadFile = File(...),
                      api_key: str = check_api_key,
                      ):
    suffix = os.path.splitext(file.filename)[-1]
    tmp_file_name = f"{datetime}{suffix}"
    tmp_path = f"./tmp/{tmp_file_name}"

    with open(tmp_path, "wb") as f:
        f.write(await file.read())

    try:
        docs = load_document(tmp_path)
        chunks = splitter.split_documents(docs)
        get_kb_vdb(kb_id).add_documents(chunks)
        logger.info(f"知识库入库完成 kb_id:{kb_id} 分片数:{len(chunks)}")
        return {
            "code": 200,
            "msg": "上传并入库成功",
            "kb_id": kb_id,
            "chunk_count": len(chunks)
        }
    finally:
        # 无论成功失败，都删除临时文件
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
