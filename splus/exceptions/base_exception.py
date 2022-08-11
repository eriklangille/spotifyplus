from splus.models.error import Error

class BaseRequestException(Exception):
  def __init__(self, error : Error):
    self.error = error
  
  def _get_error_message(self, info: str) -> str:
    return f"{info}. Message: {self.error.message}"