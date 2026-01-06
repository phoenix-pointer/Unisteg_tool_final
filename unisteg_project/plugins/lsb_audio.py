from .base import Analyzer
import wave
class Analyzer(Analyzer):
    name = "lsb_audio"
    supported_mimes = [r"audio/x-wav"]
    
    def decode(self, file_path: str) -> str:
        song = wave.open(file_path, mode='rb')
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str, extracted[i:i+8])),2)) for i in range(0, len(extracted),8))
        decoded = string.split("#")[0]
        return decoded

        

    
    def encode(self, file_path: str,secret_data, dest: str):
        song = wave.open(file_path, mode='rb')
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        secret_data+=int((len(frame_bytes)-(len(secret_data)*8*8))/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in secret_data])))
        for i, bit in enumerate(bits):
         frame_bytes[i] = (frame_bytes[i] & 254) | bit
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)

# Write bytes to a new wave audio file
        with wave.open(dest, 'wb') as fd:
         fd.setparams(song.getparams())
         fd.writeframes(frame_modified)
        song.close()



