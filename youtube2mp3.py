from __future__ import unicode_literals
import youtube_dl
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True)
args = parser.parse_args()

ydl_opts = {
    'outtmpl': 'output.mp3',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])
except:
    pass

