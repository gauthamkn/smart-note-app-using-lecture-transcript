# utils/whisper_utils.py
import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("base")  # You can use 'tiny' for faster results
    result = model.transcribe(file_path)
    return result["text"]
