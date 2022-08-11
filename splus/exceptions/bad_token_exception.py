from splus.exceptions.base_exception import BaseRequestException

class BadTokenException(BaseRequestException):
  def __repr__(self) -> str:
    return self._get_error_message("Bad/Expired Token")