from tkinter import *

root=Tk()
root.title('ToDo List')
root.geometry('500x650+400+100')
root.resizable(False,False)

task_list=[]

def addTask():
    task = task_entry.get()
    task_entry.delete(0,END)

    if task:
        with open('tasklist.txt','a')as taskfile:
            taskfile.write(f'\n{task}')
        task_list.append(task)
        listbox.insert(END,task)

def updateTask():
    global task_list
    selection_index = listbox.curselection()
    if selection_index:
        selected_task_index = selection_index[0]
        updated_task = task_entry.get()
        
        if updated_task:
            task_list[selected_task_index] = updated_task
            listbox.delete(selected_task_index)
            listbox.insert(selected_task_index, updated_task)
            
            with open('tasklist.txt', 'w') as taskfile:
                for task in task_list:
                    taskfile.write(task + '\n')
            
            task_entry.delete(0, END)

            
def deleteTask():
    global task_list
    task = str(listbox.get(ANCHOR))
    if task in task_list:
        task_list.remove(task)
        with open('tasklist.txt','w') as taskfile:
            for task in task_list:
                taskfile.write(task+'\n')
        listbox.delete(ANCHOR)
        
def toggleSelection(event):
    widget = event.widget
    index = widget.nearest(event.y)
    
    if widget.curselection():
        current_index = widget.curselection()[0]
        if current_index == index:
            widget.selection_clear(current_index)
        else:
            widget.selection_clear(current_index)
            widget.selection_set(index)
    else:
        widget.selection_set(index)

        
def openTaskFile():
    try:
        global task_list
        with open('tasklist.txt','r') as taskfile:
            tasks = taskfile.readlines()
        for task in tasks:
            if task != '\n':
                task_list.append(task)
                listbox.insert(END,task)
    except:
        file=open('tasklist.txt','w')
        file.close()

#Creating Icon
image_icon=PhotoImage(file=r'images/icon.png')
root.iconphoto(False,image_icon)

#Top bar
top_image=PhotoImage(file=r"images/top_bar.png")
Label(root,image=top_image,bg='pink').pack()

#delete
delete_icon=PhotoImage(file=r"images/delete.png")
Button(root,image=delete_icon,bg='pink',bd=0,command=deleteTask).place(x=230,y=554)

#main
frame=Frame(root,width=408,height=40,bg='#837bea')
frame.place(x=46,y=148)

task=StringVar()
task_entry=Entry(frame,width=28,font='times 18',fg='black',bg='white',bd=0)
task_entry.place(x=5,y=5)
task_entry.focus()

button=Button(frame,text='Add',font='times 12 bold',width=5,bg='#837bea',fg='white',bd=0,command=addTask)
button.place(x=291,y=5)
button=Button(frame,text='Update',font='times 12 bold',width=5,bg='#837bea',fg='white',bd=0,command=updateTask)
button.place(x=348,y=5)

#list box
frame1=Frame(root,bd=3,width=700,height=280,bg='#837bea')
frame1.place(x=46,y=192)

listbox=Listbox(frame1,font=('times',14),width=42,height=16,bg='pink',fg='black',cursor='hand2',selectbackground='#837bea')
listbox.pack(side=LEFT,fill=BOTH,padx=2)
scrollbar=Scrollbar(frame1,bg='pink')
scrollbar.pack(side= RIGHT, fill=BOTH)

#scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

#bind single click toggle selection
listbox.bind("<Button-1>", toggleSelection)

openTaskFile()

root.mainloop()
