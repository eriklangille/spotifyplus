from splus.auth.access_token import AccessToken
from splus.auth.authenticate import Authenticate
from splus.auth.access_token_handler import AccessTokenHandler
from splus.commands.copy_playlist import CopyPlaylist
from splus.utils.spotify_session import SpotifySession

def main():
  print("Congrats its running!")
  auth = Authenticate()
  handler = AccessTokenHandler()
  token : AccessToken = None

  try:
    token = handler.load_token()
    if token.is_expired():
      handler.refresh_token(token)
  except:
    token = auth.authenticate()
    handler.save_token(token)

  session = SpotifySession(token)
  print(token.scope, token.expires_in)
  copy = CopyPlaylist(session)
  copy.run()


if __name__ == "__main__":
  main()