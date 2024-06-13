#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import pyttsx3

class TodoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")

        self.frame_tasks = tk.Frame(master)
        self.frame_tasks.pack(pady=10)

        self.listbox_tasks = tk.Listbox(self.frame_tasks, height=10, width=50, border=0)
        self.listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar_tasks = tk.Scrollbar(self.frame_tasks, orient=tk.VERTICAL, command=self.listbox_tasks.yview)
        self.scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_tasks.config(yscrollcommand=self.scrollbar_tasks.set)

        self.entry_task = tk.Entry(master, width=50)
        self.entry_task.pack(pady=5)

        self.frame_priority = tk.Frame(master)
        self.frame_priority.pack()

        self.radio_priority = tk.StringVar(value="non-important")
        self.radio_important = tk.Radiobutton(self.frame_priority, text="Important", variable=self.radio_priority, value="important")
        self.radio_important.pack(side=tk.LEFT)

        self.radio_non_important = tk.Radiobutton(self.frame_priority, text="Non-important", variable=self.radio_priority, value="non-important")
        self.radio_non_important.pack(side=tk.LEFT)

        self.frame_buttons = tk.Frame(master)
        self.frame_buttons.pack()

        self.buttons = [
            ("Add Task", self.add_task),
            ("Delete Task", self.delete_task),
            ("Clear All", self.clear_tasks),
        ]

        for text, command in self.buttons:
            button = tk.Button(self.frame_buttons, text=text, width=10, command=command)
            button.pack(side=tk.LEFT)

        self.entry_search = tk.Entry(master, width=30)
        self.entry_search.pack(pady=5)

        self.button_search_task = tk.Button(master, text="Search", width=10, command=self.search_task)
        self.button_search_task.pack()

        self.load_tasks()

       
        self.engine = pyttsx3.init()

       
        self.master.after(60000, self.check_reminders)

    def add_task(self):
        task = self.entry_task.get().strip()
        priority = self.radio_priority.get()
        if priority == "important":
            reminder_time = simpledialog.askstring("Reminder", "Enter reminder time (format: HH:MM):")
            if not reminder_time:
                messagebox.showwarning("Warning", "Reminder time not set.")
                return
        else:
            reminder_time = None

        if task:
            task_info = f"{task} - ({priority}) - {reminder_time if reminder_time else 'None'}"
            self.listbox_tasks.insert(tk.END, task_info)
            self.save_tasks()  # Corrected method call
            self.entry_task.delete(0, tk.END)
            messagebox.showinfo("Success", "Task added successfully.")
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        try:
            index = self.listbox_tasks.curselection()[0]
            self.listbox_tasks.delete(index)
            self.save_tasks()
            messagebox.showinfo("Success", "Task deleted successfully.")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def clear_tasks(self):
        self.listbox_tasks.delete(0, tk.END)
        self.save_tasks()
        messagebox.showinfo("Success", "All tasks cleared successfully.")

    def search_task(self):
        keyword = self.entry_search.get().strip().lower()
        found = False
        self.listbox_tasks.selection_clear(0, tk.END)
        for i in range(self.listbox_tasks.size()):
            if keyword in self.listbox_tasks.get(i).lower():
                self.listbox_tasks.selection_set(i)
                self.listbox_tasks.activate(i)
                self.listbox_tasks.see(i)
                found = True
        if not found:
            messagebox.showinfo("Info", f"No tasks containing '{keyword}' found.")

    def save_tasks(self):
        tasks = self.listbox_tasks.get(0, tk.END)
        with open("tasks.txt", "w") as f:
            for task in tasks:
                f.write(task + "\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                for line in f:
                    self.listbox_tasks.insert(tk.END, line.strip())
        except FileNotFoundError:
            pass

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def check_reminders(self):
        current_time = datetime.now().strftime("%H:%M")
        for index in range(self.listbox_tasks.size()):
            task_info = self.listbox_tasks.get(index)
            task_time = task_info.split("-")[-1].strip()
            if task_time and current_time == task_time:
                self.speak(f"Don't forget to complete {task_info.split('-')[0].strip()}")
       
        self.master.after(60000, self.check_reminders)


def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:




