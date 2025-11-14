import tkinter
import tkinter.messagebox

class MyGUI():
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.top_frame = tkinter.Frame(self.main_window)
        self.middle_frame = tkinter.Frame(self.main_window)
        self.bottom_frame = tkinter.Frame(self.main_window)
        self.main_window.title("Km to Miles Converter")
        self.label = tkinter.Label(self.top_frame, text = "Km to Miles")
        self.entry = tkinter.Entry(self.top_frame, width=10)
        self.result = tkinter.StringVar()
        self.result.set("")
        self.label2 = tkinter.Label(self.middle_frame, textvariable = self.result)
        self.label3 = tkinter.Label(self.middle_frame, text = "Converted to miles")
        
        self.convert_button = tkinter.Button(self.bottom_frame, text = "Convert", command = self.display_conversion)
        self.top_frame.pack()
        self.label.pack(side = 'left')
        self.entry.pack(side = 'left')
        self.label3.pack(side = "left")
        self.label2.pack(side = "left")
        self.middle_frame.pack()
        self.convert_button.pack(side = 'left')
        self.bottom_frame.pack()
        tkinter.mainloop()

    def display_conversion(self):
        self.input = float(self.entry.get())
        miles = self.input * 0.621
        self.result.set(str(miles))

my_gui = MyGUI()