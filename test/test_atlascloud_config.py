import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import atlascloud_config as atlascloud


def test_resolves_atlascloud_alias_to_default_model_and_env_key():
    env = {"ATLASCLOUD_API_KEY": "test-key"}

    model, api_key, base_url = atlascloud.resolve_atlascloud_request("atlascloud", environ=env)

    assert model == "qwen/qwen3.5-flash"
    assert api_key == "test-key"
    assert base_url == "https://api.atlascloud.ai/v1/"


def test_resolves_prefixed_atlascloud_model_without_rewriting_model_id():
    env = {"ATLASCLOUD_API_KEY": "test-key"}

    model, api_key, base_url = atlascloud.resolve_atlascloud_request(
        "atlascloud/deepseek-ai/deepseek-v4-pro",
        environ=env,
    )

    assert model == "deepseek-ai/deepseek-v4-pro"
    assert api_key == "test-key"
    assert base_url == "https://api.atlascloud.ai/v1/"


def test_atlascloud_base_url_uses_env_key_when_key_is_empty():
    env = {"ATLAS_CLOUD_API_KEY": "fallback-key"}

    model, api_key, base_url = atlascloud.resolve_atlascloud_request(
        "qwen/qwen3.5-flash",
        base_url="https://api.atlascloud.ai/v1/",
        environ=env,
    )

    assert model == "qwen/qwen3.5-flash"
    assert api_key == "fallback-key"
    assert base_url == "https://api.atlascloud.ai/v1/"


def test_env_reference_resolution():
    env = {"ATLASCLOUD_API_KEY": "test-key"}

    assert atlascloud.resolve_env_reference("env:ATLASCLOUD_API_KEY", env) == "test-key"


if __name__ == "__main__":
    test_resolves_atlascloud_alias_to_default_model_and_env_key()
    test_resolves_prefixed_atlascloud_model_without_rewriting_model_id()
    test_atlascloud_base_url_uses_env_key_when_key_is_empty()
    test_env_reference_resolution()
