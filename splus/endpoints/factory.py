from splus.auth.access_token import AccessToken
from splus.endpoints.users import UserEndpoints
from splus.utils.spotify_session import SpotifySession
from splus.auth.access_token import AccessToken
from splus.endpoints.playlists import PlaylistEndpoints

class Endpoints:
  def __init__(self, token : AccessToken):
    session = SpotifySession(token)
    self.playlists = PlaylistEndpoints(session)
    self.users = UserEndpoints(session)