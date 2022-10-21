from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
import pandas as pd
import youtube_dl
import whisper

app = Flask(__name__)
api = Api(app)

ydl_opts = {
    'ignoreerrors': True,
    'outtmpl': 'Downloader/%(title)s.%(etx)s',
    'format': 'bestaudio/best',
    'no_check_certificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'prefer_ffmpeg': True
}

@app.route('/transcribe/') 
def transcription_get():
  url = request.args.get('url')
  if url == None:
    return "No transcription requested"

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
    info_dict = ydl.extract_info(url)

    path = "Downloader/" + info_dict.get("title", None) + ".mp3"


  model = whisper.load_model("base")
  result = model.transcribe(path)

  return "Transcription Result: \n" + result['text']

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=4999)