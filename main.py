from tkinter import *
from tkinter import ttk
from datetime import date, datetime
import tkinter as tk
from PIL import Image, ImageTk
import time

class week_plan_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("WEEK PLAN")
        self.geometry("600x500+710+320")
        self.minsize(500,400)
        self.columnconfigure( (0,1,2,3), weight = 1, uniform="a")
        self.rowconfigure(0,weight=1,uniform="a")
        self.rowconfigure(1,weight=2,uniform="a")
        self.rowconfigure(2,weight=4,uniform="a")
        self.grab_set()  #To make the root window untouchable
        self.set_gui()
    
    
    def set_gui(self):
        #HEAD
        nav_bar_img = Image.open("./img/9293128.png").resize((35,35))
        self.nav_bar_img_tk = ImageTk.PhotoImage(nav_bar_img)
        nav_bar_button = Button(self , image = self.nav_bar_img_tk, width="50", height="50",bg="white" )
        nav_bar_button.grid(column=0,row=0,sticky="nws",padx = 5,pady=5)
        clock = Label(self ,text="WEEKLY PLANNER", font = ("Verdana", 17) , bg="#e84118" , fg = "#353b48")
        clock.grid(column=0, row=0, columnspan=4, sticky="nwse", ipadx = "20" ,ipady="20")
        nav_bar_button.lift()
        
        # Select Day
        select_day_label = Label(self, text="SELECT DAY:", font = ("Verdana", 13,"bold"))
        select_day_label.grid(row=1, column=0,sticky="nse",padx=5,pady=10)
        day_selected = tk.StringVar() 
        monthchoosen = ttk.Combobox(self, width = 27, textvariable = day_selected)  
        
        monthchoosen['values'] = (' January',   #placeholder
                          ' February', 
                          ' March', 
                          ' April', 
                          ' May', 
                          ' June', 
                          ' July', 
                          ' August', 
                          ' September', 
                          ' October', 
                          ' November', 
                          ' December')  
        monthchoosen.grid(row=1,column=1,padx=5,pady=10)

        add_day_img = Image.open("./img/add_button.png").resize((35,35))
        self.add_day_img_tk = ImageTk.PhotoImage(add_day_img)
        add_button = Button(self , image = self.add_day_img_tk, width="50", height="50",borderwidth=0 )
        add_button.grid(column=2,row=1,sticky="nsw",padx = 5,pady=5)
        
        
        
week_days = {0 : "Mon" , 1 : "Tue" , 2 : "Wed" , 3 : "Thu" , 4 : "Fri" , 5 : "Sat" , 6 : "Sun" }

def get_time():
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    today = date.today()
    curr_day = today.strftime(" %d/%m/%Y ")
    timevar = week_days[today.weekday()] + ", " +curr_time  + "\n"  + curr_day 
    clock.config(text = timevar)
    clock.after(200,get_time)


def start_session():
    open_week_plan_button.config(bg='black')
    
    
def open_daiy_plan_window():
    root.grab_set()
    extra_window = week_plan_window()
  


root = Tk()
root.title("DEEP WORK ASSISTANT")
root.geometry("700x600+610+220")
root.config(bg="black")
root.minsize(600,500)
#root.maxsize(600,500)

#Grid Layout configuration
root.columnconfigure((0,1),weight=1, uniform="a")
root.rowconfigure(0,weight=1, uniform="a")
root.rowconfigure(1,weight=4, uniform="a")
root.rowconfigure(2,weight=2, uniform="a")

#Nav / Menu bar open button

nav_bar_img = Image.open("./img/9293128.png").resize((35,35))
nav_bar_img_tk = ImageTk.PhotoImage(nav_bar_img)
nav_bar_button = Button(root, image = nav_bar_img_tk, command=open_daiy_plan_window, width="50", height="50",bg="white" )
nav_bar_button.grid(column=0,row=0,sticky="nws",padx = 5,pady=5)

#Clock

clock = Label(root, font = ("Verdana", 17) , bg="#e84118" , fg = "#353b48")
clock.grid(column=0, row=0, columnspan=2, sticky="nwse", ipadx = "20" ,ipady="20")
nav_bar_button.lift()
get_time()


#Set Week Plan Button

open_week_plan_img = Image.open("./img/TEMP_LOGO.png").resize((200,200))
open_week_plan_img_tk = ImageTk.PhotoImage(open_week_plan_img)
open_week_plan_button = Button(root,command=start_session, image = open_week_plan_img_tk,  bg="#0F0F0F", width="50", height="50")
open_week_plan_button.grid(column=1,row=2,sticky="nwse",padx = 20 ,pady=20)


#Label list Activity

""" activity_label = Label(root, text="Next Activities:", font = ("Verdana", 15,"bold"))
activity_label.grid(row=1, column=0,sticky="sw",padx=5,pady=10) """

#Next Activity to Do

activity = [i for i in range(26)]
list_activity = StringVar(value=activity)
activity_listbox = Listbox(root, listvariable=list_activity, height=6,selectmode="extended", font=("Verdana", 10),justify=CENTER )
activity_listbox.grid(row = 2 , column= 0,sticky="nsew",padx = 5,pady=5)

scrollbar_activity = ttk.Scrollbar(root, orient="vertical", command=activity_listbox.yview) 
scrollbar_activity.grid(row = 2 , column= 0,sticky="nse")

activity_listbox["yscrollcommand"] = scrollbar_activity.set


#Today Plan

def highlight_current_activity(): 
   
    current_time = datetime.now().strftime("%H:%M")  

    for idx, (time_range, activity) in enumerate(daily_schedule):
        start_time, end_time = time_range.split(" - ")  

       
        if start_time <= current_time <= end_time:
            activity_labels[idx].config(background="yellow", font=("Verdana", 12, "bold"))
        else:
            activity_labels[idx].config(background="red", font=("Verdana", 12))  

   
    root.after(60000, highlight_current_activity)




schedule_data = {
    "05/12/2024": [("09:00 - 10:00", "Code Interview"), ("16:00 - 17.00", "Meeting"), ("14:00 - 15:00", "Code Review")],
    "06/12/2024": [("08:00", "Exercise"), ("09:30", "Team Standup"), ("11:00", "Project Planning"), 
                   ("13:00", "Lunch"), ("15:00", "Team Sync"), ("17:00", "Wrap Up Meeting"), 
                   ("18:00", "Personal Study")],
   
}

today = date.today()
current_day = today.strftime("%d/%m/%Y")  
activity_labels = []  # References daily plan Labels 

left_frame = ttk.Frame(root)
left_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=5)

right_frame = ttk.Frame(root)
right_frame.grid(row=1, column=1, sticky="nsew", padx=10,pady=5)


daily_schedule = schedule_data.get(current_day, [])

for idx, (time, activity) in enumerate(daily_schedule[:10]):

    target_frame = left_frame if idx < 6 else right_frame
    row = idx if idx < 6 else idx - 6 

    label_text = f"{time}   {activity}"
    label = ttk.Label(target_frame, text=label_text, font=("Verdana", 12), background="red")
    label.grid(row=row, column=0, sticky="w", pady=10,padx=5)

    activity_labels.append(label)
highlight_current_activity()
""" upper_frame = Label(root, background="red", text ="ROSSO" )
lower_frame = Label(root, background="blue", text ="BLUE" )
upper_frame.grid(column=1, row=0,sticky="nswe")
lower_frame.grid(column=0, row=0,sticky="nswe") """


root.mainloop()
