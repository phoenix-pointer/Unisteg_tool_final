from .base import Analyzer

class Analyzer(Analyzer):
    name = "appended_image"
    supported_mimes = [r"image/png", r"image/jpeg"]
    
    def decode(self, file_path: str) -> str:
        # plugins/appended_detector.py

     with open(file_path, 'rb') as f:
        data = f.read()
    
    # For PNG: look for IEND chunk
     if b'PNG' in data[:8]:
        iend_pos = data.find(b'IEND')
        if iend_pos != -1:
            appended = data[iend_pos + 8:]  # Data after IEND
            if len(appended) > 0:
                return appended
    
    # For JPEG: look for FFD9 (end marker)
     elif b'\xff\xd8' in data[:2]:
        ffd9_pos = data.rfind(b'\xff\xd9')
        if ffd9_pos != -1:
            appended = data[ffd9_pos + 2:]
            if len(appended) > 0:
                return appended
    
     return None

    
    def encode(self, file_path: str,secret_data, dest: str):
        flag=secret_data.encode('utf-8')
        with open(file_path, 'rb') as f:
         data = f.read()
        with open(dest,'wb') as fd:
           fd.write(data)
           fd.write(flag)