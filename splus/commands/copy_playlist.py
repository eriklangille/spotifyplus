from typing import Tuple
from splus.commands.base_command import BaseCommand

class CopyPlaylist(BaseCommand):
  def run(self, copy_from : str, copy_to : str = ""):
    playlist = self._endpoints.playlists.get_playlist(copy_from)
    uris = list(map(lambda item: item.track.uri, playlist.tracks.items))

    if not copy_to:
      user = self._endpoints.users.get_me()
      new_playlist = self._endpoints.playlists.create_playlist(user.id, playlist.name + " Copy", description=playlist.description)
      copy_to = new_playlist.id

    self._endpoints.playlists.add_playlist_items(copy_to, uris)
  
  def help(self) -> list[str]:
    return [
      "Copies a playlist to a specified playlist, otherwise creating a new playlist.",
      "The playlist ID to copy from",
      "The playlist ID to copy to. If not specified a new playlist is created"
    ]

  def name(self) -> Tuple[str, str]:
    return ("copy_playlist", "cp")
