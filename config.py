# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - 配置文件
Configuration file for API keys and settings
"""

import os
from typing import Optional

# LLM API 配置
# OpenAI 兼容接口配置
# 支持 OpenAI, Azure OpenAI, 通义千问, 智谱AI, DeepSeek 等
# API_KEY: str = os.getenv("OPENAI_API_KEY", "your-api-key-here")
# API_BASE_URL: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
# MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# OpenAI配置
API_KEY = "sk-enjuilxyOwCDla1n0dEeCc8cAf224930A9D79330F3AcEcBb"
API_BASE_URL = "https://api.aigc369.com/v1"
MODEL_NAME = "gpt-3.5-turbo"

# 服务器配置
BACKEND_HOST: str = "127.0.0.1"
BACKEND_PORT: int = 8000
BACKEND_URL: str = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# 系统配置
SYSTEM_NAME: str = "AI 智能辅助学习系统"
SYSTEM_VERSION: str = "v1.0.0"

# 评估等级配置
GRADE_A_THRESHOLD: float = 0.85  # A级理解阈值
GRADE_B_THRESHOLD: float = 0.60  # B级理解阈值
MAX_RETRY_COUNT: int = 3  # 最大重试次数

# 验证配置
def validate_config() -> bool:
    """验证配置是否有效"""
    if API_KEY == "your-api-key-here" or not API_KEY:
        print("⚠️ 警告: 请在 config.py 中配置您的 API_KEY")
        return False
    return True

def get_config_summary() -> dict:
    """获取配置摘要"""
    return {
        "api_configured": API_KEY != "your-api-key-here",
        "api_base_url": API_BASE_URL,
        "model_name": MODEL_NAME,
        "backend_url": BACKEND_URL,
        "system_version": SYSTEM_VERSION
    }
