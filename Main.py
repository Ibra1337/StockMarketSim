import tkinter as tk
from PIL import Image, ImageTk
import StartFrame
import subprocess
from sqlalchemy import create_engine
from sqlalchemy import create_engine, inspect
from DBHandler import DatabaseHandler

def resize_background(event):
    width = event.width
    height = event.height

    resized_image = original_image.resize((width, height), Image.LANCZOS)

    root.background_image = ImageTk.PhotoImage(resized_image)
    background_label.config(image=root.background_image)

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

smaller_width = int(screen_width * 0.9)  # 90% of the screen width
smaller_height = int(screen_height * 0.9)  # 90% of the screen height

x_position = (screen_width - smaller_width) // 2
y_position = (screen_height - smaller_height) // 2

root.title("Background Example")
root.geometry(f"{smaller_width}x{smaller_height}+{x_position}+{y_position}")

original_image = Image.open("bg.png")

engine = create_engine('sqlite:///usersdatabase.db')
dbh = DatabaseHandler(engine)
sf = StartFrame.StartFrame(root , dbh)
sf.place(relx=0.5, rely=0.5, anchor="center")

width, height = root.winfo_width(), root.winfo_height()
resized_image = original_image.resize((width, height), Image.LANCZOS)

root.background_image = ImageTk.PhotoImage(resized_image)
background_label = tk.Label(root, image=root.background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

root.bind("<Configure>", resize_background)
sf.lift() 
python_file = "DBHandler.py"


inspector = inspect(engine)

table_names = inspector.get_table_names()

if 'user' in table_names:
    print("The table exists.")
else:
    subprocess.call(["python", python_file])

# Run the main event loop
root.mainloop()

