from flask import Flask
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

def is_supported(url):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False

transcribe_req_args = reqparse.RequestParser()
transcribe_req_args.add_argument("video-url", type=str, help="YouTube video URL to transcribe from", required=True)

class Transcribe(Resource):
  def get(self):
    args = transcribe_req_args.parse_args()

    if is_supported(args["video-url"]) == False:
      return {"whisper-response" : "YouTube URL provided is invalid."}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([args["video-url"]])
      info_dict = ydl.extract_info(args["video-url"])
      
      path = "Downloader/" + info_dict.get("title", None) + ".mp3"



    model = whisper.load_model("base")
    result = model.transcribe(path)
   
    return { "whisper-response" : result["text"] }

api.add_resource(Transcribe, "/transcribe")

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=4999, debug=True)