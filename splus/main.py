from splus.auth.access_token import AccessToken
from splus.auth.authenticate import Authenticate
from splus.auth.access_token_handler import AccessTokenHandler
from splus.commands.command_factory import CommandFactory
from splus.endpoints.factory import Endpoints

def main():
  auth = Authenticate()
  handler = AccessTokenHandler()
  token : AccessToken = None

  try:
    token = handler.load_token()
    if token.is_expired():
      handler.refresh_token(token)
      print(token.scope, token.expires_in)
  except:
    token = auth.authenticate()
    handler.save_token(token)
    print(token.scope, token.expires_in)

  endpoints = Endpoints(token)
  factory = CommandFactory(endpoints)
  factory.parse()

if __name__ == "__main__":
  main()
