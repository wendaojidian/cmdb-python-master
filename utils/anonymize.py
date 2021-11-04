import hashlib
import shutil


#: 作用:归档
#: 参数: base_name:目标文件名,format:压缩包后缀,base_dir:开始打包路径
#: 返回值: 返回文件名
def archive(base_name, format, base_dir):
    filename = shutil.make_archive(base_name, format, base_dir)
    return filename


#: 作用: 哈希加密
#: 参数: 加密字符串
#: 返回值: 加密后字符串
def hash(ori):
    p = hashlib.sha256()
    p.update(bytes(ori, encoding='utf-8'))
    res = p.hexdigest()
    return res


# #: 作用:函数化名
# #: 参数:旧函数名,新函数名
# #: 返回值: 命名成功true,失败false
# def pseudon(ori,)


#: 作用: 截断
#: 参数: 数据
#: 返回值: 匿名化数据
def truncate(ori, k):
    return ori[:len(ori) - k] + k * "*"


#: 作用: 化名
#: 参数: 数据
#: 返回值: 匿名化数据
def pseudonym():
    pass
