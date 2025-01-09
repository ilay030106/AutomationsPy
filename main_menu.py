import customtkinter as ctk
import tkinter.messagebox as messagebox
import pytube
def main_menu_mainloop():
    """
    Launches the main menu window using the customtkinter library.

    This function creates a GUI window with options to navigate to different automation systems,
    such as a calculator, or placeholder options for future automations. The user can also exit
    the application from this menu.
    """
    # Set appearance mode: Choose between "Dark", "Light", or "System" (system default)
    ctk.set_appearance_mode("Dark")

    # Set a custom button color theme using hex color codes
    button_blue = "#0747f7"  # Default button color
    button_blue_hover = "#0963ff"  # Hover color for buttons

    # Set color theme: Options include "blue", "green", "dark-blue", or custom themes
    ctk.set_default_color_theme("blue")

    # Create the main menu window
    main_menu = ctk.CTk()  # CTk is the main window class in customtkinter
    main_menu.title("Automation Main Menu")  # Set the window title
    main_menu.geometry("400x300")  # Set the size of the window in pixels (width x height)

    # Define custom fonts for labels and buttons
    font_title = ("Helvetica", 24, "bold")  # Font for the title text
    font_buttons = ("Helvetica", 18)  # Font for the buttons

    # Configure the grid layout for the main menu
    main_menu.columnconfigure(0, weight=1)
    main_menu.rowconfigure(0, weight=1)

    # Create a title label at the top of the window
    ctk.CTkLabel(
        main_menu, text="Choose an Automation", font=font_title
    ).grid(row=0, column=0, pady=(20, 10), sticky="n")

    # Function to open the calculator GUI
    def open_calculator():
        """
        Closes the main menu and opens the calculator GUI.

        This function imports the calculator GUI dynamically to avoid circular imports and
        starts its main event loop.
        """
        main_menu.destroy()
        from calc import calculator_mainloop  # Import the calculator module
        calculator_mainloop()  # Start the calculator GUI

    # Function to handle placeholder automation
    def placeholder_automation():
        """
        Displays a popup message indicating that the feature is under construction.

        Uses tkinter.messagebox to show an informational message to the user.
        """
        messagebox.showinfo("Automation", "This automation is under construction!")

    # Create a frame for better layout
    frame = ctk.CTkFrame(main_menu)
    frame.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
    frame.columnconfigure(0, weight=1)

    # Button to open the calculator GUI
    ctk.CTkButton(
        frame,
        text="Open Calculator",  # Button text
        font=font_buttons,
        command=open_calculator,  # Action to perform when clicked
        height=40,  # Button height in pixels
        width=200,  # Button width in pixels
        fg_color=button_blue,  # Button default color
        hover_color=button_blue_hover  # Hover color for the button
    ).grid(row=0, column=0, pady=(20, 10), padx=10)

    # Button for a placeholder automation
    ctk.CTkButton(
        frame,
        text="Placeholder Automation",  # Button text
        font=font_buttons,
        command=placeholder_automation,  # Action to perform when clicked
        height=40,
        width=200,
        state=ctk.DISABLED,  # Properly disable the button
        fg_color=button_blue,  # Button default color
        hover_color=button_blue_hover,  # Hover color for the button
    ).grid(row=1, column=0, pady=10, padx=10)

    # Button to exit the main menu
    ctk.CTkButton(
        frame,
        text="Exit",  # Button text
        font=font_buttons,
        command=main_menu.destroy,  # Close the main menu window
        height=40,
        width=200,
        fg_color="red",  # Background color of the button
        hover_color="darkred"  # Hover color for the button
    ).grid(row=2, column=0, pady=(10, 20), padx=10)

    # Start the main event loop for the main menu
    main_menu.mainloop()

if __name__ == "__main__":
    main_menu_mainloop()
