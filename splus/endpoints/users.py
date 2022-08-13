from splus.endpoints.base_endpoint import BaseEndpoint
from splus.models.user import User

class UserEndpoints(BaseEndpoint):
  def get_me(self):
    res = self._session.get('me')
    return User.from_dict(res.json())