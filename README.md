# Spotify-Downloader
A python script to download my spotify playlist for offline playing of songs.

#How to Start Using It.

- Clone the repo `cd && git clone https://github.com/akul08/Spotify-Downloader.git && cd Spotify-Downloader`

- Install the dependencies :
	- `pip install spotipy`

	- `pip install beautifulsoup4`

	- `pip install --upgrade google-api-python-client`

	- `pip install requests`

- In terminal Run these commands:
	- `export SPOTIPY_CLIENT_ID='06e4213bc2324960891fc9713cc3e82d'`     
	- `export SPOTIPY_CLIENT_SECRET='ad8fd4b52f8c4c62bfeaa0e48d8e305d'` 
	- `export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'` 

- Now, run the script `python spotify.py your_spotify_username`

- Verify Your account as specified in terminal.

- After this step you will have your songs in a file similar to playlist.txt .

- Now, run the script with your playlist `python download.py -f="playlist.txt"`

- More options :

	-`-q` for specifing a song to download
	-`-m` for maximum list of songs to choose from.
	-`-mp4` to download video instead of audio.

- Simple. Isn't It. Enjoy.
