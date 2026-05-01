from typing import Dict, Any
import threading
from common.logger import logger
from config.settings import MODEL_USE_GPU, OCR_MODEL_DIR

class ModelManager:
    _instance = None
    _lock = threading.Lock()
    _model_cache: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def get_model(self, model_key: str, init_func):
        """
        获取模型，不存在则初始化并缓存
        :param model_key: 模型唯一标识
        :param init_func: 模型初始化函数
        """
        if model_key not in self._model_cache:
            with self._lock:
                if model_key not in self._model_cache:
                    logger.info(f"初始化模型： {model_key}")
                    self._model_cache[model_key] = init_func()
        return self._model_cache[model_key]

    def preheat_all(self, preheat_func_list):
        """服务启动主动预热所有模型"""
        logger.info("========== 开始模型启动预热 ==========")
        for func in preheat_func_list:
            func()

        logger.info("========== 所有模型预热完成 ==========")


model_mgr = ModelManager()
