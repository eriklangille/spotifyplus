from requests import Response
from splus.commands.base_command import BaseCommand
from splus import constants

PLAYLIST_ID = "1nYXOKEmZXnXRp31dCO031"

class CopyPlaylist(BaseCommand):
  def run(self):
    res : Response = self._session.get(f'playlists/{PLAYLIST_ID}/tracks')
    print(res.text)
