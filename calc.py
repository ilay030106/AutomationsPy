import customtkinter as ctk
import tkinter.messagebox as messagebox
import sqlite3
import math

class CalculatorApp:
    def __init__(self):
        self.conn = sqlite3.connect("calculator_history.db")
        self.cursor = self.conn.cursor()
        self.initialize_database()
        self.equation_history = self.load_history_from_db()
        self.scrollable_frame = None
        self.memory = None
        self.history_visible = False
        self.create_ui()

    def initialize_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equation TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_equation_to_db(self, equation):
        self.cursor.execute("INSERT INTO history (equation) VALUES (?)", (equation,))
        self.conn.commit()

    def clear_database(self):
        self.cursor.execute("DELETE FROM history")
        self.conn.commit()

    def load_history_from_db(self):
        self.cursor.execute("SELECT equation FROM history")
        equations = self.cursor.fetchall()
        return [eq[0] for eq in equations]

    def create_ui(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Calculator")
        self.app.geometry("800x600")

        font_buttons = ("Helvetica", 26)
        font_display = ("Helvetica", 24)
        button_blue = "#0747f7"
        button_blue_hover = "#0963ff"

        self.disp = ctk.CTkEntry(self.app, font=font_display, justify="right", corner_radius=10, height=50, width=400)
        self.disp.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        self.clear_history_btn = ctk.CTkButton(self.app, text="Clear History", font=font_display, command=self.clear_history, width=150, height=70)
        self.clear_history_btn.grid(row=7, column=4, padx=10)

        self.toggle_history_btn = ctk.CTkButton(self.app, text="Toggle History", font=font_display, command=self.toggle_history, width=150, height=70)
        self.toggle_history_btn.grid(row=7, column=3, padx=10)

        self.refresh_history()

        btns = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '=', '+', 'C', '√', '%', 'M+', 'MR', 'MC']
        for i, b in enumerate(btns):
            ctk.CTkButton(self.app, text=b, command=lambda x=b: self.clk(x), font=font_buttons, height=70, width=90, corner_radius=20, fg_color=button_blue, hover_color=button_blue_hover, text_color="white").grid(row=i // 4 + 2, column=i % 4, padx=5, pady=5)

        ctk.CTkButton(self.app, text="Exit to Main Menu", command=self.return_to_main, font=font_buttons, height=40, width=220, corner_radius=15, fg_color="#ff0f07", hover_color="#6e0602", text_color="white").grid(row=8, column=1, columnspan=2, pady=10, padx=5)

        for i in range(9):
            self.app.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.app.grid_columnconfigure(j, weight=1)

        self.app.mainloop()

    def clear_history(self):
        self.clear_database()
        self.equation_history.clear()
        if self.scrollable_frame:
            self.scrollable_frame.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self.app, width=300, height=400)
        self.scrollable_frame.grid(row=2, column=4, rowspan=4, padx=10, sticky="nsew")
        messagebox.showinfo("Equation History", "Equation History has been cleared!")

    def refresh_history(self):
        if self.scrollable_frame:
            self.scrollable_frame.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self.app, width=300, height=400)
        self.scrollable_frame.grid(row=2, column=4, rowspan=4, padx=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        for i, equation in enumerate(self.equation_history):
            ctk.CTkButton(self.scrollable_frame, text=equation, font=("Helvetica", 24), anchor="center", command=lambda eq=equation: self.set_equation(eq), fg_color="transparent").grid(row=i, column=0, sticky="we", padx=10, pady=5)

    def set_equation(self, equation):
        self.disp.delete(0, ctk.END)
        self.disp.insert(0, equation.split("=")[1])

    def clk(self, b):
        if b == '=':
            try:
                eq = self.disp.get()
                result = eval(self.disp.get())
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, str(result))
                full_equation = f"{eq} = {result}"
                self.equation_history.append(full_equation)
                self.add_equation_to_db(full_equation)
                self.refresh_history()
            except Exception:
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, "Error")
        elif b == 'C':
            self.disp.delete(0, ctk.END)
        elif b == '√':
            try:
                result = math.sqrt(float(self.disp.get()))
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, str(result))
            except Exception:
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, "Error")
        elif b == '%':
            try:
                result = float(self.disp.get()) / 100
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, str(result))
            except Exception:
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, "Error")
        elif b == 'M+':
            try:
                self.memory = float(self.disp.get())
            except Exception:
                self.memory = None
        elif b == 'MR':
            if self.memory is not None:
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, str(self.memory))
        elif b == 'MC':
            self.memory = None
        else:
            if '=' in self.disp.get():
                if b in '-+/*':
                    result = self.disp.get().split('=')[0].strip()
                    self.disp.delete(0, ctk.END)
                    self.disp.insert(0, result + b)
                else:
                    self.disp.delete(0, ctk.END)
                    self.disp.insert(0, b)
            elif "Error" in self.disp.get():
                self.disp.delete(0, ctk.END)
                self.disp.insert(0, b)
            else:
                self.disp.insert(ctk.END, b)

    def toggle_history(self):
        if self.history_visible:
            if self.scrollable_frame:
                self.scrollable_frame.grid_remove()
            self.clear_history_btn.grid_remove()
            self.app.geometry("600x600")
        else:
            if self.scrollable_frame:
                self.scrollable_frame.grid()
            else:
                self.refresh_history()
            self.clear_history_btn.grid()
            self.app.geometry("800x600")
        self.history_visible = not self.history_visible

    def return_to_main(self):
        self.conn.close()
        self.app.destroy()
        from main_menu import main_menu_mainloop
        main_menu_mainloop()

if __name__ == "__main__":
    CalculatorApp()