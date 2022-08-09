from requests import Response
from splus.commands.base_command import BaseCommand
from splus import constants
from splus.models.page import Page

PLAYLIST_ID = "1nYXOKEmZXnXRp31dCO031"

# Copies a playlist to a specified playlist, otherwise creating a new playlist. Override to delete all existing songs within the new playlist
class CopyPlaylist(BaseCommand):
  def run(self, old_playlist=PLAYLIST_ID, new_playlist : str = None):
    res : Response = self._session.get(f'playlists/{old_playlist}/tracks')
    result = res.json()
    page = Page.from_dict(result)
    for item in page.items: 
      print(item.track.href)
