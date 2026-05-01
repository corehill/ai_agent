from paddleocr import PaddleOCR
from common.logger import logger
from config.settings import OCR_MODEL_DIR, MODEL_USE_GPU
from core.model_manager import model_mgr


# ======================
# Python 后端生产级技能
# 1. 模型路径从配置读取，不硬编码
# 2. 全局单例，服务启动加载一次（sync.Once 效果）
# 3. 纯离线，禁止联网下载模型
# 4. 关闭日志，降低生产干扰
# 5. 异常捕获，服务不崩溃
# ======================

# 生产级离线OCR引擎（最终稳定版）
def init_ocr_engine():
    return PaddleOCR(
        # 基础配置
        use_angle_cls=True,     # 倾斜图片自动矫正（生产必备）
        lang="ch",              # 中文
        use_gpu=MODEL_USE_GPU,          # 生产CPU环境
        enable_mkldnn=True,     # CPU加速（生产必开）
        use_tensorrt=False,

        # 【离线核心】本地模型目录（配置化，不从网络下载）
        det_model_dir=f"{OCR_MODEL_DIR}/det",
        rec_model_dir=f"{OCR_MODEL_DIR}/rec",
        cls_model_dir=f"{OCR_MODEL_DIR}/cls",

        # 生产环境必须关闭
        show_log=False,         # 关闭PaddleOCR杂乱日志
        use_onnx=False,
        download_enabled=False  # 强制离线，绝对禁止联网下载
    )

ocr_engine = model_mgr.get_model("paddle_ocr", init_ocr_engine)

def image_ocr_to_text(img_path: str) -> str:
    """
    图片OCR识别：截图、照片、扫描件提取纯文本
    return: 拼接后的完整文本
    """
    try:
        result = ocr_engine.ocr(img_path, cls=True)
        text_lines = []
        for res in result:
            for line in res:
                text = line[1][0]
                text_lines.append(text)

        full_text = "".join(text_lines)
        logger.info(f"OCR识别完成 {img_path} 提取行数：{len(text_lines)}")
        return full_text
    except Exception as e:
        logger.error(f"OCR识别失败：{str(e)}")
        raise