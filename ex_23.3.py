import tkinter
import tkinter.messagebox

class MyGUI():
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title("NYUAD")
        self.address_button = tkinter.Button(self.main_window, text = "Address", command = self.display_address)
        self.address_button.pack()
        tkinter.mainloop()
    def display_address(self):
        tkinter.messagebox.showinfo("NYUAD Address","New York University Abu Dhabi PO Box 129188, Saadiyat island, Abu Dhabi, United Arab Emirates")

my_gui = MyGUI()