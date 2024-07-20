import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

DEVICE_ID = None

class SpotifyVision:

    def __init__(self):
        load_dotenv()

        CLIENT_ID = "INSERT_CLIENT_ID HERE"
        CLIENT_SECRET = "INSERT_CLIENT_SECRET HERE"

        scope ="user-read-playback-state,user-modify-playback-state,user-library-read,user-library-modify"
        redirect_uri = "http://localhost:8080"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri=redirect_uri, scope=scope))
        if len(self.sp.devices()["devices"]) == 0:
            print("No devices found")
            exit()

        while True:
            devices_data = self.sp.devices()["devices"]
            try:
                print("")
                print("Select available devices:")

                print("-" * 50)
                for i, device in enumerate(devices_data):
                    print(f"{i + 1}: {device['name']}")
                print("-" * 50)
                print("")

                print("Enter 'q' to quit.")
                response = input("Enter the number of the device you want to use: ")
                print("")

                if response.lower() in ["q", "quit"]:
                    print("Exiting the program.\n")
                    exit()

                device_index = int(response) - 1

                if device_index >= len(devices_data):
                    raise IndexError("Invalid device number. Please try again.")

                if devices_data[device_index]["is_active"] == False:
                    print("Device is not active. Please activate the device.")
                    print("Exiting the program.\n")
                    exit()

                DEVICE_ID = devices_data[device_index]["id"]
                print(f"Selected Device ID: {DEVICE_ID}\n")
                break
            
            except ValueError:
                print("Please enter a valid number.")

            except IndexError as e:
                print(e)


    def is_playing(self):
        return self.sp.current_playback()["is_playing"]
    
    
    def artist(self):
        return self.sp.current_playback()["item"]["artists"][0]["name"]
    
    
    def song(self):
        return self.sp.current_playback()["item"]["name"]
    
    
    def pause(self):
        return self.sp.pause_playback(device_id=DEVICE_ID)


    def resume(self):
        return self.sp.start_playback(device_id=DEVICE_ID)


    def next_song(self):
        return self.sp.next_track(device_id=DEVICE_ID)


    def like_song(self):
        return self.sp.current_user_saved_tracks_add(tracks=[self.sp.current_playback()["item"]["id"]])

    
    def print_playing(self):
        return f"Playing: {self.song()} by {self.artist()}"
    

    def print_paused(self):
        return f"Paused: {self.song()} by {self.artist()}"
    

    def print_liked(self):
        return f"Liked: {self.song()} by {self.artist()}"
    
    
    def display_playlists(self):
        playlists = self.sp.current_user_playlists(limit=50)
        print("Your playlists:")
        playlist_map = dict()
        for idx, playlist in enumerate(playlists['items']):
            print(f"{idx + 1}: {playlist['name']} (ID: {playlist['id']})")
            playlist_map[idx + 1] = playlist['id']
        return playlist_map
    

    def select_playlist(self):
        playlist_map = self.display_playlists()
        selected_playlist_id = None
        while selected_playlist_id == None:
            try:
                response = int(input("\nEnter the number of the playlist you want to select: "))
                selected_playlist_id = playlist_map[response]
                print(f"You selected playlist ID: {selected_playlist_id}\n")
                print(self.print_playing())
            except (ValueError, KeyError):
                print("\nInvalid selection. Please enter a valid number.\n")
                self.display_playlists()
        
        return self.sp.start_playback(device_id=DEVICE_ID, context_uri=f"spotify:playlist:{selected_playlist_id}")