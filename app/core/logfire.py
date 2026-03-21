import logfire
import os
from fastapi import FastAPI
from app.core.config import settings

def setup_observability(app: FastAPI):
    """
    初始化大模型与 Web 应用的全链路追踪可观测性 (Observability)
    """
    # 核心判断：如果有 Token(海外云)，或者配了本地的 OTEL 导出器(国内本地)，则开启监控
    if settings.logfire_token or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
        
        # 1. 初始化，开启 Pydantic 深度参数捕获
        logfire.configure(
            send_to_logfire=bool(settings.logfire_token), 
            pydantic_plugin=logfire.PydanticPlugin(record="all")
        )
        
        # 2. 自动追踪 FastAPI：每一个请求进来、报错、耗时，都会形成一层包裹
        logfire.instrument_fastapi(app)
        
        # 3. 自动追踪 HTTPX：Agent 调 MLOps 或者去网络搜索时，自动记录外网请求
        logfire.instrument_httpx()
        
        # 注意：不要手动 instrument PydanticAI！PydanticAI 内核级自带了与 Logfire 的绝佳配合。
        
        print("✅ [可观测性] Agent 引擎监控系统已启动 (Logfire / OTEL)")
    else:
        print("⚠️ [可观测性] 监控配置为空，正在以静默模式(裸奔)运行！")
