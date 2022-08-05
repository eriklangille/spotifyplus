from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin

@dataclass
class AccessToken(DataClassJSONMixin):
  access_token: str
  token_type: str
  scope: str
  expires_in: int
  refresh_token: str
