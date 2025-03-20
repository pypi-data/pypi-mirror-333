from plexflow.core.context.partial_context import PartialContext
from typing import List
from qbittorrentapi.torrents import TorrentDictionary

class MovieAssets(PartialContext):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def all(self) -> List[TorrentDictionary]:
        return self.get("download/completed")

    def movie_path(self) -> str:
        return self.get("assets/movie/path")

    def subtitle_paths(self) -> List[str]:
        return self.get("assets/subtitle/path")

    def update_movie_path(self, path: str):
        self.set("assets/movie/path", path)

    def update_subtitle_paths(self, paths: List[str]):
        self.set("assets/subtitle/path", paths)
