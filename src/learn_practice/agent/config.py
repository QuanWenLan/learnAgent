"""Agent 配置：API 地址、密钥、模型等常量集中在这里，代码中统一引用。

与 agentClaw 项目共用同一个网关，密钥同样从项目根目录的 .env 读取，
配置方式保持一致（.env 已被 .gitignore 忽略，不会进入 Git 仓库）。
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# 按本文件位置定位项目根目录的 .env，避免因运行时工作目录不同而读取失败
_ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(_ROOT_DIR / ".env")

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise RuntimeError("缺少 API_KEY：请复制 .env.example 为 .env 并填入真实密钥")

BASE_URL = os.getenv("BASE_URL", "")
MODEL = "gpt-5.5"
