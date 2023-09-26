import PyPDF3
import pyttsx3
import pdfplumber

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.core.window import Window

from threading import Thread
from tkinter.filedialog import askopenfile

Window.size = (500, 600)


class MyApp(MDApp):
    def fileChooser(self, event):
        self.file = askopenfile(mode='r', filetypes=[("pdf files", "*.pdf")])
        self.pdf_file = self.file.name
        self.locationLabel.text = self.pdf_file
        self.convertButton.pos_hint = {'center_x': 0.5, 'center_y': 0.35}
        pass

    def convertToAudio(self):
        try:
            self.statusLabel.color = [0.2, 0.5, 0.2]
            self.statusLabel.text = "Conversion started"

            book = open(self.pdf_file, 'rb')
            pdfReader = PyPDF3.PdfFileReader(book)
            pages = pdfReader.numPages
            finalText = ""

            try:
                with pdfplumber.open(self.pdf_file) as pdf:
                    for i in range(0, pages):
                        page = pdf.pages[i]
                        text = page.extract_text()
                        finalText += text

                        try:
                            engine = pyttsx3.init()
                            engine.save_to_file(finalText, 'audioBook.mp3')
                            engine.runAndWait()
                            self.statusLabel.color = [0.2, 0.5, 0.2]
                            self.statusLabel.text = "Conversion successful"
                        except:
                            self.statusLabel.color = [1, 0, 0]
                            self.statusLabel.text = "Error. Trouble converting file"
            except:
                self.statusLabel.color = [1, 0, 0]
                self.statusLabel.text = "Error. Trouble extracting text"
        except:
            self.statusLabel.color = [1, 0, 0]
            self.statusLabel.text = "Error. Trouble opening file"

    def convert(self, event):
        thread1 = Thread(target=self.convertToAudio)
        thread1.start()

    def build(self):
        layout = MDRelativeLayout(md_bg_color=[210 / 255, 215 / 255, 217 / 255])

        self.img = Image(source='logo.png',
                         size_hint=(1, 1),
                         pos_hint={'center_x': 0.5, 'center_y': 0.85})

        self.fileChooserLabel = Label(text="Select PDF file to convert",
                                      pos_hint={'center_x': 0.4, 'center_y': 0.53},
                                      color=[0, 0, 0],
                                      font_size=20,
                                      )

        self.selectButton = Button(text="Select",
                                   size_hint=(None, None),
                                   pos=(340, 300),
                                   height=40,
                                   on_press=self.fileChooser
                                   )

        self.locationLabel = Label(text="",
                                   pos_hint={'center_x': 0.5, 'center_y': .45},
                                   color=[0.5, 0.5, 0.5],
                                   font_size=12,
                                   )

        self.convertButton = Button(text="Convert",
                                    pos_hint={'center_x': 0.5, 'center_y': 20},
                                    size_hint=(.2, .1),
                                    size=(75, 75),
                                    pos=(340, 100),
                                    height=40,
                                    on_press=self.convert,
                                    background_color=[1, 0, 110 / 255],
                                    )

        self.statusLabel = Label(text="",
                                 pos_hint={'center_x': 0.5, 'center_y': 0.25},
                                 color=[1, 0, 0],
                                 font_size=24,
                                 bold=True,
                                 )

        layout.add_widget(self.img)
        layout.add_widget(self.fileChooserLabel)
        layout.add_widget(self.selectButton)
        layout.add_widget(self.locationLabel)
        layout.add_widget(self.convertButton)
        layout.add_widget(self.statusLabel)

        return layout


if __name__ == "__main__":
    MyApp().run()
