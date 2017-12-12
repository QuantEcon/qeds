DEFAULT_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
KEY_ENV_NAME = "BLS_API_KEY"

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
