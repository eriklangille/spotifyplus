from typing import Tuple
from splus.commands.base_command import BaseCommand

# List all of the current user's playlists ids and name
class ListPlaylist(BaseCommand):
  def run(self):
    user = self._endpoints.users.get_me()
    playlists = self._endpoints.playlists.get_user_playlists(user.id)
    for playlist in playlists.items:
      print(playlist.id, playlist.name)
  
  def help(self) -> str:
    return "Lists all playlists created by the user."

  def name(self) -> Tuple[str, str]:
    return ("list_playlist", "lp")