from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from config.settings import REDIS_URL

checkpointer = AsyncRedisSaver(REDIS_URL)
checkpointer.setup()