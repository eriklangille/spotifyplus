from splus.commands.base_command import BaseCommand

# Copies a playlist to a specified playlist, otherwise creating a new playlist.
class CopyPlaylist(BaseCommand):
  def run(self, copy_from : str, copy_to : str = None):
    playlist = self._endpoints.playlists.get_playlist(copy_from)
    uris = list(map(lambda item: item.track.uri, playlist.tracks.items))

    if not copy_to:
      user = self._endpoints.users.get_me()
      new_playlist = self._endpoints.playlists.create_playlist(user.id, playlist.name + " Copy", description=playlist.description)
      copy_to = new_playlist.id

    self._endpoints.playlists.add_playlist_items(copy_to, uris)
