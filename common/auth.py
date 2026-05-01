from fastapi import Request, HTTPException
from config.settings import VALID_API_KEYS
from common.logger import logger

async def check_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key not in VALID_API_KEYS:
        logger.warning("非法访问 无效APIKey")
        raise HTTPException(status_code=401, detail="无权访问")
    return api_key