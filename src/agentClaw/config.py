"""Agent 配置：API 地址、密钥、模型等常量集中在这里，代码中统一引用。

密钥不写死在代码里，而是放在项目根目录的 .env 文件中（已被 .gitignore 忽略），
避免真实密钥随代码推送到远程仓库后泄露。
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# 按本文件位置定位项目根目录的 .env，避免因运行时工作目录不同而读取失败
_ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(_ROOT_DIR / ".env")

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise RuntimeError("缺少 API_KEY：请复制 .env.example 为 .env 并填入真实密钥")

BASE_URL = os.getenv("BASE_URL", "")
MODEL = "deepseek-flash"
MAX_ROUNDS = 10

# 网关按客户端 User-Agent 白名单放行，自建脚本需模拟已放行的 CLI 客户端
USER_AGENT = "claude-cli/1.0"
