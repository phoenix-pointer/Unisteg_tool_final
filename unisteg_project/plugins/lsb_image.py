from .base import Analyzer
import cv2
import numpy as np
def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, "08b") for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")
class Analyzer(Analyzer):
    name = "lsb_image"
    supported_mimes = [r"image/png", r"image/jpeg"]
    
    def decode(self, file_path: str):
     print("[+] Decoding...")
    # read the image
     image = cv2.imread(file_path)
     binary_data = ""
     for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
     all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
     decoded_data = ""
     for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
     return decoded_data[:-5]
    
    def encode(self, file_path: str, secret_data, dest_path: str):
    # read the image
     image = cv2.imread(file_path)
    # maximum bytes to encode
     n_bytes = image.shape[0] * image.shape[1] * 3 // 8
     print("[*] Maximum bytes to encode:", n_bytes)
     if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
     print("[*] Encoding data...")
    # add stopping criteria
     secret_data += "====="
     data_index = 0
    # convert data to binary
     binary_secret_data = to_bin(secret_data)
    # size of data to hide
     data_len = len(binary_secret_data)
     for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
     return image