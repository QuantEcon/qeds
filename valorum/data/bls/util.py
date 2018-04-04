import string
import warnings
from ..config import _get_option


def validate_api_key(key):
    API_KEY_LENGTH = 32
    if len(key) > API_KEY_LENGTH:
        key = key[:API_KEY_LENGTH]
        msg = "API key too long, using first {} characters".format(API_KEY_LENGTH)
        warnings.warn(msg)
    elif len(key) < API_KEY_LENGTH:
        msg = "API key {} too short. Should be {} chars".formaT(key, API_KEY_LENGTH)
        raise ValueError(msg)

    if not all(i in string.hexdigits for i in key):
        msg = "API key {} contains invalid characters".format(key)
        raise ValueError(msg)


_get_option("bls", "api_key").validator = validate_api_key


LIMITS = {
    "years_per_query": 20,
    "series_per_query": 50,
}

# see https://www.bls.gov/developers/api_faqs.htm
BLS_STATUS_CODE_REASONS = {
    400: "Your request did not follow the correct syntax.",
    401: "You are not authorized to make this request.",
    404: "Your request was not found and/or does not exist.",
    429: "You have made too many requests.",
    500: ("The server has encountered an unexpected condition, and the " +
          "request cannot be completed.")
}
