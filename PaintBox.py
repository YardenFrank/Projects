__author__ = 'Amit, Yahav, Yarden and Harel'

import tkinter as tk
from PictureCoordinates import *

ROW_NUMBER, COLUMN_NUMBER = 23, 36
COLOR_NAMES = ['red', 'blue', 'green', 'yellow', 'pink', 'gray', 'black', 'white', '#F0F0F0', 'orange']


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # frames
        self.frame_colors = tk.Frame(self)
        self.frame_colors.pack()

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.pack()

        self.frame_pictures = tk.Frame(self)
        self.frame_pictures.pack()

        self.button_list = []

        # current color
        self.color = 'red'

        # current picture
        self.picture = FIRST_PICTURE

        # set up the app
        self.set_up()

    def set_up(self):
        """this function sets up all the needed components of the app."""
        self.title('PaintBox')
        self.resizable(False, False)
        self.center_window()

        self.background_widgets()
        self.arrange_grid()
        self.picture_buttons()

    def center_window(self, width=1000, height=750):
        """sets the window in the middle of the screen"""

        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2) - 30
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def background_widgets(self):
        """creates the colors the user can choose from (top of the screen) + the 'erase' and 'solve' buttons"""
        for i in range(len(COLOR_NAMES)):
            numbers_label = tk.Label(self.frame_colors, text=i+1, font=("Helvetica", 10), width=3, height=2)
            numbers_label.pack(side='left', pady=20)

            color_label = tk.Label(self.frame_colors, name=COLOR_NAMES[i], bg=COLOR_NAMES[i], width=4, height=2)
            color_label.pack(side='left', pady=20)
            color_label.bind("<Button-1>", self.change_current_color)

        erase_button = tk.Button(self.frame_colors, text='erase all', width=6, height=2, command=lambda: self.erase())
        erase_button.pack(side='right', padx=10, pady=30)

        solve_button = tk.Button(self.frame_colors, text='solve', width=6, height=2, command=lambda: self.solve())
        solve_button.pack(side='right', padx=10, pady=30)

    def picture_buttons(self):
        picture1_button = tk.Button(self.frame_pictures, text='picture 1', width=6, height=2,
                                    command=lambda: self.change_picture(1))
        picture1_button.pack(side='right', padx=10, pady=30)

        picture2_button = tk.Button(self.frame_pictures, text='picture 2', width=6, height=2,
                                    command=lambda: self.change_picture(2))
        picture2_button.pack(side='right', padx=10, pady=30)

        picture3_button = tk.Button(self.frame_pictures, text='picture3', width=6, height=2,
                                    command=lambda: self.change_picture(3))
        picture3_button.pack(side='right', padx=10, pady=30)

    def change_picture(self, number):
        if number == 1:
            self.picture = FIRST_PICTURE
        elif number == 2:
            self.picture = SECOND_PICTURE
        else:
            self.picture = THIRD_PICTURE

        self.erase()

    def change_current_color(self, event):
        """changes the current color to the one the user chose"""
        self.color = event.widget._name

    def erase(self):
        """erases the whole grid and creates a new one"""
        for button in self.button_list:
            button.destroy()

        self.button_list = []
        self.arrange_grid()

    def arrange_grid(self):
        """creates a grid of buttons that when pressed - are changed to the current color"""

        for row in range(ROW_NUMBER):
            for column in range(COLUMN_NUMBER):
                button = tk.Button(self.frame_buttons, width=2, height=1)
                button['command'] = lambda b=button: self.pressed(b)

                for color in self.picture:
                    if color:
                        for element in color:
                            if element[0] == row and element[1] == column:
                                button = tk.Button(self.frame_buttons, width=2, height=1)
                                button['command'] = lambda b=button: self.pressed(b)
                                button['text'] = str(self.picture.index(color) + 1)
                                button.grid(row=row + 1, column=column + 1)
                                self.button_list.append(button)

    def pressed(self, button):
        if COLOR_NAMES[int(button['text']) - 1] == self.color:
            return button.config(bg=self.color)
        return button

    def solve(self):
        for button in self.button_list:
            button['bg'] = COLOR_NAMES[int(button['text']) - 1]


if __name__ == "__main__":
    app = App()
    app.mainloop()
