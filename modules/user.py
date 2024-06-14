import datetime
import random 
import string
from csv  import writer
from modules.errors import error_logs ### this is the file from the error.py in modules for logging errors

class users_module():

    session_ids = set()  ### this set store all the session 
    logged_users = {}

    def id_generator(num:int=15):
        res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
        while res in users_module.session_ids:
            res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
        return res


    class user:
        def __init__(self,username,ipaddress) -> None:
            self.username = username 
            self.ipaddress = ipaddress
            self.session_id = users_module.id_generator(num=32)
            self.time_of_login = datetime.datetime.now()
            if username in users_module.logged_users.keys():
                users_module.session_ids.remove(users_module.logged_users[username].session_id)
                users_module.user.logging(users_module.logged_users[username],"logout")
                del users_module.logged_users[username]
            users_module.session_ids.add(self.session_id)
            users_module.logged_users[username] = self
            if users_module.user.logging(self,"login") is False:
                del self
            
        def logging(self,type):
            try:
                with open("./logs/user_logs.csv","a") as file:
                    log_writer = writer(file)
                    if type=="login":
                        log_writer.writerow([self.username,self.ipaddress,self.session_id,self.time_of_login,"login"])
                    elif type=="logout":
                        log_writer.writerow([self.username,self.ipaddress,self.session_id,self.time_of_login,"logout",datetime.datetime.now()])
                return True
            except Exception as error: 
                error_logs(error,users_module.user.logging)
                return False
            
        def logout(self):
            try:
                users_module.session_ids.remove(self.session_id)
                del users_module.logged_users[self.username]
                users_module.user.logging(self,"logout")
                del self
                return True
            except Exception as error:
                 error_logs(error,users_module.user.logout)
                 return False