import customtkinter as ctk

def main_menu_mainloop():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    main_menu = ctk.CTk()
    main_menu.title("Automation Main Menu")
    main_menu.geometry("400x300")

    font_title = ("Helvetica", 24, "bold")
    font_buttons = ("Helvetica", 18)
    button_blue = "#0747f7"
    button_blue_hover = "#0963ff"

    main_menu.columnconfigure(0, weight=1)
    main_menu.rowconfigure(0, weight=1)

    ctk.CTkLabel(main_menu, text="Choose an Automation", font=font_title).grid(row=0, column=0, pady=(20, 10), sticky="n")

    def open_calculator():
        main_menu.destroy()
        from calc import calculator_mainloop
        calculator_mainloop()

    def open_to_do_list():
        main_menu.destroy()
        from To_do_list import list_mainloop
        list_mainloop()

    frame = ctk.CTkFrame(main_menu)
    frame.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
    frame.columnconfigure(0, weight=1)

    ctk.CTkButton(frame, text="Open Calculator", font=font_buttons, command=open_calculator, height=40, width=200, fg_color=button_blue, hover_color=button_blue_hover).grid(row=0, column=0, pady=(20, 10), padx=10)
    ctk.CTkButton(frame, text="To Do List", font=font_buttons, command=open_to_do_list, height=40, width=200, fg_color=button_blue, hover_color=button_blue_hover).grid(row=1, column=0, pady=10, padx=10)
    ctk.CTkButton(frame, text="Exit", font=font_buttons, command=main_menu.destroy, height=40, width=200, fg_color="red", hover_color="darkred").grid(row=2, column=0, pady=(10, 20), padx=10)

    main_menu.mainloop()

if __name__ == "__main__":
    main_menu_mainloop()