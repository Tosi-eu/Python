from tkinter import *
from tkinter import messagebox

def newTask():

  with open('Tasks.csv', 'w') as file:
    task = my_entry.get()
    if task != "":
        lb.insert(END, task)
        my_entry.delete(0, "end")
        task_list.append(task)
        file.write(task)
        file.close()
    
    else:
        messagebox.showwarning("warning", "Please enter some task.")
        file.close()

def newTaskHour():

    hour = my_entry.get()
    lb.insert(END, hour)
    my_entry.delete(0, "end")

def deleteTask():
    lb.delete(ANCHOR)

ws = Tk()
ws.geometry('1280x720+150+30') #widow dimensions (horizontal x vertical, Xaxis x Yaxis)
ws.title('To Do List') #widow title
ws.config(bg = '#223441') # widow color
ws.resizable(width = False, height = False)

frame = Frame(ws)
frame.pack(pady=20)

lb = Listbox(
    frame,
    width = 50,
    height = 15,
    font = ('Arial', 12),
    bd = 2,
    fg = '#464646',
    highlightthickness = 2,
    selectbackground = '#a6a6a6',
    activestyle = "none",
    
)
lb.pack(side = RIGHT, fill = BOTH)

task_list = []

for item in task_list:
    lb.insert(END, item)
    task_list.insert(item)

sb = Scrollbar(frame)
sb.pack(side = RIGHT, fill = BOTH)

lb.config(yscrollcommand = sb.set)
sb.config(command = lb.yview)

my_entry = Entry(
    ws,
    font = ('Arial', 18),
    bd = 2
    )
my_entry.pack(pady = 20)

button_frame = Frame(ws)
button_frame.pack(pady = 20)

addTask_btn = Button(
    button_frame,
    text='Add Task',
    font=('Arial', 12),
    bg='#c5f776',
    padx = 8,
    pady = 2,
    command = newTask
)
addTask_btn.pack(fill = BOTH, expand = True, side = LEFT)

addHour_btn = Button(
    button_frame,
    text='Add Hour Task',
    font=('Arial', 14),
    bg='#c5f776',
    padx = 8,
    pady = 2,
    command = None
)
addHour_btn.pack(fill = BOTH, expand = True, side = LEFT)

delTask_btn = Button(
    button_frame,
    text = 'Delete Task',
    font = ('Arial', 14),
    bg = '#ff8b61',
    padx = 8,
    pady = 2,
    command = deleteTask
)

delTask_btn.pack(fill = BOTH, expand = True, side = LEFT)

ws.mainloop()
