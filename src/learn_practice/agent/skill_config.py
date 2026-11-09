"""Markdown skill 配置加载模块。

该模块负责读取 `docs/skills/*.md` 中的 front matter 和提示词正文，
将 Markdown 文件转换为运行时可使用的 `SkillConfig` 对象。
"""

import os
import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SkillConfig:
    """描述一个可由 Markdown 文件配置的 skill。"""

    name: str
    description: str
    intent: str
    tools: List[str]
    input_hint: str
    prompt_markdown: str
    file_path: str


class SkillConfigLoader:
    """加载并解析 skill Markdown 配置文件。"""

    def __init__(self, docs_dir: str):
        """初始化加载器。

        Args:
            docs_dir: skill Markdown 文件所在目录。
        """
        self.docs_dir = docs_dir

    def load_all(self) -> Dict[str, SkillConfig]:
        """读取目录下全部 skill 配置，并按意图名称建立索引。"""
        configs = {}
        for file_name in os.listdir(self.docs_dir):
            if not file_name.endswith('.md'):
                continue
            if file_name == 'overview.md':
                continue
            file_path = os.path.join(self.docs_dir, file_name)
            config = self.load_one(file_path)
            configs[config.intent] = config
        return configs

    def load_one(self, file_path: str) -> SkillConfig:
        """读取并解析单个 skill Markdown 文件。"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        front_matter, prompt_markdown = self._split_front_matter(content)
        metadata = self._parse_front_matter(front_matter)
        tools = metadata.get('tools', [])
        return SkillConfig(
            name=metadata.get('name', ''),
            description=metadata.get('description', ''),
            intent=metadata.get('intent', ''),
            tools=tools,
            input_hint=metadata.get('input_hint', ''),
            prompt_markdown=prompt_markdown.strip(),
            file_path=file_path
        )

    def _split_front_matter(self, content: str):
        """分离 Markdown 文件的 front matter 与提示词正文。"""
        if not content.startswith('---'):
            raise ValueError('skill markdown 缺少 front matter。')
        parts = content.split('---', 2)
        if len(parts) < 3:
            raise ValueError('skill markdown front matter 格式不完整。')
        return parts[1].strip(), parts[2].strip()

    def _parse_front_matter(self, front_matter: str) -> dict:
        """解析简单的 YAML 风格元数据，支持字符串和字符串列表。"""
        metadata = {}
        current_list_key = None
        for raw_line in front_matter.splitlines():
            line = raw_line.rstrip()
            if not line:
                continue
            list_match = re.match(r'^\s*-\s*(.+)$', line)
            if list_match and current_list_key:
                metadata[current_list_key].append(list_match.group(1).strip())
                continue
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value == '[]':
                metadata[key] = []
                current_list_key = None
                continue
            if value == '':
                metadata[key] = []
                current_list_key = key
                continue
            metadata[key] = value
            current_list_key = None
        return metadata
