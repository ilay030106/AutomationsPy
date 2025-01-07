import customtkinter as ctk
import tkinter.messagebox as messagebox
from main_menu import main_menu_mainloop

def calculator_mainloop():
    """
    Launches the calculator GUI using the customtkinter library.

    This function creates a simple calculator interface with buttons for digits, basic operations, and an option to
    return to the main menu. The calculator performs arithmetic evaluations of expressions entered the display.
    """
    # Set appearance mode: Choose between "Dark", "Light", or "System" (system default)
    ctk.set_appearance_mode("System")

    # Set a custom button color theme using hex color codes
    button_blue = "#0747f7"  # Default button color
    button_blue_hover = "#0963ff"  # Hover color for buttons

    # Set color theme: Options include "blue", "green", "dark-blue", or custom themes
    ctk.set_default_color_theme("blue")

    # Create the calculator window
    app = ctk.CTk()
    app.title("Calculator")
    app.geometry("430x550")  # Set the size of the window in pixels (width x height)

    # Define custom fonts for display and buttons
    font_large = ("Helvetica", 20)  # Font for the display
    font_buttons = ("Helvetica", 18)  # Font for the buttons
    font_display = ("Helvetica", 24)  # Font for the input display

    # Entry widget for the calculator display
    disp = ctk.CTkEntry(app, font=font_display, justify="right", corner_radius=10, height=50, width=400)
    disp.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

    # Function to handle button clicks
    def clk(b):
        """
        Handles button clicks for the calculator.

        :param b: The button label (e.g., digits, operations, or commands like '=' or 'C').
        """
        if b == '=':
            try:
                disp.insert(ctk.END, f"={eval(disp.get())}")
            except Exception:
                disp.delete(0, ctk.END)
                disp.insert(0, "Error")
        elif b == 'C':
            disp.delete(0, ctk.END)
        else:
            if '=' in disp.get():
                disp.delete(0, disp.get().find('=') + 1)
            if "Error" in disp.get():
                disp.delete(0, ctk.END)
            disp.insert(ctk.END, b)

    # Function to return to the main menu
    def return_to_main():
        """
        Closes the calculator and returns to the main menu.
        """
        app.destroy()
        main_menu_mainloop()

    # Button labels for the calculator
    btns = ['7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C']

    # Configure button colors, sizes, and placement
    for i, b in enumerate(btns):
        ctk.CTkButton(app, text=b, command=lambda x=b: clk(x), font=font_buttons,
                      height=60, width=80, corner_radius=20, fg_color=button_blue,
                      hover_color=button_blue_hover, text_color="white") \
            .grid(row=i // 4 + 2, column=i % 4)

    # Add a button to return to the main menu
    ctk.CTkButton(app, text="Exit to Main Menu", command=return_to_main, font=font_buttons,
                  height=40, width=300, corner_radius=15, fg_color="#ff0f07",
                  hover_color="#6e0602", text_color="white") \
        .grid(row=6, column=1, columnspan=4, pady=10)

    # Add padding and spacing for the entire grid
    for i in range(8):
     app.grid_rowconfigure(i, weight=1)

    app.mainloop()

if __name__ == "__main__":
    calculator_mainloop()
