from abc import ABC

from splus.utils.spotify_session import SpotifySession

class BaseEndpoint(ABC):
  def __init__(self, session : SpotifySession):
    self._session = session
  