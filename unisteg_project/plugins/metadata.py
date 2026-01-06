from .base import Analyzer
import subprocess
import json
class Analyzer(Analyzer):
    name = "metadata"
    supported_mimes = [r"image/png", r"image/jpeg",r'video/mp4',r"audio/x-wav",r'']
    
    def decode(self, file_path: str) -> str:
        result = subprocess.run(
             [r"C:\Users\HP\OneDrive\College Files\InfoSec\exiftool\exiftool-13.44_64\exiftool.exe", '-json', file_path],
             capture_output=True,
             text=True
         )
        metadata = json.loads(result.stdout)[0]
        print(metadata)
    
    def encode(self, file_path: str,secret_data, dest: str):
        cmd = [r"C:\Users\HP\OneDrive\College Files\InfoSec\exiftool\exiftool-13.44_64\exiftool.exe"]
        metadata={'Comment':secret_data}
        for field, value in metadata.items():
           cmd.append(f'-{field}={value}')
        cmd.extend(['-o', dest, file_path])
        result = subprocess.run(
             cmd,
             capture_output=True, 
             text=True
         )
        if result.returncode == 0:
         print(f"✓ Metadata encoded successfully!")
         print(f"  Saved to: out.png")
        else:
         print(result.stderr)