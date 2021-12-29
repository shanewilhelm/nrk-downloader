# NRK Downloader

## Installation
The simplest way is to use the download `.exe` file found on the release page https://github.com/shanewilhelm/nrk-downloader/releases

If you're more familiar with Python, you can also run using the `main.py` file. Be sure to `pip install ffmpeg-python` instead of just `ffmpeg`!

## Usage
This is a command-line application (no GUI), so you'll have to use command prompt or powershell to run the `.exe` file. 

1) Open command prompt and `cd` to wherever you saved the `nrk-downloader.exe` file
2) Run the command `./nrk-downloader.exe {url-of-the-video}`
    - e.g. `./nrk-downloader.exe https://tv.nrk.no/serie/minibarna/sesong/3/episode/2/avspiller` 
    - Be sure your URL includes both the season/sesong and episode number, just like the above example
3) If you would like to download an entire season, or the entire series (all seasons), add either the `--season` or `--series` flag to your command
    - e.g. `./nrk-downloader.exe https://tv.nrk.no/serie/minibarna/sesong/3/episode/2/avspiller --season`