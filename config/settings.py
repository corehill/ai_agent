import os
from dotenv import load_dotenv

# Python后端技能：环境变量统一管理，全局配置中心化
load_dotenv()

# LLM
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("BASE_URL")
LLM_TEMP = float(os.getenv("LLM_TEMPERATURE", 0.05))

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# 向量库
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_data")

OCR_MODEL_DIR  = os.getenv("OCR_MODEL_DIR", "./models")

# 接口鉴权
VALID_API_KEYS = {
    "sk-ai-2026-001": "internal_app"
}

# 生产模型加载策略
MODEL_PREHEAT = os.getenv("MODEL_PREHEAT", "true") == "true"  # 启动预热
MODEL_USE_GPU = os.getenv("MODEL_USE_GPU", "false") == "true"