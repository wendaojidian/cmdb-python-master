import os
import uuid
from django.http import HttpResponse
from utils.JsonResponse import JsonResponse


#: 作用: 获取主机cookies
#: url: deviceInfo/getCookies
def getCookies(request):
    code, data, message = None, None, None
    try:
        cookie = request.COOKIES
        code, data = 200, {'cookie': cookie}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 获取主机IP
#: url: deviceInfo/getIP
def getIp(request):
    code, data, message = None, None, None
    try:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ipaddress = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ipaddress = request.META['REMOTE_ADDR']
        code, data = 200, {'ipaddress': ipaddress}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用:获取主机mac
# url: deviceInfo/getMacAddress
def getMacAddress(request):
    code, data, message = None, None, None
    try:
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ipaddress = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ipaddress = request.META['REMOTE_ADDR']
        s = 'ping ' + "223.104.29.69"
        os.system(s)
        mac = None
        for line in os.popen("arp -a"):
            print(line)
            if line.lstrip().startswith("223.104.29.69"):
                s1 = line.split()
                mac = s1[1].replace('-', ':')
        code, data = 200, {'macAddress': mac}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())
