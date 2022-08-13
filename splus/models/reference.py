from dataclasses import dataclass, field
from mashumaro.mixins.json import DataClassJSONMixin

from splus.models.href import Href

@dataclass
class Reference(DataClassJSONMixin):
  href: Href
  total: int