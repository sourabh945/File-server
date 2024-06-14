import os

def ls(path:str) -> list[tuple[str,str,int]]:
    result = []
    content = os.listdir(path)
    for i in content:
        size = os.path.getsize(i)
        size = size/1024
        if os.path.isdir(i) is True:
            result.append((i,"dir",size))
        else:
            result.append((i,"file",size))
    return result