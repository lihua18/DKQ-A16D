#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes, sys, re
from ctypes import * #因为使用的是C/C++的库，所以我们引用ctypes

dll = ctypes.windll.LoadLibrary("SynIDCardAPI.dll") #载入库

iPort = dll.Syn_FindUSBReader() #寻找USB，返回的貌似是什么端口


pucIIN = ctypes.create_string_buffer(128)
dll.Syn_StartFindIDCard(iPort, pucIIN, 1) #开始找卡

pucSN = ctypes.create_string_buffer(128)
dll.Syn_SelectIDCard(iPort, pucSN, 1) #选择卡

dll.Syn_SetBornType(2)
dll.Syn_SetUserLifeBType(2)
dll.Syn_SetUserLifeEType(2,0)
dll.Syn_SetSexType(1)
dll.Syn_SetNationType(2)
dll.Syn_SetPhotoName(2)
cPhotopath = c_char_p(("E:\\Python34\\5").encode('gbk'))
dll.Syn_SetPhotoPath(2, cPhotopath) #这一步很重要，他们默认是0.把身份证头像存在了C盘根目录，1.参数可以换到当前目录即可，2.是指定路径


#下面调用他们的最终读取函数Syn_ReadMsg，第三个参数是一个结构体，Python本身没有C/C++那样的结构体，但是可以通过ctypes的Structure来解决
class IDCardData(Structure):
    _fields_ = [
		('Name', c_char * 32), #姓名
		('Sex', c_char * 6), #性别
		('Nation', c_char * 20), #民族
		('Born', c_char * 18), #出生日期
		('Address', c_char * 72), #住址
		('IDCardNo', c_char * 38), #身份证号
		('GrantDept', c_char * 32), #发证机关
		('UserLifeBegin', c_char * 18), #有效开始日期
		('UserLifeEnd', c_char * 18), #有效截止日期
		('reserved', c_char * 38), #保留
		('PhotoFileName', c_char * 255) #照片路径
	]
data = IDCardData()
r = dll.Syn_ReadMsg(iPort, 1, byref(data))
if r == 0:
	print(getattr(data, 'Name').decode('gbk'))
	print(getattr(data, 'Sex').decode('gbk'))
	print(getattr(data, 'Nation').decode('gbk'))
	print(getattr(data, 'Born').decode('gbk'))
	print(getattr(data, 'Address').decode('gbk'))
	print(getattr(data, 'IDCardNo').decode('gbk'))
	print(getattr(data, 'GrantDept').decode('gbk'))
	print(getattr(data, 'UserLifeBegin').decode('gbk'))
	print(getattr(data, 'UserLifeEnd').decode('gbk'))
	print(getattr(data, 'reserved').decode('gbk'))
	print(getattr(data, 'PhotoFileName').decode('gbk'))
else:
	print("None")

#################################################################
#   上面的源码来源于：https://my.oschina.net/ruiorz/blog/776084        非常感谢它的作者：ruiorz
#   建议使用者使用Python3.4或者是32位的Python，因为  SynIDCardAPI.dll 就是32位的。
################################################################################################