from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit
from mashumaro.types import SerializableType

@dataclass
class Href(SerializableType):
  scheme: str
  netloc: str
  path: str
  path_sections: list[str]
  query: str
  fragment: str

  def _serialize(self) -> str:
    return urlunsplit((self.scheme, self.netloc, self.path, self.query, self.fragment))
  
  @classmethod
  def _deserialize(cls, value : str) -> 'Href':
    scheme, netloc, path, query, fragment = urlsplit(value)
    path_sections = path.lstrip('/').rstrip('/').split('/')
    return Href(scheme, netloc, path, path_sections, query, fragment)

  def __repr__(self) -> str:
    return self._serialize()