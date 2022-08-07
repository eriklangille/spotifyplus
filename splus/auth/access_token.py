import datetime
from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin

@dataclass
class AccessToken(DataClassJSONMixin):
  access_token: str
  token_type: str
  scope: str
  expires_in: int
  refresh_token: str
  created_datetime : datetime.datetime = datetime.datetime.now()

  def is_expired(self):
    return datetime.datetime.now() >= self.created_datetime + datetime.timedelta(seconds=float(self.expires_in))
