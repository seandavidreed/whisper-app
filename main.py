# Thanks to the tutorial at https://www.pythontutorial.net/tkinter/tkinter-mvc/
# for explaining the MVC design pattern using the tkinter library.

import whisper
import os
import tkinter as tk
from tkinter import filedialog, ttk

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
        '''
        The entre of the program. This function contains the
        Whisper API functionality, to which the rest of the program
        is a wrapper.
        '''
        model = whisper.load_model("medium")
        result = model.transcribe(
            audio=self.audio_filename,
            temperature=0.2,
            initial_prompt=INITIAL_PROMPT, 
            fp16=False, 
            language='en'
        )
        self.text_file = result["text"]
        self.replace_extension(new_extension=".docx")

        with open(self.text_filename, "w") as file:
            for line in self.text_file:
                file.write(line)
    
    def replace_extension(self, new_extension):
        '''
        Replaces the file extension of the audio file
        with that of the output text file.
        '''
        self.text_filename =  os.path.splitext(self.audio_filename)[0] + new_extension


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.title = ttk.Label(self, text="Speech to Text")

        self.button = ttk.Button(self, text="Select File")
        self.button.grid(row=0, column=0, padx=10)

        self.label = ttk.Label(self, text="")
        self.label.grid(row=1, column=0, padx=10)

        self.button2 = ttk.Button(self, text="Generate Text")
        self.button2.grid(row=3, column=0, padx=10)

        self.label2 = ttk.Label(self, text="")
        self.label2.grid(row=4, column=0, padx=10)

        self.controller = None

    def display_selected(self, filename):
        self.label.config(text=filename)

    def display_generating(self):
        self.label2.config(text="Generating text...")

    def display_nofile(self):
        self.label2.config(text="No File Selected")

    def set_controller(self, controller):
        self.controller = controller


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.button.config(command=self.open)

        self.view.button2.config(command=self.generate)

    def open(self):
        self.view.display_selected(self.model.audio_filename)
        self.model.open_audio_file()
        
    def generate(self):
        if self.model.audio_filename is None:
            self.view.display_nofile()
            return
        self.view.display_generating()
        self.model.speech_to_text()
        

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Text to Speech App")
        self.geometry("600x600")

        model = Model()

        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        controller = Controller(model, view)

        view.set_controller(controller)


if __name__ == "__main__":
    app = App()
    app.mainloop()

