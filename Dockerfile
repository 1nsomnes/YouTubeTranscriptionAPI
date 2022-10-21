FROM python:latest

RUN apt-get update && apt-get install ffmpeg -y

RUN pip install flask \
    pip install flask_restful \ 
    pip install pandas \
    pip install youtube_dl \
    pip install git+https://github.com/openai/whisper.git \
    pip install setuptools-rust
    
WORKDIR /Users/cedricclaessens/Documents/programming/python/TranscriptionApp-WhisperEnd

COPY . . 

EXPOSE 4999

CMD ["python", "main.py"]
