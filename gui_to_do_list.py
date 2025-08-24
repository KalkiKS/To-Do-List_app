import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

TASK_FILE = "tasks.json"


def load_task():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# Add a new task
def add_task():
    task = task_entry.get().strip()
    due_date = due_date_entry.get().strip()
    category = category_var.get()

    if not task:
        messagebox.showwarning("Input Error", "Please enter a task.")
        return
    
    tasks.append({
        "task": task,
        "due_date": due_date if due_date else None,
        "category": category,
        "done": False
    })
    save_tasks()
    update_task_list()
    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    category_var.set("General")

def toggle_done(event):
    selected = task_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    task_text = task_listbox.get(index)
    actutal_task = displayed_tasks[index]
    for t in tasks:
        if t == actutal_task:
            t['done'] = not t['done']
            break
    save_tasks()
    update_task_list()

def edit_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showinfo("Select Task", "Please select a task to edit.")
        return
    index = selected[0]
    task = displayed_tasks[index]
    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    task_entry.insert(0, task["task"])
    due_date_entry.insert(0, task.get("due_date", ""))
    category_var.set(task.get("category", "General"))
    tasks.remove(task)
    update_task_list()

def delete_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showinfo("Select Task", "Please select a task to delete.")
        return
    index = selected[0]
    task_to_delete = displayed_tasks[index]
    tasks.remove(task_to_delete)
    save_tasks()
    update_task_list()

def update_task_list():
    global displayed_tasks
    task_listbox.delete(0, tk.END)

    displayed_tasks = sorted(tasks, key=lambda x: x.get("due_date") or "9999-12-31")

    for task in displayed_tasks:
        status = "✓" if task["done"] else " "
        due = f"(Due: {task['due_date']})" if task.get("due_date") else ""
        category = f"[{task.get('category', 'General')}]"
        display_text = f"[{status}] {task['task']} {category} {due}"
        task_listbox.insert(tk.END, display_text)

# Main GUI setup
window = tk.Tk()
window.title("To-Do List")
window.geometry("700x600")
window.resizable(False, False)

ttk.Label(window, text="Task:").pack(pady=5)
task_entry = ttk.Entry(window, width=50)
task_entry.pack()

ttk.Label(window, text="Due Date (YYYY-MM-DD):").pack(pady=5)
due_date_entry = ttk.Entry(window, width=50)
due_date_entry.pack()


# Category selection (optional)
ttk.Label(window, text="Category:").pack(pady=5)
category_var = tk.StringVar(value="General")
category_menu = ttk.Combobox(window, textvariable=category_var, values=["General", "Work", "Personal", "Urgent"], state="readonly")
category_menu.pack()

ttk.Button(window, text="Add Task", command=add_task).pack(pady=10)

task_listbox = tk.Listbox(window, width=80, height=15, font=("Courier", 12))
task_listbox.pack(pady=10)
task_listbox.bind("<Double-Button-1>", toggle_done)

button_frame = ttk.Frame(window)
button_frame.pack(pady=5)

ttk.Button(button_frame, text="Edit Task", command=edit_task).pack(side="left", padx=10)
ttk.Button(button_frame, text="Delete Task", command=delete_task).pack(side="left", padx=10)

tasks = load_task()
displayed_tasks = []
update_task_list()

window.mainloop()