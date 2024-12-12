from tkinter import *
from tkinter import ttk,messagebox
from datetime import date, datetime, timedelta
import tkinter as tk
from PIL import Image, ImageTk
import json

today = date.today()
activity_labels = [] # References daily plan Labels for the main window

def add_recurrence_in_json(activity, formatted_date):
    
    with open('schedule_data.json', 'r') as f:
        schedule_data = json.load(f)

    new_activity = {"title": activity["title"], "time_range": activity["time_range"]}

    specific_day = next((day for day in schedule_data.get("specific_days", []) if day["date"] == formatted_date), None)
    if not specific_day:
        specific_day = {"date": formatted_date, "activities": []}
        schedule_data["specific_days"].append(specific_day)


    if activity["title"] not in [act["title"] for act in specific_day["activities"]]:
        specific_day["activities"].append(new_activity)

    # Save the updated data back to the file
    with open('schedule_data.json', 'w') as f:
        json.dump(schedule_data, f, indent=4)


def filter_activities_by_date(date_to_check):
    formatted_date = date_to_check.strftime("%d/%m/%Y")
    print(formatted_date)
    with open('schedule_data.json', "r") as f:
        schedule_data = json.load(f)
    
    specific_day = next((day for day in schedule_data.get("specific_days", []) if day["date"] == formatted_date), None)
    print(specific_day)
    if not specific_day:
        specific_day = {"date": formatted_date, "activities": []}
        schedule_data["specific_days"].append(specific_day)
        with open('schedule_data.json', "w") as f:
            json.dump(schedule_data, f, indent=4)
    for activity in schedule_data.get("fixed_activities", []):
        
        if activity["recurrence"] == "d" and (not activity.get("end_date") or date_to_check <= datetime.strptime(activity["end_date"], "%d/%m/%Y").date()):
            add_recurrence_in_json(activity, formatted_date)
        
        elif activity["recurrence"] == "w" and date_to_check.strftime("%A") == activity.get("day_of_week"):
            add_recurrence_in_json(activity, formatted_date)

        elif activity["recurrence"] == "m" and date_to_check.strftime("%A") == activity.get("day_of_week") and (date_to_check.day - 1) // 7 + 1 == activity.get("week_of_month"):
            add_recurrence_in_json(activity, formatted_date)
    
    # Reload the updated schedule data to include added recurrences
    with open('schedule_data.json', "r") as f:
        schedule_data = json.load(f)
        
    
    specific_day = next((day for day in schedule_data.get("specific_days", []) if day["date"] == formatted_date), None)
    if specific_day:
        sort_activities_in_json()
        activities = specific_day["activities"]
        return [(activity["time_range"], activity["title"]) for activity in activities]
    else:
        return []
    
    
    
    



class week_plan_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("FOCUS FLOW")
        self.geometry("700x500+610+290")
        self.minsize(500,400)
        self.columnconfigure( (0,1,2,3,4), weight = 1, uniform="a")
        self.rowconfigure(0,weight=1,uniform="a")
        self.rowconfigure(1,weight=1,uniform="a")
        self.activity_labels = []
        self.rowconfigure(2,weight=1,uniform="a")
        self.rowconfigure(3,weight=4,uniform="a")
        self.grab_set()  #To make the root window untouchable
        self.set_gui()
    
    
    def set_gui(self):
        #HEAD
        nav_bar_img = Image.open("./img/9293128.png").resize((35,35))
        self.nav_bar_img_tk = ImageTk.PhotoImage(nav_bar_img)
        nav_bar_button = Button(self , command=self.open_add_activity_window, image = self.nav_bar_img_tk, width="50", height="50",bg="white",borderwidth=0 )
        nav_bar_button.grid(column=0,row=0,sticky="nws",padx = 5,pady=5)
        clock = Label(self ,text="WEEKLY PLANNER", font = ("Verdana", 17) , bg="#e84118" , fg = "#353b48")
        clock.grid(column=0, row=0, columnspan=5, sticky="nwse", ipadx = "20" ,ipady="20")
        nav_bar_button.lift()   
        
        # Select Day
        select_day_label = Label(self, text="SELECT DAY:", font = ("Verdana", 11,"bold"),bg="red")
        select_day_label.grid(row=2, column=0,sticky="nse",padx=5,pady=10)
        
        self.current_day = date.today()
       
        self.day_display_label = Label(self, text=self.current_day.strftime("%d/%m/%Y"),
        font=("Verdana", 12), bg="white", relief="solid")
        self.day_display_label.grid(row=2,column=2,padx=5,pady=10)
         # Previous Day Button
        prev_day_img = Image.open("./img/prev_day.png").resize((35, 35))
        self.prev_day_img_tk = ImageTk.PhotoImage(prev_day_img)
        self.prev_button = Button(self, image=self.prev_day_img_tk , command=self.go_to_prev_day, width="50", height="50", borderwidth=0)
        self.prev_button.grid(column=1, row=2, sticky="nswe", padx=5, pady=5)

        # Next Day Button
        next_day_img = Image.open("./img/next_day.png").resize((35, 35))
        self.next_day_img_tk = ImageTk.PhotoImage(next_day_img)
        self.next_button = Button(self, image=self.next_day_img_tk, command=self.go_to_next_day, width="50", height="50", borderwidth=0)
        self.next_button.grid(column=3, row=2, sticky="nswe", padx=5, pady=5)
        
    

        add_day_img = Image.open("./img/add_button.png").resize((35,35))
        self.add_day_img_tk = ImageTk.PhotoImage(add_day_img)
        add_button = Button(self , image = self.add_day_img_tk, width="50", height="50",borderwidth=0, command=self.open_add_activity_window )
        add_button.grid(column=4,row=2,sticky="nsw",padx = 5,pady=5)
        
        #ADD a NEW DAY PLAN
        new_day_plan_button = Button(self , text = "ADD NEW DAILY PLAN" )
        new_day_plan_button.grid(row=1,column=1,sticky="nswe",padx=10,pady=5,columnspan=3)
        
        
        
        
        #left and right frame     
        self.left_frame = ttk.Frame(self)
        self.left_frame.grid(row=3, column=0, sticky="nsew",columnspan=2, padx=10,pady=5)

        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=3, column=2, sticky="nsew", columnspan=2, padx=10,pady=5)

        self.activity_labels = []
        daily_schedule = filter_activities_by_date(self.current_day)
        sort_activities_in_json()
        display_activities(self,[self.left_frame,self.right_frame],daily_schedule,self.activity_labels)

        
    def go_to_prev_day(self):
        previous_day = self.current_day - timedelta(days=1)
        if previous_day >= date.today():
            self.current_day = previous_day
        new_day = self.current_day.strftime("%d/%m/%Y")
        self.day_display_label.config(text=new_day)
        daily_schedule = filter_activities_by_date(self.current_day)
        
        display_activities(self,[self.left_frame,self.right_frame],daily_schedule,self.activity_labels)

    def go_to_next_day(self):

        self.current_day += timedelta(days=1)
        new_day = self.current_day.strftime("%d/%m/%Y")
        self.day_display_label.config(text=new_day)
        daily_schedule = filter_activities_by_date(self.current_day)

        display_activities(self,[self.left_frame,self.right_frame],daily_schedule,self.activity_labels)

    def open_add_activity_window(self):    
        self.grab_set()
        extra_window = add_activity_window(self.current_day)
        
        
class add_activity_window(tk.Toplevel):
    def __init__(self,current_day):
        super().__init__()
        self.current_day = current_day  # Save the current_day passed from the parent window
        self.title("FOCUS FLOW")
        self.geometry("700x500+610+290")
        self.minsize(500,400)
        self.columnconfigure( (0,1,2,3,4), weight = 1, uniform="a")
        self.rowconfigure(0,weight=1,uniform="a")
        self.rowconfigure(1,weight=1,uniform="a")
        self.activity_labels = []
        self.rowconfigure(2,weight=1,uniform="a")
        self.rowconfigure(3,weight=1,uniform="a")
        self.rowconfigure(4,weight=1,uniform="a")
        self.rowconfigure(5,weight=1,uniform="a")


        self.rowconfigure(6,weight=1,uniform="a")
    
        self.grab_set()  #To make the root window untouchable
        self.set_gui()  
        
        
    def set_gui(self):
        
        #HEAD
        nav_bar_img = Image.open("./img/9293128.png").resize((35,35))
        self.nav_bar_img_tk = ImageTk.PhotoImage(nav_bar_img)
        nav_bar_button = Button(self , image = self.nav_bar_img_tk, width="50", height="50",bg="white",borderwidth=0 )
        nav_bar_button.grid(column=0,row=0,sticky="nws",padx = 5,pady=5)
        clock = Label(self ,text="ADD NEW ACTIVITY", font = ("Verdana", 17) , bg="#e84118" , fg = "#353b48")
        clock.grid(column=0, row=0, columnspan=5, sticky="nwse", ipadx = "20" ,ipady="20")
        nav_bar_button.lift()
        
        
        #NEW ACTIVITY TEXT
        name_activity=tk.StringVar()

        name_activity_entry = tk.Entry(self,textvariable = name_activity, font=('Verdana',14),bg="#ffffff",borderwidth=0)
        name_activity_entry.insert(0, "Title")
        name_activity_entry.grid(row = 1, column= 1, pady=10 , padx=10,sticky="nswe",columnspan=3)
        name_activity_entry.bind("<Button-1>", lambda event: clear_entry(event, name_activity_entry))
        
        def clear_entry(event, entry):
            entry.delete(0, END)
        
        def validate_time(self):
            start = start_time.get()
            end = end_time.get()
    
            if time_options.index(start) >= time_options.index(end):
                messagebox.showerror("Error", "Invalid Time")
            


        time_options = []
        for hour in range(24):
            for minute in [0, 30]:
                time_options.append(f"{hour:02}:{minute:02}")
        
        
        start_time = ttk.Combobox(self, values=time_options, state="readonly", width=10)
        start_time.grid(row=2, column=1, padx=10, pady=10,sticky="nwse")
        start_time.current(0)  # Imposta il valore iniziale

        # Etichetta e menu a tendina per l'ora di fine
        
        end_time = ttk.Combobox(self, values=time_options, state="readonly", width=10)
        end_time.grid(row=2, column=2, padx=10, pady=10,sticky="nwse")
        end_time.current(0)  # Imposta il valore iniziale
        end_time.bind("<<ComboboxSelected>>", validate_time)
        
        
        confirm_button = Button(self,text = "ADD", command=self.insert_new_activity)
        confirm_button.grid(row=6, column=1, padx=10, pady=10,sticky="nwse",columnspan=3)

        
        
    def insert_new_activity(self):
    # Recupera i valori inseriti dall'utente
        with open('schedule_data.json',"r") as f:
            schedule_data = json.load(f)
        activity_title = self.children["!entry"].get()
        start_time = self.children["!combobox"].get()
        end_time = self.children["!combobox2"].get()

        # Verifica che i campi siano validi
        if not activity_title or activity_title == "Title":
            messagebox.showerror("Error", "Please enter a valid title for the activity.")
            return

        if not start_time or not end_time:
            messagebox.showerror("Error", "Please select valid time ranges for the activity.")
            return

        

        new_activity = {
            "title": activity_title,
            "time_range": f"{start_time} - {end_time}"
        }

        formatted_date = self.current_day.strftime("%d/%m/%Y")
        specific_day = next((day for day in schedule_data.get("specific_days", []) if day["date"] == formatted_date), None)

        if specific_day:
            specific_day["activities"].append(new_activity)
        else:
            schedule_data["specific_days"].append({
                "date": formatted_date,
                "activities": [new_activity]
            })

        with open('schedule_data.json', 'w') as f:
            json.dump(schedule_data, f, indent=4)

        messagebox.showinfo("Success", "Activity added successfully!")

        
        
        sort_activities_in_json()
        

        
            
week_days = {0 : "Mon" , 1 : "Tue" , 2 : "Wed" , 3 : "Thu" , 4 : "Fri" , 5 : "Sat" , 6 : "Sun" }



def sort_activities_in_json():
   
    try:
        with open("schedule_data.json", 'r') as file:
            schedule_data = json.load(file)

        def extract_start_time(activity):
            start_time_str = activity["time_range"].split(" - ")[0]
            return datetime.strptime(start_time_str, "%H:%M")

        for specific_day in schedule_data.get("specific_days", []):
            specific_day["activities"] = sorted(
                specific_day["activities"], key=extract_start_time
            )

        with open("schedule_data.json", 'w') as file:
            json.dump(schedule_data, file, indent=4)


    except Exception as e:
        print(f"Errore durante l'ordinamento delle attività: {e}")




def get_time():
    curr_time = datetime.now().strftime("%H:%M:%S")
    today = date.today()
    curr_day = today.strftime(" %d/%m/%Y ")
    timevar = week_days[today.weekday()] + ", " +curr_time  + "\n"  + curr_day 
    clock.config(text = timevar)
    clock.after(200,get_time)


def start_session():
    open_week_plan_button.config(bg='black')
    
    
def open_daiy_plan_window():
    root.withdraw()
    extra_window = week_plan_window()
    extra_window.protocol("WM_DELETE_WINDOW", lambda: reopen_window(extra_window) )
    
def reopen_window(window):
    window.destroy() 
    root.deiconify()

def display_activities(self, frame, daily_schedule, list_activity):
    for label in list_activity:
        label.destroy()
    list_activity.clear()

    if not daily_schedule:  # empty day
        label = ttk.Label(frame[0], text="No activities scheduled", font=("Verdana", 12), background="lightgray")
        label.grid(row=0, column=0, sticky="w", pady=10, padx=5)
        list_activity.append(label)

        add_button = ttk.Button(frame[0], text="Add Activity", command=self.open_add_activity_window)
        add_button.grid(row=1, column=0, pady=10, padx=5)
        list_activity.append(add_button)
        return

    for idx, (time, activity) in enumerate(daily_schedule[:10]):
        target_frame = frame[0] if idx < 6 else frame[1]
        row = idx if idx < 6 else idx - 6
        label = ttk.Label(target_frame, text=f"{time} {activity}", font=("Verdana", 12), background="red")
        label.grid(row=row, column=0, sticky="w", pady=10, padx=5)
        list_activity.append(label)


root = Tk()
root.title("FOCUS FLOW")
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
nav_bar_button = Button(root, image = nav_bar_img_tk, command=open_daiy_plan_window, width="50", height="50",bg="white",borderwidth=0 )
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






left_frame = ttk.Frame(root)
left_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=5)

right_frame = ttk.Frame(root)
right_frame.grid(row=1, column=1, sticky="nsew", padx=10,pady=5)

daily_schedule = filter_activities_by_date(today)
display_activities(root,[left_frame,right_frame],daily_schedule,activity_labels)
#highlight_current_activity()



""" upper_frame = Label(root, background="red", text ="ROSSO" )
lower_frame = Label(root, background="blue", text ="BLUE" )
upper_frame.grid(column=1, row=0,sticky="nswe")
lower_frame.grid(column=0, row=0,sticky="nswe") """


root.mainloop()
