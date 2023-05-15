# Thanks to the tutorial at https://www.pythontutorial.net/tkinter/tkinter-mvc/
# for explaining the MVC design pattern using the tkinter library.
#
# Thanks to the tutorial at https://medium.com/@fareedkhandev/modern-gui-using-tkinter-12da0b983e22
# for explaining the usage of the customtkinter library.

import whisper
import os
import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

from customtkinter import filedialog

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


class View(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = ctk.CTkLabel(self, text="Speech to Text")

        self.button = ctk.CTkButton(self, text="Select File")
        self.button.grid(row=0, column=0, padx=10)

        self.label = ctk.CTkLabel(self, text="")
        self.label.grid(row=1, column=0, padx=10)

        self.button2 = ctk.CTkButton(self, text="Generate Text")
        self.button2.grid(row=3, column=0, padx=10)

        self.label2 = ctk.CTkLabel(self, text="")
        self.label2.grid(row=4, column=0, padx=10)

        self.controller = None

    def display_selected(self, filename):
        self.label.configure(text=filename)

    def display_generating(self):
        self.label2.configure(text="Generating text...")

    def display_nofile(self):
        self.label2.configure(text="No File Selected")

    def set_controller(self, controller):
        self.controller = controller


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.button.configure(command=self.open)

        self.view.button2.configure(command=self.generate)

    def open(self):
        self.view.display_selected(self.model.audio_filename)
        self.model.open_audio_file()
        
    def generate(self):
        if self.model.audio_filename is None:
            self.view.display_nofile()
            return
        self.view.display_generating()
        self.model.speech_to_text()
        

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Text to Speech App")
        self.geometry("600x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        model = Model()

        view = View(self)
        view.grid(row=0, column=0, padx=50, pady=50, sticky="nwes")

        controller = Controller(model, view)

        view.set_controller(controller)


if __name__ == "__main__":
    app = App()
    app.mainloop()

