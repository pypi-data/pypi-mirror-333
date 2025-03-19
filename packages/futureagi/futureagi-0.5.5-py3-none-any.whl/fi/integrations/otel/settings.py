import logging
import os
import urllib
import uuid
from re import compile
from typing import Dict, List, Optional

from dotenv import load_dotenv
from opentelemetry.sdk.trace.id_generator import IdGenerator

from fi.utils.constants import BASE_URL, FI_PROJECT_NAME, FI_PROJECT_VERSION_NAME

logger = logging.getLogger(__name__)


def load_environment_variables():
    """
    Load environment variables from .env file if it exists
    """
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        ".env",
    )
    print("ENV PATH :", env_path)
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logger.info(f"Loaded environment variables from {env_path}")
    else:
        logger.warning("No .env file found")


load_environment_variables()


def get_env_collector_endpoint() -> Optional[str]:
    return BASE_URL or "http://localhost:8000"


def get_env_project_name() -> str:
    return FI_PROJECT_NAME or "DEFAULT_PROJECT_NAME"


def get_env_project_version_name() -> str:
    return FI_PROJECT_VERSION_NAME or "DEFAULT_PROJECT_VERSION_NAME"


def get_env_fi_auth_header() -> Optional[Dict[str, str]]:
    api_key = os.environ.get("FI_API_KEY")
    secret_key = os.environ.get("FI_SECRET_KEY")
    if api_key and secret_key:
        return {"X-Api-Key": api_key, "X-Secret-Key": secret_key}
    return None


# Optional whitespace
_OWS = r"[ \t]*"
# A key contains printable US-ASCII characters except: SP and "(),/:;<=>?@[\]{}
_KEY_FORMAT = r"[\x21\x23-\x27\x2a\x2b\x2d\x2e\x30-\x39\x41-\x5a\x5e-\x7a\x7c\x7e]+"
# A value contains a URL-encoded UTF-8 string. The encoded form can contain any
# printable US-ASCII characters (0x20-0x7f) other than SP, DEL, and ",;/
_VALUE_FORMAT = r"[\x21\x23-\x2b\x2d-\x3a\x3c-\x5b\x5d-\x7e]*"
# A key-value is key=value, with optional whitespace surrounding key and value
_KEY_VALUE_FORMAT = rf"{_OWS}{_KEY_FORMAT}{_OWS}={_OWS}{_VALUE_FORMAT}{_OWS}"

_HEADER_PATTERN = compile(_KEY_VALUE_FORMAT)
_DELIMITER_PATTERN = compile(r"[ \t]*,[ \t]*")


def parse_env_headers(s: str) -> Dict[str, str]:
    """
    Parse ``s``, which is a ``str`` instance containing HTTP headers encoded
    for use in ENV variables per the W3C Baggage HTTP header format at
    https://www.w3.org/TR/baggage/#baggage-http-header-format, except that
    additional semi-colon delimited metadata is not supported.

    If the headers are not urlencoded, we will log a warning and attempt to urldecode them.
    """
    headers: Dict[str, str] = {}
    headers_list: List[str] = _DELIMITER_PATTERN.split(s)

    for header in headers_list:
        if not header:  # empty string
            continue

        match = _HEADER_PATTERN.fullmatch(header.strip())
        if not match:
            parts = header.split("=", 1)
            name, value = parts
            encoded_header = f"{urllib.parse.quote(name)}={urllib.parse.quote(value)}"
            match = _HEADER_PATTERN.fullmatch(encoded_header.strip())
            if not match:
                logger.warning(
                    "Header format invalid! Header values in environment variables must be "
                    "URL encoded: %s",
                    f"{name}: ****",
                )
                continue
            logger.warning(
                "Header values in environment variables should be URL encoded, attempting to "
                "URL encode header: {name}: ****"
            )

        name, value = header.split("=", 1)
        name = urllib.parse.unquote(name).strip().lower()
        value = urllib.parse.unquote(value).strip()
        headers[name] = value

    return headers


class UuidIdGenerator(IdGenerator):
    def generate_trace_id(self) -> int:
        # Generate a 32-character UUID trace ID (128-bit hexadecimal string)
        uuid_trace_id = uuid.uuid4().hex
        return int(uuid_trace_id, 16)

    def generate_span_id(self) -> int:
        # Generate a 16-character span ID (64-bit hexadecimal string)
        uuid_span_id = uuid.uuid4().hex[:16]
        return int(uuid_span_id, 16)
