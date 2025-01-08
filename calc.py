import customtkinter as ctk
import tkinter.messagebox as messagebox


def calculator_mainloop():
    """
    Launches the calculator GUI using the customtkinter library.
    """
    # Set appearance mode
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Create the calculator window
    app = ctk.CTk()
    app.title("Calculator")
    app.geometry("800x600")

    # Fonts and colors
    font_buttons = ("Helvetica", 26)
    font_display = ("Helvetica", 24)
    button_blue = "#0747f7"
    button_blue_hover = "#0963ff"

    # Calculator display
    disp = ctk.CTkEntry(app, font=font_display, justify="right", corner_radius=10, height=50, width=400)
    disp.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

    # History storage
    equation_history = []
    scrollable_frame = None  # To store the scrollable frame reference

    def clear_history():
        nonlocal scrollable_frame
        equation_history.clear()
        if scrollable_frame:
            scrollable_frame.destroy()
    # Create a new scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(app, width=300, height=400)
        scrollable_frame.grid(row=2, column=4, rowspan=4, padx=10, sticky="nsew")
        messagebox.showinfo("Equation History", "Equation History has been cleared!")


    clear_history_btn = ctk.CTkButton(app, text="Clear History", font=font_display, command=clear_history, width=150,
                                      height=70)
    clear_history_btn.grid(row=6, column=4, padx=10)
    # Function to refresh history
    def refresh_history():
        """Clears and repopulates the scrollable frame with updated history."""
        nonlocal scrollable_frame

        # Clear the previous scrollable frame if it exists
        if scrollable_frame:
            scrollable_frame.destroy()

        # Create a new scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(app, width=300, height=400)
        scrollable_frame.grid(row=2, column=4, rowspan=4, padx=10, sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=1)
        def set_equation(equation):
            disp.delete(0, ctk.END)
            disp.insert(0, equation)

        # Add each history item as a button
        for i, equation in enumerate(equation_history):
            ctk.CTkButton(
                scrollable_frame,
                text=equation,
                font=("Helvetica", 24),
                anchor="center",
                command=lambda eq=equation: set_equation(eq),  # Pass equation to set_equation
                fg_color="transparent",
            ).grid(row=i, column=0, sticky="we", padx=10, pady=5)

    # Button click handler
    def clk(b):
        if b == '=':
            try:
                result = eval(disp.get())
                disp.insert(ctk.END, f"={result}")
                equation_history.append(disp.get())
                refresh_history()  # Refresh history whenever a new equation is added
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

    # Return to main menu
    def return_to_main():
        app.destroy()
        from main_menu import main_menu_mainloop
        main_menu_mainloop()

    # Initialize empty history
    refresh_history()

    # Calculator buttons
    btns = ['7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C']
    for i, b in enumerate(btns):
        ctk.CTkButton(app, text=b, command=lambda x=b: clk(x), font=font_buttons,
                      height=70, width=90, corner_radius=20, fg_color=button_blue,
                      hover_color=button_blue_hover, text_color="white") \
            .grid(row=i // 4 + 2, column=i % 4, padx=5, pady=5)

    # Exit button
    ctk.CTkButton(app, text="Exit to Main Menu", command=return_to_main, font=font_buttons,
                  height=40, width=220, corner_radius=15, fg_color="#ff0f07",
                  hover_color="#6e0602", text_color="white") \
        .grid(row=6, column=1, columnspan=2, pady=10, padx=5)

    # Grid configuration
    for i in range(8):
        app.grid_rowconfigure(i, weight=1)
    for j in range(5):  # Add a 5th column for expanded history
        app.grid_columnconfigure(j, weight=1)

    app.mainloop()

if __name__ == "__main__":
    calculator_mainloop()
