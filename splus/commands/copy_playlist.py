from splus.commands.base_command import BaseCommand
from splus.endpoints.playlists import PlaylistEndpoints

PLAYLIST_ID = "1nYXOKEmZXnXRp31dCO031"

# Copies a playlist to a specified playlist, otherwise creating a new playlist. Override to delete all existing songs within the new playlist
class CopyPlaylist(BaseCommand):
  def run(self, old_playlist=PLAYLIST_ID, new_playlist : str = None):
    playlists = PlaylistEndpoints(self._session)
    playlists.get_playlist(old_playlist)
    # page = playlists.get_playlist_items(old_playlist)
    # for item in page.items: 
    #   print(item.track.href)
