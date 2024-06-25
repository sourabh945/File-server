import os
from modules.user import users_module
from csv import writer
from modules.errors_logger import error_logs
from datetime import datetime as dt

def download_logs(user:users_module.user,filename:str) -> bool:
    try:
        with open("./logs/download_logs.csv") as file:
            log_writer = writer(file)
            log_writer.writerow([user.username,user.ipaddress,user.session_id,dt.now(),filename])
        return True
    except Exception as error:
        error_logs(error,download_logs)
        return False