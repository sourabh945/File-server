import os

from modules.errors import error_logs


def ls(path:str) -> list[tuple[str,str,int]]:
    try:
        result = []
        content = os.listdir(path)
        for i in content:
            size = (os.path.getsize(path+"/"+i))/1024
            if size == 0:
                size_ = "0 B"
            elif size < 200 and size > 0:
                size_ = f'{round(size,3)} KB'
            elif size >= 200 and size < 800*1024:
                size = size/1024
                size_ = f'{round(size),1} MB'
            else:
                size = size/(1024*1024)
                size_ = f'{round(size,3)} GB'
            if os.path.isdir(path+"/"+i) is True:
                result.append((i,"dir",size_))
            else:
                result.append((i,"file",size_))
        return result
    except Exception as error:
        error_logs(error,ls)
        return []