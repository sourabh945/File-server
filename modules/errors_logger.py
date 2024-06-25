from csv import writer
import os

### error file maker : is the function that create log file for errors is there are not present.

def error_file_maker():
    try:
        if "logs" not in os.listdir("./"):
            os.mkdir("logs")
            with open("./logs/error_logs.csv","w") as file:
                file.close()
        elif "error_logs.csv" not in os.listdir("./logs/"):
            with open("./logs/error_logs.csv","w") as file:
                file.close()
        else: 
            return None
        return None
    except:
        print("Unable to make required folder and files ")
        raise Exception
    
### func path : is return the path of the function file use to write error messages
    
def func_path(func):
    if type(func) == "function":
        return f"{func.__code___.co_filename}/{func}"
    else:
        return f"{func}"
    
### error logs : this is the main function for log the errors and also print in the terminal output



def error_logs(error:Exception,instance):
    error_file_maker()
    with open("./logs/error_logs.csv","a") as file:
        error_writer = writer(file)
        error_writer.writerow([error,error.__traceback__,error.__cause__,error.__context__,func_path(instance)])
    print("/n >>>>>>>>>>>>>>>>>> ERROR >>>>>>>>>>>>>>>")
    print(error)
    print(error.__cause__)
    print(error.__traceback__)
    print(error.__context__)
    print(f"Instance:{func_path(instance)}") 
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
