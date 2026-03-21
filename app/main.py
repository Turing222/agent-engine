from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import api_router
from app.core.logfire import setup_observability

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化核心基础设施：可观测性监控、数据库连接池等
    setup_observability(app)
    
    yield
    # 清理退出（比如关闭 HTTPX 会话、关闭 SQLite 连接等）

app = FastAPI(title="Agent Engine API", version="0.1.0", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")
