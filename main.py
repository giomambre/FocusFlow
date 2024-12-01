from tkinter import *
from tkinter import ttk


root = Tk()
root.title("DEEP WORK ASSISTANT")
root.geometry("600x500+660+300")

""" root.minsize(400,200)
root.maxsize(600,500) """

root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.rowconfigure(0,weight=1)



upper_frame = Label(root, background="red", text ="ROSSO" )
lower_frame = Label(root, background="blue", text ="BLUE" )
upper_frame.grid(column=1, row=0,sticky="nswe")
lower_frame.grid(column=0, row=0,sticky="nswe")


root.mainloop()
