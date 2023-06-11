import tkinter as tk
from PIL import ImageTk, Image
import DBHandler
from DisplayStocksFrame import DispalyStocksFrame

class LoginFrame(tk.Frame):
    
    def __init__(self, parent , dbh: DBHandler.DatabaseHandler):
        tk.Frame.__init__(self, parent )
        
        self.dbh = dbh
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
        
        self.name_label = tk.Label(self ,text="enter user name")
        self.username_entry = tk.Entry(self)
        self.empty_label = tk.Label(self)
        self.pasword_label = tk.Label(self , text="enter password")
        self.pasword_entry = tk.Entry(self,show="*")
        self.login_button = tk.Button(self,text="log in" , command=self.__log_in__) 
        
        
        
        self.empty_space_label1.grid(row=1, column=0)
        self.empty_space_label2.grid(row=2, column=0)
        self.empty_space_label3.grid(row=3, column=0)
        self.name_label.grid(row=4 , column=0)
        self.username_entry.grid(row=5 , column=0)
        self.empty_space_label4.grid(row=6, column=0)
        self.pasword_label.grid(row=7,column=0)
        self.pasword_entry.grid(row=8,column=0)
        self.login_button.grid(row=9,column=0)      
    
    def __log_in__(self):
        if self.dbh.verivy_user(self.username_entry.get() , self.pasword_entry.get()):
            
            stock_frame = DispalyStocksFrame(self.master , self.dbh , self.username_entry.get())
            self.destroy()
            stock_frame.place(relx=0.5, rely=0.5, anchor="center")
            
        else:
            self.empty_space_label3 = tk.Label(self , text="inncorect user name or passworld\n try again")
            print("no user")
            self.master.update()
