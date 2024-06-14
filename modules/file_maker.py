import os 
import json
from modules.errors import error_logs

### this module is use to generate the all the necessary file we need to run the service

### log_file_make : Create the logs file for store the user login timing and error logs 

def log_file_make():
    try:
        if "logs" not in os.listdir("./"):
            os.mkdir("./logs")
            with open("./logs/user_logs.csv","w") as file:
                file.close()
            with open("./logs/error_logs.csv","w") as file:
                file.close()
        else:
            if "user_logs.csv" not in os.listdir("./logs"):
                with open("./logs/user_logs.csv","w") as file:
                    file.close()
            if "error_logs.csv" not in os.listdir("./logs"):
                with open("./logs/error_logs.csv","w") as file:
                    file.close()
    except Exception as error:
        error_logs(error,log_file_make)

### user login json maker : It make the file that store the user login passwords in json

def user_login_json_maker(users_login_credential:list[dict[str:str]]):
    try:
        if "database" not in os.listdir("./"):
            os.mkdir("./database")
            with open("./database/login.json","w") as file :
                json.dump(users_login_credential,file)
                return True
        else:
            if "login.json" not in os.listdir("./database"):
                with open("./database/login.json","w") as file:
                    json.dump(users_login_credential,file) 
                    return True
    except Exception as error:
        error_logs(error,user_login_json_maker)
        return False

### add users : is use to add user in the user login credential file 

def add_users(user_login_credential:dict[str:str]) -> bool:
    try:
        with open("./database/login.json","r") as file:
            existing_users_credentials = json.load(file)
        with open("./database/login.json","w") as file:
            json.dump(existing_users_credentials+user_login_credential,file)
            return True
    except Exception as error:
        error_logs(error,add_users)
        return False

### remove user : is for remove the user with its username file 
### first bool is for user is not in list and second is for operation of delete is successful or not

def remove_user(user_username:str) -> list[bool]:
    try:
        with open("./database/login.json","r") as file:
            existing_users_credentials = json.load(file)
        if user_username in existing_users_credentials.keys():
            del existing_users_credentials[user_username]
            with open("./database/login.json","w") as file:
                json.dump(existing_users_credentials,file)
            return [True,True]
        else:
            return [True,False]
    except Exception as error:
        error_logs(error,remove_user)
        return [False,False]
    
### for admin password you have to make it manually 
