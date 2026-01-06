# file_detector.py
import magic



def detect_file_type(filepath):
    
   
    
    # Use python-magic library
    file_type = magic.from_file(filepath)
    mime_type = magic.from_file(filepath, mime=True)
    
    return mime_type
if __name__=='__main__':
    print(detect_file_type(r'"C:\Users\HP\OneDrive\coding practice\udaan_ml.txt"'))

# print(detect_file_type(r'c:\Users\HP\Downloads\file-sample_100kB.rtf'))
# if __name__ == "__main__":
#     if filepath:
#         file_type, mime_type = detect_file_type(filepath)
#         print(f"File type: {file_type}")
#         print(f"MIME type: {mime_type}")


