from tkinter import *
from tkinter import ttk,messagebox
from datetime import date, datetime, timedelta
import tkinter as tk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import json
import os

today = date.today()
add_logo_img = Image.open("./img/add_button.png").resize((35,35))

def add_recurrence_in_json(activity, formatted_date):
    
    with open('schedule_data.json', 'r') as f:
        schedule_data = json.load(f)

    new_activity = {
        "title": activity["title"],
        "time_range": activity["time_range"],
        "is_fixed": True  
    }
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
    with open('schedule_data.json', "r") as f:
        schedule_data = json.load(f)
    
    specific_day = next((day for day in schedule_data.get("specific_days", []) if day["date"] == formatted_date), None)
    if not specific_day:
        specific_day = {"date": formatted_date, "activities": []}
        schedule_data["specific_days"].append(specific_day)
        with open('schedule_data.json', "w") as f:
            json.dump(schedule_data, f, indent=4)
    for activity in schedule_data.get("fixed_activities", []):
        
        if activity["recurrence"] == "D" and (not activity.get("end_date") or date_to_check <= datetime.strptime(activity["end_date"], "%d/%m/%Y").date()):
            add_recurrence_in_json(activity, formatted_date)
        
        elif activity["recurrence"] == "W" and date_to_check.strftime("%A") == activity.get("day_of_week"):
            add_recurrence_in_json(activity, formatted_date)

        elif activity["recurrence"] == "M" and date_to_check.strftime("%A") == activity.get("day_of_week") and (date_to_check.day - 1) // 7 + 1 == activity.get("week_of_month"):
            add_recurrence_in_json(activity, formatted_date)
        elif activity["recurrence"] == "Y" and (not activity.get("end_date") or date_to_check <= datetime.strptime(activity["end_date"], "%d/%m/%Y").date()) and formatted_date[:5] == activity["date"][:5]:
            add_recurrence_in_json(activity, formatted_date)

    # Reload the updated schedule data to include added recurrences
    with open('schedule_data.json', "r") as f:
        schedule_data = json.load(f)
        
    
    specific_day = next((day for day in schedule_data.get("specific_days", []) if day["date"] == formatted_date), None)
    if specific_day:
        sort_activities_in_json()
        activities = specific_day["activities"]
        return [(activity["time_range"], activity["title"], activity.get("is_fixed", False)) for activity in activities]    
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
        
    

        self.add_day_img_tk = ImageTk.PhotoImage(add_logo_img)
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
        extra_window.wait_window()
        
        daily_schedule = filter_activities_by_date(self.current_day)
        display_activities(self,[self.left_frame,self.right_frame],daily_schedule,self.activity_labels)
        display_activities(root,[left_frame,right_frame],daily_schedule,activity_labels)
        
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
        name_activity_entry.grid(row = 1, column= 0, pady=10 , padx=10,sticky="nswe",columnspan=3)
        name_activity_entry.bind("<Button-1>", lambda event: clear_entry(event, name_activity_entry))
        
        
        
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
        start_time.grid(row=2, column=0, padx=10, pady=10,sticky="nwse")
        start_time.current(0)  

        
        end_time = ttk.Combobox(self, values=time_options, state="readonly", width=10)
        end_time.grid(row=2, column=1, padx=10, pady=10,sticky="nwse")
        end_time.current(0) 
        end_time.bind("<<ComboboxSelected>>", validate_time)
        
        
        confirm_button = Button(self,text = "ADD", command=self.insert_new_activity)
        confirm_button.grid(row=6, column=1, padx=10, pady=10,sticky="nwse",columnspan=3)
        
        self.is_repeating  = tk.IntVar()
        checkbutton = tk.Checkbutton(self, text="repeating?", variable=self.is_repeating, onvalue=1, offvalue=0,font=("Verdana", 12, "bold"), command=self.check_onchange)
        checkbutton.grid(row = 3 ,column=0,padx=10, pady=10,sticky="nws")
        
        self.type_of_rec = tk.StringVar()
        self.type_of_rec_combobox = ttk.Combobox(self,textvariable= self.type_of_rec, state="readonly")
        self.type_of_rec_combobox.grid(row = 3 , column= 1,padx=10, pady=10,sticky="we")
        self.type_of_rec_combobox["values"] = ["Daily", "Weekly" , "Monthly" , "Yearly"]
        self.type_of_rec_combobox.grid_remove()
        
        
        self.end_date_label = Label(self, text="End Date:", font=("Verdana", 12))
        self.end_date_label.grid(row=4, column=0, padx=10, pady=10, sticky="nw")
        self.end_date_label.grid_remove()  

        self.end_date_button = Button(self, text="Select Date", command=self.show_calendar)
        self.end_date_button.grid(row=4, column=1, padx=10, pady=10, sticky="nw")
        self.end_date_button.grid_remove()  

        self.selected_end_date = None
    def show_calendar(self):
            calendar_window = Toplevel(self)
            calendar_window.geometry("300x300+{}+{}".format(
        self.winfo_rootx() + (self.winfo_width() // 2) - 150,
        self.winfo_rooty() + (self.winfo_height() // 2) - 150
    ))
            calendar_window.title("Select End Date")
            calendar = Calendar(calendar_window, selectmode='day')
            calendar.pack(padx=10, pady=10)

            def select_date():
                selected_date = calendar.get_date()

                formatted_date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%d/%m/%Y")                
                self.selected_end_date = formatted_date
                messagebox.showinfo("Selected Date", f"End Date Selected:  {self.selected_end_date}")
                calendar_window.destroy()

        
     
    def check_onchange(self):
        if self.is_repeating.get() == 1:
            self.type_of_rec_combobox.grid() 
            self.end_date_label.grid()  
            self.end_date_button.grid()  
        else:
            self.type_of_rec_combobox.grid_remove() 
            self.end_date_label.grid_remove()
            self.end_date_button.grid_remove()
                 
    def insert_new_activity(self):
        
        with open('schedule_data.json',"r") as f:
            schedule_data = json.load(f)
        activity_title = self.children["!entry"].get()
        start_time = self.children["!combobox"].get()
        end_time = self.children["!combobox2"].get()
        formatted_date = self.current_day.strftime("%d/%m/%Y")
        if not activity_title or activity_title == "Title":
            messagebox.showerror("Error", "Please enter a valid title for the activity.")
            return

        if not start_time or not end_time:
            messagebox.showerror("Error", "Please select valid time ranges for the activity.")
            return

        
        if self.is_repeating.get() == 1:
            
            new_fixed = {
            "name": activity_title,
            "time_range": f"{start_time} - {end_time}",
            "recurrence": str(self.type_of_rec)[0],
            "day_of_week": self.current_day.strftime("%A"),
            "week_of_month" : (self.current_day.day - 1) // 7 + 1,
            "date" : formatted_date,
            "end_date" : self.selected_end_date 
            
            }
            
            
            schedule_data["fixed_activities"].append(new_fixed)
            
        else : 
        
            new_activity = {
                "title": activity_title,
                "time_range": f"{start_time} - {end_time}"
            }

       
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
        self.destroy()
        

class blocked_sites_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("FOCUS FLOW")
        self.geometry("700x500+610+290")
        self.minsize(500, 400)
        self.columnconfigure(0, weight=2, uniform="a")

        self.columnconfigure((1, 2, 3, 4), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.activity_labels = []
        self.rowconfigure(2, weight=1, uniform="a")
        self.rowconfigure(3, weight=4, uniform="a")
        self.grab_set()  # To make the root window untouchable
        self.set_gui()

    def set_gui(self):
        # HEAD
        
        nav_bar_img = Image.open("./img/9293128.png").resize((35, 35))
        self.nav_bar_img_tk = ImageTk.PhotoImage(nav_bar_img)
        

        nav_bar_button = Button(self, image=self.nav_bar_img_tk, width="50", height="50", bg="white", borderwidth=0)
        nav_bar_button.grid(column=0, row=0, sticky="nws", padx=5, pady=5)
        clock = Label(self,text="MANAGE BLOCKED SITES",font=("Verdana", 17), bg="#e84118", fg="#353b48")
        clock.grid(column=0, row=0, columnspan=5, sticky="nwse", ipadx="20", ipady="20")
        nav_bar_button.lift()

       
        try:
            with open("blocked_sites.json", "r") as f:
                sites_data = json.load(f)
        except FileNotFoundError:
            sites_data = {"sites": []}

        sites = [site["name"] for site in sites_data.get("sites", [])]

        sites_list = tk.StringVar(value=sites)

        self.sites_listbox = tk.Listbox(
            self,
            listvariable=sites_list,
            height=6,
            selectmode="extended",
            font=("Verdana", 12, "bold"),
            bg="#f0f8ff",
            fg="#333333",
            bd=2,
            relief="solid",
            highlightthickness=0,
            selectbackground="#ffa500",selectforeground="white",activestyle="none",
        )
        self.sites_listbox.grid(row=2, column=0, columnspan=5, rowspan=2, sticky="nsew", padx=10, pady=10)

        scrollbar_sites = ttk.Scrollbar(self, orient="vertical", command=self.sites_listbox.yview)
        scrollbar_sites.grid(row=2, column=4, rowspan=2, sticky="nse")

        self.sites_listbox["yscrollcommand"] = scrollbar_sites.set

        self.name_site = tk.StringVar()
        self.name_site_entry = tk.Entry(
            self, textvariable=self.name_site, font=("Verdana", 14), bg="#ffffff", borderwidth=0
        )
        self.name_site_entry.insert(0, "Name Site")
        self.name_site_entry.grid(row=1, column=0, pady=10, padx=10, sticky="nswe", columnspan=2)
        self.name_site_entry.bind("<Button-1>", lambda event: (clear_entry(event, self.name_site_entry),self.entry_onselect(event)))

        
        
        self.add_site_img_tk = ImageTk.PhotoImage(add_logo_img)
       

        self.add_button = Button(self,image=self.add_site_img_tk,width="50",height="50",borderwidth=0,command=lambda: self.add_site_in_json(self.name_site.get(), self.sites_listbox))
        self.add_button.grid(column=2, row=1, sticky="nsw", padx=5, pady=5)
        
        remove_img = Image.open("./img/delete_button.png").resize((40,40))
        self.remove_img_tk = ImageTk.PhotoImage(remove_img)
        self.remove_button = Button(self,image=self.remove_img_tk,width="50",height="50",borderwidth=0,state="disabled",command=self.remove_site)
        self.remove_button.grid(column=3, row=1, sticky="nsw", padx=5, pady=5)
        
        
       

        
        edit_img = Image.open("./img/edit_button.png").resize((40,40))
        self.edit_img_tk = ImageTk.PhotoImage(edit_img)
        self.edit_button = Button(self,image=self.edit_img_tk,width="50",height="50",borderwidth=0,command = self.edit_site,state="disabled")
        self.edit_button.grid(column=4, row=1, sticky="nsw", padx=5, pady=5)
        
        
        
        self.sites_listbox.bind('<<ListboxSelect>>', self.listbox_onselect)
        
    def listbox_onselect(self,evt):
        
        self.edit_button.config(state="normal")
        self.remove_button.config(state="normal")
        self.add_button.config(state="disabled")
        
    def entry_onselect(self,evt):
        
        self.edit_button.config(state="disabled")
        self.remove_button.config(state="disabled")
        self.add_button.config(state="normal")
        
        
        
       

    

    def add_site_in_json(self, name, listbox):
        if not name.strip():  
            messagebox.showerror("Error", "The entry can't be Empty!")
            return

        if name == "Name Site":
            messagebox.showerror("Error", "Please enter a valid title of the website.")
            return

        try:
            with open("blocked_sites.json", "r") as f:
                sites_data = json.load(f)
        except FileNotFoundError:
            sites_data = {"sites": []}

        site = next((site for site in sites_data.get("sites", []) if site["name"] == name), None)

        if not site:
            new_site = {"name": name}
            sites_data["sites"].append(new_site)

            with open("blocked_sites.json", "w") as f:
                json.dump(sites_data, f, indent=4)

            listbox.insert(tk.END, name)
            messagebox.showinfo("Success",f'Site "{name}" Added')
        else:
            messagebox.showwarning("Sorry", "Site Already in the File")

    def remove_site(self):
                selected_indices = self.sites_listbox.curselection()
                if not selected_indices:
                    messagebox.showerror("Errore", "Seleziona un sito dalla lista per eliminarlo!")
                    return

                selected_sites = [self.sites_listbox.get(i) for i in selected_indices]
                ans = messagebox.askyesno(title="Confirm", message="Are you sure to Delete this Site?")

                if ans:
                    
                    with open("blocked_sites.json", "r") as f:
                        sites_data = json.load(f)
                    

                    sites_data["sites"] = [site for site in sites_data["sites"] if site["name"] not in selected_sites]

                    with open("blocked_sites.json", "w") as f:
                        json.dump(sites_data, f, indent=4)

                    for index in reversed(selected_indices):  
                        self.sites_listbox.delete(index)

                    messagebox.showinfo("Confirmed", "Site Deleted Successfully!")
    def edit_site(self):
        selected_index = self.sites_listbox.curselection()
        

        old_name = self.sites_listbox.get(selected_index)

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Site Name")
        edit_window.geometry("300x150+810+465")
        edit_window.minsize(300,150)
        edit_window.maxsize(300,150)

        edit_window.grab_set()  

        
        tk.Label(edit_window, text="Edit the Name:", font=("Verdana", 12)).pack(pady=10)
        new_name_var = tk.StringVar(value=old_name)
        new_name_entry = tk.Entry(edit_window, textvariable=new_name_var, font=("Verdana", 12))
        new_name_entry.pack(pady=10, padx=10, fill="x")

        def confirm_edit():
            new_name = new_name_var.get().strip()
            if not new_name:
                messagebox.showerror("Error", "The name Can't be Empty!")
                return

           
            
            with open("blocked_sites.json", "r") as f:
                sites_data = json.load(f)
            
            for site in sites_data["sites"]:
                if site["name"] == old_name:
                    site["name"] = new_name
                    break

            with open("blocked_sites.json", "w") as f:
                json.dump(sites_data, f, indent=4)

            
            self.sites_listbox.delete(selected_index)
            self.sites_listbox.insert(selected_index, new_name)

            messagebox.showinfo("Success", f'Site "{old_name}" Edited in "{new_name}".')
            edit_window.destroy()


        tk.Button(edit_window, text="Confirm", command=confirm_edit, font=("Verdana", 12)).pack(pady=5)
        


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
    timevar = today.strftime("%a") + ", " +curr_time  + "\n"  + curr_day 
    clock.config(text = timevar)
    clock.after(200,get_time)

def clear_entry(event, entry):
    entry.delete(0, END)
        
def open_daiy_plan_window():
    root.withdraw()
    extra_window = week_plan_window()
    extra_window.protocol("WM_DELETE_WINDOW", lambda: reopen_window(extra_window))
   


    
def reopen_window(window):
    window.destroy() 
    root.deiconify()

def display_activities(self, frame, daily_schedule, list_activity):
    for label in list_activity:
        label.destroy()
    list_activity.clear()
    
    if not daily_schedule and not self == root :  # empty day
        label = ttk.Label(frame[0], text="No activities scheduled", font=("Verdana", 12), background="lightgray")
        label.grid(row=0, column=0, sticky="w", pady=10, padx=5)
        list_activity.append(label)
        
        return

    for idx, (time, activity,is_fixed) in enumerate(daily_schedule[:10]):
       
        target_frame = frame[0] if idx < 6 else frame[1]
        row = idx if idx < 6 else idx - 6
        bg_color = "lightblue" if is_fixed else "#e74c3c" 
        label = ttk.Label(target_frame, text=f"{time} {activity}", font=("Verdana", 12), background=bg_color)
        label.grid(row=row, column=0, sticky="w", pady=10, padx=5)
        list_activity.append(label)
    

root = Tk()
root.title("FOCUS FLOW")
root.geometry("700x600+610+220")
root.minsize(600,500)

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


def open_blocked_sites():
    root.withdraw()
    extra_window = blocked_sites_window()
    extra_window.protocol("WM_DELETE_WINDOW", lambda: reopen_window(extra_window) )
    
#Open Blocked Sites Button

open_week_plan_button = Button(root,command = open_blocked_sites, text = "Open Blocked Sites",  bg="lightgreen", width="50", height="50")
open_week_plan_button.grid(column=1,row=2,sticky="nwse",padx = 20 ,pady=20)

    

#Next Activity to Do

next_events = ["event " + str(i) for i in range(26)]
next_events_list = StringVar(value=next_events)
next_events_list = Listbox(root, listvariable=next_events_list, height=6,selectmode="extended", font=("Verdana", 10),justify=CENTER )
next_events_list.grid(row = 2 , column= 0,sticky="nsew",padx = 5,pady=5)

scrollbar_events = ttk.Scrollbar(root, orient="vertical", command=next_events_list.yview) 
scrollbar_events.grid(row = 2 , column= 0,sticky="nse")

next_events_list["yscrollcommand"] = scrollbar_events.set


#Today Plan

activity_labels = [] # References daily plan Labels for the main window


def block_sites():
    #  hosts path
    print("Blocking")
    if os.name == "nt":  # Windows
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    else:  # Linux/Mac
        hosts_path = "/etc/hosts"

    redirect_ip = "127.0.0.1"  #
    try:
        
        with open("blocked_sites.json", "r") as f:
            sites_data = json.load(f)

        sites_to_block = [site["name"] for site in sites_data.get("sites", [])]

        # reads the current hosth file
        with open(hosts_path, "r") as file:
            hosts_content = file.readlines()

        #adds just the new one
        with open(hosts_path, "a") as file:  
            for site in sites_to_block:
                entry = f"{redirect_ip} {site}\n"
                if entry not in hosts_content:
                    file.write(entry)
                    
    except PermissionError:
        messagebox.showerror("Error ", "No Admin Permissions!!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", e)


def unblock_sites():
    print("Unblocking")

    if os.name == "nt":
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    else:
        hosts_path = "/etc/hosts"

    try:
        with open(hosts_path, "r") as file:
            hosts_content = file.readlines()

        with open(hosts_path, "w") as file:
            for line in hosts_content:
                if not line.startswith("127.0.0.1"):
                    file.write(line)
    except PermissionError:
        messagebox.showerror("Error ", "No Admin Permissions!!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", e)



def highlight_current_activity():

    
    daily_schedule = filter_activities_by_date(today)
    current_time = datetime.now().strftime("%H:%M")  
    
    for idx, (time_range, activity, is_fixed) in enumerate(daily_schedule):
        start_time, end_time = time_range.split(" - ") 
        
        if start_time <= current_time <= end_time:
            try:
                activity_labels[idx].config(background="yellow", font=("Verdana", 12, "bold"))
            except IndexError:
                print("")
           
            block_sites()
        else:
            bg_color = "lightblue" if is_fixed else "#e74c3c"
            try:
                activity_labels[idx].config(background=bg_color, font=("Verdana", 12))
            except IndexError:
                print("")
            

    
    root.after(10000, highlight_current_activity)


left_frame = ttk.Frame(root)
left_frame.grid(row=1, column=0, sticky="nsew", padx=10,pady=5)

right_frame = ttk.Frame(root)
right_frame.grid(row=1, column=1, sticky="nsew", padx=10,pady=5)

daily_schedule = filter_activities_by_date(today)
display_activities(root,[left_frame,right_frame],daily_schedule,activity_labels)
highlight_current_activity()

root.protocol("WM_DELETE_WINDOW", lambda : (unblock_sites(),root.destroy()))

root.mainloop()
