import tkinter as tk
from tkinter import filedialog
from modules.errors import error_logs

def get_folder():
    try:
        return filedialog.askdirectory()
    except Exception as error:
        error_logs(error,get_folder)
        return None