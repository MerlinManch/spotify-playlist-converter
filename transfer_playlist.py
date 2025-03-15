import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Konfiguration - Hier deine Daten eintragen!
CLIENT_ID = "0618cdc5ec9b4d9e95b995fb582b4b97"
CLIENT_SECRET = "b471a5956d6c43d2915946f7b797ff91"
REDIRECT_URI = "http://127.0.0.1:8080/callback"

def authenticate_account(account_type):
    """Authentifizierung für alten/neuen Account ohne User Management"""
    scope = ("playlist-read-private playlist-read-collaborative" if account_type == "old" 
             else "playlist-modify-private playlist-modify-public")
    
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope,
        cache_path=f".cache-{account_type}",
        show_dialog=True
    )
    
    # Manuelle Authentifizierung
    if not auth_manager.get_cached_token():
        auth_url = auth_manager.get_authorize_url()
        print(f"\nÖffne diesen Link im Browser und melde dich mit deinem {account_type.upper()} Account an:")
        print(auth_url)
        
        print(f"\nNach der Anmeldung wirst du weitergeleitet. Kopiere die VOLLE URL aus der Adressleiste:")
        response_url = input("Eingabe der gesamten URL hier: ").strip()
        
        code = auth_manager.parse_response_code(response_url)
        auth_manager.get_access_token(code, as_dict=False)

    return spotipy.Spotify(auth_manager=auth_manager)

def get_all_playlists(sp):
    """Holt alle Playlists mit Paginierung"""
    playlists = []
    results = sp.current_user_playlists(limit=50)
    
    while results:
        playlists.extend(results["items"])
        results = sp.next(results) if results["next"] else None
    
    return playlists

def get_playlist_tracks(sp, playlist_id):
    """Holt alle Tracks einer Playlist ohne Duplikate"""
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    
    seen = set()
    while results:
        for item in results["items"]:
            if item["track"] and item["track"]["uri"] not in seen:
                tracks.append(item["track"]["uri"])
                seen.add(item["track"]["uri"])
        results = sp.next(results) if results["next"] else None
    
    return tracks

def playlist_exists(sp, new_user_id, name):
    """Prüft ob Playlist bereits existiert"""
    results = sp.current_user_playlists(limit=50)
    while results:
        for pl in results["items"]:
            if pl["name"].lower() == name.lower() and pl["owner"]["id"] == new_user_id:
                return True
        results = sp.next(results) if results["next"] else None
    return False

def main():
    # Authentifiziere beide Accounts
    print("=== ALTEN ACCOUNT AUTHENTIFIZIEREN ===")
    sp_old = authenticate_account("old")
    
    print("\n=== NEUEN ACCOUNT AUTHENTIFIZIEREN ===")
    sp_new = authenticate_account("new")
    new_user_id = sp_new.me()["id"]
    
    # Playlist Transfer
    print("\nStarte Playlist-Transfer...")
    playlists = get_all_playlists(sp_old)
    
    for idx, playlist in enumerate(playlists, 1):
        name = playlist["name"]
        print(f"\nVerarbeite Playlist {idx}/{len(playlists)}: {name}")
        
        # Überspringe vorhandene Playlists
        if playlist_exists(sp_new, new_user_id, name):
            print(f"→ Überspringe (existiert bereits)")
            continue
            
        # Erstelle neue Playlist
        new_pl = sp_new.user_playlist_create(
            user=new_user_id,
            name=name,
            public=playlist["public"],
            description=playlist.get("description", "")
        )
        
        # Füge Tracks hinzu
        tracks = get_playlist_tracks(sp_old, playlist["id"])
        for i in range(0, len(tracks), 100):
            sp_new.playlist_add_items(new_pl["id"], tracks[i:i+100])
            print(f"→ {min(i+100, len(tracks))}/{len(tracks)} Tracks hinzugefügt")
            time.sleep(1)  # Rate Limit Schutz
    
    print("\nTransfer komplett! Alle Playlists wurden übertragen.")

if __name__ == "__main__":
    main()