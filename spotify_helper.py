import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import os
from typing import Optional, Dict

class SpotifyHelper:
    def __init__(self):
        """Initialize Spotify client with credentials from environment variables"""
        try:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                raise ValueError("Spotify credentials not found in environment variables")
            
            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            print(f"Error initializing Spotify client: {str(e)}")
            self.sp = None

    def get_random_top_song(self, country_code: str) -> Optional[Dict]:
        """Get a random song from country's top 50 playlist"""
        try:
            if not self.sp:
                return None
                
            # Get the Top 50 playlist for the country
            playlist_id = f"37i9dQZEVXbMDoHDwVN2tF"  # Global Top 50 as fallback
            
            # Country specific playlists follow this format
            country_playlist = f"37i9dQZEVXbO3qyFxbkOE1"  # Example for US Top 50
            
            # Get playlist tracks
            results = self.sp.playlist_tracks(playlist_id)
            tracks = results['items']
            
            if not tracks:
                return None
                
            # Select random track
            track = random.choice(tracks)['track']
            
            return {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            }
            
        except Exception as e:
            print(f"Error getting top song: {str(e)}")
            return None 