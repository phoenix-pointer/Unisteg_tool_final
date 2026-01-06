from .base import Analyzer
import wave
import os
class Analyzer(Analyzer):
    name = "appended_audio"
    supported_mimes = [r"audio/x-wav"]
    
    def decode(self, file_path: str) -> str:
     with wave.open(file_path, 'rb') as wav_file:
        nchannels = wav_file.getnchannels()
        sampwidth = wav_file.getsampwidth()
        nframes = wav_file.getnframes()
        expected_size = nchannels * sampwidth * nframes
        wav_file.close()
    
     file_size = os.path.getsize(file_path)
     header_end = 44  # Standard PCM WAV header size; adjust if LIST/INFO chunks present
     audio_data_size = file_size - header_end
    
     if audio_data_size > expected_size:
        with open(file_path, 'rb') as f:
            f.seek(header_end + expected_size)
            appended = f.read()
        return appended
     return b''
    
    def encode(self, file_path: str,secret_data, dest: str):
        flag=secret_data.encode('utf-8')
        with open(file_path, 'rb') as f:
         data = f.read()
        with open(dest,'wb') as fd:
           fd.write(data)
           fd.write(flag)