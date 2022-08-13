from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin

@dataclass
class Error(DataClassJSONMixin):
  status: int
  message: str

  def __repr__(self) -> str:
    return f"({self.status}) {self.message}"