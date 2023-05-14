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

class Model:
    def __init__(self):
        self.audio_filename = None
        self.text_filename = None
        self.audio_file = None
        self.text_file = None
    
    def open_audio_file(self):
        self.audio_filename = filedialog.askopenfilename()

    def speech_to_text(self):
        model = whisper.load_model("medium")
        result = model.transcribe(audio=self.audio_filename, initial_prompt=INITIAL_PROMPT, fp16=False, language='en')
        self.text_file = result["text"]
        self.replace_extension(new_extension=".docx")

        with open(self.text_filename, "w") as file:
            for line in self.text_file:
                file.write(line)
    
    # Replaces the file extension of the audio file
    # with that of the output text file.
    def replace_extension(self, new_extension):
        '''
        os.path.splitext splits the filename into a tuple ('filename', '.extension')
        We take the first part (the filename without the extension), 
        and add the new extension to it.
        '''
        self.text_filename =  os.path.splitext(self.audio_filename)[0] + new_extension


class View:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.title = tk.Label(self.frame, text="Speech to Text")
        self.title.pack()

        self.button = tk.Button(self.frame, text="Select File")
        self.button.pack()

        self.label = tk.Label(self.frame, text="")
        self.label.pack()

        self.button2 = tk.Button(self.frame, text="Generate Text")
        self.button2.pack()

        self.label2 = tk.Label(self.frame, text="")
        self.label2.pack()

    def display_selected(self, filename):
        self.label.config(text=filename)

    def display_generating(self):
        self.label2.config(text="Generating text...")


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root)

        self.view.button.config(command=self.open)

        self.view.button2.config(command=self.generate)

    def open(self):
        self.model.open_audio_file()
        self.view.display_selected()

    def generate(self):
        self.model.speech_to_text()
        self.view.display_generating()
        

def main():
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()

    if __name__ == "__main__":
        main()
