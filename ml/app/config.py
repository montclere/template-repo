from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    prompts_dir: str = "prompts"

    llm_base_url: str = "https://api.anthropic.com"
    llm_api_version: str = "2023-06-01"
    llm_model: str = ""
    anthropic_api_key: str = ""
    llm_max_tokens: int = 1024
    llm_timeout_seconds: float = 60
    llm_max_retries: int = 2
    llm_retry_delay_seconds: float = 1.0
    llm_log_path: str = "logs/llm.log.jsonl"
    llm_log_text: bool = True


settings = Settings()
