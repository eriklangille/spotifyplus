from splus.auth import authenticate
from splus.commands.copy_playlist import CopyPlaylist
from splus.utils.spotify_session import SpotifySession

def main():
  print("Congrats its running!")
  auth = authenticate.Authenticate()
  token = auth.authenticate()
  session = SpotifySession(token)
  print(token.scope, token.expires_in)
  copy = CopyPlaylist(session)
  copy.run()


if __name__ == "__main__":
  main()