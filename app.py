import tkinter as tk
import customtkinter as ctk
from tkinter import *
import os

def main():
    open_app()
    

def open_app():
    root = tk.Tk()
    background_color = "gray"
    set_window_background_color(root, background_color)
    resizeable(root, False)
    set_window_title(root, 'Todo List')
    set_window_icon(root, './ICON.ico')
    set_window_size(root, "500x500")
    
    # input box
    task_input_label = add_label(root, bg=background_color, text="New Task: " , x=10, y=10)
    task_input_box = add_input_box(root, width=50, x=100, y=10)

    # tasks label
    tasks_label = add_label(root, bg=background_color, text="Current Tasks: ", x=10, y=100)

    # no current tasks label (initially visible)
    no_task_label = add_label(root, bg=background_color, text="No current tasks", x=120, y=100, font=('Arial', 10, 'italic'))

    # checkbox button frame
    button_frame = add_frame(root, background_color, x=0, y=120)

    # functional buttons
    task_add_button = add_button(root, function = lambda: add_task(task_input_box, button_frame, no_task_label), text="Add Task", x=10, y=40)
    task_remove_button = add_button(root, function =lambda: remove_task(button_frame, no_task_label), text="Remove Completed Tasks", x=80, y=40)

    # load data
    load_tasks(button_frame, no_task_label)

    root.mainloop()


def set_window_background_color(root, color):
    root.configure(bg=color)


def resizeable(root, boolval=True):
    root.resizable(boolval,boolval)


def set_window_title(root, title):
    root.title(title)


def set_window_size(root, size):
    root.geometry(size)


def set_window_icon(root, iconPath):
    root.iconbitmap(iconPath)


def add_frame(root, bg="lightblue", width=500, height=350, x=0, y=0):
    frame = ctk.CTkScrollableFrame(root, width=width, height=height, fg_color=bg)
    frame.place(x=x, y=y)

    # list of check buttons
    frame.check_buttons = []

    return frame


def add_label(root, text="__labelText__", bg="lightblue", x=0, y=0, font=('Arial', 10, 'bold')):
    label = tk.Label(root, bg=bg, font=font, text=text)
    label.place(x=x, y=y)
    return label


def add_input_box(root, width=30, x=0, y=0):
    entry = tk.Entry(root, width=width)
    entry.place(x=x,y=y)
    return entry


def add_button(root, text="__buttonText__", bd=0, highlightcolor='blue', relief="raised", function=None, x=0, y=0):
    if function is None:
        function = default_function
    button = tk.Button(root, text=text, bd=bd, highlightcolor=highlightcolor, relief=relief, command=function)
    button.place(x=x,y=y)
    return button
    

def add_check_button(root, text="__checkButtonText__", height=2, width=500, bg="lightblue", anchor="w", wraplength=500):
    check_var = IntVar()
    button = Checkbutton(root, text=text, variable=check_var, onvalue=1, offvalue=0, height=height, width=width, bg=bg, anchor=anchor, wraplength=wraplength)
    button.pack(anchor=anchor)

    # add button to list of button frame buttons
    root.check_buttons.append((button, check_var))

    return button


def add_task(task_entry, checkbox_frame, no_task_label):
    task = task_entry.get()
    if task == "": # if entry box empty
        return None
    add_check_button(checkbox_frame, bg="gray", text=task)

    # remove default no tasks message
    no_task_label.place_forget()

    # save task
    save_task_to_file(task)


def remove_task(checkbox_frame, no_task_label):
    for check_button, check_var in checkbox_frame.check_buttons[:]:
        if check_var.get() == 1:  # if button checked
            check_button.destroy()
            checkbox_frame.check_buttons.remove((check_button, check_var))

    # show no tasks message if all tasks removed
    if not checkbox_frame.check_buttons:
        show_no_task_label(no_task_label)

    # after removal, save all current remaining tasks
    save_all_tasks_to_file(checkbox_frame)


    
def default_function():
    print('No button function added')


def show_no_task_label(no_task_label):
    no_task_label.place(x=120, y=100)


# tasks path
SAVED_TASKS = "tasks.txt"

def save_task_to_file(task):
    # save one task
    with open(SAVED_TASKS, "a") as file:
        file.write(task + "\n")


def save_all_tasks_to_file(checkbox_frame):
    # save all tasks
    with open(SAVED_TASKS, "w") as file:
        for check_button, check_var in checkbox_frame.check_buttons[:]:
            file.write(check_button.cget("text") + "\n")


def load_tasks(checkbox_frame, no_task_label):
    
    if os.path.exists(SAVED_TASKS):
        with open(SAVED_TASKS, "r") as file:
            tasks = file.readlines()
        
        # add saved tasks to task frame
        for task in tasks:
            task = task.strip()  # remove any leading/trailing whitespace
            add_check_button(checkbox_frame, bg="gray", text=task)

        # remove no task label if tasks, and vice versa
        if tasks:
            no_task_label.place_forget()
        else:
            show_no_task_label(no_task_label)
 


if __name__ == "__main__":
    main()