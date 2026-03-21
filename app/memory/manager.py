import os
from mem0 import Memory
from app.memory.config import get_mem0_config
from app.core.config import settings

class AgentMemoryManager:
    """Agent 专用高级记忆管理器，屏蔽底层 Qdrant 与向量处理逻辑"""
    def __init__(self):
        # 确保环境变量存在（Mem0 内部会读取 OPENAI_API_KEY）
        if settings.llm_api_key:
            os.environ["OPENAI_API_KEY"] = settings.llm_api_key
            
        # 根据我们配置的 qdrant-local 实例化全局内存池
        self.memory = Memory.from_config(get_mem0_config())

    def add_memory(self, text: str, user_id: str, agent_id: str = "tutor"):
        """让大模型提炼事实，并插入（或更新合并）到本地向量库"""
        return self.memory.add(
            text,            
            user_id=user_id, 
            agent_id=agent_id
        )

    def search_context(self, query: str, user_id: str, agent_id: str = "tutor", limit: int = 5):
        """当用户提问时，Agent 用此方法把可能相关的“旧知识/旧偏好”提取出来"""
        results = self.memory.search(
            query=query, 
            user_id=user_id, 
            agent_id=agent_id, 
            limit=limit
        )
        return results

    def get_all_preferences(self, user_id: str):
        """直观获取大模型为特定用户做的所有画像或记忆点"""
        return self.memory.get_all(user_id=user_id)

    def clear(self, user_id: str):
        """重置某个用户的世界线"""
        return self.memory.delete_all(user_id=user_id)

# 单例模式，整个引擎复用一个长生管理器
memory_manager = AgentMemoryManager()
