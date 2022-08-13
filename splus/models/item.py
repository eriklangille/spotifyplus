import datetime
from dataclasses import dataclass, field
from mashumaro.mixins.json import DataClassJSONMixin

from splus.models.track import Track

@dataclass
class Item(DataClassJSONMixin):
  added_at: datetime.datetime = field(metadata={"deserialize": "pendulum"})
  added_by: dict
  is_local: bool
  primary_color: str or None
  track: Track
  video_thumbnail: dict