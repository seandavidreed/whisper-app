# To silence the NumbaDeprecationWarning, I added nopython=True
# to the decorator on line 57 of
# /home/<USERNAME>/.local/lib/python3.10/site-packages/whisper/timing.py

import whisper
import os
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

class AudioFile():
    def __init__(self):
        self.filename = None
        self.generated_text = None
    
    def open(self):
        self.filename = filedialog.askopenfilename()
    
    def to_text(self):
        '''
        Simple wrapper method for the entre of the program:
        the speech-to-text conversion.
        '''
        if self.filename == None:
            return

        model = whisper.load_model("medium")
        result = model.transcribe(audio=self.filename, initial_prompt=INITIAL_PROMPT, fp16=False, language='en')
        self.generated_text = result["text"]


# Replaces the file extension of the audio file
# with that of the output text file.
def replace_extension(filename, new_extension):
    '''
    os.path.splitext splits the filename into a tuple ('filename', '.extension')
    We take the first part (the filename without the extension), 
    and add the new extension to it.
    '''
    return os.path.splitext(filename)[0] + new_extension


def main():
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Text To Speech")
    label = tk.Label(root, text="Open File")
    label.pack()

    audio_file = AudioFile()
    button = tk.Button(root, text="Select", command=audio_file.open)
    button.pack()

    button2 = tk.Button(root, text="Generate", command=audio_file.to_text)
    button2.pack()
    
    root.mainloop()
    
    # Prepare name for new text file.
    text_filename = replace_extension(audio_file.filename, '.docx')

    # Write generated text to file.
    with open(text_filename, "w") as file:
        for line in audio_file.generated_text:
            file.write(line)

if __name__ == "__main__":
    main()
    
