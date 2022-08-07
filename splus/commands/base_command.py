import abc
from splus.auth.access_token import AccessToken
from splus.utils.spotify_session import SpotifySession

class BaseCommand(abc.ABC):
  def __init__(self, session : SpotifySession):
    self._session = session
  
  @abc.abstractmethod
  def run(self):
    pass