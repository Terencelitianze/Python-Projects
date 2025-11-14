import tkinter

class MyGUI:
    def __init__(self):
        
        self.main_window = tkinter.Tk()
        '''
        self.label1 = tkinter.Label(self.main_window, text = "hello world!")
        self.label2 = tkinter.Label(self.main_window, text = "This is my GUI program.")
        self.label1.pack()
        self.label2.pack()'''
        self.top_frame = tkinter.Frame(self.main_window)
        self.label1 = tkinter.Label(self.top_frame, text = "Winken")
        self.label2 = tkinter.Label(self.top_frame, text = "Blinken")
        self.label3 = tkinter.Label(self.top_frame, text = "Nod")
        self.top_frame.pack()
        self.label1.pack()
        self.label2.pack()
        self.label3.pack()
        self.bottom_frame = tkinter.Frame(self.main_window)
        self.label4 = tkinter.Label(self.top_frame, text = "Winken")
        self.label5 = tkinter.Label(self.top_frame, text = "Blinken")
        self.label6 = tkinter.Label(self.top_frame, text = "Nod")
        self.bottom_frame.pack()
        self.label4.pack(side = "left")
        self.label5.pack(side = "left")
        self.label6.pack(side = "left")
        tkinter.mainloop()

my_gui = MyGUI()