import os


ATLASCLOUD_DEFAULT_BASE_URL = "https://api.atlascloud.ai/v1/"
ATLASCLOUD_DEFAULT_MODEL = "qwen/qwen3.5-flash"
ATLASCLOUD_REASONING_MODEL = "deepseek-ai/deepseek-v4-pro"
ATLASCLOUD_MODEL_ALIASES = {"atlas", "atlascloud", "atlas-cloud"}
ATLASCLOUD_MODEL_PREFIXES = ("atlas/", "atlascloud/", "atlas-cloud/")


def resolve_env_reference(value, environ=None):
    if value is None:
        return ""
    value = str(value).strip()
    if not value.startswith("env:"):
        return value

    environ = environ or os.environ
    return environ.get(value[4:].strip(), "")


def get_atlascloud_api_key(environ=None):
    environ = environ or os.environ
    return environ.get("ATLASCLOUD_API_KEY") or environ.get("ATLAS_CLOUD_API_KEY") or ""


def get_atlascloud_base_url(environ=None):
    environ = environ or os.environ
    return (
        environ.get("ATLASCLOUD_API_BASE")
        or environ.get("ATLAS_CLOUD_API_BASE")
        or ATLASCLOUD_DEFAULT_BASE_URL
    )


def is_atlascloud_base_url(base_url):
    return "api.atlascloud.ai" in str(base_url or "").lower()


def is_atlascloud_model_alias(model_name):
    normalized = str(model_name or "").strip().lower()
    return normalized in ATLASCLOUD_MODEL_ALIASES or normalized.startswith(ATLASCLOUD_MODEL_PREFIXES)


def resolve_atlascloud_model_name(model_name):
    value = str(model_name or "").strip()
    normalized = value.lower()
    if normalized in ATLASCLOUD_MODEL_ALIASES:
        return ATLASCLOUD_DEFAULT_MODEL
    for prefix in ATLASCLOUD_MODEL_PREFIXES:
        if normalized.startswith(prefix):
            return value[len(prefix) :]
    return value


def resolve_atlascloud_request(model_name, api_key="", base_url="", environ=None):
    environ = environ or os.environ
    uses_atlascloud = is_atlascloud_model_alias(model_name) or is_atlascloud_base_url(base_url)
    model_name = resolve_atlascloud_model_name(model_name)
    api_key = resolve_env_reference(api_key, environ)
    base_url = resolve_env_reference(base_url, environ)

    if uses_atlascloud or is_atlascloud_base_url(base_url):
        api_key = api_key or get_atlascloud_api_key(environ)
        base_url = base_url or get_atlascloud_base_url(environ)

    return model_name, api_key, base_url
