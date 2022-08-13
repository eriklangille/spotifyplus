from splus.exceptions.base_exception import BaseRequestException

class BadOauthToken(BaseRequestException):
  def __repr__(self) -> str:
    return self._get_error_message("Bad Oauth Request")