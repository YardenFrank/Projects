import tkinter as tk
from tkinter import filedialog
from os.path import basename


class ClientFilesGUI(tk.Tk):
    def __init__(self):
        super(ClientFilesGUI, self).__init__()

        self.file_name = None
        self.file_downloaded = None
        self.to_download = False
        self.gui_command = 'a'  # a = upload, b = download
        self.directory = r'C:\Client_Files'

        self.command_frame = tk.Frame(self)
        self.command_frame.pack(side='bottom', pady=15)

        self.message_label = tk.Label(self)
        self.message_label.pack(side='top')
        self.message_label.config(text='current directory: ' + self.directory)

        self.files_frame = tk.Frame(self)
        self.files_frame.pack(pady=30)

        self.row = 0
        self.column = 0

        # set up the app
        self.set_up()
        self.mainloop()

    def set_up(self):
        """this function sets up all the needed components of the app."""
        self.resizable(False, False)
        self.center_window()

        upload = tk.Button(self.command_frame, text='upload', width=12, height=2, padx=5,
                           command=self.upload_from_computer)
        upload.grid(row=0, column=0)

        download_button = tk.Button(self.command_frame, text='download', width=12, height=2, padx=5,
                                    command=self.download_file)
        download_button.grid(row=0, column=1, padx=30)

        change_directory_button = tk.Button(self.command_frame, text='change directory', width=15, height=2, padx=5,
                                            command=self.change_directory)
        change_directory_button.grid(row=0, column=2)

    def center_window(self, width=700, height=450):
        """sets the window in the middle of the screen"""

        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2) - 30
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def upload_from_computer(self):
        self.gui_command = 'a'
        self.file_name = filedialog.askopenfilename(initialdir="/", title="Select file")
        self.create_file_button()

    def download_file(self):
        self.gui_command = 'b'
        self.to_download = True

    def change_directory(self):
        self.message_label.config(text='Enter the directory you want your files to be in')
        self.directory = filedialog.askdirectory(initialdir="/", title="Select directory")
        self.message_label.config(text='current directory: ' + self.directory)

    def create_file_button(self):
        name = self.file_name
        file_button = tk.Button(self.files_frame, text=basename(name), width=8, padx=15)
        file_button['command'] = lambda b=file_button: self.change_file_name(name)
        file_button.grid(row=self.row, column=self.column)
        self.column += 1
        if self.column == 6:
            self.column = 0
            self.row += 1

    def change_file_name(self, text):
        self.file_downloaded = text
