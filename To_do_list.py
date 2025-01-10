import customtkinter as ctk
from tkinter import messagebox
from CTkCalendar import CTkCalendar
import MyCalender
class Task:
    _id_counter = 0  # Class-level variable for auto-increment ID

    def __init__(self, title, desc, date):
        Task._id_counter += 1
        self.id = Task._id_counter  # Assign a unique ID
        self.title = title
        self.desc = desc
        self.date = date


class List(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.tasks = {}
        self.row_index = 0

    def add_item(self, title, desc, date):
        task = Task(title.capitalize(), desc, date)

        container = ctk.CTkFrame(self, width=320, height=70, corner_radius=30)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)
        container.grid(row=self.row_index, column=0, padx=(0, 10), pady=5, sticky="ew")

        # Create label and button
        if len(title)>=15:
            title=title[:15]+"..."
            label = ctk.CTkLabel(container, text=title, font=("Arial", 18, "bold"))
        else:
            label = ctk.CTkLabel(container, text=task.title, font=("Arial", 18, "bold"))
        button = ctk.CTkButton(
            container,
            text="Remove",
            width=70,
            height=24,
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.confirm_remove_item(task.id),
        )

        # Add widgets to the container
        label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        button.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Bind click event to the container
        container.bind(
            "<Button-1>", lambda event, task=task: self.on_container_click(task)
        )

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
        if task_id in self.tasks:
            self.tasks[task_id].destroy()
            del self.tasks[task_id]
            self.rearrange_grid()

    def rearrange_grid(self):
        """Rearrange items in the grid after one is removed."""
        self.row_index = 0
        for task_id, container in self.tasks.items():
            container.grid(row=self.row_index, column=0, padx=(0, 10), pady=5, sticky="ew")
            self.row_index += 1

def list_mainloop():
    # CustomTkinter appearance settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Main application window
    app = ctk.CTk()
    app.title("To-Do List")
    app.geometry("1200x600")

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

    title_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 16), anchor="w")
    title_label.grid(row=0, column=0, sticky="nw", padx=20, pady=10)
    title_text = ctk.CTkLabel(display_frame, text="", font=("Arial", 16), anchor="w", wraplength=400, justify="left")
    title_text.grid(row=0, column=1, sticky="nw", padx=20, pady=10)

    desc_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 16), anchor="w")
    desc_label.grid(row=1, column=0, sticky="nw", padx=20, pady=10)
    desc_text = ctk.CTkLabel(display_frame, text="", font=("Arial", 16), anchor="w", wraplength=400, justify="left")
    desc_text.grid(row=1, column=1, sticky="nw", padx=20, pady=10)

    date_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 16), anchor="w")
    date_label.grid(row=2, column=0, sticky="nw", padx=20, pady=10)
    date_text = ctk.CTkLabel(display_frame, text="", font=("Arial", 16), anchor="w", wraplength=400, justify="left")
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
    title_entry = ctk.CTkEntry(info_frame, placeholder_text="Task Title", width=300, height=40)
    desc_entry = ctk.CTkEntry(info_frame, placeholder_text="Task Description", width=300, height=40)
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
    add_button.grid(row=1, column=1, pady=10, sticky="ew", padx=170)

    # Return to Main Menu button
    def return_to_menu():
        app.destroy()
        from main_menu import main_menu_mainloop
        main_menu_mainloop()

    return_button = ctk.CTkButton(creation_frame, text="Main Menu", command=return_to_menu, width=120, fg_color="red", hover_color="darkred")
    return_button.grid(row=2, column=1, pady=(10, 20), sticky="ew", padx=120)

    # Create the custom List widget
    lst = List(frame, width=370, height=480, corner_radius=30)
    lst.grid(row=0, column=0, sticky="nsw", padx=15, pady=(20, 20))

    # Add initial tasks
    lst.add_item("Task 1", "Description 1", "2025-01-09")
    lst.add_item("Task 2", "Description 2", "2025-01-10")
    lst.add_item("Task 3", "Description 3", "2025-01-11")

    app.mainloop()


if __name__ == "__main__":
    list_mainloop()
