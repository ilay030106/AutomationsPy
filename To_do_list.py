import customtkinter as ctk
from tkinter import messagebox


class List(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.tasks = {}  # A dictionary to map labels to their containers
        self.row_index = 0  # To keep track of rows for grid placement

    def add_item(self, item, image=None):
        # Create a container frame for each item
        item=item.capitalize()
        container = ctk.CTkFrame(self, width=320, height=70, corner_radius=30)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)
        container.grid(row=self.row_index, column=0, padx=(0, 10), pady=5, sticky="ew")

        # Add click event binding to the container
        container.bind("<Button-1>", lambda event, task=item: self.on_container_click(task))

        # Create the label and button
        label = ctk.CTkLabel(container, text=item, image=image, compound="center", padx=5, anchor="w",font=("Ariel",18,"bold"))
        button = ctk.CTkButton(
            container,
            text="Remove",
            width=70,
            height=24,
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.confirm_remove_item(item),
        )

        # Add widgets to the container
        label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        button.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Add to the tasks dictionary and update the row index
        self.tasks[item] = container
        self.row_index += 1

    def on_container_click(self, task):
        """Handle the click event on the container."""
        messagebox.showinfo("Container Clicked", f"You clicked on: {task}")

    def confirm_remove_item(self, item):
        """Display a confirmation dialog before removing an item."""
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{item}'?")
        if confirm:
            self.remove_item(item)

    def remove_item(self, item):
        """Remove the item by destroying its container."""
        if item in self.tasks:
            self.tasks[item].destroy()  # Destroy the container
            del self.tasks[item]       # Remove from the dictionary
            self.rearrange_grid()      # Reorganize the grid layout

    def rearrange_grid(self):
        """Rearrange items in the grid after one is removed."""
        self.row_index = 0
        for item, container in self.tasks.items():
            container.grid(row=self.row_index, column=0, padx=10, pady=5, sticky="ew")
            self.row_index += 1


def list_mainloop():
    # CustomTkinter appearance settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Main application window
    app = ctk.CTk()
    app.title("To-Do List")
    app.geometry("1200x600")

    # Create a frame
    frame = ctk.CTkFrame(app, width=400, height=550, corner_radius=30)
    frame.grid(row=0, column=0, sticky="nsw", padx=15, pady=(20, 20))

    # Create the custom List widget
    lst = List(frame, width=370, height=480, corner_radius=30)
    lst.grid(row=0, column=0, sticky="nsw", padx=15, pady=(20, 20))

    # Add items to the list
    lst.add_item("ilay")
    lst.add_item("task 2")
    lst.add_item("task 3")

    # Example of removing an item


    app.mainloop()


if __name__ == "__main__":
    list_mainloop()
