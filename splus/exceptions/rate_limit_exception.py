from splus.exceptions.base_exception import BaseRequestException

class RateLimitException(BaseRequestException):
  def __repr__(self) -> str:
    return self._get_error_message("App exceeded rate limit")