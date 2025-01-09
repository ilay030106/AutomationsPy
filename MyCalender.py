import customtkinter as ctk
import calendar
from datetime import datetime
import locale

class Calendar(ctk.CTkFrame):
    def __init__(self, master=None, command=None, year=None, month=None, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_date = None
        self.selected_button = None
        self.command = command
        self.current_year = year if year else datetime.now().year
        self.current_month = month if month else datetime.now().month

        locale.setlocale(locale.LC_TIME, '')

        self.months = [calendar.month_name[i] for i in range(1, 13)]
        self.weekdays = [calendar.day_name[i] for i in range(7)]

        # Header with navigation buttons
        self.frame_months_year = ctk.CTkFrame(self)
        self.frame_months_year.pack(pady=5)

        self.button_prev_year = ctk.CTkButton(self.frame_months_year, text='<<', width=20, height=20, command=self.prev_year)
        self.button_prev_year.grid(row=0, column=0, padx=5, pady=5)

        self.button_prev_month = ctk.CTkButton(self.frame_months_year, text='<', width=20, height=20, command=self.prev_month)
        self.button_prev_month.grid(row=0, column=1, padx=5, pady=5)

        self.label_month = ctk.CTkLabel(self.frame_months_year, text=self.months[self.current_month - 1], font=('roboto', 12, 'bold'))
        self.label_month.grid(row=0, column=2, padx=5, pady=5)

        self.button_next_month = ctk.CTkButton(self.frame_months_year, text='>', width=20, height=20, command=self.next_month)
        self.button_next_month.grid(row=0, column=3, padx=5, pady=5)

        self.label_year = ctk.CTkLabel(self.frame_months_year, text=str(self.current_year), font=('roboto', 12, 'bold'))
        self.label_year.grid(row=0, column=4, padx=5, pady=5)

        self.button_next_year = ctk.CTkButton(self.frame_months_year, text='>>', width=20, height=20, command=self.next_year)
        self.button_next_year.grid(row=0, column=5, padx=5, pady=5)

        # Frame for days
        self.frame_days = ctk.CTkFrame(self)
        self.frame_days.pack(pady=5)

        self.update_days(self.current_month, self.current_year)

    def update_days(self, month, year):
        # Clear current widgets in frame_days
        for widget in self.frame_days.winfo_children():
            widget.destroy()

        # Set Sunday as the first day of the week
        calendar.setfirstweekday(calendar.SUNDAY)

        # Get days of the month and the first weekday
        num_days = calendar.monthrange(year, month)[1]
        first_day = calendar.monthrange(year, month)[0]

        # Draw weekday labels
        for idx, day in enumerate(self.weekdays):
            label = ctk.CTkLabel(self.frame_days, text=day[:3], font=('roboto', 10, 'bold'))
            label.grid(row=0, column=idx, padx=2, pady=2)

        # Draw empty spaces before the first day
        day = 1
        row = 1
        for i in range(first_day):
            label = ctk.CTkLabel(self.frame_days, text=" ")
            label.grid(row=row, column=i)

        for col in range(first_day, 7):
            self.create_day_button(day, row, col, month, year)
            day += 1

        row += 1
        while day <= num_days:
            for col in range(7):
                if day > num_days:
                    break
                self.create_day_button(day, row, col, month, year)
                day += 1
            row += 1

    def create_day_button(self, day, row, col, month, year):
        def on_click():
            self.selected_date = f"{day:02d}/{month:02d}/{year}"

            # Reset the color of the previously selected button



            # Highlight the selected button
            button.configure(fg_color="#0963ff")  # Darker color
            self.selected_button = button

            if self.command:
                self.command(self.selected_date)

        button = ctk.CTkButton(self.frame_days, text=str(day), width=30, height=30, command=on_click,fg_color="#0747f7")
        button.grid(row=row, column=col, padx=2, pady=2)

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_month_year()

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_month_year()

    def next_year(self):
        self.current_year += 1
        self.update_month_year()

    def prev_year(self):
        self.current_year -= 1
        self.update_month_year()

    def update_month_year(self):
        self.label_month.configure(text=self.months[self.current_month - 1])
        self.label_year.configure(text=str(self.current_year))
        self.update_days(self.current_month, self.current_year)

    def getDate(self):
        return self.selected_date

    def resetButton(self):
        if self.selected_button :
            self.selected_button.configure(fg_color="#0747f7", hover_color="#0963ff")

        self.selected_button = None
