try:
    from .bootstrap import CURRENT_DIR
    from .skill_config import SkillConfigLoader
except ImportError:
    from bootstrap import CURRENT_DIR
    from skill_config import SkillConfigLoader


if __name__ == "__main__":
    loader = SkillConfigLoader(f"{CURRENT_DIR}/docs/skills")
    skill_configs = loader.load_all()
    for intent, config in skill_configs.items():
        print("=" * 80)
        print(f"intent: {intent}")
        print(f"name: {config.name}")
        print(f"description: {config.description}")
        print(f"tools: {config.tools}")
        print(f"input_hint: {config.input_hint}")
        print("prompt:")
        print(config.prompt_markdown)
