from tkinter import *
from tkinter import ttk
from datetime import date
from PIL import Image, ImageTk
import time

week_days = {0 : "Mon" , 1 : "Tue" , 2 : "Wed" , 3 : "Thu" , 4 : "Fri" , 5 : "Sat" , 6 : "Sun" }

def get_time():
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    today = date.today()
    curr_day = today.strftime(" %d/%m/%Y ")
    timevar = week_days[today.weekday()] + "," + curr_day  +curr_time 
    clock.config(text = timevar)
    clock.after(200,get_time)



def start_session():
    open_week_plan_button.config(bg='black')
    


root = Tk()
root.title("DEEP WORK ASSISTANT")
root.geometry("700x600+610+220")

root.minsize(600,500)
#root.maxsize(600,500)

#Grid Layout configuration
root.columnconfigure((0,1,2),weight=1, uniform="a")
root.rowconfigure(0,weight=1, uniform="a")
root.rowconfigure(1,weight=3, uniform="a")
root.rowconfigure(2,weight=3, uniform="a")
root.rowconfigure(3,weight=2, uniform="a")

#Nav / Menu bar open button

nav_bar_img = Image.open("./img/9293128.png").resize((35,35))
nav_bar_img_tk = ImageTk.PhotoImage(nav_bar_img)
nav_bar_button = Button(root, image = nav_bar_img_tk, width="50", height="50",bg="white" )
nav_bar_button.grid(column=0,row=0,sticky="nws",padx = 5,pady=5)

#Clock

clock = Label(root, font = ("Verdana", 25) , bg="#e84118" , fg = "#353b48")
clock.grid(column=0, row=0, columnspan=3, sticky="nwse", ipadx = "20" ,ipady="20")
nav_bar_button.lift()
get_time()


#Set Week Plan Button

open_week_plan_img = Image.open("./img/TEMP_LOGO.png").resize((200,200))
open_week_plan_img_tk = ImageTk.PhotoImage(open_week_plan_img)
open_week_plan_button = Button(root,command=start_session, image = open_week_plan_img_tk,  bg="#0F0F0F", width="50", height="50")
open_week_plan_button.grid(column=1,row=1,sticky="nwse",padx = 20 ,pady=20)


#Label list Activity

activity_label = Label(root, text="Next Activities:", font = ("Verdana", 15,"bold"))
activity_label.grid(row=1, column=0,sticky="sw",padx=5,pady=10)

#Next Activity to Do

activity = [i for i in range(26)]
list_activity = StringVar(value=activity)
activity_listbox = Listbox(root, listvariable=list_activity, height=6,selectmode="extended", font=("Verdana", 10),justify=CENTER )
activity_listbox.grid(row = 2 , column= 0,sticky="nsew",padx = 5,pady=5)

scrollbar_activity = ttk.Scrollbar(root, orient="vertical", command=activity_listbox.yview) 
scrollbar_activity.grid(row = 2 , column= 0,sticky="nse")

activity_listbox["yscrollcommand"] = scrollbar_activity.set





""" upper_frame = Label(root, background="red", text ="ROSSO" )
lower_frame = Label(root, background="blue", text ="BLUE" )
upper_frame.grid(column=1, row=0,sticky="nswe")
lower_frame.grid(column=0, row=0,sticky="nswe") """


root.mainloop()
