from pydantic import BaseModel

class MemoryConfig(BaseModel):
    # 使用 Qdrant 的本地磁盘模式，免除启动 Docker 的烦恼
    vector_store: dict = {
        "provider": "qdrant",
        "config": {
            "path": "data/qdrant",             # 本地数据落盘到 data/qdrant 目录下
            "collection_name": "agent_memory", # 集合名称
        }
    }
    
    # 默认大模型用于评估和抽取“记忆更新点” (基于你 .env 的 api key)
    llm: dict = {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.0
        }
    }
    
    # 词向量模型，用于 Qdrant 高维检索
    embedder: dict = {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    }

def get_mem0_config() -> dict:
    return MemoryConfig().model_dump()
