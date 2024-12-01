from tkinter import *
from tkinter import ttk
from datetime import date
from PIL import Image, ImageTk
import time

week_days = {0 : "Mon" , 1 : "Tue" , 2 : "Wed" , 3 : "Thu" , 4 : "Fri" , 5 : "Sat" , 6 : "Sun" }

def get_time():
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    today = date.today()
    timevar = week_days[today.weekday()] + ", " +curr_time 
    clock.config(text = timevar)
    clock.after(200,get_time)

root = Tk()
root.title("DEEP WORK ASSISTANT")
root.geometry("600x500+660+270")

root.minsize(600,500)
#root.maxsize(600,500)


root.columnconfigure((0,1),weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure((1,2),weight=3)



clock = Label(root, font = ("Arial", 50) , bg="#e84118" , fg = "#353b48")

clock.grid(column=1, row=0,columnspan=2, sticky="nswe")
get_time()

nav_bar_img = Image.open("./img/9293128.png").resize((30,30))
nav_bar_img_tk = ImageTk.PhotoImage(nav_bar_img)
nav_bar_button = Button(image = nav_bar_img_tk, width="50", height="50")
nav_bar_button.grid(column=0,row=0, stick ="nswe")
""" upper_frame = Label(root, background="red", text ="ROSSO" )
lower_frame = Label(root, background="blue", text ="BLUE" )
upper_frame.grid(column=1, row=0,sticky="nswe")
lower_frame.grid(column=0, row=0,sticky="nswe") """


root.mainloop()
