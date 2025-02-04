import customtkinter as ctk
from tkinter import messagebox
from CTkCalendar import CTkCalendar
import MyCalender
import sqlite3

class Task:
    _id_counter = 0  # Class-level variable for auto-increment ID

    def __init__(self, title, desc, date, task_id=None):
        if task_id is None:
            Task._id_counter += 1
            self.id = Task._id_counter  # Assign a unique ID
        else:
            self.id = task_id  # Use the provided ID
        self.title = title
        self.desc = desc
        self.date = date

class List(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.tasks = {}  # Dictionary to store tasks by their ID
        self.row_index = 0  # To keep track of rows for grid placement

    def add_item(self, title, desc, date, task_id=None, save_to_db=True):
        # Create a Task instance
        task = Task(title.capitalize(), desc, date, task_id)

        # Save to database if needed
        if save_to_db:
            task_id = add_task_to_db(title, desc, date)
            task.id = task_id

        # Create a container frame for the task
        container = ctk.CTkFrame(self, width=320, height=70, corner_radius=30)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)
        container.grid(row=self.row_index, column=0, padx=(0, 10), pady=5, sticky="ew")

        # Create label and buttons
        if len(title) > 15:
            title = f"{title[:15]}..."
        label = ctk.CTkLabel(container, text=title, font=("Arial", 18, "bold"))
        remove_button = ctk.CTkButton(
            container,
            text="Remove",
            width=70,
            height=24,
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.confirm_remove_item(task.id),
        )
        edit_button = ctk.CTkButton(
            container,
            text="Edit",
            width=70,
            height=24,
            fg_color="blue",
            hover_color="darkblue",
            command=lambda: self.edit_item(task.id),
        )

        # Add widgets to the container
        label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        remove_button.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        edit_button.grid(row=0, column=2, sticky="e", padx=10, pady=5)

        # Bind click event to the container
        container.bind(
            "<Button-1>", lambda event, task=task: self.on_container_click(task)
        )

        # Store the task and its container
        self.tasks[task.id] = container
        self.row_index += 1

    def on_container_click(self, task):
        """Handle the click event on the container."""
        title_label.configure(text="Title:")
        title_text.configure(text=task.title, wraplength=400, justify="left")
        desc_label.configure(text="Description:")
        desc_text.configure(text=task.desc, wraplength=400, justify="left")
        date_label.configure(text="Date:")
        date_text.configure(text=task.date, wraplength=400, justify="left")

    def confirm_remove_item(self, task_id):
        """Display a confirmation dialog before removing an item."""
        confirm = messagebox.askyesno(
            "Confirm Removal", f"Are you sure you want to remove this task?"
        )
        if confirm:
            self.remove_item(task_id)

    def remove_item(self, task_id):
        """Remove the task by destroying its container."""
        print(f"Attempting to remove task with ID: {task_id}")  # Debug statement
        if task_id in self.tasks:
            print(f"Task with ID: {task_id} found. Removing...")  # Debug statement
            self.tasks[task_id].destroy()  # Destroy the container
            del self.tasks[task_id]  # Remove from the dictionary
            remove_task_from_db(task_id)  # Remove from database
            self.rearrange_grid()  # Reorganize the grid layout
            print(f"Task with ID: {task_id} removed successfully.")  # Debug statement
        else:
            print(f"Task with ID: {task_id} not found.")  # Debug statement

    def rearrange_grid(self):
        """Rearrange items in the grid after one is removed."""
        self.row_index = 0
        for task_id, container in self.tasks.items():
            container.grid(row=self.row_index, column=0, padx=(0, 10), pady=5, sticky="ew")
            self.row_index += 1

    def edit_item(self, task_id):
        """Function to edit a task."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            edit_window = ctk.CTkToplevel(self)
            edit_window.title("Edit Task")
            edit_window.geometry("400x300")

            title_entry = ctk.CTkEntry(edit_window, placeholder_text="Task Title", width=300, height=40, font=("Arial", 18))
            desc_entry = ctk.CTkEntry(edit_window, placeholder_text="Task Description", width=300, height=40, font=("Arial", 18))
            calendar = MyCalender.Calendar(edit_window, width=300, height=200)

            title_entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
            desc_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            calendar.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

            def save_changes():
                new_title = title_entry.get()
                new_desc = desc_entry.get()
                new_date = calendar.getDate()
                if new_title and new_desc and new_date:
                    update_task_in_db(task_id, new_title, new_desc, new_date)
                    self.tasks[task_id].destroy()
                    del self.tasks[task_id]
                    self.add_item(new_title, new_desc, new_date, task_id=task_id, save_to_db=False)
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Invalid Input", "All fields are required to edit a task!")

            save_button = ctk.CTkButton(edit_window, text="Save", command=save_changes, width=120, fg_color="green", hover_color="darkgreen")
            save_button.grid(row=3, column=0, pady=10, sticky="ew", padx=10)

def initialize_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_task_to_db(title, description, date):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, date)
        VALUES (?, ?, ?)
    """, (title, description, date))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def remove_task_from_db(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task_in_db(task_id, title, description, date):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, date = ?
        WHERE id = ?
    """, (title, description, date, task_id))
    conn.commit()
    conn.close()

def load_tasks_from_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def search_tasks(query):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE title LIKE ?", ('%' + query + '%',))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def list_mainloop():
    # CustomTkinter appearance settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Main application window
    app = ctk.CTk()
    app.title("To-Do List")
    app.geometry("1200x680")
    app.resizable(False,False)
    # Configure grid weights
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # Create a frame for the task list
    frame = ctk.CTkFrame(app, width=400, height=550, corner_radius=30)
    frame.grid(row=0, column=0, rowspan=2, sticky="nsw", padx=15, pady=(20, 20))

    # Create display frame
    display_frame = ctk.CTkFrame(app, corner_radius=30)
    display_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=(20, 10))
    display_frame.grid_rowconfigure((0, 1, 2), weight=1)
    display_frame.grid_columnconfigure((0, 1), weight=1)

    global title_label, title_text, date_label, date_text, desc_label, desc_text

    title_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 20), anchor="w")
    title_label.grid(row=0, column=0, sticky="nw", padx=20, pady=10)
    title_text = ctk.CTkLabel(display_frame, text="", font=("Arial", 20), anchor="w", wraplength=400, justify="left")
    title_text.grid(row=0, column=1, sticky="nw", padx=20, pady=10)

    desc_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 20), anchor="w")
    desc_label.grid(row=1, column=0, sticky="nw", padx=20, pady=10)
    desc_text = ctk.CTkLabel(display_frame, text="", font=("Arial", 20), anchor="w", wraplength=400, justify="left")
    desc_text.grid(row=1, column=1, sticky="nw", padx=20, pady=10)

    date_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 20), anchor="w")
    date_label.grid(row=2, column=0, sticky="nw", padx=20, pady=10)
    date_text = ctk.CTkLabel(display_frame, text="", font=("Arial", 20), anchor="w", wraplength=400, justify="left")
    date_text.grid(row=2, column=1, sticky="nw", padx=20, pady=10)

    # Create creation frame
    creation_frame = ctk.CTkFrame(app, corner_radius=30)
    creation_frame.grid(row=1, column=1, sticky="nsew", padx=15, pady=(10, 20))
    creation_frame.grid_columnconfigure((0, 2), weight=1)
    creation_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

    # Create an info frame inside creation_frame
    info_frame = ctk.CTkFrame(creation_frame, corner_radius=30)
    info_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
    info_frame.grid_columnconfigure((0, 1), weight=1)
    info_frame.grid_rowconfigure((0, 1), weight=1)

    # Entry fields
    title_entry = ctk.CTkEntry(info_frame, placeholder_text="Task Title", width=300, height=40,font=("Arial", 18))
    desc_entry = ctk.CTkEntry(info_frame, placeholder_text="Task Description", width=300, height=40,font=("Arial", 18))
    calendar = MyCalender.Calendar(info_frame, width=300, height=200)

    title_entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    desc_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    calendar.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")

    # Add Task button
    def add_task():
        """Function to add a task dynamically."""
        title = title_entry.get()
        desc = desc_entry.get()
        date = calendar.getDate()
        if title and desc and date:
            lst.add_item(title, desc, date)
            title_entry.delete(0, "end")
            desc_entry.delete(0, "end")
            calendar.resetButton()
        else:
            messagebox.showwarning("Invalid Input", "All fields are required to create a task!")

    add_button = ctk.CTkButton(creation_frame, text="Add Task", command=add_task, width=120, fg_color="green", hover_color="darkgreen")
    add_button.grid(row=1, column=1, pady=10, sticky="ew", padx=210)
    frame.grid_columnconfigure(0, weight=1)

    # Return to Main Menu button
    def return_to_menu():
        app.destroy()
        from main_menu import main_menu_mainloop
        main_menu_mainloop()

    return_button = ctk.CTkButton(creation_frame, text="Main Menu", command=return_to_menu, width=120, fg_color="red", hover_color="darkred")
    return_button.grid(row=2, column=1, pady=(10, 20), sticky="ew", padx=180)

    # Create the custom List widget
    lst = List(frame, width=300, height=480, corner_radius=30)
    lst.grid(row=0, column=0, sticky="nsw", padx=15, pady=(20, 20))

    def clear_tasks():
        """Function to clear all tasks from the list and the database."""
        # Confirm with the user before clearing
        confirm = messagebox.askyesno(
            "Confirm Clear", "Are you sure you want to clear all tasks?"
        )
        if not confirm:
            return

        # Clear the database
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        conn.close()

        # Clear the tasks from the List widget
        for task_id, container in lst.tasks.items():
            container.destroy()  # Destroy the UI element
        lst.tasks.clear()  # Clear the dictionary
        lst.row_index = 0  # Reset the row index

        # Inform the user
        messagebox.showinfo("Clear List", "All tasks have been cleared!")

    # Add a row configuration for the Clear List button
    frame.grid_rowconfigure(1, weight=0)

    # Add the Clear List button
    clear_btn = ctk.CTkButton(
        frame,
        text="Clear List",
        command=clear_tasks,
        width=120,
        fg_color="red",
        hover_color="darkred",
    )
    clear_btn.grid(row=1, column=0, pady=10, sticky="ew", padx=20)

    # Add search bar and button
    search_entry = ctk.CTkEntry(frame, placeholder_text="Search Tasks", width=200, height=40, font=("Arial", 18))
    search_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    def search():
        query = search_entry.get()
        tasks = search_tasks(query)
        for task_id, container in lst.tasks.items():
            container.destroy()
        lst.tasks.clear()
        lst.row_index = 0
        for task in tasks:
            lst.add_item(task[1], task[2], task[3], task_id=task[0], save_to_db=False)

    search_button = ctk.CTkButton(frame, text="Search", command=search, width=120, fg_color="blue", hover_color="darkblue")
    search_button.grid(row=3, column=0, pady=10, sticky="ew", padx=20)

    # Load tasks from database
    tasks = load_tasks_from_db()
    for task in tasks:
        lst.add_item(task[1], task[2], task[3], task_id=task[0], save_to_db=False)

    app.mainloop()

if __name__ == "__main__":
    initialize_database()
    list_mainloop()