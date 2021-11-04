from django.shortcuts import *
from cmdb.views.dao import userInfoDao, userGroupDao
from utils.JsonResponse import JsonResponse
import hashlib
from utils.UserSession import checkUserSession
from utils.anonymize import *
from utils.kafka.producer import *
from utils.nats.publisher import *


#: 作用: 添加用户
#: url: userInfo/setFromUserInfo
#: 参数: email, phone, userName, password
def setFromUserInfo(request):
    code, data, message = None, None, None
    try:
        email = request.GET.get('email')
        phone = request.GET.get('phone')
        userName = request.GET.get('userName')
        password = request.GET.get('passWord')
        if email and phone and userName and password:
            if userName == 'admin':
                raise Exception('参数报错: 不能注册管理员账号！')
            userInfo = userInfoDao.getFromUserInfoByLogin(phone)
            if userInfo:
                raise Exception("注册失败,手机号码已存在")
            userInfo = userInfoDao.getFromUserInfoByLogin(email)
            if userInfo:
                raise Exception("注册失败,邮箱已存在")
            # h = hashlib.sha256()
            # h.update(bytes(password, encoding='utf-8'))
            # password = h.hexdigest()
            password = hash(password)
            userGroup = userGroupDao.getAllFromUserGroupByGroupName('员工部')
            userInfoDao.setFromUserInfo(email, phone, userName, password, userGroup.group_id)
            code, message = 200, '账号注册成功'
        else:
            raise Exception('参数报错: 邮箱, 手机号码, 用户名, 密码 都不能为空!')
    except Exception as e:
        code, message = 300, str(e)
    finally:
        kafka_saveLog("getFromUserInfoByLogin", code)
        NATS_publish("getFromUserInfoByLogin")
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户信息-个人用户使用
#: url: userInfo/updInfoFromUserInfo
#: 参数: userName, password
def updInfoFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userId = request.session["userId"]
        userInfo = userInfoDao.getAllFromUsreInfoByUserId(userId=userId)
        userName = request.GET.get('userName')
        phone = request.GET.get('phone')
        email = request.GET.get('email')
        if userName:
            if phone:
                checkUserInfo = userInfoDao.getFromUserInfoByLogin(phone)
                if checkUserInfo and checkUserInfo.user_id != userInfo['user_id']:
                    raise Exception("参数报错: 手机号码已存在")
            if email:
                checkUserInfo = userInfoDao.getFromUserInfoByLogin(phone)
                if checkUserInfo and checkUserInfo.user_id != userInfo['user_id']:
                    raise Exception("参数报错: 邮箱已存在")
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], userName=userName, phone=phone, email=email)
            code, message = 200, '信息更新成功'
        else:
            raise Exception('参数报错: 用户名不能修改为空！')
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updInfoFromUserInfo")
        kafka_saveLog("updInfoFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户密码-个人用户使用
#: url: userInfo/updPassWordFromUserInfo
#: 参数: oldPassWrod, newPassWord
def updPassWordFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        oldPassWrod = request.GET.get('oldPassWrod')
        newPassWord = request.GET.get('newPassWord')
        if oldPassWrod and newPassWord:
            #: 密旧码验证
            oldPassWrod = hash(oldPassWrod)
            dbPassWord = userInfoDao.getPassWordFromUserInfoByUserId(userInfo['user_id'])
            if oldPassWrod != dbPassWord:
                raise Exception('参数报错: 老密码错误，请重新输入谢谢！')
            #: 新密码更新
            newPassWord = hash(newPassWord)
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], password=newPassWord)
            code, message = 200, '密码修改成功'
        else:
            raise Exception("参数报错: 新旧密码不能为空！")
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updPassWordFromUserInfo")
        kafka_saveLog("updPassWordFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户工作-个人用户使用
#: url: userInfo/updJobTitleFromUserInfo
#: 参数: JobTitle
def updJobTitleFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        jobTitle = request.GET.get('jobTitle')
        if jobTitle:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], jobTitle=jobTitle)
            code, message = 200, '工作修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updJobTitleFromUserInfo")
        kafka_saveLog("updJobTitleFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户工资-个人用户使用
#: url: userInfo/updSalaryFromUserInfo
#: 参数: salary
def updSalaryFromUserInfo(request):
    try:
        userInfo = checkUserSession(request)
        salary = request.GET.get('salary')
        if salary:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], salary=salary)
            code, message = 200, '工资修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updSalaryFromUserInfo")
        kafka_saveLog("updSalaryFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户感情状况-个人用户使用
#: url: userInfo/updMaritalStatusFromUserInfo
#: 参数: salary
def updMaritalStatusFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        maritalStatus = request.GET.get('maritalStatus')
        if maritalStatus:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], maritalStatus=maritalStatus)
            code, message = 200, '感情状况修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updMaritalStatusFromUserInfo")
        kafka_saveLog("updMaritalStatusFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户宗教-个人用户使用
#: url: userInfo/updReligionFromUserInfo
#: 参数: religion
def updReligionFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        religion = request.GET.get('religion')
        if religion:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], religion=religion)
            code, message = 200, '宗教修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updReligionFromUserInfo")
        kafka_saveLog("updReligionFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户国家-个人用户使用
#: url: userInfo/updCountryFromUserInfo
#: 参数: Country
def updCountryFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        country = request.GET.get('country')
        if country:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], country=country)
            code, message = 200, '国家修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updCountryFromUserInfo")
        kafka_saveLog("updCountryFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户座机电话-个人用户使用
#: url: userInfo/updHouseNumberFromUserInfo
#: 参数: houseNumber
def updHouseNumberFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        houseNumber = request.GET.get('houseNumber')
        if houseNumber:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], houseNumber=houseNumber)
            code, message = 200, '座机电话修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updHouseNumberFromUserInfo")
        kafka_saveLog("updHouseNumberFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户姓名-个人用户使用
#: url: userInfo/updNameFromUserInfo
#: 参数: name
def updNameFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        name = request.GET.get('name')
        if name:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], name=name)
            code, message = 200, '姓名修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updNameFromUserInfo")
        kafka_saveLog("updNameFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户指纹信息-个人用户使用
#: url: userInfo/updBiometricDataFromUserInfo
#: 参数: biometricData
def updBiometricDataFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        biometricData = request.GET.get('biometricData')
        if biometricData:
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], biometricData=biometricData)
            code, message = 200, '指纹信息修改成功'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updBiometricDataFromUserInfo")
        kafka_saveLog("updBiometricDataFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 登录验证+session
#: url: userInfo/getFromUserInfoByLogin
#: 参数: account, password
def getFromUserInfoByLogin(request):
    code, data, message = None, None, None
    try:
        account = request.GET.get('account')
        password = request.GET.get('password')
        if account and password:
            userInfo = userInfoDao.getFromUserInfoByLogin(account)
            if userInfo:
                if userInfo.state == 2:
                    raise Exception('登录报错: 对不起，您已离职，账号无法再次使用！')
                if userInfo.password == hash(password):
                    request.session['userId'] = userInfo.user_id
                    code, data, message = 200, {'userName': userInfo.user_name}, "登录完成"
                else:
                    raise Exception('密码输入错误')
            else:
                raise Exception("用户不存在")
        else:
            raise Exception('参数报错: 登录名与密码不能为空')
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("getFromUserInfoByLogin")
        kafka_saveLog("getFromUserInfoByLogin", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 注销登录
#: url: userInfo/delFromSessionByKey
#: 参数: None
def delFromSessionByKey(request):
    code, data, message = None, None, None
    try:
        del request.session["userId"]
        code, message = 200, '注销完成'
    except Exception as e:
        code, message = 300, '用户没有登录，无需注销'
    finally:
        NATS_publish("delFromSessionByKey")
        kafka_saveLog("delFromSessionByKey", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 查询指定用户信息-admin用户使用
#: url: userInfo/getAllFromUsreInfoByUserId
#: 参数: userId
def getAllFromUsreInfoByUserId(request):
    code, data, message = None, None, None
    try:
        # checkUserSession(request)
        userId = request.GET.get('userId')
        if userId is None:
            raise Exception('参数报错: userId不能为空！')
        userInfo = userInfoDao.getAllFromUsreInfoByUserId(userId)
        code, data = 200, {'userInfo': userInfo}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("getAllFromUsreInfoByUserId")
        kafka_saveLog("getAllFromUsreInfoByUserId", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 查询全部用户id与用户名
#: url: userInfo/getAllUserInfo
#: 参数: None
def getAllUserInfo(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        groupId = request.GET.get("groupId")
        userInfoList = userInfoDao.getAllUserInfo(groupId=groupId)
        code, data = 200, list(userInfoList)
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("getAllUserInfo")
        kafka_saveLog("getAllUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 用户信息查询分页功能，模糊查询
#: url: userInfo/getAllFromUserInfoByPage
#: 参数: groupId, userName
def getAllFromUserInfoByPage(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        page = request.GET.get('page')
        groupId = request.GET.get('groupId')
        userName = request.GET.get('userName')
        userInfoList, numPages = userInfoDao.getAllFromUserInfoByPage(page=page, groupId=groupId, userName=userName)
        code = 200
        data = {
            'userInfoList': list(userInfoList),
            'numPages': numPages,
            'page': int(page)
        }
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("getAllFromUserInfoByPage")
        kafka_saveLog("getAllFromUserInfoByPage", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 查询个人用户信息
#: url: userInfo/getAllFromUsreInfoByMyself
#: 参数: userId
def getAllFromUsreInfoByMyself(request):
    code, data, message = None, None, None
    try:
        userId = request.session["userId"]
        userInfo = userInfoDao.getAllFromUsreInfoByUserId(userId=userId)
        userInfo = userInfoDao.getAllFromUsreInfoByUserId(userInfo['user_id'])
        code, data = 200, {'userInfo': userInfo}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("getAllFromUsreInfoByMyself")
        kafka_saveLog("getAllFromUsreInfoByMyself", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 重置用户密码-管理员使用
#: url: userInfo/updPassWordFromUserInfoByUserId
#: 参数: userId, password
def updPassWordFromUserInfoByUserId(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        userId = request.GET.get('userId')
        password = request.GET.get('password')
        if userId and password:
            password = hash(password)
            userInfoDao.updAllFromUserInfoByUserId(userId, password=password)
            code, message = 200, '重置密码成功'
        else:
            raise Exception("参数报错: userId与password 都不能为空！")
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updPassWordFromUserInfoByUserId")
        kafka_saveLog("updPassWordFromUserInfoByUserId", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户分组-管理员使用
#: url: userInfo/updGroupFromUserInfoByUserId
#: 参数: userId, password
def updGroupFromUserInfoByUserId(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        userId = request.GET.get('userId')
        groupId = request.GET.get('groupId')
        state = request.GET.get('state')
        if userId:
            userInfoDao.updAllFromUserInfoByUserId(userId, groupId=groupId, state=state)
            code, message = 200, '修改用户信息完成'
        else:
            raise Exception("参数报错: userId 不能为空！")
    except Exception as e:
        code, message = 300, str(e)
    finally:
        NATS_publish("updHouseNumberFromUserInfo")
        kafka_saveLog("updHouseNumberFromUserInfo", code)
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())
