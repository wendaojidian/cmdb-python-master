import shutil


#: 将信息存储为文件
#: 参数: message,fileName
def saveInfoAsFile(message, fileName):
    with open(fileName, 'w+', encoding='utf-8') as f:
        f.write(message)
    return True


#: 将文件存储在指定位置
#: 参数: file,location
def saveFileToAssignedLocation(ori, des):
    try:
        shutil.move(ori, des)
    except Exception:
        print("保存文件错误")
        return False
    return True
