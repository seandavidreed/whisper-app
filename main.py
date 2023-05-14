# To silence the NumbaDeprecationWarning, I added nopython=True
# to the decorator on line 57 of
# /home/<USERNAME>/.local/lib/python3.10/site-packages/whisper/timing.py

import whisper
import os
import sys
import time
import threading
import tkinter as tk
from tkinter import filedialog

# Example formatting to tell the model
# how to punctuate the output and to
# exclude pauses and filler words.
INITIAL_PROMPT = (
    "Ultimately, I think the answer is a new job."
    "That's all there is to it;"
    "Do you Agree?"
)

# Generates a dynamic "Loading..." output to the console
# using it's own thread to as not to halt the program.
class LoadingEllipsis(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        sys.stdout.write("Generating Text")
        while self.running:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)

    def stop(self):
        self.running = False
        print()


# Replaces the file extension of the audio file
# with that of the output text file.
def replace_extension(filename, new_extension):
    '''
    os.path.splitext splits the filename into a tuple ('filename', '.extension')
    We take the first part (the filename without the extension), 
    and add the new extension to it.
    '''
    return os.path.splitext(filename)[0] + new_extension


def speech_to_text(audio_file_path):
    '''
    Simple wrapper function for the entre of the program:
    the speech-to-text conversion.
    '''
    model = whisper.load_model("medium")
    result = model.transcribe(audio=audio_file_path, initial_prompt=INITIAL_PROMPT, fp16=False, language='en')
    return result["text"]


def main():
    root = tk.Tk()
    filename = filedialog.askopenfilename(parent=root)
    root.mainloop()

    # Get audio file path
    audio_file_path = filename

    # Generate "Loading..." on separate thread
    loading_ellipsis = LoadingEllipsis()
    loading_ellipsis.start()

    # Generate text from audio file with OpenAI's Whisper API.
    text = speech_to_text(audio_file_path)

    # Terminate "Loading..."
    loading_ellipsis.stop()
    loading_ellipsis.join()
    
    # Prepare name for new text file.
    text_file = replace_extension(audio_file_path, '.docx')

    # Write generated text to file.
    with open(text_file, "w") as file:
        for line in text:
            file.write(line)

if __name__ == "__main__":
    main()
    
