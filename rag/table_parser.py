import os
import pandas as pd
from langchain_core.documents import Document
from common.logger import logger
from rag.ocr_parser import image_ocr_to_text

def parse_excel(file_path: str) -> list[Document]:
    docs = []
    excel_file = pd.ExcelFile(file_path)

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        table_text = f"工作表： {sheet_name}\n"
        table_text += df.to_string(index=False)

        docs.append(Document(page_content=table_text,
                             metadata= {"source": file_path, "type": "excel", "sheet": sheet_name}
                             ))

    logger.info(f"Excel解析完成：{file_path}，工作表数：{len(excel_file.sheet_names)}")
    return docs

def parse_image_table(file_path: str) -> list[Document]:
    text = image_ocr_to_text(file_path)
    return [Document(
        page_content=f"图片表格内容：\n{text}",
        metadata={"source": file_path, "type": "image_table"}
    )]