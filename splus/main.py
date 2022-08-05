from splus.auth import authenticate

def main():
  print("Congrats its running!")
  auth = authenticate.Authenticate()
  auth.request_permission()
  token = auth.get_token()
  print(token.scope, token.expires_in)


if __name__ == "__main__":
  main()