import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from common.logger import logger
from langchain_core.documents import Document
from rag.ocr_parser import extract_text_from_image
from rag.table_parser import parse_image_table, parse_excel

IMAGE_SUFFIX = [".jpg", ".jpeg", ".png", ".bmp"]
EXCEL_TYPES = [".xlsx", ".xls", ".csv"]
DOC_TYPES = [".pdf", ".docx"]


def load_document(filepath: str):
    """
    自动识别 PDF / DOCX 并解析
    return: List[Document]
    """
    ext = Path(filepath).suffix.lower()
    try:
        if ext in IMAGE_SUFFIX:
            return parse_image_table(filepath)
        if ext in EXCEL_TYPES:
            return parse_excel(filepath)
        elif ext == ".pdf":
            return PyPDFLoader(filepath).load()
        elif ext == ".docx":
            return Docx2txtLoader(filepath).load()
        else:
            raise ValueError(f"不支持文件类型: {ext}")

        docs = loader.load()
        logger.info(f"文档解析成功 {filepath} 页数/段落数: {len(docs)}")
        return docs
    except Exception as e:
        logger.error(f"文档解析失败 {filepath}: {str(e)}")
        raise