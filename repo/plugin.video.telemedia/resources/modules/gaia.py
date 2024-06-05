# -*- coding: utf-8 -*-
import xbmc,time,os,re,xbmcgui,xbmcaddon,xbmcvfs,sys
Addon = xbmcaddon.Addon()
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION<=18:
    translatepath=xbmc.translatePath

else:#קודי19
    translatepath=xbmcvfs.translatePath
START=True


HOME           = translatepath('special://home/')
ADDONS         = os.path.join(HOME,     'addons')
PACKAGES       = os.path.join(ADDONS,   'packages')
iconx = Addon.getAddonInfo('icon')
DIALOG         = xbmcgui.Dialog()
def fix():
    xbmc.executebuiltin('UpdateLocalAddons()')
    xbmc.sleep(1000)
    xbmc.executeJSONRPC('{{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{{"addonid":"{0}","enabled":true}},"id":1}}'.format('repository.gaia.2'))
def gdrive():
    try:
        from urllib.request import urlopen
        from urllib.request import Request
    except ImportError:
        from urllib2 import urlopen
        from urllib2 import Request
    from resources.modules import extract
    HOME           = translatepath('special://home/')
    ADDONS         = os.path.join(HOME,     'addons')
    PACKAGES       = os.path.join(ADDONS,   'packages')
    link= 'https://github.com/vip200/victory/blob/master/n.zip?raw=true'
    iiI1iIiI = translatepath ( os . path . join ( 'special://home/addons' , 'packages' ) )
    OOooO = os . path . join ( PACKAGES , 'isr.zip' )
    req = Request(link)
    remote_file = urlopen(req)
    f = open(OOooO, 'wb')
    try:
      total_size = remote_file.info().getheader('Content-Length').strip()
      header = True
    except AttributeError:
          header = False # a response doesn't always include the "Content-Length" header
    if header:
          total_size = int(total_size)
    bytes_so_far = 0
    start_time=time.time()
    while True:
          buffer = remote_file.read(8192)
          if not buffer:
              sys.stdout.write('\n')
              break

          bytes_so_far += len(buffer)
          f.write(buffer)

    II111iiii = translatepath ( os . path . join ( 'special://home/addons' ) )
    f.close()
    extract.all  ( OOooO , II111iiii)

    try:
      os.remove(OOooO)
    except:
      pass
    
    fix()
gdrive()