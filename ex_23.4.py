import tkinter
import tkinter.messagebox

class MyGUI():
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title("Km to Miles Converter")
        self.label = tkinter.Label(self.main_window, text = "Km to Miles")
        self.entry = tkinter.Entry(self.main_window, width=10)
        
        self.convert_button = tkinter.Button(self.main_window, text = "Convert", command = self.display_conversion)
        self.label.pack(side = 'left')
        self.entry.pack(side = 'left')
        self.convert_button.pack(side = 'left')
        tkinter.mainloop()

    def display_conversion(self):
        self.input = float(self.entry.get())
        miles = self.input * 0.621
        tkinter.messagebox.showinfo("Result", f"{self.input} equals to {miles} miles")

my_gui = MyGUI()