from .spotify import Spotify_To_Youtube
from .selenium_add_to_playlist import AddSongsToPlaylist
from dotenv import load_dotenv #TODO: add everything to .env file later 

import yaml
import argparse

def run(args):
    # Set up
    if args.setup:
        setup()
        return
    elif args.showsetup:
        showSetUp()
        return
    
    # Create instances of spotify to youtube and selenium add to playlist
    with open("config.yaml", "r") as config:
        secrets = yaml.load(config, Loader=yaml.Loader)
    spty = Spotify_To_Youtube(secrets["client_id"], secrets["client_secret"], secrets["redirect_uri"])
    astp = AddSongsToPlaylist(secrets["profile"], secrets["executable_path"])

    if args.all:
        spty.add_all_spotify_playlists(astp)
    elif args.liked:
        spty.add_spotify_liked(astp)
    elif args.playlist:
        spty.add_spotify_playlist(astp, args.playlist, args.ytname if args.ytname else None)

def setup():
    secrets_dict = {}
    secrets_dict["client_id"] = input("Please input your spotify API client id: ")
    secrets_dict["client_secret"] = input("Please input your spotify API client secret: ")
    secrets_dict["profile"] = input("Please input your the complete filepath to your firefox profile: ")
    secrets_dict["executable_path"] = input("Please input your the complete filepath to your firefox executable path: ")
    secrets_dict["redirect_uri"] = "http://localhost:8000" 
    print("Setup complete!")
    # Remember to open the file!
    with open("config.yaml", "w") as config:
        yaml.dump(secrets_dict, config)


def showSetUp():
    with open("config.yaml", "r") as config:
        secrets = yaml.load(config, Loader=yaml.Loader)
    for key in secrets:
        print(f"Your {key} is: {secrets[key]}")


def main():
    """
    Functionality:
    set up (--setup, --s)
    show current setup (--showsetup, --ss)
    add all playlists (--all --a)
    add one playlist (-playlist playlist_name, -pl name)
    add liked playlist (-liked)
    """
    parser = argparse.ArgumentParser(description="clone spotify playlists to youtube")

    # Set up group
    setup_group = parser.add_mutually_exclusive_group()
    setup_group.add_argument("--setup", "--s", action="store_true", help="setup environment variables to run spotify-to-youtube commands")
    setup_group.add_argument("--showsetup", "--ss", action="store_true", help="display all current setup environment variables")
    
    # Add playlist group
    add_playlist_group = parser.add_mutually_exclusive_group()
    add_playlist_group.add_argument("--all", "--a", action="store_true", help="clone all spotify playlists to youtube")
    add_playlist_group.add_argument("-playlist", "-pl", type=str, help="clone singular playlist that has name PLAYLIST to youtube") # TODO: enforce required for everything except -d and --l
    add_playlist_group.add_argument("-liked", action="store_true", help="clone liked spotify playlist to youtube")

    # Extra flag to indicate name of playlist (enfore: only useable for single playlist adding)
    parser.add_argument("-ytname", "-ytn", type=str, help="clone spotify playlist as youtube playlist name YTNAME")
    
    # Set default function as run()
    parser.set_defaults(func=run)

    # Get arguments from user
    args = parser.parse_args()

    # Run default function with args as arguments
    args.func(args)

if __name__ == "__main__":
    main()




