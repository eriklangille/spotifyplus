import os
from dotenv import load_dotenv
load_dotenv()

DEFAULT_PORT = 8888
RESPONSE_TYPE = "code"
STATE = "state"
GRANT_TYPE = "authorization_code"
GRANT_TYPE_REFRESH = "refresh_token"
REDIRECT_URI = f"http://localhost:{DEFAULT_PORT}/callback"
SCOPE = "playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private"
AUTH_URI = "https://accounts.spotify.com/authorize?"
TOKEN_URI = "https://accounts.spotify.com/api/token"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")