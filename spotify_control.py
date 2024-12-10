import spotipy
from spotipy.oauth2 import SpotifyOAuth
from queue import Queue

command_queue = Queue()

class SpotifyPlayer:
    def __init__(self, sp):
        self.sp = sp
        self.track_list = []
        self.current_track_index = 0
        self.is_playing = False

    def play_track(self, spotify_url):
        track_list = []
        if "track" in spotify_url:
            track_uri = spotify_url.split('/')[-1]
            track_list.append(f"spotify:track:{track_uri}")
        elif "playlist" in spotify_url:
            playlist_id = spotify_url.split('/')[-1]
            playlist_tracks = self.sp.playlist_tracks(playlist_id)['items']
            track_list.extend(track['track']['uri'] for track in playlist_tracks)
        else:
            print("지원하지 않는 URL 형식입니다.")
            return

        self.track_list = track_list
        self.start_playback(self.track_list[self.current_track_index])

    def start_playback(self, track_uri):
        devices = self.sp.devices()["devices"]
        if devices:
            device_id = devices[0]["id"]
            self.sp.start_playback(device_id=device_id, uris=[track_uri])
            self.is_playing = True
            print(f"Playing {track_uri} on device: {devices[0]['name']}")
        else:
            print("No active devices found.")

    def next_track(self):
        if self.current_track_index < len(self.track_list) - 1:
            self.current_track_index += 1
            self.start_playback(self.track_list[self.current_track_index])
        else:
            print("This is the last track in the playlist.")

    def previous_track(self):
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.start_playback(self.track_list[self.current_track_index])
        else:
            print("This is the first track in the playlist.")

    def pause_or_play(self):
        devices = self.sp.devices()["devices"]
        if devices:
            device_id = devices[0]["id"]
            if self.is_playing:
                self.sp.pause_playback(device_id=device_id)
                self.is_playing = False
                print("Playback paused.")
            else:
                self.sp.start_playback(device_id=device_id, uris=[self.track_list[self.current_track_index]])
                self.is_playing = True
                print("Playback resumed.")

    def handle_user_input(self):
        while True:
            if not command_queue.empty():
                command = command_queue.get()
            else:
                command = input("Enter command (n: next, p: previous, s: play/pause, q: quit): ").strip().lower()

            if command == "n" or command == "next":
                self.next_track()
            elif command == "p" or command == "previous":
                self.previous_track()
            elif command == "s" or command == "pause":
                self.pause_or_play()
            elif command == "q" or command == "quit":
                print("Exiting player.")
                break
            else:
                print("Invalid input.")
