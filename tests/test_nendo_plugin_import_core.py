import unittest

from nendo import Nendo, NendoConfig

nd = Nendo(
    config=NendoConfig(
        log_level="INFO",
        plugins=["nendo_plugin_import_core"],
    ),
)


class ImportCoreTests(unittest.TestCase):
    def test_import_track_from_file_link(self):
        nd.library.reset(force=True)
        tracks = nd.plugins.import_core(links=["https://okio.ai/assets/audio/example1/original.mp3"])
        self.assertEqual(len(tracks), 1)
        self.assertEqual(len(nd.library), 1)
        self.assertTrue(tracks[0].has_meta("original_link"))
        self.assertEqual(tracks[0].get_meta("title"), "original")

    def test_import_track_from_youtube_video(self):
        nd.library.reset(force=True)
        tracks = nd.plugins.import_core(links=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"])
        self.assertEqual(len(tracks), 1)
        self.assertEqual(len(nd.library), 1)
        self.assertTrue(tracks[0].has_meta("original_link"))
        self.assertEqual(tracks[0].get_meta("title"), "Rick Astley - Never Gonna Give You Up (Official Music Video)")

    def test_import_track_from_youtube_playlist(self):
        both_titles = [
            "Outkast - B.O.B. (Bombs Over Baghdad) (Official HD Video)",
            "Outkast - Hey Ya! (Official HD Video)"
        ]
        nd.library.reset(force=True)
        tracks = nd.plugins.import_core(
            links=["https://www.youtube.com/playlist?list=PLAMk5GdNAs4OL2ePoB-Qb37cKJtY9lwFL"])
        self.assertEqual(len(tracks), 2)
        self.assertEqual(len(nd.library), 2)
        self.assertTrue(tracks[0].has_meta("original_link"))
        self.assertTrue(tracks[1].has_meta("original_link"))
        self.assertTrue(tracks[0].get_meta("title") in both_titles)
        self.assertTrue(tracks[1].get_meta("title") in both_titles)

    def test_import_track_from_youtube_playlist_with_limit(self):
        nd.library.reset(force=True)
        tracks = nd.plugins.import_core(
            links=["https://www.youtube.com/playlist?list=PLAMk5GdNAs4OL2ePoB-Qb37cKJtY9lwFL"],
            limit=1
        )
        self.assertEqual(len(tracks), 1)
        self.assertEqual(len(nd.library), 1)
        self.assertTrue(tracks[0].has_meta("original_link"))
        self.assertEqual(tracks[0].get_meta("title"), "Outkast - Hey Ya! (Official HD Video)")

    def test_import_tracks_from_different_link_sources(self):
        nd.library.reset(force=True)
        tracks = nd.plugins.import_core(
            links=[
                "https://www.youtube.com/playlist?list=PLAMk5GdNAs4OL2ePoB-Qb37cKJtY9lwFL",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "https://okio.ai/assets/audio/example1/original.mp3"
            ]
        )
        self.assertEqual(len(tracks), 4)
        self.assertEqual(len(nd.library), 4)
        for track in tracks:
            self.assertTrue(track.has_meta("original_link"))
            self.assertTrue(".mp3" not in track.get_meta("title"))


if __name__ == "__main__":
    unittest.main()
