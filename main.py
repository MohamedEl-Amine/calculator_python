import tkinter as tk

white = "#FFFFFF"
light_gray = '#F5F5F5'
label_color = '#25265E'
small_font = ('Arial', 18)
large_font = ('Arial', 40)
button_font = ('Arial', 24, 'bold')
default_font = ('Arial', 20)
off_white = "#F0FAFF"
light_blue = "#CCEDFF"
Error = False


class Calculator:
    def __init__(self):
        # build the calculator --------------------------------
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.window.iconbitmap('icon.ico')
        self.total_expressions = ""
        self.current_expressions = ""

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.display_label()
        self.digits = {  # for place of button numbers
            7: (1, 1), 8: (2, 1), 9: (3, 1),
            4: (1, 2), 5: (2, 2), 6: (3, 2),
            1: (1, 3), 2: (2, 3), 3: (3, 3),
            0: (2, 4), '.': (1, 4)
        }
        # for adding operation button
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.button_frame = self.create_button_frame()
        self.create_num_buttons()
        self.create_op_button()
        self.create_special_button()
        self.use_keyboard()
        self.button_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)

    def start(self):
        self.window.mainloop()

    # build the frame of calculator
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=light_gray)
        frame.pack(expand=True, fill="both")
        return frame

    def create_button_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    # Adding the labels ---------------
    def display_label(
            self):  # the display label have two label one of total expressions and the second of current expression
        total_label = tk.Label(self.display_frame, text=self.total_expressions, anchor=tk.E, bg=light_gray,
                               fg=label_color, padx=24, font=small_font)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expressions, anchor=tk.E, bg=light_gray,
                         fg=label_color, padx=24, font=large_font)
        label.pack(expand=True, fill='both')
        return total_label, label

    def add_to_exp(self, value):  # when press one of the button the current expression update with add the number
        global Error
        if Error:
            self.current_expressions = ""
            self.total_expressions = ""
            self.update_total_exp()
            Error = False
        self.current_expressions += str(value)
        self.update_label()

    def add_operator(self, operator):
        # when press button of operations the current text move to total expressions with  add the opp
        self.total_expressions += self.current_expressions + str(operator)
        self.current_expressions = ""
        self.update_total_exp()
        self.update_label()

    def update_total_exp(self):  # for update the total expressions

        expression = self.total_expressions
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f"{symbol}")
        self.total_label.config(text=expression)

    def use_keyboard(self):
        self.window.bind("<Return>", lambda event: self.equal_fun())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_exp(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.add_operator(operator))

    def update_label(self):  # for update the current expressions

        self.label.config(text=self.current_expressions[:11])

    def clear_fun(self):  # for function of clear button
        self.current_expressions = ""
        self.total_expressions = ""
        self.update_label()
        self.update_total_exp()

    def square_fun(self):
        self.current_expressions = str(round(eval(f"{self.current_expressions}**2"), 8))
        self.update_label()

    def sqrt_fun(self):
        self.current_expressions = str(round(eval(f"{self.current_expressions}**0.5"), 8))
        self.update_label()

    def equal_fun(self):
        global Error
        self.total_expressions += self.current_expressions
        self.update_total_exp()
        try:
            self.current_expressions = str(round(eval(self.total_expressions), 8))
            self.total_expressions = ""
        except Exception as e:
            self.current_expressions = 'Error'
            Error = True
        finally:
            self.update_label()

    # Adding the buttons
    def create_num_buttons(self):
        for digit, grid_values in self.digits.items():
            button = tk.Button(self.button_frame, text=str(digit), bg=white, fg=label_color, borderwidth=0,
                               font=button_font, command=lambda x=digit: self.add_to_exp(x))
            button.grid(row=grid_values[1], column=grid_values[0], sticky=tk.NSEW)

    def create_op_button(self):
        i = 0
        for operation, symbol in self.operations.items():
            button = tk.Button(self.button_frame, text=symbol, bg=off_white, fg=label_color, font=default_font,
                               borderwidth=0, command=lambda x=operation: self.add_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_special_button(self):
        clear = tk.Button(self.button_frame, text="C", bg=off_white, fg=label_color, font=default_font,
                          borderwidth=0, command=self.clear_fun)
        clear.grid(row=0, column=1, sticky=tk.NSEW)

        button_equal = tk.Button(self.button_frame, text="=", bg=light_blue, fg=label_color, font=default_font,
                                 borderwidth=0, command=self.equal_fun)
        button_equal.grid(row=4, column=3, columnspan=3, sticky=tk.NSEW)

        button_sqrt = tk.Button(self.button_frame, text="\u221ax", bg=off_white, fg=label_color, font=default_font,
                                borderwidth=0, command=self.sqrt_fun)
        button_sqrt.grid(row=0, column=2, sticky=tk.NSEW)

        button_square = tk.Button(self.button_frame, text="x\u00B2", bg=off_white, fg=label_color, font=default_font,
                                  borderwidth=0, command=self.square_fun)
        button_square.grid(row=0, column=3, sticky=tk.NSEW)


# must add the equal actif and the error actif to fix the last problem in this calculator
if __name__ == "__main__":
    cal = Calculator()
    cal.start()
