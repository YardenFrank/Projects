import tkinter as tk


class ClientGUI(tk.Tk):
    def __init__(self):
        super(ClientGUI, self).__init__()

        self.text = ''
        self.text_widget = tk.Text(self)
        self.text_widget.pack()

        self.message = None
        self.gui_command = 1

        self.send_frame = tk.Frame(self)
        self.send_frame.pack(side='bottom', pady=15)
        self.entry = tk.Entry(self.send_frame, font='ariel 24')

        self.command_frame = tk.Frame(self)
        self.command_frame.pack(side='right', padx=15)

        # set up the app
        self.set_up()
        self.mainloop()

    def set_up(self):
        """this function sets up all the needed components of the app."""
        self.resizable(False, False)
        self.center_window()

        self.entry = tk.Entry(self.send_frame, font='ariel 24')
        self.entry.grid(row=0, column=0)

        send_button = tk.Button(self.send_frame, text='send', width=12, height=2, command=self.set_message)
        send_button.grid(row=0, column=1, padx=5)

        command1 = tk.Button(self.command_frame, text='chat', width=12, height=2, padx=5, command=lambda: self.set_command(1))
        command1.grid(row=0, column=0, pady=3)

        command2 = tk.Button(self.command_frame, text='make manager', width=12, height=2, padx=5, command=lambda: self.set_command(2))
        command2.grid(row=1, column=0, pady=3)

        command3 = tk.Button(self.command_frame, text='kick', width=12, height=2, padx=5, command=lambda: self.set_command(3))
        command3.grid(row=2, column=0, pady=3)

        command4 = tk.Button(self.command_frame, text='mute', width=12, height=2, padx=5, command=lambda: self.set_command(4))
        command4.grid(row=3, column=0, pady=3)

        command5 = tk.Button(self.command_frame, text='private message', width=12, height=2, padx=5, command=lambda: self.set_command(5))
        command5.grid(row=4, column=0, pady=3)

    def center_window(self, width=1000, height=750):
        """sets the window in the middle of the screen"""

        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2) - 30
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def set_message(self):
        self.message = self.entry.get()
        self.entry.delete(0, 'end')

    def set_command(self, command):
        self.gui_command = command
