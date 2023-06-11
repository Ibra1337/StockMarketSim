import tkinter as tk
from PIL import ImageTk, Image
import LoginFrame
from DBHandler import DatabaseHandler
import sys

class StartFrame(tk.Frame):
    def __init__(self, parent , dbh:DatabaseHandler):
        
        tk.Frame.__init__(self, parent )
        self.parent = parent
        self.dbh = dbh
        # Load the image
        image = Image.open("logo.jpg")
        resized_image = image.resize((200, 100), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)
        
        # Create an image label
        
        
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=0,column=0)
        
        self.empty_space_label1 = tk.Label(self )
        self.empty_space_label2 = tk.Label(self )
        self.empty_space_label3 = tk.Label(self )
        self.empty_space_label4 = tk.Label(self )

        self.empty_space_label1.grid(row=1, column=0)
        self.empty_space_label2.grid(row=2, column=0)
        self.empty_space_label3.grid(row=3, column=0)
        self.empty_space_label4.grid(row=5, column=0)

        # Create two buttons
        self.startButton = tk.Button(self, text="Start" , command=self.__start_button_action__)
        self.startButton.grid(row = 4, column=0)
        

        self.ExitButton = tk.Button(self, text="Exit" , command= self.__exit__)
        self.ExitButton.grid(row=6,column=0  ) 

    def __start_button_action__(self):
        self.destroy()
        lf = LoginFrame.LoginFrame(self.master , self.dbh )
        lf.place(relx=0.5, rely=0.5, anchor="center")
        print("CLICK")
    
    def __exit__(self):
        sys.exit()