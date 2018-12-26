KEY_ENV_NAME = "SOCRATA_API_KEY"

# see https://dev.socrata.com/docs/response-codes.html
SOCRATA_STATUS_CODE_REASONS = {
    200: "Success",
    202: "Still processing",
    400: "Your request did not follow the correct syntax.",
    401: "You are not authorized to make this request.",
    403: "You are not authorized to access this resource",
    404: "Your request was not found and/or does not exist.",
    429: "You have made too many requests",
    500: "Server error"
}
