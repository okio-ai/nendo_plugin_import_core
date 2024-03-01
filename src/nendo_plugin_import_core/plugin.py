from typing import List, Any
import time
import os
import yt_dlp
from pathlib import Path
import requests
from tqdm import tqdm

from nendo import Nendo, NendoGeneratePlugin, NendoConfig, NendoTrack, NendoError
from nendo.utils import AudioFileUtils
from .config import ImportCoreConfig

settings = ImportCoreConfig()


def download_file(link: str, output_path: str) -> str:
    with requests.get(link, stream=True, timeout=2000) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get("content-length", 0))
        block_size = 1024 * 10  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        with open(output_path, "wb") as f:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            os.remove(output_path)
            raise NendoError(f"Error while downloading {link}.")
    return output_path


def download_yt_dlp(link: str, output_path: str, limit: int) -> str:
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }
    if limit > 0:
        ydl_opts["playlistend"] = limit

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([link])
            if error_code:
                raise NendoError(f"Error while downloading {link}.")
        return output_path
    except Exception as e:
        raise NendoError(f"Error while downloading {link}.") from e


class ImportCore(NendoGeneratePlugin):
    nendo_instance: Nendo = None
    config: NendoConfig = None
    import_folder: str = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if settings.import_folder is not None:
            os.makedirs(settings.import_folder, exist_ok=True)
            self.import_folder = settings.import_folder
        else:
            self.import_folder = os.path.join(Path.home(), ".cache", "nendo", "imported")
            os.makedirs(self.import_folder, exist_ok=True)

    @NendoGeneratePlugin.run_track
    def import_track(self, links: List[str], limit: int = -1) -> List[NendoTrack]:
        tracks = []

        for link in links:
            # check if link is a file path
            if AudioFileUtils().is_supported_filetype(link):
                output_path = os.path.join(self.import_folder, link.split("/")[-1])
                download_file(link, output_path)
                track = self.nendo_instance.library.add_track(
                    file_path=output_path,
                    meta={"original_link": link}
                )
                track.set_meta({
                    "title": link.split("/")[-1].split(".")[0]
                })
                tracks.append(track)
            else:
                try:
                    output_path = os.path.join(self.import_folder, "yt-dlp", str(time.time_ns()))
                    download_yt_dlp(link, output_path, limit)
                    downloaded_tracks = self.nendo_instance.library.add_tracks(path=output_path)
                    for t in downloaded_tracks:
                        title = t.get_meta("title")
                        t.set_meta({
                            "original_link": link,
                            "title": title.replace(f".{title.split('.')[-1]}", "")
                        })
                    tracks.extend(downloaded_tracks)
                except Exception as e:
                    # TODO here we try the final fallback
                    # which is downloading page body and checking for audio links
                    raise e

        return tracks
