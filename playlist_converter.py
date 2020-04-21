import requests, json, base64
import subprocess, os
import xml_parser

client_id = '1e020bd65a934fa88aa8e49a05f75b60'
client_secret = ''


def get_token(code):
    bash = f"curl -H 'Authorization: Basic MWUwMjBiZDY1YTkzNGZhODhhYThlNDlhMDVmNzViNjA6NTQ1Y2MwZmU5MzQ5NDE1YmFjNWRkYmNkOWQ5MzQ0MGY=' -d grant_type=authorization_code -d code={code} -d redirect_uri=https%3A%2F%2Fexample.com%2F https://accounts.spotify.com/api/token"
    print("\nToken:")
    os.system(bash)
    print("\n")
    token = input("Enter the token (access token field without quotes): \n")
    refresh_token = input("Enter the refresh token (just leave blank and hit enter): \n")
    return token, refresh_token
    

def refresh_token(refresh_token):
    bash = f"curl -H 'Authorization: Basic MWUwMjBiZDY1YTkzNGZhODhhYThlNDlhMDVmNzViNjA6NTQ1Y2MwZmU5MzQ5NDE1YmFjNWRkYmNkOWQ5MzQ0MGY=' -d grant_type=refresh_token -d refresh_token={refresh_token} https://accounts.spotify.com/api/token"
    print("\nNew token:")
    os.system(bash)
    print("\n")
    token = input("Enter the token (access token field without quotes): \n")
    return token

def create_spotify_playlist(user_id, token):
    playlist_name = input("Enter name of playlist: \n")
    playlist_desc = input("Enter playlist description (or leave blank): \n")
    request = json.dumps({
        "name" : playlist_name, 
        "public" : True,
        "collaborative" : "false",
        "description" : playlist_desc
    })

    query = f'https://api.spotify.com/v1/users/{user_id}/playlists'

    response = requests.post(
        query, 
        data=request,
        headers={
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        } 
    )
    json_response = response.json()
    return json_response["id"]


def get_song_uri(token, songname, artist):
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=1".format(songname, artist)
    response = requests.get(
        query, 
        headers={
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"}
    )
    response_json = response.json()
    songs = response_json["tracks"]["items"]
    #print(response_json)
    try:
         uri = songs[0]["uri"]
         return uri
    except:
        return "none"
   

def add_song(token, user_id, uri, playlist):
    uri_string = ""
    print(uri)
    query = f"https://api.spotify.com/v1/playlists/{playlist}/tracks?uris={uri}"
    response = requests.post(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()
    return response_json


def main():
    print("This application will allow you to transfer Apple Music playlists (xml) into Spotify playlists.")
    print("Make sure the Apple Music playlists are exported as .xml files and are in the wd.")
    input("Press any key to continue...")
    url = "https://accounts.spotify.com/authorize?client_id=1e020bd65a934fa88aa8e49a05f75b60&response_type=code&redirect_uri=https%3A%2F%2Fexample.com%2F&scope=user-read-private%20user-read-email%20playlist-modify-private%20playlist-modify-public"
    print("Copy this URL into browser and hit enter. Your code will appear in the URL (code=_).\nCopy the code and paste it back in terminal.\nURL:\n " + url)
    code = input("Enter code: \n")
    access_token, refresh_token = get_token(code)
    user_id = input("Enter your spotify user ID: \n")
    flag = "y"
    while flag == "y":
        apple_playlist = input("Enter name of file with playlist data (.xml): \n")
        apple_playlist_tree = xml_parser.parse_xml(apple_playlist)
        song_list = xml_parser.get_songlist(apple_playlist_tree)
        playlist = create_spotify_playlist(user_id, access_token)
        print("Playlist created...")
        song_uris = []
        print("Adding songs to playlist...")
        count = 0
        for song in song_list:
            name = song[0]
            artist = song[1]
            uri = get_song_uri(access_token, name, artist)
            if uri == "none":
                print(f"Error adding {name} by {artist}")
                pass
            else:
                song_uris.append(uri)
                add_song(access_token, user_id, uri, playlist)
                count+=1
        #uri = get_song_uri(access_token, "I'm not the sun", "Arkells")
        print(add_song(access_token, user_id, uri, playlist))
        print()
        print(f"{count} Songs added to playlist!\n")
        flag = input("Would you like to convert another playlist (y for yes, n for no)?")

if __name__ == "__main__":
    main()

