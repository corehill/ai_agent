import logging

# Python后端技能：日志封装成独立工具类，全局统一格式
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    return logging.getLogger(__name__)

logger = setup_logger()