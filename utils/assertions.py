from utils.exceptions import RateLimitExceededException

def check_rate_limit(response):
    """
    Call this after every API response
    Raises RateLimitExceededException if the response indicates a rate limit has been exceeded.
    """
    if response.status_code == 405:
        raise RateLimitExceededException(
            f"Daily request limit reached (405). "
            f"URL: {response.url} | "
            f"Response: {response.text}"
        )