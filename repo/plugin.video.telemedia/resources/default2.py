# -*- coding: utf-8 -*-
import socket,xbmcaddon,os,xbmc,xbmcgui,urllib,re,xbmcplugin,sys,logging,shutil,time,xbmcvfs,json,base64
from datetime import date
import random
import requests
import zlib
import codecs
import xbmcvfs
xbmc_tranlate_path=xbmcvfs.translatePath
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc_tranlate_path(__addon__.getAddonInfo('path'))
Addon = xbmcaddon.Addon()
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
addon_id=__addon__.getAddonInfo('id')
from  resources.modules import pyxbmct
global clear
clear=True
global global_var,stop_all#global
global stopnext
global stopnow
stopnow=False
stopnext =False
global bot
bot =False
global_var=[]
import  threading
from threading import Thread
global break_window,play_status
# break_window_rd=False
break_window=False
play_status=''
update='עדכון מהיר זמין עבורכם'
global nextepisode,namenextupepisode
nextepisode=''
namenextupepisode=''
global stopbuffer
stopbuffer=False
global break_buffer
break_buffer=False
from resources.modules.globals import *
from resources.modules import cache as  cache
from resources.modules.public import addNolink,addDir3,addLink,lang,user_dataDir,addNolink2,addNolink3,addLink_db
from resources.modules import log#,sub
try:
    logo_path=os.path.join(user_dataDir, 'logo')
    tmdb_data_dir = os.path.join(addonPath, 'resources', 'tmdb_data')
    if not xbmcvfs.exists(logo_path+'/'):
         os.makedirs(logo_path)
    icons_path=os.path.join(user_dataDir, 'icons')
    if not xbmcvfs.exists(icons_path+'/'):
         os.makedirs(icons_path)
    fan_path=os.path.join(user_dataDir, 'fan')
    if not xbmcvfs.exists(fan_path+'/'):
         os.makedirs(fan_path)
    addon_path=os.path.join(user_dataDir, 'addons')
    if not xbmcvfs.exists(addon_path+'/'):
         os.makedirs(addon_path)
    addon_extract_path=os.path.join(user_dataDir, 'addons','temp')
    if not xbmcvfs.exists(addon_extract_path+'/'):
         os.makedirs(addon_extract_path)
except: pass

que=urllib.parse.quote_plus
url_encode=urllib.parse.urlencode

unque=urllib.parse.unquote_plus
global break_jump,silent,clicked,selected_index
selected_index=-1
clicked=False
silent=False
break_jump=0
addonInfo = xbmcaddon.Addon().getAddonInfo
settings = xbmcaddon.Addon().getSetting
profilePath = xbmc_tranlate_path(addonInfo('profile'))#.decode('utf-8')
skipFile = os.path.join(profilePath, 'skipintro.json')
time_ep_File = os.path.join(profilePath, 'time_ep.json')
defaultSkip = settings('default.skip')
default_ep_Skip = int(Addon.getSetting("window"))
if not os.path.exists(profilePath): xbmcvfs.mkdir(profilePath)
global id,playing_file,seek_time,exit_now
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path=dir_path.replace('resources','')
telemaia_icon=os.path.join(dir_path,'icon.png')
telemaia_fan=os.path.join(dir_path,'fanart.jpg')
exit_now=0
global list_index,str_next,sources_searching,list_index_list
global botplay
botplay=False
sources_searching=False
str_next=''
list_index=999
list_index_list=444


import importlib
importlib.reload (sys )#line:61


domain_s='https://'
id=0
listen_port=Addon.getSetting("port")
seek_time=0
playing_file=False
FMANAGER  = {0:'com.android.documentsui',1:'com.android.documentsui'}[0]
# socket.setdefaulttimeout(40.0)
cacheFile2 = os.path.join(user_dataDir, 'lastsubs.db')
global playing_text
playing_text=''
ACTION_PLAYER_STOP = 13
ACTION_BACK          = 92
ACTION_NAV_BACK =  92## Backspace action
ACTION_PARENT_DIR    = 9
ACTION_PREVIOUS_MENU = 10
ACTION_CONTEXT_MENU  = 117
ACTION_C_KEY         = 122

ACTION_LEFT  = 1
ACTION_RIGHT = 2
ACTION_UP    = 3
ACTION_DOWN  = 4
domain_s='https://'
COLOR2='yellow'
COLOR1='white'

ADDONTITLE='Telemedia'
DIALOG         = xbmcgui.Dialog()


def LogNotify(title, message, times=2000, icon=telemaia_icon,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)
def botplaytime():
    if Addon.getSetting("super_bot")=='false':
        
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous Power Bot'),'[COLOR %s]מנגן דרך הבוט[/COLOR]' % COLOR2)
        xbmc.executebuiltin('Action(Play)')
        Addon.setSetting('super_bot','true')
        xbmc.sleep(15000)
        Addon.setSetting('super_bot','false')
    else:
       LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous Power Bot'),'[COLOR %s]ניגון דרך הבוט מוגדר כבר כברירת מחדל[/COLOR]' % COLOR2)
def set_botplaytime():
    if Addon.getSetting("super_bot")=='false':
        
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous Power Bot'),'[COLOR %s]ניגון דרך הבוט הופעל.[/COLOR]' % COLOR2)
        Addon.setSetting('super_bot','true')
        sys.exit()
    if Addon.getSetting("super_bot")=='true':
       LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous Power Bot'),'[COLOR %s]ניגון דרך הבוט בוטל.[/COLOR]' % COLOR2)
       Addon.setSetting('super_bot','false')
       sys.exit()
       

def read_firebase(table_name):
    from resources.modules.firebase import firebase
    firebase = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = firebase.get('/', None)
    if table_name in result:
        return result[table_name]
    else:
        return {}

def write_firebase(original_title,tmdb,season,episode,playtime,total,free,table_name):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)


    result = fb_app.post(table_name, {'original_title':original_title,'tmdb':tmdb,'season':season,'episode':episode,'playtime':playtime,'total':total,'free':free})
    return 'OK'
def write_firebase_search(name,free,table_name):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)


    result = fb_app.post(table_name, {'name':name,'free':free})
    return 'OK'
def write_firebase_intro(data,table_name):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)


    result = fb_app.post(table_name, {'data':data})
    return 'OK'

def write_firebase_trackt(name,url,iconimage,fanart,overview,year,original_title,season,episode,tmdb,eng_name,show_original_year,heb_name,isr,type,table_name):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)


    result = fb_app.post(table_name, {'name':name,'url':url,'iconimage':iconimage,'fanart':fanart,'overview':overview,'year':year,'original_title':original_title,'season':season,'episode':episode,'tmdb':tmdb,'eng_name':eng_name,'show_original_year':show_original_year,'heb_name':heb_name,'isr':isr,'type':type})
    return 'OK'
def delete_firebase(table_name,record):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = fb_app.delete(table_name, record)
    return 'OK'
def jump_seek(name,id,season,episode,tvdb_id):
    global break_jump
    break_jump=1
    timeout=0
    while timeout<200:
        timeout+=1
        if break_jump==0:
            break
        if xbmc.Player().isPlaying():
            break
        xbmc.sleep(100)
    mark_once=0
    counter_stop=0
    g_timer=0
    avg=0
    while xbmc.Player().isPlaying():
        
        if break_jump==0:
            break
        try:
        
            vidtime = xbmc.Player().getTime()
        except Exception as e:
            vidtime=0
            pass

        if vidtime>0.2:
            try:
               g_timer=xbmc.Player().getTime()
               
                
                
               g_item_total_time=xbmc.Player().getTotalTime()
               time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
               avg=(g_timer*100)/g_item_total_time
               if mark_once==0:
                    mark_once=1
                    count=0
                    while (count<10):
                        try:
                            post_trk(id,season,episode,progress=True,len_progress=int(avg),type_progress='start',tvdb_id=tvdb_id)
                            break
                        except:
                            pass
                        count+=1
                        time.sleep(1)
               if ((avg>time_to_save_trk) and (g_item_total_time>100)):
                    count=0
                    while (count<10):
                        try:
                            post_trk(id,season,episode,tvdb_id=tvdb_id)
                            
                            break
                        except:
                            pass
                        count+=1
                        time.sleep(1)
                    done=1
            except:
                pass

    post_trk(id,season,episode,progress=True,len_progress=int(avg),type_progress='pause',tvdb_id=tvdb_id)

def  sync_firebase():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))#.decode("utf-8")
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'database.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    #המשך צפייה
    try:
        dbcur.execute("SELECT * FROM playback ")
        match = dbcur.fetchall()
    except:pass
    #חיפוש
    try:
        dbcur.execute("SELECT * FROM search ")
        matchsearch = dbcur.fetchall()
    except:pass
    #מעקב סדרות
    try:
        dbcur.execute("SELECT * FROM Lastepisode ")
        matchtrackt = dbcur.fetchall()
    except:pass



    all_names={}
    all_search={}
    all_trackt={}
    dp = xbmcgui.DialogProgress()
    try:
        dp.create("Firebase", 'מעדכן', 'אנא המתן',"")
    except:
        dp.create("Firebase", 'מעדכן'+'\n'+'אנא המתן'+'\n'+"")
   
    dp.update(0)
                
    count_m=0
    try:
        for name,tmdb,season,episode,playtime,totaltime,free in match:
            
            #log.warning('גגגג:'+str(match))
            all_names[name]=[]
            all_names[name].append((name,tmdb,season,episode,playtime,totaltime,free))
        all_record=read_firebase('playback')
        all_fire_names=[]
        for itt in all_record:
            #log.warning(all_record[itt]['original_title'])
            all_fire_names.append(all_record[itt]['original_title'])
        count=0
        # log.warning('Start'+all_names)
        for items in all_names:
            try:
                dp.update(int((count) / (len(all_names)) * 100.0), 'אנא המתן', items, '')
            except:
                dp.update(int((count) / (len(all_names)) * 100.0), 'אנא המתן'+'\n'+ items+'\n'+ '')
            count+=1
            if dp.iscanceled():
                dp.close()
            
            if items not in all_fire_names:

                name,tmdb,season,episode,playtime,totaltime,free=all_names[items][0]
                write_firebase(name,tmdb,season,episode,playtime,totaltime,free,'playback')

    except:pass
    count_m=0
    
    try:
        for name,free in matchsearch:
            all_search[name]=[]
            all_search[name].append((name,free))
        all_record=read_firebase('search')
        all_fire_names=[]
        for itt in all_record:
            all_fire_names.append(all_record[itt]['name'])
        count=0
        for items in all_search:
            try:
                dp.update(int((count) / (len(all_search)) * 100.0), 'אנא המתן', items, '')
            except:
                dp.update(int((count) / (len(all_search)) * 100.0), 'אנא המתן'+'\n'+ items+'\n'+ '')
            count+=1
            if dp.iscanceled():
                dp.close()
            if items not in all_fire_names:

                name,free=all_search[items][0]
                write_firebase_search(name,free,'search')
                
                
                
    except:pass
    count_m=0
    try:
        for name,url,iconimage,fanart,overview,year,original_title,season,episode,tmdb,eng_name,show_original_year,heb_name,isr,type in matchtrackt:
            name=name.replace('%27',"'")
            heb_name=heb_name.replace('%27',"'")
            
            if type=='movie':
             continue
            # log.warning('גגגג:'+str(match))
            all_trackt[name]=[]
            all_trackt[name].append((name,url,iconimage,fanart,overview,year,original_title,season,episode,tmdb,heb_name,show_original_year,heb_name,isr,type))
        all_record=read_firebase('trackt')
        all_fire_names=[]
        for itt in all_record:
            #log.warning(all_record[itt]['name'])
            all_fire_names.append(all_record[itt]['name'])
        count=0
        # log.warning('Start'+all_names)
        for items in all_trackt:
            try:
                dp.update(int((count) / (len(all_trackt)) * 100.0), 'אנא המתן', items, '')
            except:
                dp.update(int((count) / (len(all_trackt)) * 100.0), 'אנא המתן'+'\n'+ items+'\n'+ '')
            count+=1
            if dp.iscanceled():
                dp.close()
            
            if items not in all_fire_names:
                name,url,iconimage,fanart,overview,year,original_title,season,episode,tmdb,eng_name,show_original_year,heb_name,isr,type=all_trackt[items][0]
                write_firebase_trackt(name.replace('%27',"'"),url,iconimage,fanart,overview,year,original_title,season,episode,tmdb,heb_name.replace('%27',"'"),show_original_year,heb_name.replace('%27',"'"),isr,type,'trackt')
                

                
    except:pass
    
    dp.close()
    database_auto()
def get_html_result(url):
    # from  resources.modules.client import  get_html
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    html=requests.get(url,headers=headers).json()
    
    return html

OK_BUTTON = 201
NEW_BUTTON = 202
DISABLE_BUTTON = 210
ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92
INSTRUCTION_LABEL = 203
AUTHCODE_LABEL = 204
WARNING_LABEL = 205
CENTER_Y = 6
CENTER_X = 2

class CustomDialog(xbmcgui.WindowXMLDialog):

    def __init__(self, xmlFile, resourcePath, show):
        self.tvshow = show
    def background_skip(self):
        timeout=0
        break_jumpx=1
        time_left=999999
        while timeout<200:
            timeout+=1
            if break_jumpx==0:
                break
            if xbmc.Player().isPlaying():
                break
            xbmc.sleep(100)
        while xbmc.Player().isPlaying():
                if break_jumpx==0:
                    break
                timeNow = xbmc.Player().getTime()
                if int(timeNow) >= int(self.skipValue)+10:

                  self.close()
    
    def onInit(self):
        instuction = ''
        self.skipValue = int(getSkip(self.tvshow))
        skipLabel = 'דלג על הקדימון: %s' % self.skipValue
        skipButton = self.getControl(OK_BUTTON)
        timeNow = xbmc.Player().getTime()
        skipButton.setLabel(skipLabel)
        startTime = checkStartTime(original_title)
        # Thread(target=self.background_skip).start()
        # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous',startTime)))

        # self.close()
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
            self.close()

    def onControl(self, control):
        pass

    def onFocus(self, control):
        pass

    def onClick(self, control):
        print ('onClick: %s' % (control))

        if control == OK_BUTTON:
            timeNow = xbmc.Player().getTime()
            skipTotal = int(timeNow) + int(self.skipValue)
            xbmc.Player().seekTime(int(skipTotal-5))			

        if control == NEW_BUTTON:
            self.close()
            timeNow = xbmc.Player().getTime()
            dialog = xbmcgui.Dialog()
            # xbmc.executebuiltin('10115')
            xbmc.executebuiltin( "ActivateWindow(12905)" )
            # xbmc.Player().pause() 
            d = int(timeNow) #dialog.input('הכנס את אורך הקדימון בשניות', type=xbmcgui.INPUT_NUMERIC)
            d2 = 2
            # d2 = dialog.input('הכנס את זמן תחילת הקדימון', type=xbmcgui.INPUT_NUMERIC)
            if d2 == '' or d2 == None: d2 = 0
            if str(d) != '' and str(d) != '0': newskip(self.tvshow , d , start=d2)
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR2, 'הגדרת קדימון נשמרה לסדרה זו'),self.tvshow )
            # xbmc.Player().pause()
            
			
        if control == DISABLE_BUTTON:
            self.close()
            updateSkip(self.tvshow, seconds=self.skipValue, service=False)
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR2, 'חלון קדימון בוטל לסדרה זו'),self.tvshow )

        if control in [OK_BUTTON, NEW_BUTTON, DISABLE_BUTTON]:
            self.close()

class Chose_ep(xbmcgui.WindowXMLDialog):

    def __new__(cls, addonID, heb_name,name, id,season,episode,dates,original_title,dp,all_w):
        if Addon.getSetting("left_ep")=='true':
         FILENAME='chose_epold.xml'
        else:
         FILENAME='chose_ep.xml'
        return super(Chose_ep, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,heb_name,name, id,season,episode,dates,original_title,dp,all_w):
        super(Chose_ep, self).__init__()
        
        self.labelcontrol1=1020
        self.labelcontrol2=1021
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.season=season
        self.original_title=original_title
        self.id=id
        self.episode=episode
        self.heb_name=heb_name
        self.name=name
        self.dates=dates
        self.imagess=[]
        self.plotss=[]
        self.labelss=[]
        self.labelss1=[]
        self.dp=dp
        self.all_w=all_w
        
    def onInit(self):
        added_pre=''
        url='https://api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=%s'%(self.id,self.season,lang)
        try:
            self.dp.update(0, 'Series Traker','Loading', 'Get Html 1' )
        except:
            self.dp.update(0, 'Series Traker'+'\n'+ 'Loading'+'\n'+ 'Get Html 1' )
        html=cache.get(get_html_result,24,url, table='posters')
        
        
        url5='https://api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(self.id,self.season)
        try:
           self.dp.update(0, 'Series Traker','Loading', 'Get Html 1' )
        except:
           self.dp.update(0, 'Series Traker'+'\n'+ 'Loading'+'\n'+ 'Get Html 1' )
        html5=cache.get(get_html_result,24,url5, table='posters')
        
        
        try:
            maste_image='https://'+'image.tmdb.org/t/p/original/'+html['poster_path']
        except:
            maste_image=fanart

        if 'overview' not in html:
                html={}
                
                from resources.modules.tvdb import TVDB

                t = TVDB()
               
                url=domain_s+'api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=en&append_to_response=external_ids'%id
                # from  resources.modules.client import  get_html
                html=requests.get(url).json()
                if 'first_air_date' in html:
                 show_original_year=html['first_air_date'].split("-")[0]
                else:
                 show_original_year=0
              
                tvdb_id=str(html['external_ids']['tvdb_id'])
               
               
                if tvdb_id=='None':
                 #log.warning('Tryning None')
                 try:
                    tvdb_id_pre=t.getShow( original_title)
                    for itt in tvdb_id_pre['data']:
                        if itt['seriesName'].lower()==original_title.lower():
                            tvdb_id=str(itt['id'])
                    show=t.getShow_id(tvdb_id)
                 except:
                    show={'data':[]}
                    pass
                
                
                else:
                  show=t.getShow_id(tvdb_id)
                
                show_data=t.getShowData_id(tvdb_id)
                #log.warning(json.dumps(show_data))
                html['overview']=show_data['data']['overview']
                html['name']=show_data['data']['seriesName']
                html['episodes']=[]
                maste_image='https://www.thetvdb.com/banners/'+show_data['data']['fanart']
                match=[]
                all_episodes_tmdb=[]
                all_episodes=[]
                for item_tvdb in show['data']:
                    if item_tvdb['filename']!='':
                        img='https://www.thetvdb.com/banners/'+item_tvdb['filename']
                    else:
                        img=maste_image
                    match.append(('(T) '+item_tvdb['episodeName'],item_tvdb['airedEpisodeNumber'],item_tvdb['firstAired'],item_tvdb['overview'],item_tvdb['airedSeason'],img))
                all_season=[]
                all_season_tvdb_data=[]
                season_ep_count={}
                for ep_name,ep_num,aired,overview,s_number,image in match:
                   season_ep_count[s_number]=ep_num
                for ep_name,ep_num,aired,overview,s_number,image in match:
     
                     if str(s_number)==str(self.season):
                         if ep_num not in all_episodes:
                           
                           all_episodes.append(str(ep_num))
                           
                           all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"overview":overview,"season_number":s_number,"still_path":image,"poster_path":image})
   
                for items_a in all_episodes:
                     if items_a not in all_episodes_tmdb:
                       html['episodes'].append(all_season_tvdb_data[all_episodes.index(items_a)])
        master_plot=html['overview']
        
        master_name=html['name']
            
            
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        try:
          self.dp.update(0, 'Series Traker','Loading', 'DB' )
        except:
          self.dp.update(0, 'Series Traker'+'\n'+ 'Loading'+'\n'+  'DB' )
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode)+1)))
     
        match = dbcur.fetchone()
        # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous',id)))
        color_next='while'
        if match!=None:
           color_next='red'
        
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode))))
     
        match = dbcur.fetchone()
        color_current='green'
        
        if match!=None:
           color_current='white'
           
           
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode)-1)))
     
        match = dbcur.fetchone()
        dbcur.close()
        dbcon.close()
        color_prev='red'
        if match!=None:
           color_prev='magenta'
           
        height=1100
        self.getControl(5001).setHeight(height)
            
        self.list = self.getControl(3000)
        self.list.setHeight(height)

        newY = 360 - (height/2)

        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)

        self.params    = None
        
        self.paramList = []
        #צריך לבדוק   all_d=json.loads(unque(self.dates))
        all_d=json.loads(unque(self.dates))
        # logging.warning('323232W'+str(all_d))
        if len(all_d)<2:
            all_d=['','','']
      
        self.nextseason=False
        next_season_json={}
        try:
            self.dp.update(0, 'Series Traker','Loading', 'Get Html 2' )
        except:
            self.dp.update(0, 'Series Traker'+'\n'+ 'Loading'+'\n'+  'Get Html 2' )
        if all_d[2]==0:
            # from  resources.modules.client import  get_html
            ur='http://api.themoviedb.org/3/tv/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=en&append_to_response=external_ids'%self.id
            next_season_json=requests.get(ur).json()
            
            if int(next_season_json['number_of_seasons'])>int(season):
                
                
                url='https://api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s'%(self.id,str(int(self.season)+1),lang)
  
                html2=cache.get(get_html_data,24,url, table='posters')
                if 'episodes' in html2 and len(html2['episodes'])>0:
                    self.nextseason=True
        if self.nextseason:

            
            if 1:#len(html2['episodes'])>int(self.episode):
                items=html2['episodes'][0]
                title='[COLOR %s]'%color_next+items['name']+'[/COLOR]'
                plot=items['overview']
                image=maste_image
                if items['still_path']!=None:
                    if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                    else:
                        image=items['still_path']
                self.imagess.append(image)
                title=title+ Addon.getLocalizedString(32149)+str(1)
                self.labelss.append(title)
                liz   = xbmcgui.ListItem(title)
                
                liz.setProperty('title_type', '[COLOR magenta]'+Addon.getLocalizedString(32150)+'[/COLOR]'+html2['episodes'][0]['air_date'])
                self.labelss1.append('[COLOR magenta]'+Addon.getLocalizedString(32150)+'[/COLOR]'+html2['episodes'][0]['air_date'])
                liz.setProperty('image', image)
                liz.setProperty('description',plot)
                self.plotss.append(plot)
                

                
                self.list.addItem(liz)
            else:
                liz   = xbmcgui.ListItem(Addon.getLocalizedString(32149)+str(int(self.episode)+1))
                liz.setProperty('title_type', 'Play next episode - '+all_d[2])
                self.labelss1.append('Play next episode - '+all_d[2])
                
                liz.setProperty('image', '')
                liz.setProperty('description','')
                self.plotss.append('')
                
                
                self.list.addItem(liz)
            #current ep
            if len(html['episodes'])>(int(self.episode)-1):
                items=html['episodes'][int(self.episode)-1]
                title='[COLOR %s]'%color_current+': '+items['name']+'[/COLOR]'
                plot=items['overview']
                image=maste_image
                if items['still_path']!=None:
                    if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                    else:
                        image=items['still_path']
                self.imagess.append(image)
                title=Addon.getLocalizedString(32149)+str(int(self.episode))+' '+title
                    
            else:
                title=Addon.getLocalizedString(32149)+self.episode
                plot=''
                image=maste_image
                

            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32151)+all_d[1])
            self.labelss1.append(Addon.getLocalizedString(32151)+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            
            self.list.addItem(liz)
            
            #prev ep
            if len(html['episodes'])>(int(self.episode)-2):
                items=html['episodes'][int(self.episode)-2]
                title='[COLOR %s]'%color_prev+': '+items['name']+'[/COLOR]'
                plot=items['overview']
                image=maste_image
                if items['still_path']!=None:
                    if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                    else:
                        image=items['still_path']
                self.imagess.append(image)
                title=Addon.getLocalizedString(32149)+str(int(self.episode)-1)+' '+title
                self.labelss.append(title)
            else:
                title=Addon.getLocalizedString(32149)+str(int(self.episode)-1)
                plot=''
                image=maste_image
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32152)+all_d[0])
            self.labelss1.append(Addon.getLocalizedString(32152)+all_d[0])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
          

            
            self.list.addItem(liz)
                
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type',Addon.getLocalizedString(32153))
            self.labelss1.append(Addon.getLocalizedString(32153))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #season ep
            
            title=self.heb_name
            title=title.replace('%20',' ')
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32154))
            self.labelss1.append(Addon.getLocalizedString(32154))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            
        elif all_d[0]==0:
            #next ep
            if len(html['episodes'])>int(self.episode):
                
                try:
                 items=html['episodes'][int(self.episode)]
                 title='[COLOR %s]'%color_next+': '+items['name']+'[/COLOR]'
                except:
                 items=html5['episodes'][int(self.episode)]
                 try:
                  title='[COLOR %s]'%color_next+':'+items['name']+'[/COLOR]'
                 except:title='[COLOR %s]'%color_next+': '+'[/COLOR]'
                plot=items['overview']
                
                image=maste_image
                if items['still_path']!=None:
                    if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                    else:
                        image=items['still_path']
                self.imagess.append(image)
                title= 'פרק - '+str(int(self.episode)+1)+title
                self.labelss.append(title)
                liz   = xbmcgui.ListItem(title)
                liz.setProperty('title_type',Addon.getLocalizedString(32155)+all_d[2])
                self.labelss1.append(Addon.getLocalizedString(32155)+all_d[2])
                
                liz.setProperty('image', image)
                liz.setProperty('description',plot)
                self.plotss.append(plot)
                

                
                self.list.addItem(liz)
            else:
                liz   = xbmcgui.ListItem(Addon.getLocalizedString(32149)+str(int(self.episode)+1))
                liz.setProperty('title_type', Addon.getLocalizedString(32155)+all_d[2])
                self.labelss1.append(Addon.getLocalizedString(32155)+all_d[2])
                
                liz.setProperty('image', '')
                liz.setProperty('description','')
                self.plotss.append('')
                

                
                self.list.addItem(liz)
            #current ep
            ee=str(self.episode)
            if ee in self.all_w:
                  try:
                   all_w_time=int((float(self.all_w[ee]['resume'])*100)/float(self.all_w[ee]['totaltime']))
                  except:all_w_time=0
                  added_pre=' [COLOR yellow][I] - '+str(all_w_time)+'% אחוז צפיתם [/I] [/COLOR]'
            try:
             items=html['episodes'][int(self.episode)-1]
             title='[COLOR %s]'%color_current+' : '+items['name']+'[/COLOR]'
            except:
             items=html5['episodes'][int(self.episode)-1]
             try:
              title='[COLOR %s]'%color_current+' : '+items['name']+'[/COLOR]'
             except:title='[COLOR %s]'%color_current+' : '+'[/COLOR]'
            plot=items['overview']
            image=maste_image
            if items['still_path']!=None:
                if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                else:
                    image=items['still_path']
            self.imagess.append(image)
            title=Addon.getLocalizedString(32149)+self.episode+title
            self.labelss.append(title)
     
                
            
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', '[COLOR yellow]'+Addon.getLocalizedString(32151)+all_d[1]+'[/COLOR]'+added_pre)
            self.labelss1.append(Addon.getLocalizedString(32151)+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            

            self.list.addItem(liz)
            

            
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32153))
            self.labelss1.append(Addon.getLocalizedString(32153))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            
            #season ep
            
            title=self.heb_name
            title.replace('%20',' ')
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32154))
            self.labelss1.append(Addon.getLocalizedString(32154))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #choise=['Play next episode - '+all_d[2],'Play current episode - '+all_d[1],'Open season episodes','Open season selection']
        elif all_d[2]==0:
            
            
            #current ep
            try:
             items=html['episodes'][int(self.episode)-1]
             title='[COLOR %s]'%color_current+': '+items['name']+'[/COLOR]'
            except:
             items=html5['episodes'][int(self.episode)-1]
             try:
              title='[COLOR %s]'%color_current+': '+items['name']+'[/COLOR]'
             except:title='[COLOR %s]'%color_current+': '+'[/COLOR]'
            plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
            image=maste_image
            if items['still_path']!=None:
                if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                else:
                    image=items['still_path']
            self.imagess.append(image)
            title=Addon.getLocalizedString(32149)+self.episode+' '+title
                
            
                
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32151)+all_d[1])
            self.labelss1.append(Addon.getLocalizedString(32151)+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            
            self.list.addItem(liz)
            
            #prev ep
            try:
             items=html['episodes'][int(self.episode)-2]
             title='[COLOR %s]'%color_prev+': '+items['name']+'[/COLOR]'
            except:
             items=html5['episodes'][int(self.episode)-2]
             try:
              title='[COLOR %s]'%color_prev+': '+items['name']+'[/COLOR]'
             except:title='[COLOR %s]'%color_prev+': '+'[/COLOR]'
            plot=items['overview']
            image=maste_image
            if items['still_path']!=None:
                if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                else:
                    image=items['still_path']
            self.imagess.append(image)
            title=Addon.getLocalizedString(32149)+str(int(self.episode)-1)+' '+title
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type','[COLOR yellow]'+Addon.getLocalizedString(32151)+all_d[0]+'[/COLOR]')
            self.labelss1.append( Addon.getLocalizedString(32151)+all_d[0])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
          

            
            self.list.addItem(liz)
            
            
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32153))
            self.labelss1.append(Addon.getLocalizedString(32153))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #season ep
            
            title=self.heb_name
            title.replace('%20',' ')
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32154))
            self.labelss1.append(Addon.getLocalizedString(32154))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)
 

            self.list.addItem(liz)
            #choise=['Play current episode - '+all_d[1],'Play previous episode - '+all_d[0],'Open season episodes','Open season selection']
        else:
            #next ep
            if len(html['episodes'])>int(self.episode):
                try:
                 items=html['episodes'][int(self.episode)]
                 title='[COLOR %s]'%color_next+': '+items['name']+'[/COLOR]'
                except:
                 items=html5['episodes'][int(self.episode)]
                 try:
                  title='[COLOR %s]'%color_next+': '+items['name']+'[/COLOR]'
                 except:title='[COLOR %s]'%color_next+': '+'[/COLOR]'
                plot=items['overview']
                image=maste_image
                if items['still_path']!=None:
                    if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                    else:
                        image=items['still_path']
                self.imagess.append(image)
                title=Addon.getLocalizedString(32149)+str(int(self.episode)+1)+' '+title
                self.labelss.append(title)
                liz   = xbmcgui.ListItem(title)
                if 'magenta' not in all_d[2]:
                
                    liz.setProperty('title_type', Addon.getLocalizedString(32150)+all_d[2])
                    self.labelss1.append(Addon.getLocalizedString(32150)+all_d[2])
                else:
                
                    liz.setProperty('title_type', '[COLOR magenta]'+Addon.getLocalizedString(32150)+'[/COLOR]'+all_d[2])
                    self.labelss1.append('[COLOR magenta]'+Addon.getLocalizedString(32150)+'[/COLOR]'+all_d[2])
                liz.setProperty('image', image)
                liz.setProperty('description',plot)
                self.plotss.append(plot)
                

                
                self.list.addItem(liz)
            else:
                liz   = xbmcgui.ListItem(Addon.getLocalizedString(32149)+str(int(self.episode)+1))
                liz.setProperty('title_type', 'Play next episode - '+all_d[2])
                self.labelss1.append('Play next episode - '+all_d[2])
                
                liz.setProperty('image', '')
                liz.setProperty('description','')
                self.plotss.append('')
                
                
                self.list.addItem(liz)
            #current ep
            if len(html['episodes'])>(int(self.episode)-1):
                try:
                 items=html['episodes'][int(self.episode)-1]
                 title='[COLOR %s]'%color_current+': '+items['name']+'[/COLOR]'
                except:
                 items=html5['episodes'][int(self.episode)-1]
                 try:
                  title='[COLOR %s]'%color_current+': '+items['name']+'[/COLOR]'
                 except:title='[COLOR %s]'%color_current+': '+'[/COLOR]'
                plot=items['overview']
                image=maste_image
                if items['still_path']!=None:
                    if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                    else:
                        image=items['still_path']
                self.imagess.append(image)
                title=Addon.getLocalizedString(32149)+str(int(self.episode))+' '+title
                    
            else:
                title=Addon.getLocalizedString(32149)+self.episode
                plot=''
                image=maste_image
                

            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            ee=str(self.episode)
            if ee in self.all_w:
                  try:
                   all_w_time=int((float(self.all_w[ee]['resume'])*100)/float(self.all_w[ee]['totaltime']))
                  except:all_w_time=0
                  added_pre=' [COLOR yellow][I] - '+str(all_w_time)+'% אחוז צפיתם [/I] [/COLOR]'
            
            liz.setProperty('title_type', ' [COLOR yellow]'+Addon.getLocalizedString(32151)+all_d[1]+'[/COLOR]'+added_pre)
            self.labelss1.append(Addon.getLocalizedString(32151)+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            
            self.list.addItem(liz)
            
            #prev ep
            if len(html['episodes'])>(int(self.episode)-2):
                try:
                 items=html['episodes'][int(self.episode)-2]
                 title='[COLOR %s]'%color_prev+': '+items['name']+'[/COLOR]'
                except:
                 items=html5['episodes'][int(self.episode)-2]
                 try:
                  title='[COLOR %s]'%color_prev+': '+items['name']+'[/COLOR]'
                 except:title='[COLOR %s]'%color_prev+': '+'[/COLOR]'
                plot=items['overview']
                image=maste_image
                if items['still_path']!=None:
                    if 'https' not in items['still_path']:
                        image='https://'+'image.tmdb.org/t/p/original/'+items['still_path']
                    else:
                        image=items['still_path']
                self.imagess.append(image)
                title=Addon.getLocalizedString(32149)+str(int(self.episode)-1)+' '+title
                self.labelss.append(title)
            else:
                title=Addon.getLocalizedString(32149)+str(int(self.episode)-1)
                plot=''
                image=maste_image
            
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32152)+all_d[0])
            self.labelss1.append(Addon.getLocalizedString(32152)+all_d[0])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
          

            
            self.list.addItem(liz)
                
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type',Addon.getLocalizedString(32153))
            self.labelss1.append(Addon.getLocalizedString(32153))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #season ep
            
            title=self.heb_name
            title=title.replace('%20',' ')
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', Addon.getLocalizedString(32154))
            self.labelss1.append(Addon.getLocalizedString(32154))
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            

           

        try:
          self.dp.update(0, 'Series Traker','Loading', 'Final' )
        except:
          self.dp.update(0, 'Series Traker'+'\n'+ 'Loading'+'\n'+  'Final' )
        self.setFocus(self.list)
        self.getControl(self.imagecontrol).setImage(iconimage)
        self.getControl(self.bimagecontrol).setImage(maste_image)
        self.getControl(self.txtcontrol).setText(self.plotss[0])
        
        self.getControl(self.labelcontrol1).setLabel (heb_name.replace('%27',"'"))
        self.getControl(self.labelcontrol2).setLabel ('התאריך היום הוא: '+str(date.today()))
            
    def onAction(self, action):  
        actionId = action.getId()

        try:
            self.getControl(self.imagecontrol).setImage(iconimage)
            self.getControl(self.txtcontrol).setText(self.plotss[self.list.getSelectedPosition()])
            self.getControl(self.labelcontrol1).setLabel (heb_name.replace('%27',"'"))
            self.getControl(self.labelcontrol2).setLabel ('התאריך היום הוא: '+str(date.today()))
        except:
            pass
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = -1
            xbmc.sleep(100)
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = -1
            
            return self.close()


    def onClick(self, controlId):
        
        if controlId != 3001:
        
            index = self.list.getSelectedPosition()        
            
           
            #self.getControl(self.txtcontrol).setText(self.plotss[index])
            try:    self.params = index
            except: self.params = None

        self.close()
        

    def onFocus(self, controlId):
        pass

class UpNext(xbmcgui.WindowXMLDialog):
    item = None
    cancel = False
    watchnow = False
    
    progressStepSize = 0
    currentProgressPercent = 100

    def __init__(self, *args, **kwargs):
        #log.warning('INIT UPNEXT')
        global clicked
        from platform import machine
        
        OS_MACHINE = machine()
        self.closenow=0
        clicked=False
        self.action_exitkeys_id = [10, 13]
        #log.warning('INIT UPNEXT0')
        self.progressControl = None
        if OS_MACHINE[0:5] == 'armv7':
            xbmcgui.WindowXMLDialog.__init__(self)
        else:
            xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
        #log.warning('INIT UPNEXT2')
        
    def background_task2(self):
        if Addon.getSetting("keep_show")=='true':
            timeout=0
            break_jumpx=1
            time_left=999999
            while timeout<200:
                timeout+=1
                if break_jumpx==0:
                    break
                if xbmc.Player().isPlaying():
                    break
                xbmc.sleep(100)
            while xbmc.Player().isPlaying():
              xbmc.sleep(200)
              if not xbmc.Player().isPlaying():
                      self.close()
    def background_task(self):
        global list_index,clicked_id,clicked
        t=int(self.time_c)*10
        counter_close=0
        self.progressControl = self.getControl(3014)
        e_close=0
        before_end=int(Addon.getSetting("before_end2"))*10
        global_t=t-before_end
        counter_close2=t-before_end
        #log.warning('counter_close2_t:'+str(t))
        while(t>30):
            self.label=self.getControl(3015)
            if Addon.getSetting('play_nextup_wait')=='true' :
             self.label.setLabel(('הפרק הבא בעוד [COLOR FFFF4081] %s [/COLOR] שניות')%str(int(counter_close2)/10))

            counter_close2-=1
            if counter_close2==0:
                t=0
                
                break
            self.currentProgressPercent=int((counter_close2*100)/global_t)
       
            self.progressControl.setPercent(self.currentProgressPercent)
            xbmc.sleep(100)
            t-=1
            if self.closenow==1:
                break
        if self.closenow==0:
            list_index=self.list.getSelectedPosition()        
        self.close()
    def onInit(self):
        self.time_c=30
        try:
            self.time_c=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
        except:
            self.time_c=30
        
        
            
        self.list = self.getControl(3000)
        self.but = self.getControl(3012)
        self.closebut=self.getControl(3013)
        # self.but2 = self.getControl(3017)
        self.setFocus(self.but)
        if len(self.item['list'])==0:
                self.but.setVisible(False)
                self.setFocus(self.closebut)
        # if len(self.item['list'])==0:
                # self.but2.setVisible(False)
                # self.setFocus(self.closebut)
        for it in self.item['list']:
         
          
          liz   = xbmcgui.ListItem(it[0])
          self.list.addItem(liz)

        if Addon.getSetting('play_nextup_wait')=='true' :
         Thread(target=self.background_task).start()
        else:
         Thread(target=self.background_task2).start()
        self.setInfo()
        self.prepareProgressControl()

    def setInfo(self):
        #log.warning('INIT UPNEXT2')
       
        episodeInfo = str(self.item['season']) + 'x' + str(self.item['episode']) + '.'
        if self.item['rating'] is not None:
            rating = str(round(float(self.item['rating']), 1))
        else:
            rating = None
        
        if self.item is not None:
            self.setProperty(
                'fanart', self.item['art'].get('tvshow.fanart', ''))
            self.setProperty(
                'landscape', self.item['art'].get('tvshow.landscape', ''))
            self.setProperty(
                'clearart', self.item['art'].get('tvshow.clearart', ''))
            self.setProperty(
                'clearlogo', self.item['art'].get('tvshow.clearlogo', ''))
            self.setProperty(
                'poster', self.item['art'].get('tvshow.poster', ''))
            self.setProperty(
                'thumb', self.item['art'].get('thumb', ''))
            self.setProperty(
                'plot', self.item['plot'].replace("\n",'').strip())
            self.setProperty(
                'tvshowtitle', self.item['showtitle'])
            self.setProperty(
                'title', self.item['title'])
            self.setProperty(
                'season', str(self.item['season']))
            self.setProperty(
                'episode', str(self.item['episode']))
            self.setProperty(
                'seasonepisode', episodeInfo)
            self.setProperty(
                'year', str(self.item['firstaired']))
            self.setProperty(
                'rating', rating)
            self.setProperty(
                'playcount', str(self.item['playcount']))

    def prepareProgressControl(self):
        try:
            self.progressControl = self.getControl(3014)
            if self.progressControl is not None:
                self.progressControl.setPercent(self.currentProgressPercent)
        except Exception:
            pass

    def setItem(self, item):
        self.item = item

    def setProgressStepSize(self, progressStepSize):
        self.progressStepSize = progressStepSize

    def updateProgressControl(self):
        # noinspection PyBroadException
        try:
            self.currentProgressPercent = self.currentProgressPercent - self.progressStepSize
         
            self.progressControl = self.getControl(3014)
           
            if self.progressControl is not None:
                self.progressControl.setPercent(self.currentProgressPercent)
        except Exception:
            pass

    def setCancel(self, cancel):
        self.cancel = cancel

    def isCancel(self):
        return self.cancel

    def setWatchNow(self, watchnow):
        self.watchnow = watchnow

    def isWatchNow(self):
        return self.watchnow

    def onFocus(self, controlId):
        pass

    def doAction(self):
        pass

    def closeDialog(self):
        self.close()

    def onClick(self, control_id):
        global list_index,clicked,clicked_id,list_index_list
        clicked_id=str(control_id)
        
        if control_id == 3012:
            try:
                timeNow = xbmc.Player().getTotalTime()-xbmc.Player().getTime()
            except:
                timeNow=0
            d = int(timeNow)+10
            t = Thread(target=ep_time, args=(original_title,d,))
            t.start()
            # thread=[]
            
            # thread.append(Thread(ep_time,original_title,d))

            
            # thread[0].start()
            # ep_time(original_title,d, start=d2)

            # watch now
            clicked=True
            list_index=0
            self.setWatchNow(True)
            self.closenow=1
            self.close()
            
        elif control_id == 3013:

            # cancel
            clicked=False
            list_index=888
            list_index_list=555
            self.setCancel(True)
            self.closenow=1
            self.close()
        elif control_id == 3017:
            # פתח מקורות
            clicked=True
            list_index_list=0
            self.setWatchNow(True)
            self.closenow=1
            self.close()

        elif control_id == 3000:
            clicked=True
            index = self.list.getSelectedPosition()        
            list_index=index
            self.closenow=1
            self.close()
        pass

    def onAction(self, action):
        
        if action == ACTION_PLAYER_STOP:
            self.closenow=1
            self.close()


class ContextMenu_new2(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID, menu,icon,fan,txt,coun):
        FILENAME='contextmenu_new3.xml'
        return super(ContextMenu_new2, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID, menu,icon,fan,txt,coun):
        global playing_text,selected_index
        #log.warning('Init')
        super(ContextMenu_new2, self).__init__()
        self.menu = menu
        self.auto_play=0
        selected_index=-1
        self.params    = 666666
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.count_server=3
        self.tick_label=6001
        self.icon=icon
        self.fan=fan
        self.text=txt
        self.count_s=coun
        playing_text=''
        self.tick=60
        self.done=0
        self.story_gone=0
        self.count_p=0
        self.keep_play=''
        self.tick=60
        self.s_t_point=0
        self.start_time=time.time()
        #log.warning('dInit')
    def background_work(self):
        global playing_text,mag_start_time_new,now_playing_server,done1_1
        tick=0
        tick2=0
        changed=1
        vidtime=0
        while(1):
            
            all_t=[]
            for thread in threading.enumerate():
                if ('tick_time' in thread.getName()) or ('background_task' in thread.getName()) or ('get_similer' in thread.getName()) or ('MainThread' in thread.getName()) or ('sources_s' in thread.getName()):
                    continue

                if (trd_alive(thread)):#קודי19
                     all_t.append( thread.getName())
            self.getControl(606).setLabel(','.join(all_t))
            if  xbmc.getCondVisibility('Window.IsActive(busydialog)'):
                self.getControl(102).setVisible(True)
                if tick2==1:
                    self.getControl(505).setVisible(True)
                    tick2=0
                else:
                    self.getControl(505).setVisible(False)
                    tick2=1
            else:
                self.getControl(102).setVisible(False)
                self.getControl(505).setVisible(False)
            if len(playing_text)>0 or  self.story_gone==1 :
                changed=1
                vidtime=0
                if xbmc.Player().isPlaying():
                    vidtime = xbmc.Player().getTime()
                
                t=time.strftime("%H:%M:%S", time.gmtime(vidtime))
                
                if len(playing_text)==0:
                    playing_text=self.keep_play
                try:
                    self.keep_play=playing_text
                    self.getControl(self.txtcontrol).setText(t+'\n'+playing_text.split('$$$$')[0]+'\n'+now_playing_server.split('$$$$')[0]+'\n'+now_playing_server.split('$$$$')[1])
                    if vidtime == 0:
                        if tick==1:
                            self.getControl(303).setVisible(True)
                            tick=0
                        else:
                            self.getControl(303).setVisible(False)
                            tick=1
                except Exception as e:
                    #log.warning('Skin ERR:'+str(e))
                    self.params = 888
                    self.done=1
                    #log.warning('Close:4')
                    xbmc.executebuiltin( "Action(Fullscreen)" )
                    done1_1=3
                    self.close()
                    pass
            
            elif changed==1:
                    changed=0
                
                    self.getControl(303).setVisible(False)
                    self.getControl(self.txtcontrol).setText(self.text)
            
            if self.done==1:
                break
            if xbmc.Player().isPlaying():
                self.tick=60
                self.count_p+=1
                self.st_time=0
                
                vidtime = xbmc.Player().getTime()
                if self.s_t_point==0:
                    
                    
                    if vidtime > 0:
                        self.getControl(3000).setVisible(False)
                        self.getControl(self.imagecontrol).setVisible(False)
                        self.getControl(505).setVisible(False)
                        self.getControl(909).setPosition(1310, 40)
                        self.getControl(2).setPosition(1310, 100)
                        self.s_t_point=1
                        self.getControl(303).setVisible(False)
                        self.story_gone=1
                        #log.warning('Change seek Time:'+str(mag_start_time_new))
                        try:
                            if int(float(mag_start_time_new))>0:
                                xbmc.Player().seekTime(int(float(mag_start_time_new)))
                        except:
                            pass
                
                if vidtime > 0:
                    playing_text=''
     
                try:
                    value_d=(vidtime-(int(float(mag_start_time_new)))) 
                except:
                    value_d=vidtime
                play_time=int(Addon.getSetting("play_full_time"))
                if value_d> play_time and self.s_t_point>0:
                    self.params = 888
                    self.done=1
                    #log.warning('Close:1')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    done1_1=3
                    self.close()
              
                if self.count_p>(play_time+30) :
                   if Addon.getSetting("play_first")!='true':
                   
                    self.params = 888
                    self.done=1
                    #log.warning('Close:3')
                    xbmc.executebuiltin( "Action(Fullscreen)" )
                    done1_1=3
                    self.close()
            else:
                self.count_p=0
                self.s_t_point=0
                self.getControl(3000).setVisible(True)
         
                #self.getControl(505).setVisible(True)
                self.getControl(self.imagecontrol).setVisible(True)
                self.story_gone=0
                self.getControl(2).setPosition(1310, 700)
                self.getControl(909).setPosition(1310, 10)
            xbmc.sleep(1000)
    def tick_time(self):
        global done1_1
        while(self.tick)>0:
            self.getControl(self.tick_label).setLabel(str(self.tick))
            self.tick-=1
            
            if self.params == 888:
                break
            xbmc.sleep(1000)
        if self.params != 888:
            self.params = 888
            self.done=1
            ##log.warning('Close:93')
            xbmc.executebuiltin( "Action(Fullscreen)" )
            done1_1=3
            self.close()
    def fill_table(self,all_his_links):
        #log.warning('Start Fill')
        count=0
        self.paramList = []
        all_liz_items=[]
        try:
            for item in self.menu:
                self.getControl(202).setLabel(str(((count*100)/len(self.menu))) + '% Please Wait ')
                count+=1
                self.paramList.append(item[6])
                '''
                info=(PTN.parse(item[0]))
                if 'excess' in info:
                    if len(info['excess'])>0:
                        item[0]='.'.join(info['excess'])
                '''
                # golden=False
                # if 'Cached ' in item[0]:
                    # golden=True
                # item[0]=item[0].replace('Cached ','')
                # if len(item[0])>45 and '►►►' not in item[0]:
                # #    item[0]="\n".join(textwrap.wrap(item[0],60))
                     # item[0]=item[0][0:45]+'\n'+item[0][45:len(item[0])]
                title =item[0]
                if len(item[1].strip())<2:
                    item[1]=''
                if len(item[2].strip())<2:
                    item[2]='--'
                if len(item[3].strip())<2:
                    item[3]=''
                if len(item[4])<2:
                    item[4]=''
                if len(item[5])<2:
                    item[5]=''
                server=item[1]
                pre_n='[COLOR white]'+item[2]+'[/COLOR]'
                q=item[3]
                supplay='[COLOR lightblue]'+item[4]+'[/COLOR]'
                size='[COLOR coral]'+item[5]+'[/COLOR]'
                link=item[6]
                
                if item[7]==True or ('magnet' in server and allow_debrid):
                    supplay='[COLOR white][I]RD - '+supplay+'[/I][/COLOR]'
              
                if '►►►' in item[0]:
                    
                    title=''
                    supplay=item[0]
               
                
                if q=='2160':
                    q='4k'
                liz   = xbmcgui.ListItem(title)
                liz.setProperty('server', server)
                liz.setProperty('pre',pre_n)
                liz.setProperty('Quality', q)
                liz.setProperty('supply', supplay)
                liz.setProperty('size', size)
                try:
                    if item[6].encode('base64') in all_his_links:
                        liz.setProperty('history','100')
                except:pass
                if '►►►' not in item[0]:
                    liz.setProperty('server_v','100')
                if item[7]==True or ('magnet' in server and allow_debrid):
                    liz.setProperty('rd', '100')
                # if golden:
                    # liz.setProperty('magnet', '200')
                
                elif 'magnet' in server:
                    liz.setProperty('magnet', '100')
                all_liz_items.append(liz)
            #log.warning(' Done Loading')
            self.getControl(202).setLabel('')
            self.list.addItems(all_liz_items)

            self.setFocus(self.list)
        except Exception as e:
            log.warning('Fill error:'+str(e))
        
    def onInit(self):
        #log.warning('Start')
        xbmc.Player().stop()
        xbmc.executebuiltin('Dialog.Close(busydialog)')

        all_his_links=[]
        t = Thread(target=self.fill_table, args=(all_his_links,))
        t.start()
        # thread=[]
        # thread.append(Thread(self.fill_table,all_his_links))
        # thread[len(thread)-1].setName('fill_table')

        # thread[0].start()





        line   = 38
        spacer = 20
        delta  = 0 
        #log.warning('1')
        nItem = len(self.menu)
        if nItem > 16:
            nItem = 16
            delta = 1
        #log.warning('2')
        self.getControl(self.imagecontrol).setImage(self.icon)
        self.getControl(self.bimagecontrol).setImage(self.fan)
        #log.warning('3')
        if len(playing_text)==0:
            self.getControl(self.txtcontrol).setText(self.text)
        self.getControl(self.count_server).setText('Telemedia Results: '+str(self.count_s))
            
        height = (line+spacer) + (nItem*line)
        height=1100
        self.getControl(5001).setHeight(height)
        self.list = self.getControl(3000)
        self.list.setHeight(height)
        newY = 360 - (height/2)
        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)

    def played(self):
        self.params =7777
    def onAction(self, action):  
        global done1_1,selected_index
        actionId = action.getId()
        self.tick=60
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            #log.warning('Close:5')
            self.params = 888
            selected_index=-1
            
            self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK,ACTION_NAV_BACK]:
            self.params = 888
            selected_index=-1
            self.close()

    
    def onClick(self, controlId):
        global playing_text,done1_1,selected_index
        self.tick=60
        
        if controlId != 3001:

            index = self.list.getSelectedPosition()        
            
            try:    
                self.params = index
            except:
                self.params = None
            xbmc.executebuiltin( "Action(Fullscreen)" )
            selected_index=self.params
            self.close()
        else:
            selected_index=-1
            self.close()
        
    def close_now(self):
        global done1_1
        #log.warning('Close:8')
        self.params = 888
        self.done=1
        xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
        xbmc.sleep(1000)
        #log.warning('Close now CLosing')
        done1_1=3
        self.close()
    def onFocus(self, controlId):
        pass
def meta_get(video_data,item):

    if item=='year' or item=='rating' or item=='votes' or item=='duration':
        try:
            int(video_data.get(item,'0'))
        except:
            try:
                float(video_data.get(item,'0'))
            except:
                video_data[item]='0'
        return video_data.get(item,'0')
    if item=='country' or item=='cast':
        return video_data.get(item,[])
    return video_data.get(item,' ')
    return video_data.get(item,' ')
class OverlayText:
    def __init__(self):
        #log.warning('(Overlay) Initialize overlay text')
        x, y, w, h = self._calculate_the_size()

        self._shown       = False
        self._window     = xbmcgui.Window(12005)
        self._label      = xbmcgui.ControlLabel(x, y, w, h, '', alignment=0x00000002 | 0x00000004)
        media_path=os.path.join(xbmc_tranlate_path(Addon.getAddonInfo("path")),'resources','media')
        self._background = xbmcgui.ControlImage(x, y, w, h, os.path.join(media_path, "black.png"))

        self._background.setColorDiffuse("0xD0000000")

    def __enter__(self):
        return self

    def open(self):
        if not self._shown:
            self._window.addControls([self._background, self._label])
            self._shown = True

    def isShowing(self):
        return self._shown

    def setText(self, text):
        if self._shown:
            self._label.setLabel(text)

    def _calculate_the_size(self):
        # get skin resolution
        import xml.etree.ElementTree as ET
        tree = ET.parse(os.path.join(xbmc_tranlate_path("special://skin/"), "addon.xml"))
        res = tree.findall("./extension/res")[0]
        viewport_w = int(res.attrib["width"])
        viewport_h = int(res.attrib["height"])
        # Adjust size based on viewport, we are using 1080p coordinates
        w = int(int(1920.0 * 0.7) * viewport_w / 1920.0)
        h = int(150 * viewport_h / 1088.0)
        x = int((viewport_w - w) / 2)
        y = int((viewport_h - h) / 2)
        return x, y, w, h

    def __exit__(self, *exc_info):
        self.close()
        return not exc_info[0]

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, '_background') and self._shown:
            self._window.removeControls([self._background, self._label])
            self._shown = False

def selection_time_window(msg,iconImage,fanart,title,percent):
    class MyWindow(xbmcgui.WindowXMLDialog):
        global selection,clicked
        selection=''
        clicked=''
        def __init__(self, *args, **kwargs):
            THEME2         = '[COLOR white]%s[/COLOR]'
            # self.test = kwargs['test']
            self.message =  THEME2 % kwargs['msg']
        
        def onInit(self):
            self.image       = 101
            self.image3       = 107
            self.image4       = 1077
            self.titlebox    = 102
            self.titleimage  = 103
            self.titleimage2  = 109
            self.textbox     = 104
            # self.scroller    = 105
            self.closewindow  = 200
            self.dismiss     = 201
            self.fastupdate  = 202
            
            self.showdialog()
            self.list_index=-1
        def showdialog(self):
            PATH           = xbmcaddon.Addon().getAddonInfo('path')
            ART            = os.path.join(PATH, 'resources', 'art')
            self.testimage = os.path.join(ART, 'text.png')
            self.getControl(self.image4).setImage(iconImage)
            self.getControl(self.image3).setImage(fanart)
            self.getControl(self.image).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setLabel(self.message)
            self.setFocusId(self.dismiss)
            THEME2         = '[COLOR white]%s[/COLOR]'
            self.getControl(self.titlebox).setLabel(THEME2 % title)
            self.getControl(5000).setPercent(percent)

        def doBotplay(self):
                    
                global selection,clicked
                selection=1
                clicked=1
                self.close()
        def doSaveLocation(self):
                global selection,clicked
                # click=0
                selection=0
                self.close()
        def doclose(self):
                global selection,clicked
                # selection=1
                clicked=1
                self.close()

        def onAction(self,action):
            global selection,clicked
            if   action == ACTION_PREVIOUS_MENU:

                # selection=-1
                clicked=0
                self.close()
            elif action == ACTION_NAV_BACK:

                # selection=-1
                clicked=0
                self.close()

        def onClick(self, controlId):
            if (controlId == self.dismiss): self.doSaveLocation()
            elif (controlId == self.closewindow): self.doclose()
            else: self.doBotplay()
    
    notify = MyWindow( "time_selection.xml" , Addon.getAddonInfo('path'), 'DefaultSkin', msg=msg)
    notify.doModal()
    del notify
    return selection,clicked
def selection_time_menu(title='',item=''):
    try:
     class selection_time(pyxbmct.AddonDialogWindow):
        
        def __init__(self, title='',item=''):
           
            super(selection_time, self).__init__(title)
            #'Play from beginning'
            self.item=[item,Addon.getLocalizedString(32043)]
            self.setGeometry(350, 180,2, 1,pos_x=600, pos_y=200)
            self.list_index=-1

            self.clicked=0
            self.getWindowTitle()
            self.set_active_controls()
            self.set_navigation()
            # Connect a key action (Backspace) to close the window.
            self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        def getWindowTitle(self):
            self.setWindowTitle('נגן מאיפה שהופסק')
        def get_selection(self):
            """ get final selection """
            return self.list_index
        def click_list(self):
            self.clicked=1
            self.list_index=self.list.getSelectedPosition()
           
            self.close()
        
        def set_active_controls(self):

            # List
            self.list = pyxbmct.List(font ='font15')
            self.placeControl(self.list, 0,0,  rowspan=2)
            # Add items to the list

            self.list.addItems(self.item)
            # Connect the list to a function to display which list item is selected.
            self.connect(self.list, self.click_list)

        def set_navigation(self):
            
            self.setFocus(self.list)

        def setAnimation(self, control):
            # Set fade animation for all add-on window controls
            control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=0',),
                                    ('WindowClose', 'effect=fade start=100 end=0 time=0',)])
     window = selection_time(title,item)
     window.doModal()
     selection = window.get_selection()
     clicked=window.clicked
     del window
     return selection,clicked
    except:
        pass
class player_window(xbmcgui.WindowXMLDialog):
    def __new__(cls, addonID,id,tv_movie,season,episode,fanart):
        
        
        FILENAME='play_window.xml'
        
        return super(player_window, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,id,tv_movie,season,episode,fanart):
        super(player_window, self).__init__()
        self.tv_movie=tv_movie
        self.id=id
        self.poster=1
        self.label=5
        self.label2=6
        self.close_now=False
        self.playbutton=5003
    def onAction(self, action):
        global break_buffer
        
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            break_buffer=True
            self.close_now=True
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            break_buffer=True
            self.close_now=True
            return self.close()
    def get_img_ch(self,tv_movie,id):
        # from  resources.modules.client import  get_html

        url='https://api.themoviedb.org/3/%s/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&include_image_language=ru,null&append_to_response=images,external_ids'%(self.tv_movie,self.id,lang)
       
        html=requests.get(url).json()
        return html
    def get_img(self):
        # self.html=cache.get(self.get_img_ch, 0,self.tv_movie,self.id,table='pages')
        # logging.warning('3333333'+str(self.html))
        # try:
            # fan=domain_s+'image.tmdb.org/t/p/original/'+self.html['backdrop_path']
            # self.getControl(self.poster).setImage(fan)
        # except:
             # fan='special://home/addons/plugin.video.telemedia/tele/windows_play.jpg'
        self.getControl(self.poster).setImage(fanart)
        try:
          tvdb_id=str(self.html['external_ids']['tvdb_id'])
        except:
         tvdb_id=''
        # logging.warning('tvdb::'+tvdb_id)
        all_n_fan=[]
        all_banner=[]
        try:
            
            time_to_save=int(Addon.getSetting("save_time"))
            full_art= cache.get(get_more_meta, time_to_save, self.id,self.tv_movie,tvdb_id, table='pages') 
            
            
            if self.tv_movie=='tv':
                logo=full_art['hdtvlogo']
                if len(logo)>0:
                   
                    all_logo=[]
                    for itt in logo:
                       if itt['lang']=='en':
                        all_logo.append(itt['url'])
                    random.shuffle(all_logo)
                    self.getControl(5002).setImage(all_logo[0])
                
                
                for itt in full_art['showbackground']:
                   if itt['lang']=='en':
                    all_n_fan.append(itt['url'])
                for itt in full_art['tvbanner']:
                   if itt['lang']=='en':
                    all_banner.append(itt['url'])
            else:
                logo=full_art['hdmovielogo']
                if len(logo)>0:
                    all_logo=[]
                    for itt in logo:
                      if itt['lang']=='en':
                        all_logo.append(itt['url'])
                    random.shuffle(all_logo)
                    self.getControl(5002).setImage(all_logo[0])
                
                
                for itt in full_art['moviebackground']:
                   if itt['lang']=='en':
                    all_n_fan.append(itt['url'])
                for itt in full_art['moviebanner']:
                   if itt['lang']=='en':
                    all_banner.append(itt['url'])
        except Exception as e:
            logging.warning('Fanart Err:'+str(e))
            self.getControl(self.label2).setLabel(name)
    def onInit(self):
        global break_window
        t = Thread(target=self.get_img, args=())
        t.start()
        # thread=[]
        # thread.append(Thread(self.get_img))
        # thread[len(thread)-1].setName('background_task')
        
        # for td in thread:
            # td.start()
            
        
        timeout=0
        start_time=time.time()
        while timeout<2000:
            timeout+=1
            if self.close_now:
                break
            elapsed_time = time.time() - start_time

            # self.getControl(self.label).setLabel('המתן לניגון'+': '+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+', '+play_status)
            self.getControl(self.label).setLabel(play_status)
            #self.getControl(self.playbutton).setVisible(True)
            
            # if xbmc.Player().isPlaying():
                    
                # try:
                    # vidtime = xbmc.Player().getTime()
                    # # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', vidtime)))
                    # if vidtime>0.5:
                        # break
                # except:
                    # pass
           
                
            if break_window:
                break
            xbmc.sleep(10)
        # if not break_window:
         # xbmc.sleep(300)
        return self.close()
def free_space_window(msg,iconImage):
    class MyWindow(xbmcgui.WindowXMLDialog):
        def __init__(self, *args, **kwargs):
            THEME2         = '[COLOR white]%s[/COLOR]'
            # self.test = kwargs['test']
            self.message =  THEME2 % kwargs['msg']
        
        def onInit(self):
            self.image       = 101
            self.image3       = 107
            self.titlebox    = 102
            self.titleimage  = 103
            self.titleimage2  = 109
            self.textbox     = 104
            # self.scroller    = 105
            self.closewindow  = 200
            self.dismiss     = 201
            self.fastupdate  = 202
            self.titlebox2    = 1022
            self.showdialog()

        def showdialog(self):
            PATH           = xbmcaddon.Addon().getAddonInfo('path')
            ART            = os.path.join(PATH, 'resources', 'art')
            self.testimage = os.path.join(ART, 'text.png')
            self.getControl(self.image3).setImage(iconImage)
            self.getControl(self.image).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setLabel('מקום פנוי במכשיר: '+self.message+'Gb')
            self.setFocusId(self.fastupdate)
            THEME2         = '[COLOR white]%s[/COLOR]'
            self.getControl(self.titlebox).setLabel(THEME2 % 'אין מספיק שטח אחסון לניגון התוכן')
            self.getControl(self.titlebox2).setText(THEME2 % 'ניתן לנגן את התוכן דרך הבוט או לבחור מיקום הורדה של התוכן לכונן SSD בלבד')

        def doBotplay(self):
                    
                global bot
                bot=True
                self.close()
        def doSaveLocation(self):
                # Addon.openSettings()
                HOME             = translatepath('special://home/')
                path=Addon.getSetting("directory_mod")
                if path:
                  path = xbmcgui.Dialog().browse(0,"בחר תקייה", 'files')
                  Addon.setSetting("movie_download_directory",path)
                  Addon.setSetting('directory_mod','true')
                  ok=xbmcgui.Dialog().yesno(("יש להפעיל את הקודי מחדש לאחר שינוי זה."),('להפעיל מחדש?'))
                  if ok:
                       os._exit(1)
                  xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                self.close()
        def doclose(self):
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                self.close()

        def onAction(self,action):
            if   action == ACTION_PREVIOUS_MENU: self.doclose()
            elif action == ACTION_NAV_BACK: self.doclose()

        def onClick(self, controlId):
            if (controlId == self.dismiss): self.doSaveLocation()
            elif (controlId == self.closewindow): self.doclose()
            else: self.doBotplay()

    notify = MyWindow( "size_info.xml" , Addon.getAddonInfo('path'), 'DefaultSkin', msg=msg)
    notify.doModal()
    return True
    del notify

def timer_clear_files():
    stop_time = time.time() + 30

    while 1:

          if time.time() > stop_time:
            clear_files()
            break
    return 
def clear_files():
    
    # xbmc.sleep(100)
    try:    
        os.remove(os.path.join(translatepath("special://userdata/"),"addon_data","plugin.video.telemedia","database","db.sqlite"))
    except:
        pass
    # try:    
    directory_mod=Addon.getSetting("directory_mod")
    if directory_mod =='true':
    #db_path=os.path.join(user_dataDir, 'files','temp')
        user_dataDir2=str(xbmc_tranlate_path(Addon.getSetting("movie_download_directory")))
        db_path=os.path.join(user_dataDir2,'temp')
    else:
        db_path=os.path.join(user_dataDir, 'files','temp')
    
    if os.path.exists(db_path):
        onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
        
        for fl in onlyfiles:
            #dp.update(0, 'Please Wait...','Removing File', fl )
            re_fl=os.path.join(db_path,fl)
            
            if os.path.exists(re_fl):
              try:
                os.remove(re_fl)
              except Exception as e:
                try:
                    xbmc.sleep(5000)
                    os.remove(re_fl)
                    logging.warning('Err:'+str(e))
                except:pass
    db_path=os.path.join(user_dataDir, 'files','documents')
    if os.path.exists(db_path):
        onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
        for fl in onlyfiles:
            #dp.update(0, 'Please Wait...','Removing File', fl )
            re_fl=os.path.join(db_path,fl)
            if os.path.exists(re_fl):
              try:
                os.remove(re_fl)
              except Exception as e:
                try:
                    xbmc.sleep(5000)
                    os.remove(re_fl)
                    logging.warning('Err2:'+str(e))
                except:pass
    
    db_path=os.path.join(user_dataDir, 'files','videos')
    if os.path.exists(db_path):
        onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
        for fl in onlyfiles:
            #dp.update(0, 'Please Wait...','Removing File', fl )
            re_fl=os.path.join(db_path,fl)
            if os.path.exists(re_fl):
              try:
                os.remove(re_fl)
              except Exception as e:
                try:
                    xbmc.sleep(5000)
                    os.remove(re_fl)
                    logging.warning('Err3:'+str(e))
                except:pass
    db_path=os.path.join(user_dataDir, 'files','photos')
    if os.path.exists(db_path):
        onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
        for fl in onlyfiles:
            #dp.update(0, 'Please Wait...','Removing File', fl )
            re_fl=os.path.join(db_path,fl)
            if os.path.exists(re_fl):
              try:
                os.remove(re_fl)
              except Exception as e:
                try:
                    xbmc.sleep(5000)
                    os.remove(re_fl)
                    logging.warning('Err4:'+str(e))
                except:pass
    db_path=os.path.join(user_dataDir, 'files','music')
    if os.path.exists(db_path):
        onlyfiles = [f for f in os.listdir(db_path) if os.path.isfile(os.path.join(db_path, f))]
        for fl in onlyfiles:
            #dp.update(0, 'Please Wait...','Removing File', fl )
            re_fl=os.path.join(db_path,fl)
            if os.path.exists(re_fl):
              try:
                os.remove(re_fl)
              except Exception as e:
                try:
                    xbmc.sleep(5000)
                    os.remove(re_fl)
                    logging.warning('Err5:'+str(e))
                except:pass
    # xbmc.sleep(10000)
    # except Exception as e:
        # log.warning('Error removing files:'+str(e))

def write_trackt(original_name_r,url,iconimage,fanart,description,year,original_name_c,season,episode,tmdb,heb_name,show_original_year,eng_name,isr,tv_movie,table_name):
        table_name='trackt'
        all_firebase=read_firebase(table_name)
        write_fire=True
        for items in all_firebase:
            if all_firebase[items]['name']==heb_name:
                delete_firebase(table_name,items)
                break
        if write_fire:
            write_firebase_trackt(heb_name,url,iconimage,fanart,description,year,original_name_r,season,episode,tmdb,heb_name,show_original_year,heb_name,isr,tv_movie,table_name)


def is_hebrew(input_str):    
       try:
        import unicodedata
        input_str=input_str.replace(' ','').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
        nfkd_form = unicodedata.normalize('NFKD', input_str.replace(' ','').replace('\n','').replace('\r','').replace('\t','').replace(' ',''))
        a=False
        for cha in input_str:
            
            a='HEBREW' in unicodedata.name(cha.strip())
            if a:
                break
        return a
       except:
            return True
def get_more_meta(id,tv_movie,tvdb_id):
    # from  resources.modules.client import  get_html
    user = 'cf0ebcc2f7b824bd04cf3a318f15c17d'

    headers = {'api-key': 'a7ad21743fd710fccb738232f2fbdcfc'}

    headers.update({'client-key': user})
    if tv_movie=='tv':
        m_type='tv'
    else:
        m_type='movies'
    f_id=id
    if tv_movie=='tv':
        f_id=tvdb_id
    art=requests.get('http://webservice.fanart.tv/v3/%s/%s'%(m_type,f_id),headers=headers).json()

    return art
def get_extra_art(id,tv_movie,tvdb_id):
    try: 
            
            all_logo=[]
            all_banner=[]
            all_n_fan=[]
            all_clear_art=[]
            r_logo=''
            r_art=''
            time_to_save=int(Addon.getSetting("save_time"))
            full_art= cache.get(get_more_meta, time_to_save, id,tv_movie,tvdb_id, table='pages') 

            if tv_movie=='tv':
                logo=full_art['hdtvlogo']
                if len(logo)>0:
                   
                    
                    for itt in logo:
                       if itt['lang']=='en':
                        all_logo.append(itt['url'])
                    random.shuffle(all_logo)
                    r_logo=all_logo[0]
                
                
                for itt in full_art['showbackground']:
                   if itt['lang']=='en':
                    all_n_fan.append(itt['url'])
                for itt in full_art['tvbanner']:
                   if itt['lang']=='en':
                    all_banner.append(itt['url'])
            else:
            
                logo=full_art['hdmovielogo']
                if len(logo)>0:
                    all_logo=[]
                    for itt in logo:
                      if itt['lang']=='en':
                        all_logo.append(itt['url'])
                    random.shuffle(all_logo)
                    r_logo=all_logo[0]
                
                for itt in full_art['hdmovieclearart']:
                   if itt['lang']=='en':
                    all_clear_art.append(itt['url'])
                
                random.shuffle(all_clear_art)
                r_art=all_clear_art[0]
                for itt in full_art['moviebackground']:
                   if itt['lang']=='en':
                    all_n_fan.append(itt['url'])
                for itt in full_art['moviebanner']:
                   if itt['lang']=='en':
                    all_banner.append(itt['url'])
    except Exception as e:
        logging.warning('Fanart Err:'+str(e))
    return all_logo,all_n_fan,all_banner,all_clear_art,r_logo,r_art
def forward_messages(l_data):
    import logging
    num=random.randint(0,60000)
    c_id=l_data['c_id']
    m_id=l_data['m_id']
    PURN=[-1001039298836,-1001387798924,-1001251614658]
    for i in PURN:
     if c_id==i:
        return 
    data={'type':'td_send',
         'info':json.dumps({'@type': 'forwardMessages','chat_id':(-1001648442555), 'from_chat_id': c_id,'message_ids':[m_id],'options':{'@type': 'messageSendOptions'},'send_copy':True,'@extra': num})
         }
    # data={'type':'td_send',
         # 'info':json.dumps({'@type': 'forwardMessages','chat_id':(-1001648442555), 'from_chat_id': c_id,'message_ids':[m_id],'@extra': num})
         # }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()


    try:#מרענן רשימת קבוצות
        if 'Chat to forward messages to not found' in event['message']:
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChats','offset_chat_id':'0','offset_order':'0', 'limit': '50','chat_list':{'@type': 'chatListMain'}, '@extra': num})
                 }
            event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    except:pass

    try:#מוסיף את הערוץ אם לא קיים
        if 'Have no write access to the chat' in event['message'] or 'Chat to forward messages to not found' in event['message']:

            if not os.path.exists(os.path.join(user_dataDir, '4.1.2')):
                invite_link="https://t.me/+xy0aI2dz1L42NmU0"
                data={'type':'td_send',
                 'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
                 }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'forwardMessages','chat_id':(-1001648442555), 'from_chat_id': c_id,'message_ids':[m_id],'options':{'@type': 'messageSendOptions'},'send_copy':True,'@extra': num})
                     }

                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                file = open(os.path.join(user_dataDir, '4.1.2'), 'w') 
                file.write(str('Done'))
                file.close()
    except:pass
    
class TelePlayer(xbmc.Player):
    
    def __init__(self, *args, **kwargs):
       
        self.g_timer=0
        self.g_item_total_time=0
        xbmc.Player.__init__(self)
        
    def onPlayBackStarted(self):
        global id,playing_file
        self.g_timer=0

        playing_file=True
    def onPlayBackResumed(self):
        global id,playing_file

        playing_file=True

    def onPlayBackPaused(self):
        global id,playing_file

        playing_file=True
    def onPlayBackEnded(self):
        global id,playing_file

        num=random.randint(0,60000)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        playing_file=False

    def update_db(self):
        global name
        global original_title
        if original_title=='':
         original_title=name

        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        self.dbcon = database.connect(cacheFile)
        self.dbcur = self.dbcon.cursor()
        self.dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        
        self.dbcon.commit()
        self.season=self.season.replace('%20','0').replace(' ','0')
        self.episode=self.episode.replace('%20','0').replace(' ','0')
        
        if len(str(self.tmdb))<2 and tmdb!='%20':
            only_name=True
            self.dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(original_title.replace("'","%27"),self.season,self.episode))
        else:
            only_name=False
            self.dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(self.tmdb,self.season,self.episode))
        match = self.dbcur.fetchall()
        
        if match==None:
          self.dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (original_title.replace("'","%27"),self.tmdb,self.season,self.episode,str(self.g_timer),str(self.g_item_total_time),' '))
          self.dbcon.commit()
          table_name='playback'
          if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
                
                try:
                    all_firebase=read_firebase(table_name)
                    write_fire=True
                    for items in all_firebase:
                  
                        if all_firebase[items]['original_title']==original_title:
                         if all_firebase[items]['season']==self.season:
                          if all_firebase[items]['episode']==self.episode:
                            t = Thread(target=delete_firebase, args=(table_name,items,))
                            t.start()
                            break
                    if write_fire:
                        t = Thread(target=write_firebase, args=(original_title,self.tmdb,self.season,self.episode,str(self.g_timer),str(self.g_item_total_time),'',table_name,))
                        t.start()

                except Exception as e:
                  import linecache,sys
                  exc_type, exc_obj, tb = sys.exc_info()
                  f = tb.tb_frame
                  lineno = tb.tb_lineno
                  log.warning('Error :'+ str(e) +',line no:'+str(lineno))
                  match_playtime = self.dbcur.fetchone()
                  LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)

        else:
           if len(match)>0:
            name,timdb,season,episode,playtime,totaltime,free=match[0]
            table_name='playback'
            if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
             if only_name:
                
                try:
                    all_firebase=read_firebase(table_name)
                    write_fire=True
                    for items in all_firebase:
                  
                        if all_firebase[items]['original_title']==original_title:
                         if all_firebase[items]['season']==self.season:
                          if all_firebase[items]['episode']==self.episode:

                            # delete_firebase(table_name,items)
                            t = Thread(target=delete_firebase, args=(table_name,items,))
                            t.start()
                            break
                    
                    if write_fire:
                        t = Thread(target=write_firebase, args=(original_title,tmdb,season,episode,str(playtime),str(totaltime),free,table_name,))
                        t.start()
                except Exception as e:
                  import linecache,sys
                  exc_type, exc_obj, tb = sys.exc_info()
                  f = tb.tb_frame
                  lineno = tb.tb_lineno
                  log.warning('Error :'+ str(e) +',line no:'+str(lineno))
                  match_playtime = self.dbcur.fetchone()
                  LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)

            if str(self.g_timer)!=playtime:
                if only_name:
                    self.dbcur.execute("UPDATE playback SET playtime='%s' where name='%s' and  season='%s' and episode='%s'"%(str(self.g_timer),original_title.replace("'","%27"),self.season,self.episode))

                else:
                    self.dbcur.execute("UPDATE playback SET playtime='%s' where tmdb='%s' and  season='%s' and episode='%s'"%(str(self.g_timer),self.tmdb,self.season,self.episode))
                    table_name='playback'
                    if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
                        try:
                            all_firebase=read_firebase(table_name)
                            write_fire=True
                            for items in all_firebase:
                          
                                if all_firebase[items]['original_title']==original_title:
                                 if all_firebase[items]['season']==self.season:
                                  if all_firebase[items]['episode']==self.episode:
                                    t = Thread(target=delete_firebase, args=(table_name,items,))
                                    t.start()
                                    break
                            
                            if write_fire:
                                t = Thread(target=write_firebase, args=(original_title,tmdb,season,episode,str(self.g_timer),str(totaltime),free,table_name,))
                                t.start()

                        except Exception as e:
                          import linecache,sys
                          exc_type, exc_obj, tb = sys.exc_info()
                          f = tb.tb_frame
                          lineno = tb.tb_lineno
                          log.warning('Error :'+ str(e) +',line no:'+str(lineno))
                          match_playtime = self.dbcur.fetchone()
                          LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)

                self.dbcon.commit()
           else:
                
                self.dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (original_title.replace("'","%27"),self.tmdb,self.season,self.episode,str(self.g_timer),str(self.g_item_total_time),' '))
                self.dbcon.commit()
                table_name='playback'
                if 0:#Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
                    try:
                        all_firebase=read_firebase(table_name)
                        write_fire=True
                        for items in all_firebase:
                      
                            if all_firebase[items]['original_title']==original_title:
                             if all_firebase[items]['season']==self.season:
                              if all_firebase[items]['episode']==self.episode:
                                # delete_firebase(table_name,items)
                                t = Thread(target=delete_firebase, args=(table_name,items,))
                                t.start()

                                break
                        if write_fire:
                            t = Thread(target=write_firebase, args=(original_title,self.tmdb,self.season,self.episode,str(self.g_timer),str(self.g_item_total_time),'',table_name,))
                            t.start()

                    except Exception as e:
                      import linecache,sys
                      exc_type, exc_obj, tb = sys.exc_info()
                      f = tb.tb_frame
                      lineno = tb.tb_lineno
                      log.warning('Error :'+ str(e) +',line no:'+str(lineno))
                      match_playtime = self.dbcur.fetchone()
                      LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)

        self.dbcur.close()
        self.dbcon.close()


    def onPlayBackStopped(self):
        global id,playing_file
        # log('(Tele Player) Stop playback')
        
        num=random.randint(0,60000)
        
        data={'type':'td_send',
             'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

        playing_file=False
    def download_buffer(self):
        
        try:

            buffer_size=long(Addon.getSetting("buffer_size_new4"))*1000000
            global id,playing_file
            dp = xbmcgui.DialogProgress()
            
            dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32044))
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'downloadFile','file_id':int(id), 'priority':2,'offset':(994694350-(993165312)),'limit':994694350, '@extra': num})
             }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            # j_enent_o=(event)
            once=True
            while True:
                data={'type':'listen',
                 'info':''
                 }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                if dp.iscanceled():
                    try:
                        self.path=event['file']['local']['path']
                    except: 
                        self.path=''
                        pass
                    break
                if self.stop==1:
                    break
                if event:
                    
                    if event.get('@type') =='error':
                        if Addon.getSetting("poptele")=='true':
                         xbmcgui.Dialog().ok('Error occurred',str(event.get('message')))
                        break

                    if 'updateFile' in event['@type']:
                        
                        dp.update(int((event['file']['local']['downloaded_prefix_size']*100.0)/buffer_size),'[B][COLOR=green]%s[/COLOR][/B]'%self.saved_name, '[B][COLOR=yellow]%s %s/%s[/COLOR][/B]'%(Addon.getLocalizedString(32045),str(event['file']['local']['downloaded_prefix_size']),str(buffer_size)))
                        if len(event['file']['local']['path'])>0 and event['file']['local']['downloaded_prefix_size']>(0x500):
                            size=event['file']['size']
                           
                            break
                xbmc.sleep(10)
            dp.close()
        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            if Addon.getSetting("poptele")=='true':
             xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
    def download_file(self):
        global stopnow,break_buffer
        global play_status
        
        # play_status='טוען באפר'
        try:

            buffer_size_d=int(Addon.getSetting("buffer_size_new4"))*1000000
            buffer_size=buffer_size_d
            global id,playing_file
            dp = xbmcgui.DialogProgress()

            if Addon.getSetting('new_play_window2')=='false' :#or kitana=='true':
                dp.create('AnonymousTv', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32044))
            num=random.randint(0,60000)
            start = time.time()
            data={'type':'td_send',
             'info':json.dumps({'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':0,'limit':0, '@extra': num})
             }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            do_buffer=True
            if 'expected_size' in event :
                if len(event['local']['path'])>0 and  (event['local']['is_downloading_completed']==True):
                    do_buffer=False
                    self.path='Done'
            if 'size' in event:
                if event['size']==0:
                    do_buffer=False
                    self.path='Stop'
            xx=0
            if do_buffer:
                if 'size' in event:
                
                    if buffer_size>=event['size']:
                            buffer_size=event['size']-1000
                            
                    # j_enent_o=(event)
                    
                    
                    
                    # j_enent_o=(event)
                    
                    while True:
                        data={'type':'get_file_size',
                         'info':id
                         }
                        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                        
                        if 'path' in event:
                            path=event['path']
                            file_size=event['file_size']
                            if Addon.getSetting('new_play_window2')=='true' :#or kitana=='true':and not kitana=='true':
                                if break_buffer:
                                    stopnow=True
                                    data={'type':'td_send',
                                         'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
                                         }
                                    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                                    try:
                                        self.path='Done'
                                    except: 
                                        self.path=''
                                        pass
                                    break
                            else:

                                if dp.iscanceled():
                                    stopnow=True

                                    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                                    data={'type':'td_send',
                                         'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
                                         }
                                    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                                    try:
                                        self.path='Done'
                                    except: 
                                        self.path=''
                                        pass
                                    break
                            if file_size!=0:
                                
                                    try:
                                      speed=int((file_size//(time.clock() - start)))
                                    except:
                                       speed=int((file_size//(time.time() - start)))
                                    t_remiain=(buffer_size_d-file_size)/speed
                                    
                                    play_status='טוען באפר: '+str(int(((file_size* 100.0)/buffer_size)))+'%'
                                    if Addon.getSetting('new_play_window2')=='false' :#or kitana=='true':or kitana=='true':

                                            dp.update(int((file_size*100.0)/buffer_size),'[B][COLOR=green]%s[/COLOR][/B]'%self.saved_name+'\n'+ '[B][COLOR=yellow]%s %s/%s[/COLOR][/B]'%(Addon.getLocalizedString(32045),str(file_size),str(buffer_size))+'\n'+str(int(speed/(1024)))+' Kbps / '+str(int(t_remiain))+' sec')
                                    if len(path)>0 and int(file_size)>=buffer_size:
                                        self.path=path
                                        break
                    # xbmc.sleep(10)
                else:
                    self.path='Done'
                    if Addon.getSetting("poptele")=='true':
                     xbmcgui.Dialog().ok('Error occurred',str(event))
                data={'type':'kill_file_size',
                     'info':id
                     }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if Addon.getSetting('new_play_window2')=='false' :#or kitana=='true':or kitana=='true':
                dp.close()
            if stopnow is False:
               if Addon.getSetting('new_play_window2')=='false' :#or kitana=='true':or kitana=='true':
                    xbmc.executebuiltin('ActivateWindow(busydialognocancel)')

        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
            self.path='Done'
    def get_resume(self):

        global name,break_window,play_status,stopbuffer,original_title,stopnow
        play_status='בודק נקודת צפייה אחרונה'
        if original_title=='':
         original_title=name
        if stopnow is True:
             sys.exit()
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        self.dbcon = database.connect(cacheFile)
        self.dbcur = self.dbcon.cursor()
        self.dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        self.dbcon.commit()

        if len(str(self.tmdb))>2 and self.tmdb!='%20':
            self.dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(self.tmdb,str(self.season).replace('%20','0').replace(' ','0'),str(self.episode).replace('%20','0').replace(' ','0')))
            
        else:
            self.dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(self.saved_name.replace("'","%27"),str(self.season).replace('%20','0').replace(' ','0'),str(self.episode).replace('%20','0').replace(' ','0')))

        
        if 0:#Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_time")=='true' and len(Addon.getSetting("firebase"))>0:
            if Addon.getSetting('new_play_window2')=='false':
                xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
            try:
                all_db=read_firebase('playback')
                match=[]

                if str(self.season)!=None and str(self.season)!=' ' and str(self.season)!="%20" and str(self.season)!="0":
                    
                    if all_db =={}:
                      match_playtime=None
                    for itt in all_db:
                        if all_db[itt]['original_title']==original_title:
                         if all_db[itt]['season']==str(self.season):
                          if all_db[itt]['episode']==str(self.episode):
                            items=all_db[itt]
                            match.append((items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
                            break
                          else:
                           match_playtime=None
                         else:
                           match_playtime=None
                        else:
                           match_playtime=None
                else:
                    if all_db =={}:
                      match_playtime=None
                    for itt in all_db:
                        if all_db[itt]['original_title']==original_title:
                            items=all_db[itt]
                            match.append((items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
                            break
                        else:
                           match_playtime=None
                all_names={}
                count_m=0
                for name,tmdb,season,episode,playtime,totaltime,free in match:

                    all_names[name]=[]
                    all_names[name].append((name,tmdb,season,episode,str(playtime),str(totaltime),free))

                for items in all_names:
                  match_playtime=name,tmdb,season,episode,playtime,totaltime,free=all_names[items][0]
            except Exception as e:
              import linecache,sys
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              log.warning('Error :'+ str(e) +',line no:'+str(lineno))
              match_playtime = self.dbcur.fetchone()
              LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)

        else:
         match_playtime = self.dbcur.fetchone()

        if match_playtime!=None:
            name_r,timdb_r,season_r,episode_r,playtime,totaltime,free=match_playtime
            res={}
            res['wflag']=False
            res['resumetime']=playtime
            res['totaltime']=totaltime
        else:
            res=False
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
        set_runtime=0
        if res:
            if not res['wflag']:

                if res['resumetime']!=None:
                    choose_time=Addon.getLocalizedString(32042)+time.strftime("%H:%M:%S", time.gmtime(float(res['resumetime'])))
                    if float(res['resumetime'])>=(100*(float(res['totaltime']))):
                        selection=1
                        clicked=1
                    else:
                        if Addon.getSetting("new_time_window")=='true':
                            selection,clicked=selection_time_window(choose_time,iconimage,fanart,heb_name,(100*(float(res['resumetime'])/(float(res['totaltime'])+1))))

                        else:

                            selection,clicked=selection_time_menu('Menu',choose_time)
                    if clicked==0:
                        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                        break_window=True
                        stopbuffer=True
                        return -1
                        
                    if selection==-1:
                       stop_auto_play=1
                       
                       return 0
                    if selection==0:
                        
                        set_runtime=float(res['resumetime'])
                        set_total=res['totaltime']
                        
                        
                    elif selection==1:
                        
                        
                        set_runtime=0
                        set_total=res['totaltime']
        self.dbcur.close()
        self.dbcon.close()
        
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
        return set_runtime
    def playTeleFile(self, id_pre,data,name,no_subs,tmdb,season,episode,original_title,heb_name,description,iconimage,fan,resume,l_data,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='false',tvdb_id='',checks=''):
      global play_status

      broken_play=True
      fanart=fan

      num=random.randint(0,60000)
      global stopnow
      global stopbuffer
      global bot
      if stopnow is True:
         sys.exit()
      original_name_r=original_title

      try:
        self.tmdb=tmdb
        self.saved_name=name
        self.season=season
        self.episode=episode
        global id,playing_file,seek_time,break_window
        if Addon.getSetting('new_play_window2')=='false' :#or kitana=='true':or kitana=='true':
           xbmc.executebuiltin('ActivateWindow(busydialognocancel)')

        id=id_pre
        self.stop=0
        self.path=''
        o_name=name
        link=('http://127.0.0.1:%s/'%listen_port)+id
        if not tmdb=='0':
            if not resume:
                resume_time=self.get_resume()
            else:
                resume_time=resume
        else:
            resume_time=0
        if stopbuffer == True:
         sys.exit()
        if checks=='':
            try:
                ok=check_free_space(description,iconimage)
                
                if not ok:
                    if bot == True:
                        return broken_play,resume_time
                    else:
                        sys.exit() 
            except:pass
        # t = Thread(target=self.download_file, args=())
        # t.start()
        self.download_file()
        
        count_timeout=0
        # while self.path=='' :
            # xbmc.sleep(10)
            # count_timeout+=1
            # # if (count_timeout>1000):
            # if (count_timeout>10000):
                # break
        
        if self.path=='Stop':
            xbmcgui.Dialog().ok('Error occurred','קובץ לא תקין')
            return 'Not ok'
        langs='he'
        play_status='מתחיל ניגון'
        
        if kitana=='true':
            # break_window=True
            video_data={}
            listItem = xbmcgui.ListItem(name, path=link) 
            if season!=None and season!=' ' and season!="%20" and season!="0":
               video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
               video_data['mediatype']='tvshow'
               tv_movie='tv'
            else:
               video_data['mediatype']='movies'
               tv_movie='movie'

            video_data['title']=heb_name
            video_data['Writer']=tmdb
            video_data['season']=season
            video_data['episode']=episode
            video_data['plot']=plot
            video_data['year']=year
            video_data['premiered']=premiered
            video_data['imdb']=tmdb
            video_data['code']=tmdb
            video_data['Tagline']=tag_line
            video_data['imdbnumber']=tmdb
            video_data['imdb_id']=tmdb
            video_data['IMDBNumber']=tmdb
            video_data['rating']=rating
            video_data['genre']=genre
            video_data['OriginalTitle']=original_title
            if no_subs=='1':
                   video_data[u'mpaa']=str('heb')
                   
            if KODI_VERSION>19:
                info_tag = listItem.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
                if (tv_movie=='tv'):
                    info_tag.setTvShowTitle(meta_get(video_data,'TVshowtitle'))
                    try:
                        info_tag.setSeason(int(season))
                        info_tag.setEpisode(int(episode))
                    except:
                        pass
                info_tag.setPlot(meta_get(video_data,'plot'))
                try:
                    year_info=int(meta_get(video_data,'year'))
                    if (year_info>0):
                        info_tag.setYear(year_info)
                except:
                    pass
                try:
                    info_tag.setRating(float(meta_get(video_data,'rating')))
                except:
                    pass
                info_tag.setVotes(int(meta_get(video_data,'votes')))
                info_tag.setMpaa(meta_get(video_data,'mpaa'))
                info_tag.setDuration(int(meta_get(video_data,'duration')))
                info_tag.setCountries(meta_get(video_data,'country'))
                
                info_tag.setTrailer(meta_get(video_data,'trailer'))
                info_tag.setPremiered(meta_get(video_data,'premiered'))
                
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                
                info_tag.setUniqueIDs({'imdb': tmdb, 'tmdb':tmdb})
                info_tag.setIMDBNumber(tmdb)
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                info_tag.setOriginalTitle(original_title)
                info_tag.setTagLine(original_title)
            if KODI_VERSION<19:
                listItem.setInfo(type=types, infoLabels=video_data)
                listItem.setUniqueIDs({ 'imdb': tmdb, 'tmdb' : tmdb }, "imdb")
            
            all_logo,all_n_fan,all_banner,all_clear_art,r_logo,r_art=get_extra_art(tmdb,tv_movie,tvdb_id)
            listItem.setArt({'clearlogo':r_logo,'clearart':r_art,'icon': iconimage, 'thumb': fanart, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage})

        else:
            break_window=True
            listItem = xbmcgui.ListItem(name, path=link) 
            video_data={}
            if season!=None and season!=' ' and season!="%20" and season!="0":
               video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
               video_data['mediatype']='tvshow'
               
            else:
               video_data['mediatype']='movies'
            if season!=None and season!=' ' and season!="%20" and season!="0":
               tv_movie='tv'
               url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
            else:
               tv_movie='movie'
               
               url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')

            if tv_movie=='tv':
                url_media='https://api.themoviedb.org/3/%s/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&include_image_language=ru,null&append_to_response=images,external_ids'%(tv_movie,tmdb,lang)
                   
                html_media=requests.get(url_media).json()
                try:
                  tvdb_id=str(html_media['external_ids']['tvdb_id'])
                except:
                  tvdb_id=''

            if 'tt' not in tmdb:
                 try:
                    
                    imdb_id=requests.get(url2,timeout=10).json()['external_ids']['imdb_id']
                    
                 except Exception as e:
                    log.warning('IMDB err:'+str(e))
                    imdb_id=" "
            else:
             imdb_id=tmdb
            
            if 'Music File' in description:
                types='music'
                video_data['title']=name
            else:
                types='Video'
                try:
                    if '@' in name and '.' in name:
                        nm=name.split('.')
                        ind=0
                        for items in nm:
                            if '@' in items:
                                nm.pop(ind)
                            ind+=1
                        name='.'.join(nm)
                except:pass
                video_data['title']=heb_name.replace('.mkv','').replace('.avi','').replace('.mp4','').replace('גוזלן','').replace('.',' ').replace('_',' ').replace('WEB-DL','').replace('900p','').replace('360p','').replace('430p','').replace('570p','').replace('720p','').replace('900P','').replace('360P','').replace('570P','').replace('720P','').replace('1080P','').replace('נתי מדיה','').replace('לולו סרטים','').replace('CD1','').replace('CD2','').replace('CD3','').replace('WEBRip','').replace('HDTV','').replace('חננאל ס','').replace('מדיה VOD','').replace('TVRip','').replace('x264','').replace('x265','').replace('AAC','').replace('2CH','').replace('HebDub','').replace('HebSub','').replace('SMG','').replace('-','').replace('HAIMMedia','')
                video_data['Writer']=tmdb
                video_data['season']=season
                video_data['episode']=episode
                video_data['plot']=(xbmc.getInfoLabel("ListItem.Plot"))
                video_data['year']=data
                video_data['imdb']=imdb_id
                video_data['code']=imdb_id
                video_data['icon']=fanart
                video_data['Tagline']=self.saved_name
                video_data['imdbnumber']=imdb_id
                video_data['poster']=fanart
                video_data['imdb_id']=imdb_id
                video_data['IMDBNumber']=imdb_id
                video_data['rating']=xbmc.getInfoLabel ("ListItem.Rating")
                video_data['genre']=xbmc.getInfoLabel("ListItem.Genre ")
                video_data['OriginalTitle']=original_title

                if no_subs=='1' or is_hebrew(str(name)):
                      video_data[u'mpaa']=str('heb')

                if 'HebSub' in name:
                        video_data[u'mpaa']=('heb')
                        
                        
                if KODI_VERSION>19:
                    info_tag = listItem.getVideoInfoTag()
                    info_tag.setMediaType(meta_get(video_data,'mediatype'))
                    info_tag.setTitle(meta_get(video_data,'title'))
                    if (tv_movie=='tv'):
                        info_tag.setTvShowTitle(meta_get(video_data,'TVshowtitle'))
                        try:
                            info_tag.setSeason(int(season))
                            info_tag.setEpisode(int(episode))
                        except:
                            pass
                    info_tag.setPlot(meta_get(video_data,'plot'))
                    try:
                        year_info=int(meta_get(video_data,'year'))
                        if (year_info>0):
                            info_tag.setYear(year_info)
                    except:
                        pass
                    try:
                        info_tag.setRating(float(meta_get(video_data,'rating')))
                    except:
                        pass
                    info_tag.setVotes(int(meta_get(video_data,'votes')))
                    info_tag.setMpaa(meta_get(video_data,'mpaa'))
                    info_tag.setDuration(int(meta_get(video_data,'duration')))
                    info_tag.setCountries(meta_get(video_data,'country'))
                    
                    info_tag.setTrailer(meta_get(video_data,'trailer'))
                    info_tag.setPremiered(meta_get(video_data,'premiered'))
                    
                    info_tag.setStudios((meta_get(video_data,'studio') or '',))
                    
                    info_tag.setUniqueIDs({'imdb': imdb_id, 'tmdb':tmdb})
                    info_tag.setIMDBNumber(imdb_id)
                    info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                    info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                    info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                    info_tag.setOriginalTitle(original_title)
                    info_tag.setTagLine(original_title)
            try:
                s=int(season)
                tv_movie='tv'
                video_data['mediatype']='episode'
            except:
                tv_movie='movie'
                video_data['mediatype']='movie'
            if KODI_VERSION<19:
                listItem.setInfo(type=types, infoLabels=video_data)
                listItem.setUniqueIDs({ 'imdb': imdb_id, 'tmdb' : tmdb }, "imdb")
            all_logo,all_n_fan,all_banner,all_clear_art,r_logo,r_art=get_extra_art(tmdb,tv_movie,tvdb_id)
            listItem.setArt({'clearlogo':r_logo,'clearart':r_art,'icon': iconimage, 'thumb': fanart, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage})

            eng_name=''
            if 0:# Addon.getSetting("sync_mod")=='true' and tv_movie=='tv' and len(Addon.getSetting("firebase"))>0:

                table_name='trackt'
                t = Thread(target=write_trackt, args=(original_name_r,url,iconimage,fanart,description,year,original_name_r,season,episode,tmdb,heb_name,show_original_year,original_name_r,isr,tv_movie,table_name,))
                t.start()

            try:
                from sqlite3 import dbapi2 as database
            except:
                from pysqlite2 import dbapi2 as database
            cacheFile=os.path.join(user_dataDir,'database.db')
            dbcon = database.connect(cacheFile)
            dbcur = dbcon.cursor()
            if season!=None and season!=' ' and season!="%20":
               table_name='lastlinktv'
            else:
               table_name='lastlinkmovie'
            dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""tmdb TEXT);"%table_name)
            dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""tmdb TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')

            dbcon.commit()
            dbcur.execute("DELETE FROM %s"%table_name)
            match = dbcur.fetchone()
            if match==None:
                dbcur.execute("INSERT INTO %s Values ('f_name','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s');" %  (table_name,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '))
                dbcon.commit()
                try:
                    try:
                        desk=description.replace("'","%27")
                    except:
                        desk=''
                    dbcur.execute("UPDATE %s SET name='%s',url='%s',iconimage='%s',fanart='%s',description='%s',data='%s',season='%s',episode='%s',original_title='%s',saved_name='%s',heb_name='%s',show_original_year='%s',eng_name='%s',isr='%s',prev_name='%s',tmdb='%s' WHERE o_name = 'f_name'"%(table_name,original_title.replace("'","%27"),base64.b64encode(url.encode("utf-8")).decode("utf-8") ,iconimage,fanart,desk,str(show_original_year).replace("'","%27"),season,episode,original_title.replace("'","%27"),original_title.replace("'","%27"),original_title.replace("'","%27"),show_original_year,original_title.replace("'","%27").replace("'","%27"),'0',original_title.replace("'","%27"),tmdb))
                    dbcon.commit()

                    
                except Exception as e:
                    log.warning('Error in Saving Last:'+str(e))
                    pass
            
            if table_name=='lastlinktv':
                tv_movie='tv'
            else:
                tv_movie='movie'
            
            dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27"),tv_movie))
            match = dbcur.fetchone()
            dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27").replace(" ","%20"),tv_movie))
            match_space = dbcur.fetchone()
            
            if match==None and match_space!=None:
                cache.clear(['last_view'])
                dbcur.execute("UPDATE Lastepisode SET original_title='%s' WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27"),original_title.replace("'","%27").replace(" ","%20"),tv_movie))
                
                dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27"),tv_movie))
                match = dbcur.fetchone()
            try:
                if match==None:
                  cache.clear(['last_view'])
                  try:
                    dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (heb_name.replace("'","%27"),url,iconimage,fanart,description.replace("'","%27"),show_original_year,original_title.replace("'","%27"),season,episode,tmdb,original_title.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),'0',tv_movie))
                    
                  except:
                    try:
                        dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (heb_name.replace("'","%27"),url,iconimage,fanart,description.decode('utf-8').replace("'","%27"),show_original_year,original_title.replace("'","%27"),season,episode,tmdb,original_title.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),'0',tv_movie))

                    except:
                        dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (heb_name.replace("'","%27"),url,iconimage,fanart,' ',show_original_year,original_title.replace("'","%27"),season,episode,tmdb,original_title.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),'0',tv_movie))
                  dbcon.commit()
                 
                else:
                  dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s' and season='%s' and episode='%s'"%(original_title.replace("'","%27"),tv_movie,season,episode))

                  match = dbcur.fetchone()
                  
                  if match==None:
                    cache.clear(['last_view'])
                    dbcur.execute("UPDATE Lastepisode SET season='%s',episode='%s',image='%s',heb_name='%s' WHERE original_title = '%s' and type='%s'"%(season,episode,fanart,heb_name.replace("'","%27"),original_title.replace("'","%27"),tv_movie))
                    dbcon.commit()
            except: pass
            dbcur.close()
            dbcon.close()
            if (Addon.getSetting("auto_trk")=='true'):
                t = Thread(target=jump_seek, args=(original_title,tmdb,season,episode,tvdb_id,))
                t.start()

            if (Addon.getSetting("nextup_episode")=='true' and tv_movie=='tv' and nextup=='true') or (Addon.getSetting("nextup_movie")=='true' and tv_movie=='movie') :
                t = Thread(target=search_next, args=(dd,tv_movie,tmdb,heb_name,))
                t.start()

            if (Addon.getSetting("skip_intro")=='true' and tv_movie=='tv'):
                t = Thread(target=skip_intro, args=())
                t.start()
        
        broken_play=True
        resume_time=float(resume_time)
        dp = xbmcgui . DialogProgress ( )
        if watched_indicators=='1':

           listItem. setProperty('StartPercent', str(resume_time))
        if resume_time!=-1:
            if stopnow is True:
             sys.exit()
            # logging.warning('4343434343434343434'+str(link))
            # link=''
            
            self.play(link,listitem=listItem,windowed=False)
            # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', link)))
            
            dp.create(self.saved_name,Addon.getLocalizedString(32040))
            w_time=int(Addon.getSetting("wait_size"))
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            try_play=False
            for _ in range(w_time):
                play_status=Addon.getLocalizedString(32040)+' : '+str(int(_/10))
                # if Addon.getSetting('new_play_window2')=='false':
                # if kitana=='false':# ניסיוני - בודק אם לא קורס כאשר עוברים לפרק הבא בקיטנה
                # break_window=True
                
                dp.update(0,Addon.getLocalizedString(32040)+' : '+str(int(_/10)))
                if not self.isPlaying():
                    xbmc.executebuiltin('SendClick(11)')
                    time.sleep(2)
                    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                    # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous2', link)))
                    self.play(link,listitem=listItem,windowed=False)
                    try_play=True
                    # xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                    # broken_play=False

                    break
                if dp.iscanceled():
                    dp.close()
                    broken_play=False
                    break
                try:
                    vidtime = self.getTime()
                except:
                    vidtime=0
                    pass
                if self.isPlaying() and vidtime>0:
                    broken_play=False
                    
                    break

                time.sleep(0.100)

            if not broken_play:
                xbmc.executebuiltin('SendClick(11)')
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')

            self.path=''
            if resume_time>0:
                if watched_indicators=='0':

                    try:
                        self.seekTime(int(float(resume_time-2)))
                    except Exception as e:
                        log.warning('Seek Err:'+str(e))
                        pass
                        
            dp.close()
            break_window=True
            if not broken_play:
                 while(self.isPlaying()):
                     try:
                        vidtime = self.getTime()
                     except:
                        vidtime = 0
                     try:
                        self.g_timer=xbmc.Player().getTime()
                        self.g_item_total_time=xbmc.Player().getTotalTime()
                     except:
                        pass
                     time.sleep(0.1)
            else:
                data={'type':'stop_now',
                     'info':''
                     }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
        self.stop=1
        num=random.randint(0,60000)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        if resume_time!=-1 and kitana=='false':
            if not tmdb=='0':
                try:
                    self.update_db()
                except:
                    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]קובץ דאטה בשימוש[/COLOR]' % COLOR2)
        t = Thread(target=forward_messages, args=(l_data,))
        t.start()
        
        if broken_play==False or try_play==False:
            time.sleep(1)

            clear_files()

        playing_file=True
        # if kitana=='true':
            # broken_play=False
        return broken_play,resume_time
      except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))




def get_custom_params(item):
        param=[]
        item=item.split("?")
        if len(item)>=2:
          paramstring=item[1]
          
          if len(paramstring)>=2:
                params=item[1]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param  
def get_params():
        param=[]
        if len(sys.argv)>=2:
          paramstring=sys.argv[2]
          if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     

def download_photo(id,counter,f_name,mv_name):
   try:
    
    data={'type':'download_photo',
             'info':id
             }

    file=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    xbmc.sleep(100)
    if xbmcvfs.exists(file):
        try:
            shutil.move(file,mv_name)
        except Exception as e:
            logging.warning('File copy err:'+str(e))
            pass
        
    else :
        return 'None'
    
    return mv_name
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Photo:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia ERR','Err:'+str(e)+'Line:'+str(lineno)))

        return ''
def infiniteReceiver(all_d,last_id,archive='chatListMain',chat_filter_id='0',next_page='0'):
   global exit_now
   anonymous = xbmcaddon.Addon('plugin.program.Anonymous')
   dragon=anonymous.getSetting('dragon')
   try:

    dp = xbmcgui . DialogProgress ( )

    dp.create('קבוצות שלי')
    dp.update(0, 'נכנס לקבוצות...')
    num=random.randint(0,60000)
    order=last_id.split('$$$')[1]
    leid=last_id.split('$$$')[0]
    
    if chat_filter_id=='0':
        data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':leid,'offset_order':order, 'limit': '15000','chat_list':{'@type': archive}, '@extra': num})
             }
    else:
        data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':leid,'offset_order':order, 'limit': '15000','chat_list':{'@type': 'chatListFilter','chat_filter_id':int(chat_filter_id)}, '@extra': num})
             }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    # xbmc.sleep(1000)
    # event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    exit_now=0
   
    if 'status' in event:
        xbmcgui.Dialog().ok('Error occurred',event['status'])
        exit_now=1
    if exit_now==0:
       

        
        
        counter=0
        counter_ph=10000
    
        j_enent_o=(event)
        zzz=0
        items=''
        next_page=int(next_page)
        start_value=next_page*200
        if event.get('@type') =='error':
            logging.warning('start_value:  '+str(j_enent_o))
            return 
        # logging.warning('start_value:  '+str(j_enent_o))
        # log.warning('start_value:'+str(start_value))
        next_page_exist=False
        len_size=len(j_enent_o['chat_ids'])
        if len_size>200:
            len_size=200
        for items in j_enent_o['chat_ids']:
            # log.warning('counter:'+str(counter))
            counter+=1
            if (counter<start_value):
                continue
               
            if (counter>(start_value+200)):
                next_page_exist=True
                break
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':counter})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
          
            if 'status' in event:
                xbmcgui.Dialog().ok('Error occurred',event['status'])
                exit_now=1
                break
            # log.warning(json.dumps(event))
            order=''
            try:
                order=event['positions'][0]['order']
            except:
                pass
            
            if dp.iscanceled():
                          dp.close()
                         
                          break
            j_enent=(event)

            dp.update(int(((zzz* 100.0)/(len_size)) ), 'נכנס לקבוצות...'+'\n'+ j_enent['@type'] )
            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
                icon_id=''
                fan_id=''
                icon='special://home/addons/plugin.video.telemedia/tele/icon.jpg'
                fanart='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                name=j_enent['title']
                # log.warning(name+':'+str(items))
                
                color='white'
                if 'is_channel' in j_enent['type']:
                    if j_enent['type']['is_channel']==False:
                        
                        genere='Chat'
                        color='white'
                    else:
                        genere='Channel'
                        color='white'
                else:
                     genere=j_enent['type']['@type']
                     color='white'
                if 'last_message' in j_enent:
                    plot=name
                    pre=j_enent['last_message']['content']
               
                    if 'caption' in pre:
                        plot=j_enent['last_message']['content']['caption']['text']
                    elif 'text' in pre:
                        if 'text' in pre['text']:
                            plot=j_enent['last_message']['content']['text']['text']
                    
                        
                else:
                    plot=name
                dp.update(int(((zzz* 100.0)/(len_size)) ), 'נכנס לקבוצות...'+'\n'+ name)
                zzz+=1
                name=name.replace('סדרות מהלב','').replace('@ dragon','@dragon')
                if '@dragon' in name and dragon =='true':
                    if 'photo' in j_enent:
                       
                       if 'small' in j_enent['photo']:
                         counter_ph+=1
                         icon_id=j_enent['photo']['small']['id']
                         f_name=str(j_enent['id'])+'_small.jpg'
                         mv_name=os.path.join(logo_path,f_name)
                         if os.path.exists(mv_name):
                            icon=mv_name
                         else:
                            icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                       if 'big' in j_enent['photo']:
                         counter_ph+=1
                         fan_id=j_enent['photo']['big']['id']
                         f_name=str(j_enent['id'])+'_big.jpg'
                         mv_name=os.path.join(logo_path,f_name)
                         if os.path.exists(mv_name):
                            fanart=mv_name
                         else:
                            fanart=download_photo(fan_id,counter_ph,f_name,mv_name)
                mode=2
                last_id_fixed='0$$$0$$$0$$$0'
                
                if 'group links' in name.lower() or 'ערוץ קישורים' in name or 'קישורים לכל הקבוצות' in name:
                    mode=38
                    color='olive'
                    last_id_fixed='0'
                #log.warning(name)
                #log.warning(j_enent_o['chat_ids'])


                if '@dragon' in name and not dragon =='true':
                 continue
                aa=addDir3('[COLOR %s]'%color+name.replace('@dragon','')+'[/COLOR]',str(items),mode,icon,fanart,plot+'\nfrom_plot',generes=genere,data='0',last_id=last_id_fixed,image_master=icon+'$$$'+fanart,menu_leave=True,original_title=name)
                all_d.append(aa)
            
            
    if items!='' and next_page_exist:
        last_id=str(items)+'$$$'+str(order)
        # log.warning('last_id:'+str(last_id))
        aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32026)+'[/COLOR]',archive,12,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','Next',data='all',last_id=last_id,next_page=str(int(next_page+1)))
        all_d.append(aa)
    
    dp.close()
    return all_d
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Main:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
exec(codecs.decode(base64.b64decode(r'aW1wb3J0IG9zCmlmIG5vdCBvcy5wYXRoLmV4aXN0cyh4Ym1jdmZzLnRyYW5zbGF0ZVBhdGgoInNwZWNpYWw6Ly9ob21lL2FkZG9ucy8iKSArICdwbHVnaW4ucHJvZ3JhbS5Bbm9ueW1vdXMnKSBvciBub3Qgb3MucGF0aC5leGlzdHMoeGJtY3Zmcy50cmFuc2xhdGVQYXRoKCJzcGVjaWFsOi8vaG9tZS9hZGRvbnMvIikgKyAncmVwb3NpdG9yeS5nYWlhLjInKSBvciBub3Qgb3MucGF0aC5leGlzdHMoeGJtY3Zmcy50cmFuc2xhdGVQYXRoKCJzcGVjaWFsOi8vaG9tZS9hZGRvbnMvIikgKyAnc2tpbi5QcmVtaXVtLm1vZCcpOgogICAgc3lzLmV4aXQoKQ==')))
def my_groups(last_id,url,groups_id,next_page):
    log.warning('Start Main')
    try:
        all_d=[]
        if groups_id=='11':
            aa=addDir3('סדרות בטורקית - TMDB','https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,'tr'),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32046))

        else:
            aa=addDir3('חיפוש',str(id),167,'special://home/addons/plugin.video.telemedia/tele/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Search All',last_id='0$$$0',data='all')
        all_d.append(aa)
        all_d=infiniteReceiver(all_d,last_id,archive=url,chat_filter_id=groups_id,next_page=next_page)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Main:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))

def login_ktuvit():
    
    headers = {
    'authority': 'www.ktuvit.me',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://www.ktuvit.me',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    
    'accept-language': 'en-US,en;q=0.9',
    
    }

    data = '{"request":{"Email":"hatzel6969@gmail.com","Password":"Jw1n9nPOZRAHw9aVdarvjMph2L85pKGx79oAAFTCsaE="}}'

    login_cook = requests.get('https://www.ktuvit.me/Services/MembershipService.svc/Login', headers=headers, data=data).cookies
    login_cook_fix={}
    for cookie in login_cook:

            login_cook_fix[cookie.name]=cookie.value
    return login_cook_fix

def last_tv_subs(url):

    all_d=[]
    cookies_login=cache.get(login_ktuvit,1, table='subs')
    
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    x=requests.get(url,headers=headers,cookies=cookies_login).content.decode('utf-8')

    regex='<div class="col-md-12">(.+?)</span>'
    match=re.compile(regex,re.DOTALL).findall(x)

    for items in match:
        regex='<img src="(.+?)".+?<h3>(.+?)\((.+?)\)</h3>.+?<h4>עונה (.+?) פרק (.+?)</h4>.+?data-elipsis-hidden="true">(.+?)<.+?data-title="(.+?)"'
        m2=re.compile(regex,re.DOTALL).findall(items)
        if len(m2)>0:
            icon='https://www.ktuvit.me'+m2[0][0]
            image=icon
            new_name=m2[0][1]
            original_title=m2[0][2]
            season=m2[0][3]
            episode=m2[0][4]
            plot=m2[0][5]
            id=m2[0][6]

            aa=addDir3('[COLOR yellow] עונה %s פרק %s '%(season,episode)+'[/COLOR]'+new_name, url,20, icon,image,plot,original_title=original_title,season=season,episode=episode,data=year,eng_name=original_title,heb_name=new_name,id=id)
            all_d.append(aa)
    regex='<li ><a href="(.+?)">הבא</a></li>'
    m3=re.compile(regex).findall(x)
    if len(m3)>0:
        aa=addDir3( '[COLOR yellow][I]הדף הבא[/I][/COLOR]', 'https://www.ktuvit.me'+m3[0],119, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','הדף הבא')
        all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def res_q(quality):
    fk=Addon.getSetting("4K")
    fp=Addon.getSetting("1080p")
    fh=Addon.getSetting("720p")
    fm=Addon.getSetting("480p")
    fz=Addon.getSetting("360p")
    fx=Addon.getSetting("240p")
    f_q=' '
    if '4k' in quality.lower():
        quality='2160'
    if '2160' in quality and fk=='true' and Addon.getSetting("netflix_mod")=='false':
      f_q='2160'
    elif '1080' in quality and fp=='true':
      f_q='1080'
    elif '720' in quality and fh=='true':
      f_q='720'
    elif '480' in quality and fm=='true':
      f_q='480'
    
    elif '360' in quality and fz=='true' or 'sd' in quality.lower() and fz=='true':
      f_q='360'
    elif '240' in quality and fx=='true':
      f_q='240'
    elif 'hd' in quality.lower() and fh=='true' or 'hq' in quality.lower() and fh=='true':
      f_q='720'
    elif '' in quality.lower() and fh=='true' or 'hq' in quality.lower() and fh=='true':
      f_q='unk'
    return f_q
    
def fix_q_links(quality):
    f_q=100
    if '4k' in quality.lower():
        quality='2160'
    if '2160' in quality:
      f_q=1
    elif '1080' in quality:
      f_q=2
    elif '720' in quality:
      f_q=3
    elif '480' in quality:
      f_q=4
    
    elif '360' in quality or 'sd' in quality.lower():
      f_q=5
    elif '240' in quality:
      f_q=6
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q=3
    return f_q
def get_q(name):
    q=res_q(name)
    loc=fix_q_links(q)
    '''
    log.warning('Q test:'+name)
    log.warning('Q s:'+q)
    log.warning('Q loc:'+str(loc))
    '''
    return q,loc
def searchtmdb(tmdb,type,last_id_pre,search_entered_pre,icon_pre,fan_pre,season,episode,no_subs=0,original_title='',heb_name='',dont_return=True,manual=True):
    

    last_id=last_id_pre.split('$$$')[0]
    last_id_msg=last_id_pre.split('$$$')[1]
   
    query=search_entered_pre
    query=query.replace('%20',' ').replace('%27',"'").replace('%3a',":")

    num=random.randint(1,1001)
    all_links=[]
    filter_size=int(Addon.getSetting("filter_size"))*1024*1024
    # from  resources.modules.client import  get_html
    
    if type=='all' and os.path.exists(os.path.join(xbmc_tranlate_path("special://userdata"),"addon_data", "plugin.video.telemedia/database","td.binlog")):
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchMessages', 'query': query,'offset_message_id':last_id,'offset_chat_id':last_id_msg,'limit':100, '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        
        counter_ph=0
        for items in event['messages']:  
            #log.warning(items)
            
            if 'document' in items['content']:
                name=items['content']['document']['file_name']
                if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name and '.wmv' not in name:
                    continue
                size=items['content']['document']['document']['size']
                if size<filter_size:
                    continue
                f_size2=''

                f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                q,loc=get_q(name)
                link_data={}
                link_data['id']=str(items['content']['document']['document']['id'])
                link_data['m_id']=items['id']
                link_data['c_id']=items['chat_id']
                f_lk=json.dumps(link_data)
                all_links.append((name, f_lk,3,q,loc, icon_pre,fan_pre,f_size2,no_subs,tmdb,season,episode,original_title))

            if 'video' in items['content']:
                    name=items['content']['video']['file_name']
                    
                    size=items['content']['video']['video']['size']
                    if size<filter_size:
                        continue

                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    q,loc=get_q(name)
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    all_links.append(( name, f_lk,3,q,loc, icon_pre,fan_pre,f_size2,no_subs,tmdb,season,episode,original_title))
            if 'caption' in items['content']:
                    txt_lines=items['content']['caption']['text'].split('\n')
                    all_l=[]
                    name=txt_lines[0]
                    rem_lines=[]
                    for lines in txt_lines:
                        if 'upfile' not in lines and 'drive.google' not in lines:
                          rem_lines.append(lines)
                          continue
                        
                            
                        all_l.append(lines)
                    if len(all_l)==0:
                        continue
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']['caption']:
                        counter_ph+=1
                        icon_id=items['content']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=''
                        counter_ph+=1
                        loc=items['content']['photo']['sizes']
                        icon_id=items['content']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=''
                    q,loc=get_q(txt_lines[0])
                    all_links.append(('[COLOR lightgreen]'+ txt_lines[0]+' מקור גוגל'+'[/COLOR]' , '$$$'.join(all_l),9,q,loc, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),no_subs,tmdb,season,episode,original_title))

            elif 'web_page' in items['content']:
                name=items['content']['web_page']['title']
                link=items['content']['web_page']['url']
                try:
                 plot=items['content']['web_page']['description']['text']
                except: plot=''
                if 'upfile' not in link and 'drive.google' not in link:
                      
                      continue
                icon=icon_pre
                fan=fan_pre
                if 'photo' in items['content']['web_page']:
                    counter_ph+=1
                    icon_id=items['content']['web_page']['photo']['sizes'][0]['photo']['id']
                    f_name=items['content']['web_page']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                    mv_name=os.path.join(icons_path,f_name)
                    if os.path.exists(mv_name):
                        icon=mv_name
                    else:
                       icon=''
                    counter_ph+=1
                    loc=items['content']['web_page']['photo']['sizes']
                    icon_id=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['id']
                    f_name=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                    mv_name=os.path.join(fan_path,f_name)
                    if os.path.exists(mv_name):
                        fan=mv_name
                    else:

                       fan=''
                q,loc=get_q(name)
                all_links.append(('[COLOR lightgreen]'+ name+'  מקור גוגל '+'[/COLOR]', link,9,q,loc, icon,fan,plot.replace('\n\n','\n'),no_subs,tmdb,season,episode,original_title))
            f_id=items['chat_id']

    if dont_return:
        all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
        filter_dup=Addon.getSetting("dup_links")=='true'
        all_t_links=[]
        for  name, link,mode,q,loc, icon,fan,plot,no_subs,tmdb,season,episode,original_title in all_links:
            
            if name not in all_t_links or filter_dup==False:
            
           
                all_t_links.append(name)
                addLink( name, link,mode,False, icon,fan,plot,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
        try:
            last_id=str(items['id'])+'$$$'+str(f_id)
            
        except:
            #xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', 'No result for:'+query))
            pass
    return all_links

def write_search(query,free,table_name):

            all_firebase=read_firebase(table_name)
            write_fire=True
            for items in all_firebase:
                if all_firebase[items]['name']==query:
                    delete_firebase(table_name,items)
                    break
            if write_fire:
                write_firebase_search(query,free,table_name)
def add_remove_trakt(name,original_title,id,season,episode,o_name):
    
    from resources.modules.general import post_trakt
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
        
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    
    if season=='%20' or season=='':
        season='0'
    if episode=='%20' or episode=='':
        episode='0'
    
    if original_title=='add':
        if name=='tv':
           
           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           
           i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
        else:
          
           i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))
    elif original_title=='remove':
        if name=='tv':
           
           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           
           i = (post_trakt('/sync/history/remove', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
           from resources.modules.general import call_trakt
           result=call_trakt('sync/playback/episodes')

           f_id=None
           for items in result:
                t_id=str(items['show']['ids']['tmdb'])
                season_t=str(items['episode']['season'])
                episode_t=str(items['episode']['number'])
                t_id=str(items['show']['ids']['tmdb'])
                # if t_id=='60735':

                    # log.warning(episode)
                if str(id)==t_id and str(season_t)==season and str(episode_t)==episode:
                    f_id=str(items['id'])
                    break
           if f_id:
            j=call_trakt('sync/playback/'+f_id, is_delete=True)
           dbcur.execute("DELETE FROM playback where tmdb='%s' and season='%s' and episode='%s';"%(id,season,episode))
        else:
         
           i = (post_trakt('/sync/history/remove',data= {"movies": [{"ids": {"tmdb": id}}]}))
           from resources.modules.general import call_trakt
           result=call_trakt('sync/playback/movies')
           f_id=None
           for items in result:
                t_id=str(items['movie']['ids']['tmdb'])   
                if str(id)==t_id:
                    f_id=str(items['id'])
                    break
           if f_id:
            j=call_trakt('sync/playback/'+f_id, is_delete=True)
            #log.warning(j)
           dbcur.execute("DELETE FROM playback where tmdb='%s'"%(id))
    if 'added' in i:
       xbmc.executebuiltin((u'Notification(%s,%s)' % (o_name, 'סמן כנצפה')))
    elif 'deleted' in i:
       xbmc.executebuiltin((u'Notification(%s,%s)' % (o_name, 'נצפה הוסר')))
    else:
      xbmc.executebuiltin((u'Notification(%s,%s)' % (o_name, 'Error'.encode('utf-8'))))
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    ClearCache()
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    xbmc.executebuiltin('Container.Refresh')
def GetModuleName(module, mode, moreData, catName=''):
    import resources.modules.common as common
    mode = str(mode)
    
    moduleName = ''
    if module == 'kan': 		moduleName = common.GetLocaleString(30400) if catName == '' else catName
    elif module == 'keshet': 	moduleName = common.GetLocaleString(30603)
    elif module == 'reshet': 	moduleName = common.GetLocaleString(30604)
    elif module == '14tv': 	moduleName = common.GetLocaleString(30606)
    elif module == '9tv': 		moduleName = common.GetLocaleString(30630)
    elif module == '891fm': 	moduleName = common.GetLocaleString(30734)
    elif module == 'sport5': 	moduleName = common.GetLocaleString(30632)
    elif module == 'sport1': 	moduleName = common.GetLocaleString(31000)
    elif module == '99fm': 	moduleName = common.GetLocaleString(30704)
    elif module == 'glz': 	moduleName = common.GetLocaleString(30702)
    elif module == '100fm': 	moduleName = common.GetLocaleString(30726)
    return moduleName
    
    
def search_tmdb(search_entered_pre):
    from resources.modules.tmdb_cobra import get_movies
    query=search_entered_pre
    query=query.replace('%20',' ').replace('%27',"'").replace('%3a',":")
    addNolink( '[COLOR red][I]--- סרטים ---[/I][/COLOR]', id,27,False,fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png', iconimage='special://home/addons/plugin.video.telemedia/tele/cobra_icon2.png',plot=' ')
    get_movies('http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query={0}&language={1}&append_to_response=origin_country&page=1'.format(que(query),lang),global_s=True)

    addNolink( '[COLOR red][I]--- סדרות ---[/I][/COLOR]', id,27,False,fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png', iconimage='special://home/addons/plugin.video.telemedia/tele/cobra_icon2.png',plot=' ')
    get_movies('http://api.themoviedb.org/3/search/tv?api_key=34142515d9d23817496eeb4ff1d223d0&query={0}&language={1}&page=1'.format(que(query),lang),global_s=True)
def search_idanplus(search_entered_pre,dp):
    query=search_entered_pre
    query=query.replace('%20',' ').replace('%27',"'").replace('%3a',":")
    addNolink( '[COLOR red][I]--- עידן פלוס ---[/I][/COLOR]', id,27,False,fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png', iconimage='special://home/addons/plugin.video.telemedia/tele/idanplus.png',plot=' ')
    import resources.modules.common as common
    series = common.GetUpdatedList(common.seriesFile, common.seriesUrl, isZip=True, sort=True)
    filteredSeries = []
    seriesLinks = []
    searchText = query
    if searchText != '':
        for serie in series:
            if serie['name'].lower().startswith(searchText):
                filteredSeries.append(serie)
                seriesLinks.append(serie['name'])
        for serie in series:
            if searchText in serie['name'].lower() and serie['name'] not in seriesLinks:
                filteredSeries.append(serie)
                seriesLinks.append(serie['name'])
    programNameFormat = int(common.GetAddonSetting("programNameFormat"))
    for serie in filteredSeries:
        serieMoreData = serie.get('moreData', '')
        serieCatName = serie.get('catName', '')
        serieName = serie['name']
        dp.update(20, serieName)
        moduleName = GetModuleName(serie['module'], serie['mode'], serieMoreData, serieCatName)
        name = common.getDisplayName(serieName, moduleName, programNameFormat, bold=True)
        infos = {"Title": name, "Plot": serie['desc']}
        isFolder = False if serieMoreData == 'youtube' else True
        common.addDir(name, serie['url'], serie['mode'], common.encode(serie['icon'], 'utf-8'), infos, module=serie['module'], moreData=common.encode(serieMoreData, 'utf-8'), totalItems=len(filteredSeries), isFolder=isFolder, urlParamsData={'name': common.GetLabelColor(serieName, keyColor="prColor", bold=True)})
def search_person(search_entered_pre,dp):
    all_d=[]

    link='https://api.themoviedb.org/3/search/person?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&page=1&include_adult=false'%search_entered_pre
    
    headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
    html=requests.get(link,headers=headers).json()
    for items in html['results']:
        icon=items['profile_path']
        if len (items['known_for'])==0:
            
            continue
        if 'backdrop_path' in items['known_for'][0]:
            fanart=items['known_for'][0]['backdrop_path']
        else:
            fanart=' '
        if icon==None:
          icon=' '
        else:
          icon=domain_s+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart=domain_s+'image.tmdb.org/t/p/original/'+fanart
        dp.update(40, items['name'])
        aa=addDir3(items['name'],str(items['id']),272,icon,fanart,items['name'])
        all_d.append(aa)
    if len(all_d)>0:
        addNolink( '[COLOR red][I]--- שחקנים ---[/I][/COLOR]', id,27,False,fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png', iconimage='special://home/addons/plugin.video.telemedia/tele/cobra_icon2.png',plot=' ')
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))




def search_medovavim(search_entered_pre,dp):
    query=search_entered_pre
    query=query.replace('%20',' ').replace('%27',"'").replace('%3a',":")
    dataDir_medovavim =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube.db')
    medovavim_dbcon = database.connect(dataDir_medovavim)
    medovavim_dbcur = medovavim_dbcon.cursor()
    medovavim_dbcur.execute("SELECT * FROM kids_movie_ordered where name like '%{0}%'".format(query))

    match2 = medovavim_dbcur.fetchall()
    
    all_w={}
    x=0
    all_l=[]

    for name ,link,icon, image,plot,data,tmdbid ,date_added in match2:
        
        all_l.append(addLink_db(name,link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
        x+=1
        dp.update(0, name)
    if len(all_l)>0:
        
        addNolink( '[COLOR red][I]%s[/I][/COLOR]'%'--- סרטים מדובבים ---', 'www',99,False,iconimage='special://home/addons/plugin.video.telemedia/tele/kidsdub.png',fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png')
    xbmcplugin.addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))
    medovavim_dbcur.close()
    medovavim_dbcon.close()
def search_chats(search_entered_pre,dp):
    num=random.randint(0,60000)
    try:
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChats', 'query': query,'limit':1000, '@extra': num})
             }
             
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        counter=0
        zzz=0

        for items in event['chat_ids']:
            
            data={'type':'td_send',
                     'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':num})
                     }
            event_in=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            j_enent=(event_in)
            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
                icon_id=''
                fan_id=''
                name=j_enent['title']
                color='white'
                if 'is_channel' in j_enent['type']:
                    if j_enent['type']['is_channel']==False:
                        
                        genere='Chat'
                        # color='lightblue'
                    else:
                        genere='Channel'
                        # color='khaki'
                else:
                     genere=j_enent['type']['@type']
                     # color='lightgreen'
                if 'last_message' in j_enent:
                    plot=name
                    pre=j_enent['last_message']['content']
               
                    if 'caption' in pre:
                        plot=j_enent['last_message']['content']['caption']['text']
                    elif 'text' in pre:
                        if 'text' in pre['text']:
                            plot=j_enent['last_message']['content']['text']['text']
                else:
                    plot=name
                zzz+=1
                icon='special://home/addons/plugin.video.telemedia/tele/files2.png'
                fanart='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                aa=addDir3('[COLOR %s]'%color+name+'[/COLOR]',str(items),2,icon,fanart,plot+'\nfrom_plot',generes=genere,data='0',last_id='0$$$0$$$0$$$0',image_master=icon+'$$$'+fanart,join_menu=True)
                all_d2.append(aa)
                dp.update(50, name)
            counter+=1
        
        if len(all_d2)>0:
             
            addNolink( '[COLOR red][I]%s[/I][/COLOR]'%'--- תוצאות מקבוצות שלי ---', 'www',99,False,iconimage='special://home/addons/plugin.video.telemedia/tele/telemedia2.png',fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png')
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d2,len(all_d2))
    except:pass
def search_public_chats(search_entered_pre,dp):
    all_d=[]
    num=random.randint(0,60000)
    query=search_entered_pre
    query=query.replace('עונה ','ע').replace('פרק ','פ')
    data={'type':'td_send',
         'info':json.dumps({'@type': 'searchPublicChats', 'query': query, '@extra': num})
         }
         
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

    counter=0
    counter_ph=10000
    zzz=0
    for items in event['chat_ids']:
        data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':num})
                 }
        event_in=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        j_enent=(event_in)
        if j_enent['@type']=='chat' and len(j_enent['title'])>1:
            name=j_enent['title']
        
            color='white'
            if 'is_channel' in j_enent['type']:
                if j_enent['type']['is_channel']==False:
                    
                    genere='Chat'
                else:
                    genere='Channel'
            else:
                 genere=j_enent['type']['@type']
            if 'last_message' in j_enent:
                plot=name
                pre=j_enent['last_message']['content']
           
                if 'caption' in pre:
                    plot=j_enent['last_message']['content']['caption']['text']
                elif 'text' in pre:
                    if 'text' in pre['text']:
                        plot=j_enent['last_message']['content']['text']['text']
                
                    
            else:
                plot=name

            zzz+=1
            icon='special://home/addons/plugin.video.telemedia/tele/files2.png'
            fanart='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
            aa=addDir3('[COLOR %s]'%color+name+'[/COLOR]',str(items),2,icon,fanart,plot+'\nfrom_plot',generes=genere,data='0',last_id='0$$$0$$$0$$$0',image_master=icon+'$$$'+fanart,join_menu=True)
            all_d.append(aa)
            dp.update(60, name)
        counter+=1
    
    if len(all_d)>0:
         
        addNolink( '[COLOR red][I]%s[/I][/COLOR]'%'--- תוצאות מקבוצות בטלגרם ---', 'www',99,False,iconimage='special://home/addons/plugin.video.telemedia/tele/telemedia2.png',fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png')
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def search_tele_allfiles(last_id_pre,tmdb,search_entered_pre,icon_pre,fan_pre,season,episode,dp,no_subs=0,original_title=''):
    query=search_entered_pre
    query=query.replace('עונה ','ע').replace('פרק ','פ')
    last_id=last_id_pre.split('$$$')[0]
    last_id_msg=last_id_pre.split('$$$')[1]
    all_links=[]
    num=random.randint(0,60000)
    filter_size=int(Addon.getSetting("filter_size"))*1024*1024
    # try:
    data={'type':'td_send',
         'info':json.dumps({'@type': 'searchMessages', 'query': query,'offset_message_id':last_id,'offset_chat_id':last_id_msg,'limit':1000, '@extra': num})
         }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    counter_ph=0
    for items in event['messages']:  
        if 'document' in items['content']:
            name=items['content']['document']['file_name']
            if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name and '.wmv' not in name:
                continue
            size=items['content']['document']['document']['size']
            if size<filter_size:
                continue
            f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
            q,loc=get_q(name)
            link_data={}
            link_data['id']=str(items['content']['document']['document']['id'])
            link_data['m_id']=items['id']
            link_data['c_id']=items['chat_id']
            f_lk=json.dumps(link_data)
            all_links.append((name, f_lk,3,q,loc, icon_pre,fan_pre,f_size2,no_subs,tmdb,season,episode,name))
            dp.update(70, name)
        if 'video' in items['content']:
                name=items['content']['video']['file_name']
                size=items['content']['video']['video']['size']
                if size<filter_size:
                    continue
                f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                q,loc=get_q(name)
                link_data={}
                link_data['id']=str(items['content']['video']['video']['id'])
                link_data['m_id']=items['id']
                link_data['c_id']=items['chat_id']
                f_lk=json.dumps(link_data)
                all_links.append(( name, f_lk,3,q,loc, icon_pre,fan_pre,f_size2,no_subs,tmdb,season,episode,name))
                dp.update(80, name)
        if 'caption' in items['content']:
                txt_lines=items['content']['caption']['text'].split('\n')
                all_l=[]
                name=txt_lines[0]
                rem_lines=[]
                for lines in txt_lines:
                    if 'upfile' not in lines and 'drive.google' not in lines:
                      rem_lines.append(lines)
                      continue
                    all_l.append(lines)
                if len(all_l)==0:
                    continue

                icon='special://home/addons/plugin.video.telemedia/tele/Play4.png'
                fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                q,loc=get_q(txt_lines[0])
                all_links.append(('[COLOR lightgreen]'+ txt_lines[0]+'[/COLOR]' , '$$$'.join(all_l),9,q,loc, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),no_subs,tmdb,season,episode,original_title))
                dp.update(90, name)
        elif 'web_page' in items['content']:
            name=items['content']['web_page']['title']
            link=items['content']['web_page']['url']
            try:
             plot=items['content']['web_page']['description']['text']
            except: plot=''
            if 'upfile' not in link and 'drive.google' not in link:
                  
                  continue


            icon='special://home/addons/plugin.video.telemedia/tele/Play4.png'
            fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
            q,loc=get_q(name)
            all_links.append(('[COLOR lightgreen]'+ name+'[/COLOR]', link,9,q,loc, icon,fan,plot.replace('\n\n','\n'),no_subs,tmdb,season,episode,name))
            dp.update(100, name)
        f_id=items['chat_id']
    all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
    all_t_links=[]

    if len(all_links)>0:
        addNolink( '[COLOR red][I]%s[/I][/COLOR]'%'--- תוצאות אחרונות ---', 'www',99,False,iconimage='special://home/addons/plugin.video.telemedia/tele/telemedia2.png',fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png')
    for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in all_links:
        if name not in all_t_links :
            all_t_links.append(name)
            addLink( clean_name_search(name), link,mode,False, icon,fan,f_size2,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
    # except:pass
    
def sdr_search_all(keyword,cookies={},page='0',get_all=False):
    BASE_URL='https://www.sdarot.tw'
    headers = {
        'authority': BASE_URL.replace('https://',''),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'referer': BASE_URL,
        'Host': BASE_URL.replace('https://',''),
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    Addon = xbmcaddon.Addon()
    params = {
        'srl': '1',
    }
    max_per_page=int(Addon.getSetting('num_p'))
    response = requests.get(BASE_URL+'/ajax/index', params=params, cookies=cookies, headers=headers,verify=False).json()
    all_data_pre=[]
    all_data=[]
    start_pos=int(page)*max_per_page
    end_pos=start_pos+max_per_page
    count=0
    for item in response:
        
            if keyword in item['heb'] or keyword in item['eng'] or get_all:
                all_data_pre.append((item['heb'],item['eng'],item['id'],'https://static.sdarot.tw/series/'+item['poster'],'/watch/'+item['id']))
    all_data_pre=sorted(all_data_pre, key=lambda x: x[0], reverse=False)
    for name,eng_name,sid,img,link in all_data_pre:
        if count>=start_pos and count<end_pos:
            all_data.append({'name':name,'eng_name':eng_name,'sid':sid,'img':img,'link':link})
        count+=1
    return all_data,len(response)
def search_sdarot_tv(search_entered,page):
    Addon = xbmcaddon.Addon()

    max_per_page=int(Addon.getSetting('num_p'))-1
    all_d=[]
    all_items,max_count=sdr_search_all(search_entered,page=page)
    max_page=100#max_count/max_per_page
    addNolink( '[COLOR red][I]--- סדרות TV ---[/I][/COLOR]', id,27,False,fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png', iconimage='special://home/addons/plugin.video.telemedia/tele/idanplus.png',plot=' ')
    for items in all_items:
        all_d.append(addDir3(items['name'],items['link'],278,items['img'],items['img'],items['eng_name']))

   
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    
def searchallinone(tmdb,type,last_id_pre,search_entered_pre,icon_pre,fan_pre,season,episode,no_subs=0,original_title='',heb_name='',dont_return=True,manual=True):
    icon_pre='special://home/addons/plugin.video.telemedia/tele/Play4.png'
    from sqlite3 import dbapi2 as database

    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
    dbcon.commit()
    dbcur.execute("SELECT * FROM search")
    match_search = dbcur.fetchall()
    all_pre_search=[]
    menu=[]
    for nm,fr in match_search:
        all_pre_search.append(nm)
    last_id=last_id_pre.split('$$$')[0]
    last_id_msg=last_id_pre.split('$$$')[1]
    query=search_entered_pre
    query=query.replace('%20',' ').replace('%27',"'").replace('%3a',":")
    if query.replace("'","%27") not in all_pre_search and manual:
        dbcur.execute("INSERT INTO search Values ('%s','%s');" %  (query.replace("'","%27"),' '))
        dbcon.commit()
    dbcur.close()
    dbcon.close()

    dp = xbmcgui . DialogProgress ( )
    dp.create('מבצע חיפוש')
    try:
        search_tmdb(search_entered_pre)
    except:pass
    # try:
        # search_sdarot_tv(search_entered_pre,'0')
    # except:pass
    try:
        search_idanplus(search_entered_pre,dp)
    except:pass
    try:
        search_person(search_entered_pre,dp)
    except:pass
    try:
        search_medovavim(search_entered_pre,dp)
    except:pass
    try:
        search_chats(search_entered_pre,dp)
    except:pass 
    try:
        search_public_chats(search_entered_pre,dp)
    except:pass 
    try:
        search_tele_allfiles(last_id_pre,tmdb,search_entered_pre,icon_pre,fan_pre,season,episode,dp,no_subs,original_title)
    except:pass
    

    # search_sdarot_tv(search_entered_pre,'0')
    dp.close()


def latest_subs_chace(url):
    o_url=url
    all_d=[]
    import datetime
    now = datetime.datetime.now()
    selected_year=[2023,2022]#int(now.year)#-1
    modein='1'

    
    if 'opensubtitles.org' not in url:

        x='https://www.opensubtitles.org/en/search/sublanguageid-heb/searchonlymovies-on/movieyearsign-%s/movieyear-%s/sort-5/asc-0'%(modein,str(2023))
    else:
      x=url
    headers = {
                                
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    html=requests.get(x,headers=headers).content.decode('utf-8')#()
    
    # html=requests.get(x,headers=headers).content.decode('utf-8')
    regex='http://www.imdb.com/title/(.+?)/'
    match=re.compile(regex).findall(html)
    
    if 'opensubtitles.org' not in url:

        x='https://www.opensubtitles.org/en/search/sublanguageid-heb/searchonlymovies-on/movieyearsign-%s/movieyear-%s/sort-5/asc-0'%(modein,str(2022))
    else:
      x=url
    headers = {
                                
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    html=requests.get(x,headers=headers).content.decode('utf-8')
    regex='http://www.imdb.com/title/(.+?)/'
    match2=re.compile(regex).findall(html)

    return match+match2

def latest_subs(url,new_imdb=False):
    o_url=url
    all_d=[]
    import datetime
    now = datetime.datetime.now()
    selected_year=[2023,2022]#int(now.year)#-1
    modein='1'
    from sqlite3 import dbapi2 as database
    dbcon2 = database.connect(cacheFile2)
    dbcur2 = dbcon2.cursor()
    dbcur2.execute("CREATE TABLE IF NOT EXISTS %s ( ""new_name TEXT,""url TEXT,""mode TEXT,""icon TEXT,""fan TEXT,""plot TEXT,""year TEXT,""original_name TEXT,""id TEXT,""rating TEXT,""new_name2 TEXT,""year2 TEXT,""genere TEXT,""trailer TEXT,""imdb TEXT);"% 'latestsubs')



    dbcur2.execute("SELECT  * FROM latestsubs")
    match2 = dbcur2.fetchall()
    
    all_imdb=[]
    match=cache.get(latest_subs_chace,24,url, table='cookies')
    html_g=html_g_movie
    # match=latest_subs_chace()
    all_db_imdb=[]
    for new_name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,genere,trailer,imdb in match2:
        all_db_imdb.append(imdb)
    count=0
    for imdb in match:
       if imdb not in all_db_imdb:
         count+=1
    # if count>10 and not new_imdb:
       # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Telemedia', 'אנא המתן סורק סרטים... '+str(count) )))
    whats_new=[]
    whats_new_images=[]
    
    for imdb in match:
       #log.warning('ccc '+str(match))
       if imdb not in all_imdb:
        all_imdb.append(imdb)
        if imdb in all_db_imdb:
            dbcur2.execute("SELECT * FROM latestsubs WHERE  imdb='%s'"%imdb)
            match = dbcur2.fetchone()
            new_name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,genere,trailer,imdb=match
            if not new_imdb:
                
                aa=addDir3(new_name.replace("%27","'"),id+' סרט',int(mode),icon,fan,plot.replace("%27","'"),data=year,original_title=original_name.replace("%27","'"),id=id,rating=rating,heb_name=new_name.replace("%27","'"),show_original_year=year,isr='0',generes=genere,trailer=trailer)
                all_d.append(aa)
        else:

                url=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=he'%imdb
                html=requests.get(url).json()
                for data in html['movie_results']:

                 if 'vote_average' in data:
                   rating=data['vote_average']
                 else:
                  rating=0
                 if 'first_air_date' in data:
                   year=str(data['first_air_date'].split("-")[0])
                 else:
                    year=str(data['release_date'].split("-")[0])
                 if data['overview']==None:
                   plot=' '
                 else:
                   plot=data['overview']
                 if 'title' not in data:
                   tv_movie='tv'
                   new_name=data['name']
                 else:
                   tv_movie='movie'
                   new_name=data['title']
                 if 'original_title' in data:
                   original_name=data['original_title']
                   mode=258
                   
                   id=str(data['id'])
                  
                 else:
                   original_name=data['original_name']
                   id=str(data['id'])
                   mode=258
                 if data['poster_path']==None:
                  icon=' '
                 else:
                   icon=data['poster_path']
                 if 'backdrop_path' in data:
                     if data['backdrop_path']==None:
                      fan=' '
                     else:
                      fan=data['backdrop_path']
                 else:
                    fan=html['backdrop_path']
                 if plot==None:
                   plot=' '
                 if 'http' not in fan:
                   fan=domain_s+'image.tmdb.org/t/p/original/'+fan
                 if 'http' not in icon:
                   icon=domain_s+'image.tmdb.org/t/p/original/'+icon
                 genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                        if i['name'] is not None])
                 try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
                 except:genere=''

                 trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s&tv_movie=%s" % (id,tv_movie)
                 try:
                    dbcur2.execute("INSERT INTO latestsubs Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s');" %  (new_name.replace("'",'%27'),url,mode,icon,fan,plot.replace("'",'%27'),year,original_name.replace("'",'%27'),id,rating,new_name.replace("'",'%27'),year,genere,trailer,imdb))
                 except:
                    pass
                 whats_new.append((new_name,url,icon,fan,plot.replace("'",'%27'),year,original_name,id))
                 if len(whats_new_images)<19:
                    whats_new_images.append(icon)
                 if not new_imdb:

                    aa=addDir3(new_name,id+' סרט',mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr='0',generes=genere,trailer=trailer)
                    all_d.append(aa)
    try:
        dbcon2.commit()
    except:
       pass
    regex='offset-(.+?)$'
    match=re.compile(regex).findall(o_url)

    if len(match)==0:
      next='20'
    else:
      next=str(int(match[0])+20)
    if not new_imdb:
        aa=addDir3('[COLOR aqua][I]עמוד הבא[/I][/COLOR]','https://www.opensubtitles.org/en/search/sublanguageid-heb/searchonlymovies-on/movieyearsign-%s/movieyear-%s/sort-5/asc-0/offset-'%(modein,str(selected_year))+next,120,'http://www.stefanovettor.com/wp-content/uploads/2015/09/mySubtitles_logo_256.png','https://youprogrammer.com/wp-content/uploads/2018/01/MOvies-subtitle-download-sites.png','עמוד הבא')
        all_d.append(aa)

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def latest_subs2(url,new_imdb=False):
    o_url=url
    all_d=[]
    import datetime
    now = datetime.datetime.now()
    selected_year=[2022,2023]#int(now.year)#-1
    
        # i=selected_year
        
    modein='1'
    
    if url=='years':
        all_years=['כל הכתוביות משנה ... עד היום']
        
    
        for year in range(now.year,1970,-1):
             all_years.append(str(year))
        ret=xbmcgui.Dialog().select("בחר שנה", all_years)
        selected_year_pre=''
        modein='1'
        if ret!=-1:
          if ret==0:
            keyboard = xbmc.Keyboard(selected_year_pre, 'הכנס שנה')
            
            keyboard.doModal()
            if keyboard.isConfirmed():
                selected_year_pre = keyboard.getText()
                if selected_year_pre.isdigit():
                    selected_year=int(selected_year_pre)
                    modein='5'
          else:
          
            selected_year=int(all_years[ret])
        else:
         sys.exit()
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    #log.warning('last')
    dbcon2 = database.connect(cacheFile2)
    dbcur2 = dbcon2.cursor()
    dbcur2.execute("CREATE TABLE IF NOT EXISTS %s ( ""new_name TEXT,""url TEXT,""mode TEXT,""icon TEXT,""fan TEXT,""plot TEXT,""year TEXT,""original_name TEXT,""id TEXT,""rating TEXT,""new_name2 TEXT,""year2 TEXT,""genere TEXT,""trailer TEXT,""imdb TEXT);"% 'latestsubs')
    from resources.modules.tmdb import html_g_movie
    
    html_g=html_g_movie
    if 'opensubtitles.org' not in url:
      for i in selected_year:
        
        x='https://www.opensubtitles.org/en/search/sublanguageid-heb/searchonlymovies-on/movieyearsign-%s/movieyear-%s/sort-5/asc-0'%(modein,str(i))
      
    else:
      x=url
    # logging.warning('43343434343 '+str(x))
    headers = {
                                
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    html=requests.get(x,headers=headers).content.decode('utf-8')#()
    
    # html=requests.get(x,headers=headers).content.decode('utf-8')
    regex='http://www.imdb.com/title/(.+?)/'
    match=re.compile(regex).findall(html)
    
    all_imdb=[]
    dbcur2.execute("SELECT  * FROM latestsubs")
    
    match2 = dbcur2.fetchall()
    all_db_imdb=[]
    
    for new_name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,genere,trailer,imdb in match2:
        all_db_imdb.append(imdb)
    count=0
    for imdb in match:
       if imdb not in all_db_imdb:
         count+=1
    if count>10 and not new_imdb:
       xbmc.executebuiltin((u'Notification(%s,%s)' % ('Telemedia', 'אנא המתן סורק סרטים... '+str(count) )))
    whats_new=[]
    whats_new_images=[]
    
    for imdb in match:
       #log.warning('ccc '+str(match))
       if imdb not in all_imdb:
        all_imdb.append(imdb)
        if imdb in all_db_imdb:
            dbcur2.execute("SELECT * FROM latestsubs WHERE  imdb='%s'"%imdb)
            match = dbcur2.fetchone()
            new_name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,genere,trailer,imdb=match
            if not new_imdb:

                aa=addDir3(new_name.replace("%27","'"),url,int(mode),icon,fan,plot.replace("%27","'"),data=year,original_title=original_name.replace("%27","'"),id=id,rating=rating,heb_name=new_name.replace("%27","'"),show_original_year=year,isr='0',generes=genere,trailer=trailer)
                all_d.append(aa)
        else:

                url=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=he'%imdb
                html=requests.get(url).json()
                for data in html['movie_results']:

                 if 'vote_average' in data:
                   rating=data['vote_average']
                 else:
                  rating=0
                 if 'first_air_date' in data:
                   year=str(data['first_air_date'].split("-")[0])
                 else:
                    year=str(data['release_date'].split("-")[0])
                 if data['overview']==None:
                   plot=' '
                 else:
                   plot=data['overview']
                 if 'title' not in data:
                   tv_movie='tv'
                   new_name=data['name']
                 else:
                   tv_movie='movie'
                   new_name=data['title']
                 if 'original_title' in data:
                   original_name=data['original_title']
                   mode=15
                   
                   id=str(data['id'])
                  
                 else:
                   original_name=data['original_name']
                   id=str(data['id'])
                   mode=16
                 if data['poster_path']==None:
                  icon=' '
                 else:
                   icon=data['poster_path']
                 if 'backdrop_path' in data:
                     if data['backdrop_path']==None:
                      fan=' '
                     else:
                      fan=data['backdrop_path']
                 else:
                    fan=html['backdrop_path']
                 if plot==None:
                   plot=' '
                 if 'http' not in fan:
                   fan=domain_s+'image.tmdb.org/t/p/original/'+fan
                 if 'http' not in icon:
                   icon=domain_s+'image.tmdb.org/t/p/original/'+icon
                 genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                        if i['name'] is not None])
                 try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
                 except:genere=''

                 trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s&tv_movie=%s" % (id,tv_movie)
                 try:
                    dbcur2.execute("INSERT INTO latestsubs Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s');" %  (new_name.replace("'",'%27'),url,mode,icon,fan,plot.replace("'",'%27'),year,original_name.replace("'",'%27'),id,rating,new_name.replace("'",'%27'),year,genere,trailer,imdb))
                 except:
                    pass
                 whats_new.append((new_name,url,icon,fan,plot.replace("'",'%27'),year,original_name,id))
                 if len(whats_new_images)<19:
                    whats_new_images.append(icon)
                 if not new_imdb:

                    aa=addDir3(new_name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr='0',generes=genere,trailer=trailer)
                    all_d.append(aa)
    try:
        dbcon2.commit()
    except:
       pass
    regex='offset-(.+?)$'
    match=re.compile(regex).findall(o_url)

    if len(match)==0:
      next='20'
    else:
      next=str(int(match[0])+20)
    if not new_imdb:
        aa=addDir3('[COLOR aqua][I]עמוד הבא[/I][/COLOR]','https://www.opensubtitles.org/en/search/sublanguageid-heb/searchonlymovies-on/movieyearsign-%s/movieyear-%s/sort-5/asc-0/offset-'%(modein,str(selected_year))+next,120,'http://www.stefanovettor.com/wp-content/uploads/2015/09/mySubtitles_logo_256.png','https://youprogrammer.com/wp-content/uploads/2018/01/MOvies-subtitle-download-sites.png','עמוד הבא')
        all_d.append(aa)

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        
def get_cast(url,id,season,episode):
    
    if url=='movie':
        x='http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&append_to_response=credits'%(id,lang)
    else:
        x='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&append_to_response=credits'%(id,season,episode,lang)
    html=requests.get(x).json()
   
    aa=[]
    for items in html['credits']['cast']:
        icon=items['profile_path']
        
        if icon==None:
          icon=' '
        else:
          icon='https://'+'image.tmdb.org/t/p/original/'+icon
        fanart=icon
        aa.append(addDir3(items['name']+' [COLOR yellow](%s)[/COLOR]'%items['character'],str(items['id']),169,icon,fanart,items['name']))
    
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),aa,len(aa))
    

    
def utf8_simple(params):
    
    try:
        params = params
    except:
        params='ERROR'

    return params

def clean_sources(name):


    name=name.replace('דב סרטים','').replace('לולו סרטים','').replace('דב ס','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('@yosichen','').replace('אלי ה סרטים','').replace('נ מדיה','').replace('נתי.מדיה','').replace('גוזלן','').replace('אלי ה סרטים','').replace('Silver007','').replace('Etamar','').replace('כ.ס','').replace('כל סרט','').replace('חננאל ס.','').replace('_',' ').replace('ח.ס','').replace('נ.מ','').replace('נתי מדיה','').replace('לולו סרטים','').replace('דב סרטים צפייה ישירה','').replace('מדיה VOD','').replace('קינג סרט','').replace('ז.מ','').replace('זירה מדיה','').replace('דב.ס','').replace('כל המדיה','').replace('נתן סרטים','').replace('משה סדרות','').replace('.',' ').replace('mkv','').replace('avi','').replace('mp4','').replace('-',' ').replace('@','').replace('900p','').replace('360p','').replace('430p','').replace('570p','').replace('720p','').replace('900P','').replace('360P','').replace('570P','').replace('720P','').replace('1080P','').replace('1080p','').replace('720p','').replace('480p','').replace('360p','').replace('WEBRip','').replace('HDTV','').replace('4K','').replace('4k','').replace('ת מ','').replace('BluRay','').replace('ח1','').replace('ח2','').replace('ח3','').replace('ח4','').replace('ח5','')

        
    return name
def clean_sources_nextep(name):


    name=name.replace('דב סרטים','').replace('לולו סרטים','').replace('דב ס','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('@yosichen','').replace('אלי ה סרטים','').replace('נ מדיה','').replace('נתי.מדיה','').replace('גוזלן','').replace('אלי ה סרטים','').replace('Silver007','').replace('Etamar','').replace('כ.ס','').replace('כל סרט','').replace('חננאל ס.','').replace('_',' ').replace('ח.ס','').replace('נ.מ','').replace('נתי מדיה','').replace('לולו סרטים','').replace('דב סרטים צפייה ישירה','').replace('מדיה VOD','').replace('קינג סרט','').replace('ז.מ','').replace('זירה מדיה','').replace('דב.ס','').replace('.avi','').replace('.mp4','').replace('.mkv','').replace('TVRip','').replace('x264','').replace('x265','').replace('AAC','').replace('2CH','').replace('HebDub','').replace('HebSub','').replace('SMG','').replace('WEB-DL','').replace('כל המדיה','').replace('נתן סרטים','').replace('משה סדרות','').replace('900p','').replace('360p','').replace('430p','').replace('570p','').replace('720p','').replace('900P','').replace('360P','').replace('570P','').replace('720P','').replace('1080P','').replace('1080p','').replace('720p','').replace('480p','').replace('360p','').replace('WEBRip','').replace('HDTV','').replace('  ','').replace('ע','עונה ').replace('פ','פרק ')
    
    return name
    
def file_list(id,page,last_id_all,quary,icon_pre,fan_pre,image_master='',original_title=''):
   try:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        from resources.modules.general import clean_name
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        dbcon.commit()

        dbcur.execute("SELECT * FROM playback")
        match = dbcur.fetchall()
        all_w={}
        for n,tm,s,e,p,t,f in match:
            ee=clean_name(str(n),original_title)
            all_w[ee]={}
            all_w[ee]['resume']=str(p)
            all_w[ee]['totaltime']=str(t)
        link_types=['upfile','drive.google','youtube','youtu.be','.m3u8','twitch']

        all_d=[]
        icon_pre=telemaia_icon
        fan_pre=telemaia_fan
        if image_master!='':
            fan_pre=image_master.split('$$$')[1]
            icon_pre=image_master.split('$$$')[0]
        fan_o=fan_pre
        icon_o=icon_pre
        if 'from_plot' in quary:
            quary=' '
            dont_s_again=True
        else:
            dont_s_again=False
            search_entered=''
            #'Enter Search'
            keyboard = xbmc.Keyboard(search_entered, Addon.getLocalizedString(32025))
            keyboard.doModal()
            if keyboard.isConfirmed():
                    quary = keyboard.getText()
            else:
                return 0
        
      
        last_id_doc=last_id_all.split('$$$')[0]
        last_id=last_id_all.split('$$$')[1]
        last_id_link=last_id_all.split('$$$')[2]
        last_id_audio=last_id_all.split('$$$')[3]
        
        disp_files=Addon.getSetting("disp_f")=='true'
        disp_vid=Addon.getSetting("disp_v")=='true'
        disp_links=Addon.getSetting("disp_l")=='true'
        disp_audio=Addon.getSetting("disp_a2")=='true'
        
        disp_repo=Addon.getSetting("repo")=='true'
        
        download_full_files=Addon.getSetting("download_files")=='true'
        
        
        num=random.randint(1,1001)
        plat='windows'
        if sys.platform.lower().startswith('linux'):
        
            if 'ANDROID_DATA' in os.environ:
                plat = 'android'
        on_android=False
        if Addon.getSetting("install_apk")=='true':
            on_android=plat == 'android'
        if last_id_audio!='-99' and disp_audio:
            num=random.randint(1,1001)
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary.strip(),'from_message_id':int(last_id_audio),'offset':0,'filter':{'@type': 'searchMessagesFilterAudio'},'limit':100, '@extra': num})
                 }
           
           
           
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
           
            counter_ph=1000
            for items in event['messages']:  
                    
                    
                    name=items['content']['audio']['title']
                    
                    size=items['content']['audio']['audio']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    icon=icon_pre
                    fan=fan_pre
                    # if 'album_cover_thumbnail' in items['content']['audio']:
                        # if 'photo' in items['content']['audio']['album_cover_thumbnail']:
                            # counter_ph+=1
                            # icon_id=items['content']['audio']['album_cover_thumbnail']['photo']['id']
                            # f_name=items['content']['audio']['album_cover_thumbnail']['photo']['remote']['id']+'.jpg'
                            # mv_name=os.path.join(icons_path,f_name)
                            # if os.path.exists(mv_name):
                                # icon=mv_name
                            # else:
                               # icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                            
                            # fan=icon
                    icon='special://home/addons/plugin.video.telemedia/tele/icon.jpg'
                    # fanart='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                    dur=items['content']['audio']['duration']
                    t=time.strftime("%H:%M:%S", time.gmtime(dur))
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    name=clean_name(name,original_title)
                    link_data={}
                    link_data['id']=str(items['content']['audio']['audio']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    name=name.replace('סדרות מהלב','')
                    addLink( '[COLOR lime]'+name+'[/COLOR]',f_lk ,3,False, icon,fan,f_size2+'\n'+t+'\nMusic File',da=da,all_w=all_w,in_groups=True)
                    
                
            last_id_audio=-99
            try:
             last_id_audio=items['id']
             last_id_audio_found=1
            except:
             pass
     
        if last_id_doc!='-99' and disp_files:
           num=random.randint(1,1001)
           data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary.strip(),'from_message_id':int(last_id_doc),'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':100, '@extra': num})
                 }
           

           event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
           
           for items in event['messages']:  
               
                if 'document' not in items['content']:
                    continue
                ok_name=True
                file_name=items['content']['document']['file_name']
                if 'document' in items['content']:
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            if len(items['content']['caption']['text'])>0:
                                name=items['content']['caption']['text']
                                ok_name=False
                    if ok_name:
                        name=file_name
                    if Addon.getSetting("files_display_type")=='0':
                        name=file_name
                    c_name=[]
                    if '\n' in name:
                        f_name=name.split('\n')
                        for it in f_name:
                            if '😎' not in it and it!='\n' and len(it)>1 and '💠' not in it:
                                c_name.append(it)
                        name='\n'.join(c_name)
                    
                        
                    if not(download_full_files and '_files_' in original_title.lower()):
                        
                        if on_android and 'apk' in original_title.lower():
                            if '.mkv' not in file_name and '.mp4' not in file_name and '.avi' not in file_name and '.AVI' not in file_name and '.MKV' not in file_name and '.MP4' not in file_name and '.zip' not in file_name and '.apk' not in file_name and '.wmv' not in file_name:
                                continue
                        elif disp_repo and 'repo' in original_title.lower():
                            
                            if '.mkv' not in file_name and '.mp4' not in file_name and '. mp4' not in file_name and '.avi' not in file_name and '.AVI' not in file_name and '.MKV' not in file_name and '.MP4' not in file_name  and '.zip' not in file_name and '.wmv' not in file_name:
                                continue
                        else:
                            if '.mkv' not in file_name and '.mp4' not in file_name and '.avi' not in file_name and '.AVI' not in file_name and '.MKV' not in file_name and '.MP4' not in file_name and '.wmv' not in file_name and '.mov' not in file_name and '.ts' not in file_name:
                                continue
                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    # if Addon.getSetting("remove_title")=='true':
                        # name=name.replace(original_title,'').replace('@'+original_title,'')
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    regex='.*([1-3][0-9]{3})'
                    year_pre=re.compile(regex).findall(name)
                    year=0
                    if len(year_pre)>0:
                        year=year_pre[0]
                    mode=3
                    o_name=name
                    if '.zip'  in name:
                        name='[COLOR gold]'+name+'[/COLOR]'
                        mode=24
                    if '.apk'  in name:
                        name='[COLOR gold]'+name+'[/COLOR]'
                        mode=32
                    
                    if (download_full_files and '_files_' in original_title.lower()):
                        mode=36
                        name='[COLOR khaki]'+name+'[/COLOR]'
                        
                    name=clean_name(name,original_title)
                    link_data={}
                    link_data['id']=str(items['content']['document']['document']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    name=name.replace('סדרות מהלב','')
                    addLink( name,f_lk ,mode,False, icon_pre,fan_pre,f_size2,da=da,year=year,original_title=o_name,all_w=all_w,in_groups=True)
                
                
           last_id_doc=-99
           try:
            last_id_doc=items['id']
            last_id_doc_found=1
           except:
            pass
        else:
           last_id_doc=-99
           last_id_doc_found=0
        if last_id!='-99' and disp_vid:
            num=random.randint(1,1001)
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary.strip(),'from_message_id':int(last_id),'offset':0,'filter':{'@type': 'searchMessagesFilterVideo'},'limit':100, '@extra': num})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            for items in event['messages']:  
                #log.warning(items)
                if 'video' in items['content']:
                    ok_name=True
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            if len(items['content']['caption']['text'])>0:
                                name=items['content']['caption']['text']
                                ok_name=False
                    if ok_name:
                        name=items['content']['video']['file_name']

                    if Addon.getSetting("video_display_type")=='0':
                        name=items['content']['video']['file_name']
                    c_name=[]
                    if '\n' in name:
                        f_name=name.split('\n')
                        for it in f_name:
                            if '😎' not in it and it!='\n' and len(it)>1:
                                c_name.append(it)
                        # name='\n'.join(c_name)
                    size=items['content']['video']['video']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    plot=''
                    
                    if 'caption' in items['content']:
                        plot=items['content']['caption']['text']
                        
                        if '\n' in plot and len(name)<3:
                                name=plot.split('\n')[0]
                        if not ok_name:
                         name=plot.split('\n')[0]
                         
                    # if Addon.getSetting("remove_title")=='true':
                        # name=name.replace(original_title,'').replace('@'+original_title,'')
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    regex='.*([1-3][0-9]{3})'
                    year_pre=re.compile(regex).findall(name)
                    year=0
                    if len(year_pre)>0:
                        year=year_pre[0]
                    name=clean_name(name,original_title)
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    name=name.replace('סדרות מהלב','')
                    addLink( name,f_lk,3,False, icon_pre,fan_pre,f_size2+'\n'+plot.replace('\n\n',' - ').replace('סדרות מהלב',''),da=da,year=year,all_w=all_w,in_groups=True)
                
                
               
            last_id=-99
            try:
                last_id=items['id']
            except:
                pass
                
            
        else:
            last_id=-99
        
        
        if last_id_link!='-99' and disp_links:
           num=random.randint(1,1001)
           data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':(id), 'query': quary,'from_message_id':int(last_id_link),'offset':0,'filter':{'@type': 'searchMessagesFilterUrl'},'limit':100, '@extra': num})
                 }
           
           event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

           
           counter_ph=0
           for items in event['messages']:  
                
                if 'web_page' in items['content']:
                    name=items['content']['web_page']['title']
                    link=items['content']['web_page']['url']
                    plot=items['content']['web_page']['description']['text']
                    all_l=[link]
                    ok=False
                    for items_in in link_types:
                        if items_in in link:
                            ok=True
                            break
                            
                    if not ok:
                          
                          continue
                        
                    
                    if 'text' in items['content']:
                        txt_lines=items['content']['text']['text'].split('\n')
                        
                        rem_lines=[]
                        
                        for lines in txt_lines:
                            ok=False
                            for items_in in link_types:
                                if items_in in lines:
                                    ok=True
                                    break
                                    
                            if not ok:
                                  
                                  continue
                            
                                
                            all_l.append(lines)
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']['web_page']:
                        counter_ph+=1
                        icon_id=items['content']['web_page']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['web_page']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=icon_pre#download_photo(icon_id,counter_ph,f_name,mv_name)
                        
                        counter_ph+=1
                        loc=items['content']['web_page']['photo']['sizes']
                        icon_id=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['web_page']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=fan_pre#download_photo(icon_id,counter_ph,f_name,mv_name)
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    name=clean_name(name,original_title)
                    name=name.replace('סדרות מהלב','')
                    addLink(name, utf8_simple('$$$'.join(all_l)),9,False, icon,fan,plot.replace('\n\n','\n').replace('סדרות מהלב',''),da=da,all_w=all_w,in_groups=True)
                elif 'caption' in items['content']:
                    txt_lines=items['content']['caption']['text'].split('\n')
                    all_l=[]
                    rem_lines=[]
                    
                    for lines in txt_lines:
                        ok=False
                        for items_in in link_types:
                            if items_in in lines:
                                ok=True
                                break
                                
                        if not ok:
                              rem_lines.append(lines)
                              continue
                        
                        
                            
                        all_l.append(lines)
                    if len(all_l)==0:
                        continue
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']:
                        counter_ph+=1
                        
                        icon_id=items['content']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=icon_pre#download_photo(icon_id,counter_ph,f_name,mv_name)
                        
                        counter_ph+=1
                        loc=items['content']['photo']['sizes']
                        icon_id=items['content']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=fan_pre#download_photo(icon_id,counter_ph,f_name,mv_name)
                       
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    
                    addLink( txt_lines[0], utf8_simple('$$$'.join(all_l)),9,False, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),da=da,all_w=all_w,in_groups=True)
                
                elif 'text' in items['content']:
                    txt_lines=items['content']['text']['text'].split('\n')
                    all_l=[]
                    rem_lines=[]
                    
                    for lines in txt_lines:
                        ok=False
                        for items_in in link_types:
                            if items_in in lines:
                                ok=True
                                break
                                
                        if not ok:
                              rem_lines.append(lines)
                              continue
                        
                            
                        all_l.append(lines)
                    if len(all_l)==0:
                        continue
                    
                    icon=icon_pre
                    fan=fan_pre
                    if 'photo' in items['content']:
                        counter_ph+=1
                        icon_id=items['content']['photo']['sizes'][0]['photo']['id']
                        f_name=items['content']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(icons_path,f_name)
                        if os.path.exists(mv_name):
                            icon=mv_name
                        else:
                           icon=icon_pre#download_photo(icon_id,counter_ph,f_name,mv_name)
                        
                        
                        counter_ph+=1
                        
                        loc=items['content']['photo']['sizes']
                        icon_id=items['content']['photo']['sizes'][len(loc)-1]['photo']['id']
                        f_name=items['content']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                        mv_name=os.path.join(fan_path,f_name)
                        if os.path.exists(mv_name):
                            fan=mv_name
                        else:
                           fan=fan_pre#download_photo(icon_id,counter_ph,f_name,mv_name)
                       
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    addLink( txt_lines[0], utf8_simple('$$$'.join(all_l)),9,False, icon,fan,('\n'.join(rem_lines)).replace('\n\n','\n'),da=da,all_w=all_w,in_groups=True)
                
                
                
           last_id_link=-99
           try:
            last_id_link=items['id']
            
           except:
            pass
        else:
           last_id_link=-99
          
           
        if last_id_doc==-99 and last_id==-99 and last_id_link==-99 and last_id_audio==-99:
            xbmcgui.Dialog().ok(Addon.getLocalizedString(32052),Addon.getLocalizedString(32059))
        f_last_id=str(last_id_doc)+'$$$'+str(last_id)+'$$$'+str(last_id_link)+'$$$'+str(last_id_audio)
        if quary==' ':
            quary='from_plot'
        #Next Page
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'[/COLOR]',str(id),2,'https://www.5thtackle.com/wp-content/uploads/2017/04/next-page.jpg','https://www.mcgill.ca/continuingstudies/files/continuingstudies/next-page-magazine.png',quary,data=str(int(page)+1),last_id=f_last_id,image_master=icon_o+'$$$'+fan_o)
        all_d.append(aa) 
        if dont_s_again:
            f_last_id='0$$$0$$$0$$$0'
            #'Search'
            aa=addDir3('[COLOR blue]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(id),2,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','search',data='0',last_id=f_last_id,image_master=image_master)
            all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.warning('ERROR IN Main:'+str(lineno))
        log.warning('inline:'+str(line))
        log.warning(str(e))
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))

def refresh_datatelegram():
    
    # try:    
        # os.remove(os.path.join(translatepath("special://userdata/"),"addon_data","plugin.video.telemedia","database","db.sqlite"))
    # except:
        # pass
    
    
    num=random.randint(0,60000)
    data={'type':'td_send',
         'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':0, 'limit': '15000','chat_list':{'@type': 'chatListFilter'}, '@extra': num})
         }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    # sys.exit()
# refresh_datatelegram()
def get_direct_bot_link7(l_data):
   try:
    dp = xbmcgui.DialogProgress()
    global play_status
    global break_window
    play_status='שולח קישור לבוט'
    event_info=''
    c_id=l_data['c_id']
    m_id=l_data['m_id']
    num=random.randint(0,60000)

    data={'type':'td_send',
         'info':json.dumps({'@type': 'forwardMessages','chat_id':(6238492629), 'from_chat_id': c_id,'message_ids':[m_id], '@extra': num})
         }

    logging.warning('sending')
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    new_link='empty'
    logging.warning('Wait')
    counter_sh=0
    data={'type':'clean_last_link',
             'info':''
             }


    test=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
    while(new_link=='empty'):
        data={'type':'get_last_link',
             'info':''
             }


        new_link=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        if new_link=='Found':
            logging.warning( 'Limit')
            break
        time.sleep(0.1)
        counter_sh+=1
        if (counter_sh>100):
            logging.warning('Timeout')
            break
    
    headers = {
      
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        }
    logging.warning(new_link)
    f_link=re.compile('https:(.+?)\n',re.DOTALL).findall(str(new_link))[0]
    logging.warning(f_link)
    
    return 'https:'+f_link
 
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        logging.warning('ERROR IN bot:'+str(lineno))
        logging.warning('inline:'+str(line))
        logging.warning(str(e))
        #xbmcgui.Dialog().ok('Error occurred','Err in bot:'+str(e)+'Line:'+str(lineno))
        return "Error play"
def get_direct_bot_link_ban(l_data):
    dp = xbmcgui.DialogProgress()
    
    global play_status
    global break_window
    play_status='שולח קישור לבוט'
    event_info=''
    c_id=l_data['c_id']
    m_id=l_data['m_id']
    num=random.randint(0,60000)
    # t = Thread(target=forward_messages, args=(l_data,))
    # t.start()
    data={'type':'td_send',
         'info':json.dumps({'@type': 'forwardMessages','chat_id':(6238492629), 'from_chat_id': c_id,'message_ids':[m_id], '@extra': num})
         }
    
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    try:
        if 'Chat to forward messages to not found' in event['message']:
            event_info=event
            
            get_direct_bot_link_my(l_data)
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            if Addon.getSetting('new_play_window2')=='true':
                play_status='יתכן שאתם לא מחוברים לבוט'
            else:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין תגובה מהבוט'),'[COLOR %s]יתכן שאתם לא מחוברים אליו.[/COLOR]' % COLOR2)
                
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChats','offset_chat_id':[m_id],'offset_order':100, 'limit': '10','chat_list':{'@type': 'chatListFilter','chat_filter_id':0}, '@extra': num})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

            return get_direct_bot_link_my(l_data)
        if "Message has protected content and can't be forwarded" in event['message']:
            
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            if Addon.getSetting('new_play_window2')=='true':
                play_status='קובץ חסום להעברה - עובר לניגון רגיל'
            else:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין תגובה מהבוט'),'[COLOR %s]קובץ חסום להעברה - עובר לניגון רגיל[/COLOR]' % COLOR2)
            return 'play_tele'
            
    except:pass
    
    new_link='empty'
    counter_sh=0
    data={'type':'clean_last_link',
             'info':''
             }
    test=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    stop_time = time.time() + 8
    
    if Addon.getSetting('new_play_window2')=='false':
        dp.create('Please Wait...','שולח קישור לבוט'+'\n'+ ''+'\n'+'')
    while(new_link=='empty'):
        if Addon.getSetting('new_play_window2')=='false':
            dp.update(0, 'שולח קישור לבוט...'+'\n'+'ממתין לניגון'+'\n'+ str(event_info))
        data={'type':'get_last_link',
             'info':''
             }
        new_link=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        # log.warning('32323 '+str(new_link))
        
        if time.time() > stop_time:
            # break_window=True
            
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'מעביר ניגון לבוט 2'),'[COLOR %s]המתן...[/COLOR]' % COLOR2)
            new_link='play_tele'
            return get_direct_bot_link_my(l_data)
            # break
        if Addon.getSetting('new_play_window2')=='false':
            if dp.iscanceled():
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                dp.close()
                sys.exit()
    headers = {
      
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        }

    f_link=re.compile('https:(.+?)\n',re.DOTALL).findall(str(new_link))[0]

    
    return 'https:'+f_link

def get_direct_bot_link(l_data):#def get_direct_bot_link_my(l_data):
    dp = xbmcgui.DialogProgress()
    global play_status
    global break_window
    play_status='שולח קישור לבוט'
    event_info=''
    c_id=l_data['c_id']
    m_id=l_data['m_id']
    num=random.randint(0,60000)
    # t = Thread(target=forward_messages, args=(l_data,))
    # t.start()
    data={'type':'td_send',
         'info':json.dumps({'@type': 'forwardMessages','chat_id':(1810654262), 'from_chat_id': c_id,'message_ids':[m_id], '@extra': num})
         }
    
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    try:
        if 'Chat to forward messages to not found' in event['message']:
            event_info=event
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            if Addon.getSetting('new_play_window2')=='true':
                play_status='יתכן שאתם לא מחוברים לבוט'
            else:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין תגובה מהבוט'),'[COLOR %s]יתכן שאתם לא מחוברים אליו.[/COLOR]' % COLOR2)
                
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChats','offset_chat_id':[m_id],'offset_order':100, 'limit': '10','chat_list':{'@type': 'chatListFilter','chat_filter_id':0}, '@extra': num})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

            return 'play_tele'
        if "Message has protected content and can't be forwarded" in event['message']:

            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            if Addon.getSetting('new_play_window2')=='true':
                play_status='קובץ חסום להעברה - עובר לניגון רגיל'
            else:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין תגובה מהבוט'),'[COLOR %s]קובץ חסום להעברה - עובר לניגון רגיל[/COLOR]' % COLOR2)
            return 'play_tele'
            
    except:pass
    new_link='empty'
    counter_sh=0
    data={'type':'clean_last_link',
             'info':''
             }
    test=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    stop_time = time.time() + 8
    if Addon.getSetting('new_play_window2')=='false':
        dp.create('Please Wait...','שולח קישור לבוט'+'\n'+ ''+'\n'+'')
    while(new_link=='empty'):
        if Addon.getSetting('new_play_window2')=='false':
            dp.update(0, 'שולח קישור לבוט...'+'\n'+'ממתין לניגון'+'\n'+ str(event_info))
        data={'type':'get_last_link',
             'info':''
             }
        new_link=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        # log.warning('32323 '+str(new_link))
        
        if time.time() > stop_time:
            # break_window=True
            
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'ניגון דרך הבוט לא זמין'),'[COLOR %s]עובר לניגון רגיל.[/COLOR]' % COLOR2)
            new_link='play_tele'
            # break
        if Addon.getSetting('new_play_window2')=='false':
            if dp.iscanceled():
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                dp.close()
                sys.exit()

    try:
        f_link2=new_link.replace('📎 : ','')
    except:
        f_link2=new_link
    return  f_link2

def show_new_window(tv_movie,id,season,episode,fanart):
    global break_window
    
    menu = player_window('plugin.video.telemedia', id,tv_movie,season,episode,fanart)
    menu.doModal()

    del menu
    
    break_window=True

def get_direct_bot_link_old(c_id,m_id):

    dp = xbmcgui.DialogProgress()

    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous Power Bot'),'[COLOR %s]המתן...[/COLOR]' % COLOR2)
    bot_id=Addon.getSetting("bot_id")#'772555074'
    num=random.randint(0,60000)
    data={'type':'td_send',
         'info':json.dumps({'@type': 'forwardMessages','chat_id':(1722255826), 'from_chat_id': c_id,'message_ids':[m_id], '@extra': num})
         }

    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    try:
        if 'Chat to forward messages to not found' in event['message']:
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אתם לא מחוברים לבוט'),'[COLOR %s]יש להוסיף את הבוט לחשבון שלכם.[/COLOR]' % COLOR2)
            sys.exit()
    except:pass
    new_link='empty'
    counter_sh=0
    data={'type':'clean_last_link',
             'info':''
             }

    test=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    while(new_link=='empty'):
        data={'type':'get_last_link',
             'info':''
             }
        new_link=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        new_link=new_link.replace("Link to download file: ","")
        if dp.iscanceled():
            
            dp.close()
            break
            sys.exit()
    regex='http://(.*)html'
    ver=re.compile(regex,re.DOTALL).findall(new_link)

    ver=str(ver)
    ver=ver.replace('[','').replace('\n','').replace(']','').replace("'",'')
    ver='http://'+ver+'html'

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    html=requests.get(ver,headers=headers).content.decode('utf-8')
    regex='<source src=(.+?)type="video/mp4">'
    m=re.compile(regex,re.DOTALL).findall(html)

    f_link2=m[0]
    f_link2=f_link2.replace('"','')

    return  f_link2
def play_direct(final_link,data,name,no_subs,tmdb,season,episode,original_title,description,resume,resume_time,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='false',tvdb_id=''):
        global break_window
        original_name_r=original_title
        
        if kitana=='true':

            video_data={}
            listItem = xbmcgui.ListItem(name, path=final_link) 
            if season!=None and season!=' ' and season!="%20" and season!="0":
               video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
               video_data['mediatype']='tvshow'
               tv_movie='tv'
            else:
               video_data['mediatype']='movies'
               tv_movie='movie'

            video_data['title']=heb_name
            video_data['Writer']=tmdb
            video_data['season']=season
            video_data['episode']=episode
            video_data['plot']=plot
            video_data['premiered']=premiered
            video_data['year']=year
            video_data['imdb']=tmdb
            video_data['code']=tmdb
            video_data['Tagline']=name
            video_data['imdbnumber']=tmdb
            video_data['imdb_id']=tmdb
            video_data['IMDBNumber']=tmdb
            video_data['rating']=rating
            video_data['genre']=genre
            video_data['OriginalTitle']=original_title

            if no_subs=='1' or is_hebrew(str(name)):
               video_data[u'mpaa']=str('heb')
            if 'HebSub' in name:
                   video_data[u'mpaa']=('heb')
            if KODI_VERSION>19:
                info_tag = listItem.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
                if (tv_movie=='tv'):
                    info_tag.setTvShowTitle(meta_get(video_data,'TVshowtitle'))
                    try:
                        info_tag.setSeason(int(season))
                        info_tag.setEpisode(int(episode))
                    except:
                        pass
                info_tag.setPlot(meta_get(video_data,'plot'))
                try:
                    year_info=int(meta_get(video_data,'year'))
                    if (year_info>0):
                        info_tag.setYear(year_info)
                except:
                    pass
                try:
                    info_tag.setRating(float(meta_get(video_data,'rating')))
                except:
                    pass
                info_tag.setVotes(int(meta_get(video_data,'votes')))
                info_tag.setMpaa(meta_get(video_data,'mpaa'))
                info_tag.setDuration(int(meta_get(video_data,'duration')))
                info_tag.setCountries(meta_get(video_data,'country'))
                
                info_tag.setTrailer(meta_get(video_data,'trailer'))
                info_tag.setPremiered(meta_get(video_data,'premiered'))
                
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                
                info_tag.setUniqueIDs({'imdb': tmdb, 'tmdb':tmdb})
                info_tag.setIMDBNumber(tmdb)
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                info_tag.setOriginalTitle(original_title)
                info_tag.setTagLine(original_title)
            if KODI_VERSION<19:
                listItem.setInfo(type=types, infoLabels=video_data)
                listItem.setUniqueIDs({ 'imdb': imdb_id, 'tmdb' : tmdb }, "imdb")
            
            all_logo,all_n_fan,all_banner,all_clear_art,r_logo,r_art=get_extra_art(tmdb,tv_movie,tvdb_id)
            listItem.setArt({'clearlogo':r_logo,'clearart':r_art,'icon': iconimage, 'thumb': fanart, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage})
        else:
            listItem = xbmcgui.ListItem(name, path=final_link) 

            langs='he'
            video_data={}
            if season!=None and season!=' ' and season!="%20" and season!="0":
               video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
               video_data['mediatype']='tvshow'
               
            else:
               video_data['mediatype']='movies'
            if season!=None and season!=' ' and season!="%20" and season!="0":
               tv_movie='tv'
               url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')

            else:
               tv_movie='movie'
               
               url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')

            if tv_movie=='tv':
                
                url_media='https://api.themoviedb.org/3/%s/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&include_image_language=ru,null&append_to_response=images,external_ids'%(tv_movie,tmdb,lang)
                   
                html_media=requests.get(url_media).json()
                try:
                  tvdb_id=str(html_media['external_ids']['tvdb_id'])
                except:
                  tvdb_id=''
            
            if 'tt' not in tmdb:
                 try:
                    
                    imdb_id=requests.get(url2,timeout=10).json()['external_ids']['imdb_id']
                    
                 except Exception as e:
                    log.warning('IMDB err:'+str(e))
                    imdb_id=" "
            else:
                imdb_id=tmdb


            if 'Music File' in description:
                types='music'
                video_data['title']=name
            else:
                types='Video'
                try:
                    if '@' in name and '.' in name:
                        nm=name.split('.')
                        ind=0
                        for items in nm:
                            if '@' in items:
                                nm.pop(ind)
                            ind+=1
                        name='.'.join(nm)
                except:pass
                video_data['title']=heb_name.replace('.mkv','').replace('.avi','').replace('.mp4','').replace('גוזלן','').replace('.',' ').replace('_',' ').replace('WEB-DL','').replace('900p','').replace('360p','').replace('430p','').replace('570p','').replace('720p','').replace('900P','').replace('360P','').replace('570P','').replace('720P','').replace('1080P','').replace('נתי מדיה','').replace('לולו סרטים','').replace('CD1','').replace('CD2','').replace('CD3','').replace('WEBRip','').replace('HDTV','').replace('חננאל ס','').replace('מדיה VOD','').replace('TVRip','').replace('x264','').replace('x265','').replace('AAC','').replace('2CH','').replace('HebDub','').replace('HebSub','').replace('SMG','').replace('-','').replace('HAIMMedia','')

                video_data['Writer']=tmdb
                video_data['season']=season
                video_data['episode']=episode
                video_data['plot']=(xbmc.getInfoLabel("ListItem.Plot"))
                video_data['year']=data
                video_data['imdb']=imdb_id
                video_data['code']=imdb_id
                video_data['icon']=fanart
                video_data['imdbnumber']=imdb_id
                video_data['poster']=fanart
                video_data['imdb_id']=imdb_id
                video_data['IMDBNumber']=imdb_id
                video_data['rating']=(xbmc.getInfoLabel ("ListItem.Rating"))
                video_data['genre']=(xbmc.getInfoLabel("ListItem.Genre "))
                video_data['OriginalTitle']=heb_name.replace('.mkv','').replace('.avi','').replace('.mp4','')
                if no_subs=='1' or is_hebrew(name):
                      video_data[u'mpaa']=('heb')
                if 'HebSub' in name:
                        video_data[u'mpaa']=('heb')
            try:
                s=int(season)
                tv_movie='tv'
                video_data['mediatype']='episode'


            except:
                tv_movie='movie'
                video_data['mediatype']='movie'
            if KODI_VERSION>19:
                info_tag = listItem.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
                if (tv_movie=='tv'):
                    info_tag.setTvShowTitle(meta_get(video_data,'TVshowtitle'))
                    try:
                        info_tag.setSeason(int(season))
                        info_tag.setEpisode(int(episode))
                    except:
                        pass
                info_tag.setPlot(meta_get(video_data,'plot'))
                try:
                    year_info=int(meta_get(video_data,'year'))
                    if (year_info>0):
                        info_tag.setYear(year_info)
                except:
                    pass
                try:
                    info_tag.setRating(float(meta_get(video_data,'rating')))
                except:
                    pass
                info_tag.setVotes(int(meta_get(video_data,'votes')))
                info_tag.setMpaa(meta_get(video_data,'mpaa'))
                info_tag.setDuration(int(meta_get(video_data,'duration')))
                info_tag.setCountries(meta_get(video_data,'country'))
                
                info_tag.setTrailer(meta_get(video_data,'trailer'))
                info_tag.setPremiered(meta_get(video_data,'premiered'))
                
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                
                info_tag.setUniqueIDs({'imdb': imdb_id, 'tmdb':tmdb})
                info_tag.setIMDBNumber(imdb_id)
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                info_tag.setOriginalTitle(original_title)
                info_tag.setTagLine(original_title)
                
            if KODI_VERSION<19:
                listItem.setInfo(type=types, infoLabels=video_data)
                listItem.setUniqueIDs({ 'imdb': imdb_id, 'tmdb' : tmdb }, "imdb")
            
            all_logo,all_n_fan,all_banner,all_clear_art,r_logo,r_art=get_extra_art(tmdb,tv_movie,tvdb_id)
            listItem.setArt({'clearlogo':r_logo,'clearart':r_art,'icon': iconimage, 'thumb': fanart, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage})

            eng_name=''

            if 0:# Addon.getSetting("sync_mod")=='true' and tv_movie=='tv' and len(Addon.getSetting("firebase"))>0:
                table_name='trackt'
                t = Thread(target=write_trackt, args=(original_name_r,url,iconimage,fanart,description,year,original_name_r,season,episode,tmdb,heb_name,show_original_year,original_name_r,isr,tv_movie,table_name,))
                t.start()

            try:
                from sqlite3 import dbapi2 as database
            except:
                from pysqlite2 import dbapi2 as database
            cacheFile=os.path.join(user_dataDir,'database.db')
            dbcon = database.connect(cacheFile)
            dbcur = dbcon.cursor()
            if season!=None and season!=' ' and season!="%20":
               table_name='lastlinktv'
            else:
               table_name='lastlinkmovie'
            dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""o_name TEXT,""name TEXT, ""url TEXT, ""iconimage TEXT, ""fanart TEXT,""description TEXT,""data TEXT,""season TEXT,""episode TEXT,""original_title TEXT,""saved_name TEXT,""heb_name TEXT,""show_original_year TEXT,""eng_name TEXT,""isr TEXT,""prev_name TEXT,""tmdb TEXT);"%table_name)
            dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""tmdb TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')

            dbcon.commit()
            dbcur.execute("DELETE FROM %s"%table_name)
                     
            match = dbcur.fetchone()
            if match==None:
                dbcur.execute("INSERT INTO %s Values ('f_name','%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s');" %  (table_name,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '))
                dbcon.commit()
                try:
                    try:
                        desk=description.replace("'","%27")
                    except:
                        desk=''
                    dbcur.execute("UPDATE %s SET name='%s',url='%s',iconimage='%s',fanart='%s',description='%s',data='%s',season='%s',episode='%s',original_title='%s',saved_name='%s',heb_name='%s',show_original_year='%s',eng_name='%s',isr='%s',prev_name='%s',tmdb='%s' WHERE o_name = 'f_name'"%(table_name,original_title.replace("'","%27"),base64.b64encode(url.encode("utf-8")).decode("utf-8") ,iconimage,fanart,desk,str(show_original_year).replace("'","%27"),season,episode,original_title.replace("'","%27"),original_title.replace("'","%27"),original_title.replace("'","%27"),show_original_year,original_title.replace("'","%27").replace("'","%27"),'0',original_title.replace("'","%27"),tmdb))
                    dbcon.commit()

                except Exception as e:
                    log.warning('Error in Saving Last:'+str(e))
                    pass
            if table_name=='lastlinktv':
                tv_movie='tv'
            else:
                tv_movie='movie'
            dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27"),tv_movie))
            match = dbcur.fetchone()
            dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27").replace(" ","%20"),tv_movie))
            match_space = dbcur.fetchone()
            
            if match==None and match_space!=None:
                cache.clear(['last_view'])
                dbcur.execute("UPDATE Lastepisode SET original_title='%s' WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27"),original_title.replace("'","%27").replace(" ","%20"),tv_movie))
                
                # dbcon.commit()
                dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'","%27"),tv_movie))
                match = dbcur.fetchone()

            try:
                if match==None:
                  cache.clear(['last_view'])
                  try:
                    dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (heb_name.replace("'","%27"),url,iconimage,fanart,description.replace("'","%27"),show_original_year,original_title.replace("'","%27"),season,episode,tmdb,original_title.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),'0',tv_movie))
                    
                  except:
                    try:
                        dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (heb_name.replace("'","%27"),url,iconimage,fanart,description.decode('utf-8').replace("'","%27"),show_original_year,original_title.replace("'","%27"),season,episode,tmdb,original_title.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),'0',tv_movie))

                    except:
                        dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (heb_name.replace("'","%27"),url,iconimage,fanart,' ',show_original_year,original_title.replace("'","%27"),season,episode,tmdb,original_title.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),'0',tv_movie))
                  dbcon.commit()
                 
                else:
                  dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s' and season='%s' and episode='%s'"%(original_title.replace("'","%27"),tv_movie,season,episode))

                  match = dbcur.fetchone()
                  
                  if match==None:
                    cache.clear(['last_view'])
                    dbcur.execute("UPDATE Lastepisode SET season='%s',episode='%s',image='%s',heb_name='%s' WHERE original_title = '%s' and type='%s'"%(season,episode,fanart,heb_name.replace("'","%27"),original_title.replace("'","%27"),tv_movie))
                    dbcon.commit()
            except: pass
            dbcur.close()
            dbcon.close()
            if (Addon.getSetting("auto_trk")=='true'):
                t = Thread(target=jump_seek, args=(original_title,tmdb,season,episode,tvdb_id,))
                t.start()
            if (Addon.getSetting("nextup_episode")=='true' and tv_movie=='tv') or (Addon.getSetting("nextup_movie")=='true' and tv_movie=='movie'):
                t = Thread(target=search_next, args=(dd,tv_movie,tmdb,heb_name,))
                t.start()

            if (Addon.getSetting("skip_intro")=='true' and tv_movie=='tv'):
                t = Thread(target=skip_intro, args=())
                t.start()

            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            if resume_time==-1:
                return 0
        if watched_indicators=='1':

           listItem. setProperty('StartPercent', str(resume_time))
        break_window=True
        ok=xbmc.Player().play(final_link,listitem=listItem)

def play(name,url,data,iconimage,fan,no_subs,tmdb,season,episode,original_title,heb_name,description,resume,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup):
    global break_window,botplay,play_status

    # if Addon.getSetting("free_space")=='true':
        # ok=check_free_space()
        # if not ok:
            # return 0
    
    '''
    link='http://127.0.0.1:%s/'%listen_port+url
    log.warning('Play Link:'+link)
    video_data={}
    video_data['title']=name
    video_data['poster']=fan

    video_data['icon']=iconimage
    
    listItem = xbmcgui.ListItem(video_data['title'], path=link) 
    listItem.setInfo(type='Video', infoLabels=video_data)


    listItem.setProperty('IsPlayable', 'true')

   
       
    ok=xbmc.Player().play(link,listitem=listItem)
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    '''
    if Addon.getSetting('new_play_window2')=='true' :
         # if not tmdb=='0':
            if season!=None and season!=' ' and season!="%20" and season!="0":
               tv_movie='tv'
            else:
               tv_movie='movie'
            t = Thread(target=show_new_window, args=(tv_movie, tmdb, season, episode,fan,))
            t.start()
    else:
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    if '@@@' in url:


        all_s=[]
        play_status='בחר מאיפה לנגן'
        regex='rdlink(.+?)$'
        rd_link=re.compile(regex).findall(url)
        
        regex='telelink(.+?)rdlink'
        tele_link=re.compile(regex).findall(url)

       
        all_s.append('נגן דרך טלמדיה')
        all_s.append('נגן דרך RD')
        ret = xbmcgui.Dialog().select("בחר", all_s)
        plugin = all_s[ret]
        
        if ret == -1:
            break_window=True
            return 0
        if plugin =='נגן דרך RD':

            play_status='מנגן דרך RD'
            
            path=xbmc_tranlate_path('special://home/addons/script.module.resolveurl/lib')
            sys.path.append( path)
            path=xbmc_tranlate_path('special://home/addons/script.module.six/lib')
            sys.path.append( path)
            path=xbmc_tranlate_path('special://home/addons/script.module.kodi-six/libs')
            sys.path.append( path)
            import resolveurl
            try:
                link =resolveurl .HostedMediaFile (url =rd_link[0] ).resolve ()

                video_data={}
                video_data['title']=name.replace('.mp4','').replace('.avi','').replace('.mkv','').replace('-','').replace('Google Drive','').replace('[COLOR lightblue][B]','').replace('[/B][/COLOR]','').replace(' 360','').replace(' 480','').replace(' 720','').replace(' 1080','').strip()
                video_data[u'mpaa']=('heb')
                listItem = xbmcgui.ListItem(video_data['title'], path=link) 
                listItem.setInfo(type='Video', infoLabels=video_data)
                listItem.setArt({'icon': iconimage, 'thumb': fan, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage})
                break_window=True
                resume_time=get_resume(tmdb,name,season,episode)
                if resume_time==-1:
                    return 0
                ok=xbmc.Player().play(link,listitem=listItem)
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                w_time=int(Addon.getSetting("wait_size"))
                fail_play=True
                for _ in range(w_time):
                    
                    try:
                        vidtime = xbmc.Player().getTime()
                    except:
                        vidtime=0
                        pass
                    if xbmc.Player().isPlaying() and vidtime>0:
                        fail_play=False
                        break
                    time.sleep(0.100)
                if resume_time>0:
                    try:
                        xbmc.Player().seekTime(int(float(resume_time-2)))
                    except Exception as e:
                        #log.warning('Seek Err:'+str(e))
                        pass
                try:
                  cond=xbmc.abortRequested
                except:
                   cond=xbmc.Monitor().abortRequested()
                while (not cond) and (xbmc.Player().isPlaying()):
                     try:
                        vidtime = xbmc.Player().getTime()
                     except:
                        vidtime = 0
                     try:
                        g_timer=xbmc.Player().getTime()
                        g_item_total_time=xbmc.Player().getTotalTime()
                     except:
                        pass
                     time.sleep(0.1)

                if resume_time!=-1:
                    update_db_link(tmdb,name,season,episode,g_timer,g_item_total_time)
                return 0
            except Exception as e:
                logging.warning('Error in RD turkish'+str(e))
                play_status='ניגון דרך RD נכשל'
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'ניגון דרך RD נכשל'),'[COLOR %s]מנגן דרך טלמדיה[/COLOR]' % COLOR2)
                url=tele_link[0]
        if plugin =='נגן דרך טלמדיה':
            url=tele_link[0]
    if 'google.com' in url:
        try:
            dialog = xbmcgui.DialogBusy()
            dialog.create()
        except:pass
        all_n=[]
        if '$$$' in url:
            final_links=[]
            all_urls=url.split('$$$')
            for ite in all_urls:
                if ite not in final_links:
                    final_links.append(ite)
            all_urls=final_links
        else:
            all_urls=[url]
        if len(all_urls)>1:
            for itt in all_urls:
                
                if 'upfile' in url:
                    f_link,name=get_upfile_det(itt)
                    if f_link==0:
                        return 0
                    
                    all_n.append(name)
                else:
                    all_n.append(re.compile('//(.+?)/').findall(itt)[0])
            ret = xbmcgui.Dialog().select("choose", all_n)
            if ret!=-1:
                if 'google' in all_urls[ret] and '?' in all_urls[ret] and 'google.com/open?' not in all_urls[ret]:
                    all_urls[ret]=all_urls[ret].split('?')[0]
                all_urls=[all_urls[ret]]
                
            else:
              return 0
        else:
            all_urls=[all_urls[0]]
        all_l=[]
        all_n=[]
        
        for items in all_urls:
            if 'upfile' in url:
                f_link,name=get_upfile_det(items)
                if f_link==0:
                    return 0
                all_l.append(f_link)
                all_n.append(name)
            if 'youtu' in items:
                if 'youtu.be' in items:
                    
                    items=requests.get(items).url
                regex='v\=(.+?)$'
                video_id=re.compile(regex).findall(items)[0]
                if 'list=' in items:
                    video_id=items.split ('list=')[1 ]
                    playback_url = 'plugin://plugin.video.youtube/play/?playlist_id=%s&order=shuffle&play=1'%video_id
                else:
                    playback_url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
                xbmc.executebuiltin('RunPlugin(%s)'%playback_url)
                return 0
                all_l.append(playback_url)
                all_n.append(name)
            if 'drive.google' in items or 'docs.google' in items:
              
              if 'docs.googleusercontent.com' in items:
                return 0
              
              if '=' in items and 'usp=' not in items:
                id=items.split('=')[-1]
            
              else:
               regex='/d/(.+?)/view'
               match=re.compile(regex).findall(items)
               if len(match)>0:
                 id=match[0]
               else:
                 regex='/d/(.+?)/preview'
                 match=re.compile(regex).findall(items)
                 if len(match)>0:
                    id=match[0]
                 else:
                    regex='/d/(.+?)$'
                    match=re.compile(regex).findall(items)
                    if len(match)>0:
                        id=match[0]
                    else:
                        regex='id=(.+?)$'
                        match=re.compile(regex).findall(items)
                        id=match[0]
              f_link,name= googledrive_resolve(id)
              if f_link=='Download':
                   f_link= googledrive_download(id)
                   name='Download '+str(name)
                   
              count=0
              if '$$$' in f_link:
                for item in f_link.split('$$$'):
                    all_l.append(item)
                    all_n.append(name[count])
                    count+=1
              else:
                all_l.append(f_link)
                all_n.append(name)
        if len(all_l)==1:
            final_link=all_l[0]
            name=all_n[0]
        elif len(all_l)>0:
            #"choose"
            ret = xbmcgui.Dialog().select(Addon.getLocalizedString(32028), all_n)
            if ret!=-1:
                final_link=all_l[ret]
                name=all_n[ret]
            else:
              return 0
        else:
            final_link=all_urls[0]
        if 'twitch' in final_link:
            twitch_p=os.path.join(xbmc_tranlate_path("special://home/addons/"),'plugin.video.twitch')
            if os.path.exists(twitch_p):
            
                regex='https://www.twitch.tv/(.+?)(?:$| |\r|\n|\t)'
                #ids=final_link.split('/')
                f_id=re.compile(regex).findall(final_link)[0]
                
                
                xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.twitch/?content=streams&mode=search_results&query=%s",return)'%f_id)          
            else:
                copy2clip('https://github.com/MrSprigster/Twitch-on-Kodi/releases/download/2.4.8/plugin.video.twitch-2.4.8.zip')
                xbmcgui.Dialog().ok('Error occurred','You need Twich addon to play this link\n link was copied to clipboard')
                
            return 0

        video_data={}
        if season!=None and season!=' ' and season!="%20" and season!="0":
           video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
           video_data['mediatype']='tvshow'
           
        else:
           video_data['mediatype']='movies'
        if season!=None and season!=' ' and season!="%20" and season!="0":
           tv_movie='tv'
           url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        else:
           tv_movie='movie'
           
           url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
        if 'tt' not in tmdb:
             try:
                
                imdb_id=requests.get(url2,timeout=10).json()['external_ids']['imdb_id']

             except Exception as e:
                imdb_id=" "
        else:
            imdb_id=tmdb
        video_data['title']=name.replace('.mp4','').replace('.avi','').replace('.mkv','').replace('-','').replace('Google Drive','').replace('[COLOR lightblue][B]','').replace('[/B][/COLOR]','').replace(' 360','').replace(' 480','').replace(' 720','').replace(' 1080','').strip()
        #log.warning(video_data['title'])
        video_data['Writer']=tmdb
        video_data['season']=season
        video_data['episode']=episode
        video_data['plot']='from_telemedia'
        video_data['imdb']=imdb_id
        video_data['code']=imdb_id
        video_data['year']=data
        video_data['imdbnumber']=imdb_id
        
        video_data['imdb_id']=imdb_id
        video_data['IMDBNumber']=imdb_id
        video_data['genre']=imdb_id
        if no_subs=='1':
           video_data[u'mpaa']=('heb')
        if 'HebSub' in name:
              video_data[u'mpaa']=('heb')
        listItem = xbmcgui.ListItem(video_data['title'], path=final_link) 
        listItem.setInfo(type='Video', infoLabels=video_data)
        listItem.setProperty('IsPlayable', 'true')
        resume_time=get_resume(tmdb,name,season,episode)
        if resume_time==-1:
            return 0
        break_window=True
        ok=xbmc.Player().play(final_link,listitem=listItem)
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
        w_time=int(Addon.getSetting("wait_size"))
        fail_play=True
        for _ in range(w_time):
            
            try:
                vidtime = xbmc.Player().getTime()
            except:
                vidtime=0
                pass
            if xbmc.Player().isPlaying() and vidtime>0:
                fail_play=False
                break
            time.sleep(0.100)
        if resume_time>0:
            try:
                xbmc.Player().seekTime(int(float(resume_time-2)))
            except Exception as e:
                #log.warning('Seek Err:'+str(e))
                pass
        try:
          cond=xbmc.abortRequested
        except:
           cond=xbmc.Monitor().abortRequested()
        while (not cond) and (xbmc.Player().isPlaying()):
             try:
                vidtime = xbmc.Player().getTime()
             except:
                vidtime = 0
             try:
                g_timer=xbmc.Player().getTime()
                g_item_total_time=xbmc.Player().getTotalTime()
             except:
                pass
             time.sleep(0.1)

        if resume_time!=-1:
            update_db_link(tmdb,name,season,episode,g_timer,g_item_total_time)
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    else:
        l_data=json.loads(url)
        
        if Addon.getSetting("super_bot")=='true' or botplay is True:

            if Addon.getSetting('new_play_window2')=='false' or kitana=='false':
                xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
               # xbmc.executebuiltin('ActivateWindow(busydialognocancel)')

            dp = xbmcgui.DialogProgress()
            
            f_link=get_direct_bot_link(l_data)
            # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', f_link)))

            if f_link=='play_tele':
                    url=l_data['id']
                    monitor=TelePlayer()
                    broken_play,resume_time=monitor.playTeleFile(url,data,name,no_subs,tmdb,season,episode,original_title,heb_name,description,iconimage,fan,resume,l_data,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true')
                    return 0
            if f_link!='Found':
                if not resume:
                    resume_time=get_resume(tmdb,name,season,episode)
                else:
                    resume_time=resume
                
                if resume_time==-1:
                    return 0
                
                play_status='מתחיל ניגון'
                play_direct(f_link,data,name,no_subs,tmdb,season,episode,original_title,description,resume,resume_time,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line)
                #log.warning('2')
                broken_play=True
                w_time=int(Addon.getSetting("wait_size"))
                dp.create('Anonymous Power','Playing')
                dp.update(0, 'Playing...')
                dp.close()
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                g_timer=None
                timex=resume_time
                try:
                  cond=xbmc.abortRequested
                except:
                   cond=xbmc.Monitor().abortRequested()
                while (not cond) and (xbmc.Player().isPlaying()):

                     try:
                        vidtime = xbmc.Player().getTime()
                     except:
                        vidtime = 0
                     try:
                        g_timer=xbmc.Player().getTime()
                        g_item_total_time=xbmc.Player().getTotalTime()
                     except:
                        pass
                     time.sleep(0.1)
                     if watched_indicators=='0':
                         if resume_time>0:
                            try:
                                if vidtime>0.2:

                                    xbmc.Player().seekTime(int(float(resume_time-2)))
                                    resume_time=0
                            except Exception as e:
                                log.warning('Seek Err:'+str(e))
                                pass
                
                if timex!=-1 and g_timer:
                    t = Thread(target=update_db_link, args=(tmdb,name,season,episode,g_timer,g_item_total_time,))
                    t.start()
                    # thread=[]
                    # thread.append(Thread(update_db_link,tmdb,name,season,episode,g_timer,g_item_total_time))

                    
                    # thread[0].start()

                xbmc.executebuiltin("Dialog.Close(busydialog)")
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')

                return 0

        try:
            url=l_data['id']
            monitor=TelePlayer()
            broken_play,resume_time=monitor.playTeleFile(url,data,name,no_subs,tmdb,season,episode,original_title,heb_name,description,iconimage,fan,resume,l_data,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup)
            try_next_player=Addon.getSetting("next_player_option")=='true'
            if resume_time==-1:
                return 0
            if broken_play and try_next_player:
                # xbmc.Player().stop()

                t = Thread(target=clear_files, args=())
                t.start()
                dp = xbmcgui.DialogProgress()
                dp.create('Please Wait...','Playing')
                dp.update(0, 'Please Wait...'+'\n'+'Playing')
                global bot
                if bot==False:
                    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous Power Bot'),'[COLOR %s]המתן...[/COLOR]' % COLOR2)

                
                f_link=get_direct_bot_link(l_data)
                if f_link=='play_tele':
                    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'לא הצליח לנגן'),'[COLOR %s]נסה לינק אחר[/COLOR]' % COLOR2)
                        # url=l_data['id']
                        # monitor=TelePlayer()
                        # broken_play,resume_time=monitor.playTeleFile(url,data,name,no_subs,tmdb,season,episode,original_title,heb_name,description,iconimage,fan,resume,l_data,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true',checks='true')
                        # return 0
                play_direct(f_link,data,name,no_subs,tmdb,season,episode,original_title,description,resume,resume_time,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line)
                broken_play=True
                w_time=int(Addon.getSetting("wait_size"))
                if kitana=='true':

                    return 0
                else:
                    for _ in range(w_time):

                        dp.update(0,'Playing...'+'\n'+Addon.getLocalizedString(32040)+' : '+str(_)+'\n'+ '' )
                        try:
                            vidtime = xbmc.Player().getTime()
                        except:
                            vidtime=0
                            pass
                        if xbmc.Player().isPlaying() and vidtime>0:
                            broken_play=False
                            
                            break
                        if dp.iscanceled():
                            dp.close()
                            broken_play=False
                            # xbmc.Player().stop()
                            break
                        time.sleep(0.100)

                    dp.close()
                    g_timer=None
                    try:
                      cond=xbmc.abortRequested
                    except:
                       cond=xbmc.Monitor().abortRequested()
                    while (not cond) and (xbmc.Player().isPlaying()):
                         try:
                            vidtime = xbmc.Player().getTime()
                         except:
                            vidtime = 0
                         try:
                            g_timer=xbmc.Player().getTime()
                            g_item_total_time=xbmc.Player().getTotalTime()
                         except:
                            pass
                         time.sleep(0.1)
                         if resume_time>0:
                         
                            if watched_indicators=='0':
                                try:
                                    if vidtime>0.2:
                                        xbmc.Player().seekTime(int(float(resume_time-2)))
                                        resume_time=0
                                except Exception as e:
                                    log.warning('Seek Err:'+str(e))
                                    pass
                    
                    if resume_time!=-1 and g_timer:
                        
                        update_db_link(tmdb,name,season,episode,g_timer,g_item_total_time)
                    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                    return 0
        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
        
    
def get_upfile_det(url):
    
    name=''
    #log.warning(url)
    headers = {
  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    
    'Content-Type': 'application/json;charset=utf-8',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }
    html=requests.get(url,headers=headers).content
    
       
    regex='<title>(.+?)</title>.+?<input type="hidden" value="(.+?)" name="hash">'
    match=re.compile(regex,re.DOTALL).findall(html)
    if len(match)==0:
         xbmcgui.Dialog().ok('Error occurred','Link is down')
         return 0,0
    for name,link in match:
      id=url.split('/')[-1]
      id=id.replace('.html','').replace('.htm','')
      
      playlink='http://down.upfile.co.il/downloadnew/file/%s/%s'%(id,link)
    return playlink,name

def get_upfile_det(url):
    
    name=''
    headers = {
  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    
    'Content-Type': 'application/json;charset=utf-8',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }
    html=requests.get(url,headers=headers).content
    
       
    regex='<title>(.+?)</title>.+?<input type="hidden" value="(.+?)" name="hash">'
    match=re.compile(regex,re.DOTALL).findall(html)
    if len(match)==0:
         xbmcgui.Dialog().ok('Error occurred','Link is down')
         return 0,0
    for name,link in match:
      id=url.split('/')[-1]
      id=id.replace('.html','').replace('.htm','')
      
      playlink='http://down.upfile.co.il/downloadnew/file/%s/%s'%(id,link)
    return playlink,name
def post_trk(id,season,episode,progress=False,len_progress='',type_progress='',tvdb_id=''):
    
    from resources.modules.general import post_trakt
    # from  resources.modules.client import  get_html
    if (len(id)>1 and id!='%20') or len(tvdb_id)>1:
         if season!=None and season!=' ' and season!="%20":

           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           if progress:
            ur='https://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d'%(id,season,episode)
            yy=requests.get(ur).json()
            f_id=''
            if 'id' in yy:
                f_id=yy['id']
            ddata={"progress": int(len_progress), "episode": {"ids": {"tmdb": f_id,'tvdb':tvdb_id}}}

            i = (post_trakt('/scrobble/'+type_progress, data=ddata))
           else:
               i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id,'tvdb':tvdb_id}}]}))

         else:
           if progress:
               i = (post_trakt('/scrobble/'+type_progress,data= {'movie': {'ids': {'tmdb': id}}, 'progress': int(len_progress)}))
           else:
                i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))

def googledrive_download(id):
    import urllib.request
    import sys
    import io,time
    # keys=[]
    headers = {
        'authority': 'drive.google.com',
        'content-length': '0',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'origin': 'https://drive.google.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://drive.google.com/uc?id=%s&export=download'%id,
        'accept-language': 'he-IL,he;q=0.9',
    }

    url='https://drive.google.com/uc?id=%s&export=download&confirm=t'%id
    # logging.warning(url)
    # req = urllib.request.Request(url, headers=headers)
    # resp = urllib.request.urlopen(req)
    # length = resp.getheader('content-length')

    keys=url

    # LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, keys),'[COLOR %s]מקור לא תקין, בחר מקור אחר.[/COLOR]' % COLOR2)
    return(keys)
def fix_q(quality):
    
    
    if '1080' in quality:
      f_q=0
    elif '720' in quality:
      f_q=1
    elif '480' in quality:
      f_q=2
   
    elif '360' in quality or 'sd' in quality.lower():
      f_q=3
   
    return f_q
def getPublicStream(url):
        try:
            import http.cookiejar as cookielib
        except:
            import cookielib
        import mediaurl,urllib

        pquality=-1
        pformat=-1
        acodec=-1
        fmtlist=[]
        mediaURLs = []
  
       
        cookies = cookielib.LWPCookieJar()
        try:
            handlers = [
                urllib.request.HTTPHandler(),
                urllib.request.HTTPSHandler(),
                urllib.request.HTTPCookieProcessor(cookies)
                ]
            opener = urllib.request.build_opener(*handlers)
            #log.warning(url)
            req = urllib.request.Request(url)
        except Exception as e:
            log.warning(e)
            import urllib2
            handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies)
            ]
            opener = urllib2.build_opener(*handlers)
            log.warning(url)
            req = urllib2.Request(url)
        req.add_header('User-agent',__USERAGENT__)
        result= opener.open(req)
        for cookie in cookies:
            if cookie.name=='DRIVE_STREAM':
              value=cookie.value

        #response = urllib.urlopen(req)
        
        response_data = result.read()
        #response.close()




        regex='<title>(.+?)</title>'
        name=re.compile(regex).findall(response_data)[0]
        for r in re.finditer('\"fmt_list\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            fmtlist = r.group(1)

        title = ''
        for r in re.finditer('\"title\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            title = r.group(1)


        if fmtlist==[]:
            return 'Download',None,name
        itagDB={}
        containerDB = {'x-flv':'flv', 'webm': 'WebM', 'mp4;+codecs="avc1.42001E,+mp4a.40.2"': 'MP4'}
        for r in re.finditer('(\d+)/(\d+)x(\d+)/(\d+/\d+/\d+)\&?\,?' ,
                               fmtlist, re.DOTALL):
              (itag,resolution1,resolution2,codec) = r.groups()

              if codec == '9/0/115':
                itagDB[itag] = {'resolution': resolution2, 'codec': 'h.264/aac'}
              elif codec == '99/0/0':
                itagDB[itag] = {'resolution': resolution2, 'codec': 'VP8/vorbis'}
              else:
                itagDB[itag] = {'resolution': resolution2}

        for r in re.finditer('\"url_encoded_fmt_stream_map\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            urls = r.group(1)


        
        urls = urllib.unquote(urllib.unquote(urllib.unquote(urllib.unquote(urllib.unquote(urls)))))
        urls = re.sub('\\\\u003d', '=', urls)
        urls = re.sub('\\\\u0026', '&', urls)


#        urls = re.sub('\d+\&url\='+self.PROTOCOL, '\@', urls)
        urls = re.sub('\&url\='+ 'https://', '\@', urls)

#        for r in re.finditer('\@([^\@]+)' ,urls):
#          videoURL = r.group(0)
#        videoURL1 = self.PROTOCOL + videoURL


        # fetch format type and quality for each stream
        count=0
        
        for r in re.finditer('\@([^\@]+)' ,urls):
                videoURL = r.group(1)
                for q in re.finditer('itag\=(\d+).*?type\=video\/([^\&]+)\&quality\=(\w+)' ,
                             videoURL, re.DOTALL):
                    (itag,container,quality) = q.groups()
                    count = count + 1
                    order=0
                    if pquality > -1 or pformat > -1 or acodec > -1:
                        if int(itagDB[itag]['resolution']) == 1080:
                            if pquality == 0:
                                order = order + 1000
                            elif pquality == 1:
                                order = order + 3000
                            elif pquality == 3:
                                order = order + 9000
                        elif int(itagDB[itag]['resolution']) == 720:
                            if pquality == 0:
                                order = order + 2000
                            elif pquality == 1:
                                order = order + 1000
                            elif pquality == 3:
                                order = order + 9000
                        elif int(itagDB[itag]['resolution']) == 480:
                            if pquality == 0:
                                order = order + 3000
                            elif pquality == 1:
                                order = order + 2000
                            elif pquality == 3:
                                order = order + 1000
                        elif int(itagDB[itag]['resolution']) < 480:
                            if pquality == 0:
                                order = order + 4000
                            elif pquality == 1:
                                order = order + 3000
                            elif pquality == 3:
                                order = order + 2000
                    try:
                        if itagDB[itag]['codec'] == 'VP8/vorbis':
                            if acodec == 1:
                                order = order + 90000
                            else:
                                order = order + 10000
                    except :
                        order = order + 30000

                    try:
                        if containerDB[container] == 'MP4':
                            if pformat == 0 or pformat == 1:
                                order = order + 100
                            elif pformat == 3 or pformat == 4:
                                order = order + 200
                            else:
                                order = order + 300
                        elif containerDB[container] == 'flv':
                            if pformat == 2 or pformat == 3:
                                order = order + 100
                            elif pformat == 1 or pformat == 5:
                                order = order + 200
                            else:
                                order = order + 300
                        elif containerDB[container] == 'WebM':
                            if pformat == 4 or pformat == 5:
                                order = order + 100
                            elif pformat == 0 or pformat == 1:
                                order = order + 200
                            else:
                                order = order + 300
                        else:
                            order = order + 100
                    except :
                        pass

                    try:
                        mediaURLs.append( mediaurl.mediaurl('https://' + videoURL, itagDB[itag]['resolution'] + ' - ' + containerDB[container] + ' - ' + itagDB[itag]['codec'], str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
                    except KeyError:
                        mediaURLs.append(mediaurl.mediaurl('https://'+ videoURL, itagDB[itag]['resolution'] + ' - ' + container, str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
        
        return mediaURLs,value,name
def googledrive_resolve(id):
    path=xbmc_tranlate_path('special://home/addons/script.module.resolveurl/lib')
    sys.path.append( path)
    path=xbmc_tranlate_path('special://home/addons/script.module.six/lib')
    sys.path.append( path)
    path=xbmc_tranlate_path('special://home/addons/script.module.kodi-six/libs')
    sys.path.append( path)
    import resolveurl
    try:
        f_link =resolveurl .HostedMediaFile (url =items ).resolve ()
    except:
        return 'Download',[]
    #log.warning(id)
    global tv_mode
    links_data,cookie,name=getPublicStream('https://drive.google.com/file/d/'+id+'/view')
    if links_data=='Download':
        return 'Download',name
    mediaURLs = sorted(links_data)
    options = []
    all_mediaURLs=[]
    for mediaURL in mediaURLs:
        #log.warning(mediaURL.qualityDesc)
        if '4k' in mediaURL.qualityDesc:
           
           options.append('4000')
        elif '1080' in mediaURL.qualityDesc:
           
           options.append('1080')
        elif '720' in mediaURL.qualityDesc:
           
           options.append('720')
        elif '480' in mediaURL.qualityDesc:
           
           options.append('480')
        elif '360' in mediaURL.qualityDesc:
           
           options.append('360')
        elif '240' in mediaURL.qualityDesc:
           
           options.append('240')
        else:
           
           options.append('0')
        all_mediaURLs.append((mediaURL.url,fix_q(mediaURL.qualityDesc)))
    qualities=options
    qualities=sorted(options, key=lambda x: x[0], reverse=False)
    all_mediaURLs=sorted(all_mediaURLs, key=lambda x: x[1], reverse=False)
    
    if Addon.getSetting("auto_q")=='true':
            all_n=[]
            playbackURL,qul = all_mediaURLs[0]
            playbackURL=playbackURL+'||Cookie=DRIVE_STREAM%3D'+cookie
            all_n.append(name+' - [COLOR lightblue][B]'+str(options[0])+'[/B][/COLOR]')
    else:
        #ret = xbmcgui.Dialog().select("Choose", options)
        #if ret==-1:
        #    sys.exit()
        all_l=[]
        all_n=[]
        count=0
        for items in mediaURLs:
            all_l.append(items.url+'||Cookie=DRIVE_STREAM%3D'+cookie)
            all_n.append(name+' - [COLOR lightblue][B]'+str(options[count])+'[/B][/COLOR]')
            count+=1
        playbackURL = '$$$'.join(all_l)#[ret].url


    if len(all_n)==1:
        all_n=all_n[0]
    return playbackURL ,all_n

def get_resume(tmdb,saved_name,season,episode):
        global original_title,break_window,play_status
        play_status='בודק נקודת צפייה אחרונה'
        if original_title =='':
          original_title=saved_name
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        dbcon.commit()
        if len(str(tmdb))>2:
            dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(tmdb,str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))

        else:
            dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(saved_name.replace("'","%27"),str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))

        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_time")=='true' and len(Addon.getSetting("firebase"))>0:
            if Addon.getSetting('new_play_window2')=='false':
                xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
            try:
                all_db=read_firebase('playback')
                match=[]
                # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', season)))
                # str(season)!=None
                # logging.warning('dssssss'+str(season))
                if str(season)!=None and str(season)!=' ' and str(season)!="%20" and str(season)!="0":
                    if all_db =={}:
                      match_playtime=None
                    for itt in all_db:
                        if all_db[itt]['original_title']==original_title:
                         if all_db[itt]['season']==str(season):
                          if all_db[itt]['episode']==str(episode):
                            items=all_db[itt]
                            match.append((items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
                            break
                          else:
                           match_playtime=None
                         else:
                           match_playtime=None
                        else:
                           match_playtime=None
                else:
                    if all_db =={}:
                      match_playtime=None
                    for itt in all_db:
                        if all_db[itt]['original_title']==original_title:
                            items=all_db[itt]
                            match.append((items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
                            break
                        else:
                           match_playtime=None
                all_names={}
                count_m=0
                for name,tmdb,season,episode,playtime,totaltime,free in match:

                    all_names[name]=[]
                    all_names[name].append((name,tmdb,season,episode,str(playtime),str(totaltime),free))

                for items in all_names:
                  match_playtime=name,tmdb,season,episode,playtime,totaltime,free=all_names[items][0]
            except:
             match_playtime = dbcur.fetchone()

        else:
         match_playtime = dbcur.fetchone()

        if match_playtime!=None:

            name_r,timdb_r,season_r,episode_r,playtime,totaltime,free=match_playtime
            res={}
            res['wflag']=False
            res['resumetime']=playtime
            res['totaltime']=totaltime
        else:
            res=False
            
        set_runtime=0
        if res:
            if not res['wflag']:

                if res['resumetime']!=None:

                    #Resume From 
                    choose_time=Addon.getLocalizedString(32042)+time.strftime("%H:%M:%S", time.gmtime(float(res['resumetime'])))
                    
                    if float(res['resumetime'])>=(100*(float(res['totaltime']))):
                        selection=1
                        clicked=1
                    else:
                        if Addon.getSetting("new_time_window")=='true':
                            selection,clicked=selection_time_window(choose_time,iconimage,fanart,heb_name,(100*(float(res['resumetime'])/(float(res['totaltime'])+1))))
                        else:

                            selection,clicked=selection_time_menu('Menu',choose_time)
                        # window = selection_time('Menu',choose_time)
                        # window.doModal()
                        # selection = window.get_selection()
                        # clicked=window.clicked
                        # del window
                    if clicked==0:
                        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                        break_window=True
                        set_runtime=-1
                        return -1
                    if selection==-1:
                       stop_auto_play=1
                       resume_time=-1
                       
                       return 0
                    if selection==0:
                        
                        set_runtime=float(res['resumetime'])
                        set_total=res['totaltime']
                        
                        
                    elif selection==1:
                        
                        
                        set_runtime=0
                        set_total=res['totaltime']
        dbcur.close()
        dbcon.close()
        return set_runtime
def update_db_link(tmdb,saved_name,season,episode,g_timer,g_item_total_time):
        global original_title
        if original_title=='':
         original_title=saved_name
        #log.warning('TMDB:'+str(saved_name))
        table_name='playback'
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
        dbcon.commit()
        season=season.replace('%20','0').replace(' ','0')
        episode=episode.replace('%20','0').replace(' ','0')
        if len(str(tmdb))<2  and tmdb!='%20':
            only_name=True
            dbcur.execute("SELECT * FROM playback where name='%s' and season='%s' and episode='%s'"%(saved_name.replace("'","%27"),season,episode))
        else:
            only_name=False
            dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' and episode='%s'"%(tmdb,season,episode))
        match = dbcur.fetchall()

        if match==None:
          dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (saved_name.replace("'","%27"),tmdb,season,episode,str(g_timer),str(g_item_total_time),' '))
          dbcon.commit()
          if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
                

                    all_firebase=read_firebase(table_name)
                    write_fire=True
                    for items in all_firebase:
                  
                        if all_firebase[items]['original_title']==original_title:
                         if all_firebase[items]['season']==season:
                          if all_firebase[items]['episode']==episode:
                            delete_firebase(table_name,items)

                            break

                    if write_fire:

                        write_firebase(original_title,tmdb,season,episode,str(g_timer),str(g_item_total_time),'',table_name)

        else:
           if len(match)>0:
            name,timdb,season,episode,playtime,totaltime,free=match[0]
            if str(g_timer)!=playtime:
                if only_name:
                    dbcur.execute("UPDATE playback SET playtime='%s' where name='%s' and  season='%s' and episode='%s'"%(str(g_timer),saved_name.replace("'","%27"),season,episode))
                else:
                    dbcur.execute("UPDATE playback SET playtime='%s' where tmdb='%s' and  season='%s' and episode='%s'"%(str(g_timer),tmdb,season,episode))
                dbcon.commit()
                
                if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:

                            all_firebase=read_firebase(table_name)
                            write_fire=True
                            for items in all_firebase:
                          
                                if all_firebase[items]['original_title']==original_title:
                                 if all_firebase[items]['season']==season:
                                  if all_firebase[items]['episode']==episode:
                                    delete_firebase(table_name,items)

                                    break

                            if write_fire:

                                write_firebase(original_title,timdb,season,episode,str(g_timer),str(totaltime),'',table_name)


           else:
                dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (saved_name.replace("'","%27"),tmdb,season,episode,str(g_timer),str(g_item_total_time),' '))
                dbcon.commit()
                if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:

                            all_firebase=read_firebase(table_name)
                            write_fire=True
                            for items in all_firebase:
                          
                                if all_firebase[items]['original_title']==original_title:
                                 if all_firebase[items]['season']==season:
                                  if all_firebase[items]['episode']==episode:
                                    delete_firebase(table_name,items)

                                    break

                            if write_fire:

                                write_firebase(original_title,tmdb,season,episode,str(g_timer),str(g_item_total_time),'',table_name)

        dbcur.close()
        dbcon.close()
def copy2clip(txt):
    import subprocess
    platform = sys.platform
    #log.warning(platform)
    if platform == 'win32':
        try:
            cmd = 'echo ' + txt.strip() + '|clip'
            return subprocess.check_call(cmd, shell=True)
            pass
        except:
            pass
    elif platform == 'linux2':
        try:
            from subprocess import Popen, PIPE

            p = Popen(['xsel', '-pi'], stdin=PIPE)
            p.communicate(input=txt)
        except:
            pass
    else:
        pass
    pass
def play_link(name,url,icon,fan,no_subs,tmdb,season,episode,original_title):

    all_n=[]
    if '$$$' in url:
        final_links=[]
        all_urls=url.split('$$$')
        for ite in all_urls:
            if ite not in final_links:
                final_links.append(ite)
        all_urls=final_links
    else:
        all_urls=[url]
    if len(all_urls)>1:
        for itt in all_urls:
            
            if 'upfile' in url:
                f_link,name=get_upfile_det(itt)
                if f_link==0:
                    return 0
                
                all_n.append(name)
            else:
                all_n.append(re.compile('//(.+?)/').findall(itt)[0])
        ret = xbmcgui.Dialog().select("choose", all_n)
        if ret!=-1:
            if 'google' in all_urls[ret] and '?' in all_urls[ret] and 'google.com/open?' not in all_urls[ret]:
                all_urls[ret]=all_urls[ret].split('?')[0]
            all_urls=[all_urls[ret]]
            
        else:
          return 0
    else:
        all_urls=[all_urls[0]]
    all_l=[]
    all_n=[]
    
    for items in all_urls:
        if 'upfile' in url:
            f_link,name=get_upfile_det(items)
            if f_link==0:
                return 0
            all_l.append(f_link)
            all_n.append(name)
        if 'youtu' in items:
            if 'youtu.be' in items:
                
                items=requests.get(items).url
            regex='v\=(.+?)$'
            video_id=re.compile(regex).findall(items)[0]
            if 'list=' in items:
                video_id=items.split ('list=')[1 ]
                playback_url = 'plugin://plugin.video.youtube/play/?playlist_id=%s&order=shuffle&play=1'%video_id
            else:
                playback_url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
            xbmc.executebuiltin('RunPlugin(%s)'%playback_url)
            return 0
            all_l.append(playback_url)
            all_n.append(name)
        if 'drive.google' in items or 'docs.google' in items:
          
          if 'docs.googleusercontent.com' in items:
            return 0
          
          if '=' in items and 'usp=' not in items:
            id=items.split('=')[-1]
        
          else:
           regex='/d/(.+?)/view'
           match=re.compile(regex).findall(items)
           if len(match)>0:
             id=match[0]
           else:
             regex='/d/(.+?)/preview'
             match=re.compile(regex).findall(items)
             if len(match)>0:
                id=match[0]
             else:
                regex='/d/(.+?)$'
                match=re.compile(regex).findall(items)
                if len(match)>0:
                    id=match[0]
                else:
                    regex='id=(.+?)$'
                    match=re.compile(regex).findall(items)
                    id=match[0]
          f_link,name= googledrive_resolve(id)
          if f_link=='Download':
               f_link= googledrive_download(id)
               name='Download '+str(name)
               
          count=0
          if '$$$' in f_link:
            for item in f_link.split('$$$'):
                all_l.append(item)
                all_n.append(name[count])
                count+=1
          else:
            all_l.append(f_link)
            all_n.append(name)
    if len(all_l)==1:
        final_link=all_l[0]
        name=all_n[0]
    elif len(all_l)>0:
        #"choose"
        ret = xbmcgui.Dialog().select(Addon.getLocalizedString(32028), all_n)
        if ret!=-1:
            final_link=all_l[ret]
            name=all_n[ret]
        else:
          return 0
    else:
        final_link=all_urls[0]
    if 'twitch' in final_link:
        twitch_p=os.path.join(xbmc_tranlate_path("special://home/addons/"),'plugin.video.twitch')
        if os.path.exists(twitch_p):
        
            regex='https://www.twitch.tv/(.+?)(?:$| |\r|\n|\t)'
            #ids=final_link.split('/')
            f_id=re.compile(regex).findall(final_link)[0]
            
            
            xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.twitch/?content=streams&mode=search_results&query=%s",return)'%f_id)          
        else:
            copy2clip('https://github.com/MrSprigster/Twitch-on-Kodi/releases/download/2.4.8/plugin.video.twitch-2.4.8.zip')
            xbmcgui.Dialog().ok('Error occurred','You need Twich addon to play this link\n link was copied to clipboard')
            
        return 0

    video_data={}
    if season!=None and season!=' ' and season!="%20" and season!="0":
       video_data['TVshowtitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
       video_data['mediatype']='tvshow'
       
    else:
       video_data['mediatype']='movies'
    if season!=None and season!=' ' and season!="%20" and season!="0":
       tv_movie='tv'
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
    else:
       tv_movie='movie'
       
       url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&append_to_response=external_ids'%(tmdb,'653bb8af90162bd98fc7ee32bcbbfb3d')
    if 'tt' not in tmdb:
         try:
            
            imdb_id=requests.get(url2,timeout=10).json()['external_ids']['imdb_id']

         except Exception as e:
            imdb_id=" "
    else:
        imdb_id=tmdb
    video_data['title']=name.replace('.mp4','').replace('.avi','').replace('.mkv','').replace('-','').replace('Google Drive','').replace('[COLOR lightblue][B]','').replace('[/B][/COLOR]','').replace(' 360','').replace(' 480','').replace(' 720','').replace(' 1080','').strip()
    #log.warning(video_data['title'])
    video_data['Writer']=tmdb
    video_data['season']=season
    video_data['episode']=episode
    video_data['plot']='from_telemedia'
    video_data['imdb']=imdb_id
    video_data['code']=imdb_id
    video_data['year']=data
    video_data['imdbnumber']=imdb_id
    
    video_data['imdb_id']=imdb_id
    video_data['IMDBNumber']=imdb_id
    video_data['genre']=imdb_id
    if no_subs=='1':

          video_data[u'mpaa']=('heb')
    if 'HebSub' in name:

            video_data[u'mpaa']=('heb')
    listItem = xbmcgui.ListItem(video_data['title'], path=final_link) 
    listItem.setInfo(type='Video', infoLabels=video_data)
    listItem.setProperty('IsPlayable', 'true')
    resume_time=get_resume(tmdb,name,season,episode)
    if resume_time==-1:
        return 0
        
    ok=xbmc.Player().play(final_link,listitem=listItem)
    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    w_time=int(Addon.getSetting("wait_size"))
    fail_play=True
    for _ in range(w_time):
        
        try:
            vidtime = xbmc.Player().getTime()
        except:
            vidtime=0
            pass
        if xbmc.Player().isPlaying() and vidtime>0:
            fail_play=False
            break
        time.sleep(0.100)
    if resume_time>0:
        try:
            xbmc.Player().seekTime(int(float(resume_time-2)))
        except Exception as e:
            #log.warning('Seek Err:'+str(e))
            pass
    try:
      cond=xbmc.abortRequested
    except:
       cond=xbmc.Monitor().abortRequested()
    g_timer=0
    g_item_total_time=0
    while (not cond) and (xbmc.Player().isPlaying()):
         try:
            vidtime = xbmc.Player().getTime()
         except:
            vidtime = 0
         try:
            g_timer=xbmc.Player().getTime()
            g_item_total_time=xbmc.Player().getTotalTime()
         except:
            pass
         time.sleep(0.1)

    if resume_time!=-1:
        update_db_link(tmdb,name,season,episode,g_timer,g_item_total_time)
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')

def last_viewed(url_o,isr=' '):
    global all_data_imdb
    all_data_imdb=[]
    all_folders=[]
    all_f_data=[]
    global susb_data,susb_data_next
    import datetime
    from resources.modules.general import clean_name
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile_trk = os.path.join(user_dataDir, 'cache_play_trk.db')
    dbcon_trk = database.connect(cacheFile_trk)
    dbcur_trk  = dbcon_trk.cursor()
    dbcur_trk.execute("CREATE TABLE IF NOT EXISTS %s ( ""data_ep TEXT, ""dates TEXT, ""fanart TEXT,""color TEXT,""id TEXT,""season TEXT,""episode TEXT, ""next TEXT,""plot TEXT);" % 'AllData4')
    
    dbcon_trk.commit()
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""id TEXT, ""season TEXT, ""episode TEXT);" % 'subs')#mando ok
    
    dbcon.commit()

    all_w_trk={}
    all_tv_w={}
    all_movie_w={}
    
    if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
        all_w_trk,all_tv_w,all_movie_w=get_all_trakt_resume(url_o)
    
    strptime = datetime.datetime.strptime
    start_time=time.time()
    if Addon.getSetting("dp")=='true':
     
         dp = xbmcgui.DialogProgress()
         try:
          dp.create("Collecting",Addon.getLocalizedString(32142), '')
         except:
          dp.create("Collecting",Addon.getLocalizedString(32142)+'\n'+ '')
         elapsed_time = time.time() - start_time
         try:
            dp.update(0, Addon.getLocalizedString(32142)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),Addon.getLocalizedString(32143), '')
         except:
            dp.update(0, Addon.getLocalizedString(32142)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ Addon.getLocalizedString(32143)+'\n'+  '')
    color='white'
    
    if url_o=='tv':
        dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ORDER BY rowid DESC ")
    else:
       dbcur.execute("SELECT * FROM Lastepisode WHERE  type='movie' ORDER BY rowid DESC")
    # if Addon.getSetting("sync_mod")=='true'  and Addon.getSetting("sync_trakt")=='true' and len(Addon.getSetting("firebase"))>0:
        # try:
          # all_db=read_firebase('trackt')
          # match_tv=[]
          # for itt in all_db:
            
            # items=all_db[itt]
            # # logging.warning( 'בדיקה'+ str(items))
            # match_tv.insert(0,(items['name'],items['url'],items['iconimage'],items['fanart'],items['overview'],items['year'],items['original_title'],items['season'],items['episode'],items['tmdb'],items['eng_name'],items['show_original_year'],items['heb_name'],items['isr'],items['type']))
        # except:
         # match_tv = dbcur.fetchall()
         # LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)
    
    # else:
    match_tv = dbcur.fetchall()
       
    xxx=0
    all_data_imdb=[]
    thread=[]
    
    for item in match_tv:
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
      original_title=original_title.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
      dates=' '
      next=''
      data_ep=''
      fanart=image
      if Addon.getSetting("dp")=='true' :
        try:
            dp.update(int(((xxx* 100.0)/(len(match_tv))) ), Addon.getLocalizedString(32142)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),Addon.getLocalizedString(32143), clean_name(original_title,1))
        except:
            dp.update(int(((xxx* 100.0)/(len(match_tv))) ), Addon.getLocalizedString(32142)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ Addon.getLocalizedString(32143)+'\n'+  clean_name(original_title,1))
      xxx+=1
      done_data=0
      if url_o=='tv' :
          try:
              dbcur_trk.execute("SELECT  * FROM AllData4 WHERE  id='%s' AND season='%s' AND episode='%s'"%(id,season,episode))
               
                  
              match2 = dbcur_trk.fetchone()

            
              if match2!=None:
                data_ep,dates,fanart,color,i,j,k,next,plot=match2
                dates=json.loads(dates)

                if color=='white' :
                    
                    thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                    thread[len(thread)-1].setName(clean_name(original_title,1))
                    done_data=1

              else:

                thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                thread[len(thread)-1].setName(clean_name(original_title,1))
                done_data=1

          except:
            thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
            thread[len(thread)-1].setName(clean_name(original_title,1))
            done_data=1

      added_txt=''
      if done_data==0:
          try:
            f_name=unque(heb_name)
     
          except:
            f_name=name
          if (heb_name)=='':
            f_name=name
          if len(heb_name)<2:
            heb_name=name
          if color=='peru':
            add_p='[COLOR peru][B]סדרה זו הסתיימה או בוטלה[/B][/COLOR]'+'\n'
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n='[COLOR tomato][I]פרק הבא ישודר ב ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]פרק הבא ישודר ב ' +' לא ידוע עדיין '+'[/I][/COLOR]\n'
                next='???'
          if url_o=='tv' :
            added_txt=' עונה %s פרק %s '%(season,episode)
          all_data_imdb.append((color,f_name+' '+added_txt+' '+next,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
      
    
    for td in thread:
        td.start()

        if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                try:
                   dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
                except:
                   dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ td.name+'\n'+ " ")
        if len(thread)>38:
            xbmc.sleep(10)
        else:
            xbmc.sleep(10)
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          if Addon.getSetting("dp")=='true' :
                elapsed_time = time.time() - start_time
                try:
                    dp.update(0, Addon.getLocalizedString(32142)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
                except:
                    dp.update(0, Addon.getLocalizedString(32142)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ ','.join(all_alive)+'\n'+ " ")
          xbmc.sleep(100)
          if Addon.getSetting("dp")=='true' :
              if dp.iscanceled():
                dp.close()
              
                break
    
    thread=[]
    if url_o=='tv':
        all_subs_db=[]
        if 1:#mando ok
            dbcur.execute("SELECT * FROM subs")
            match = dbcur.fetchall()
            
            for title,id,season,episode in match:
                if len(episode)==1:
                  episode_n="0"+episode
                else:
                   episode_n=episode
                if len(season)==1:
                  season_n="0"+season
                else:
                  season_n=season
                next_ep=str(int(episode_n)+1)
                if len(next_ep)==1:
                  next_ep_n="0"+next_ep
                else:
                  next_ep_n=next_ep
                sub_title=title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
                all_subs_db.append(sub_title)
        for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx in all_data_imdb:
            if len(episode)==1:
              episode_n="0"+episode
            else:
               episode_n=episode
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            next_ep=str(int(episode_n)+1)
            if len(next_ep)==1:
              next_ep_n="0"+next_ep
            else:
              next_ep_n=next_ep
            season_c=season#mando ok
            episode_c=episode

            if color=='lightblue':
                season_c=str(int(season)+1)
                
            if len(season_c)==1:
              season_c_n="0"+season_c
            else:
              season_c_n=season_c
            #log.warning(color)
            sub_title=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
            sub_title_next=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+next_ep_n
            if color=='lightblue':
                        sub_title_next=original_title.replace("%27","'")+'-'+id+'-'+season_c_n+'-'+'01'

            if (color=='gold' or color=='white' or color=='lightblue')  :
                
                if (color=='gold' or color=='lightblue') and sub_title_next not in all_subs_db:
                    
                    season_c=season
                    episode_c=episode
                    if color=='lightblue':
                        season_c=str(int(season)+1)
                        episode_c='1'
                    else:
                        episode_c=str(int(episode_c)+1)
                    try:
                        thread[len(thread)-1].setName(eng_name+' S%sE%s'%(season_c,episode_c))
                    except:pass
    susb_data={}
    susb_data_next={}
    if url_o=='tv' :
        for td in thread:
            td.start()

            if Addon.getSetting("dp")=='true' :
                    elapsed_time = time.time() - start_time
                    try:
                        dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
                    except:
                        dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ td.name+'\n'+ " ")
        while 1:

              still_alive=0
              all_alive=[]
              for yy in range(0,len(thread)):
                
                if  thread[yy].is_alive():
                  
                  still_alive=1
                  all_alive.append(thread[yy].name)
              if still_alive==0:
                break
              if Addon.getSetting("dp")=='true' :#mando ok
                    elapsed_time = time.time() - start_time
                    try:
                        dp.update(0, ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
                    except:
                       dp.update(0, ' %s '%Addon.getLocalizedString(32072)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+ ','.join(all_alive)+'\n'+ " ")
              xbmc.sleep(100)
              if Addon.getSetting("dp")=='true' :
                  if dp.iscanceled():
                    dp.close()
                  
                    break
    all_data_imdb=sorted(all_data_imdb, key=lambda x: x[19], reverse=False)
    all_o_data=[]
    level=0
    for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx in all_data_imdb:
        
        if url_o=='tv':
            if color=='gold':
                level=1
            elif color=='lightblue':
                level=2
            elif color=='green':
                level=3
            elif color=='white':
                level=4
            elif color=='peru':
                level=5
        else:
            level+=1
        all_o_data.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,level))
        
    if url_o=='tv':
        order=False
    else:
        order=True
    #if Addon.getSetting("order_latest")=='true':
    all_folders_temp=[]
    # all_o_data=sorted(all_o_data, key=lambda x: x[20], reverse=order)
    for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,pos in all_o_data:
        # logging.warning('2323 '+str(all_o_data))
        if url_o=='tv':
            if len(episode)==1:
              episode_n="0"+episode
            else:
               episode_n=episode
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
              
            season_next=str(int(season)+1)#mando ok
            if len(season_next)==1:
              season_next_n="0"+season_next
            else:
              season_next_n=season_next
            next_ep=str(int(episode_n)+1)
            if len(next_ep)==1:
              next_ep_n="0"+next_ep
            else:
              next_ep_n=next_ep
              
            sub_title=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
            if color=='lightblue':
                sub_title_next=original_title.replace("%27","'")+'-'+id+'-'+season_next_n+'-'+'01'
                
            else:
                sub_title_next=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+next_ep_n
            
            if original_title in susb_data_next:
                
                if original_title in susb_data:
                    if susb_data[original_title]==True:
                        
                        dbcur.execute("DELETE  FROM subs WHERE name = '%s' and id= '%s' and season <> '%s' "%(original_title.replace("'","%27"),id,season_n))
                        dbcur.execute("INSERT INTO subs Values ('%s', '%s','%s','%s');" %  (original_title.replace("'","%27"),id,season_n,episode_n))
                        dbcon.commit()
                        f_name='[COLOR lightblue] ▲ [/COLOR]'+f_name
                if susb_data_next[original_title]==True:
                    if color=='lightblue':
                        episode_n='01'
                        next_ep_n='01'
                        
                        season_n=season_next_n
                        
                    else:
                        dbcur.execute("DELETE  FROM subs WHERE name = '%s' and id= '%s' and season <> '%s' "%(original_title.replace("'","%27"),id,season_n))
                    dbcur.execute("INSERT INTO subs Values ('%s', '%s','%s','%s');" %  (original_title.replace("'","%27"),id,season_n,next_ep_n))
                    dbcon.commit()
                    f_name='[COLOR peru] ◄ [/COLOR]'+f_name
                
            elif original_title in susb_data:
                    
                    if susb_data[original_title]==True:
                        dbcur.execute("DELETE  FROM subs WHERE name = '%s' and id= '%s' and season <> '%s'"%(original_title.replace("'","%27"),id,season_n))
                        dbcur.execute("INSERT INTO subs Values ('%s', '%s','%s','%s');" %  (original_title.replace("'","%27"),id,season_n,episode_n))
                        dbcon.commit()
                        f_name='[COLOR lightblue] ▲ [/COLOR]'+f_name
            if sub_title in all_subs_db:
                f_name='[COLOR lightblue] ▲ [/COLOR]'+f_name
            if sub_title_next in all_subs_db:
                f_name=f_name='[COLOR peru] ◄ [/COLOR]'+f_name#End mando ok
        all_d=((dates))
        if color!='white' and len(all_d)>1:

            add_n='[COLOR aqua]'+Addon.getLocalizedString(32147)+all_d[1] + '[/COLOR]\n'
        all_f_data.append(('[COLOR %s]'%color+ f_name+'[/COLOR]', url,4, icon,fanart,add_p+data_ep+add_n+plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,json.dumps(dates)))
        
        plot=plot.replace('%27',"'")
        if url_o=='tv':
            mode=179
        else:
            mode=20
        dd=[]
        if url_o!='tv':
            data_ep=show_original_year
            dbcur.execute("SELECT * FROM playback")
            match_playback = dbcur.fetchall()
            all_w={}
              
            for n,tm,s,e,p,t,f in match_playback:
                    ee=str(tm)
                    all_w[ee]={}
                    all_w[ee]['resume']=str(p)
                    all_w[ee]['totaltime']=str(t)
            
        else:
            dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' "%(id,str(season)))
            match_playback = dbcur.fetchall()
            
            all_w={}
        
            for n,t,s,e,p,t,f in match_playback:
                ee=str(e)
                all_w[ee]={}
                all_w[ee]['resume']=str(p)
                all_w[ee]['totaltime']=str(t)
                
        added_res_trakt=''
        
        if (id) in all_w_trk:
            
            if url_o=='tv':
               
                if season==all_w_trk[id]['season'] and episode==all_w_trk[id]['episode']:
                    added_res_trakt=all_w_trk[id]['precentage']
            else:
                added_res_trakt=all_w_trk[id]['precentage']
        watched='no'
        
        if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
            if url_o=='movie':
                if id in all_movie_w:
                    watched='yes'
            else:
                if id in all_tv_w:
                   if season+'x'+episode in all_tv_w[id]:
              
                    watched='yes'
        
        dd.append((f_name,show_original_year,original_title,id,season,episode,show_original_year))
        #'[COLOR %s]'%color+ f_name.replace('%27',"'")+'[/COLOR]' שם של הסדרה כולל הפרק הוסר לטובת שם של הסדרה בלבד
        
        # aa=addNolink3(heb_name.replace('%27',"'"), url,mode,False, iconimage=icon,all_w_trk=added_res_trakt,all_w=all_w,heb_name=heb_name,fanart=fanart,data=data_ep,plot=add_p+data_ep+add_n+plot.replace('%27',"'"),original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,watched=watched,show_original_year=show_original_year,dates=json.dumps(dates),dd=json.dumps(dd),dont_place=True)
        
        all_folders_temp.append(('[COLOR %s]'%color+ f_name.replace('%27',"'")+'[/COLOR]', url,mode, icon,added_res_trakt,all_w,f_name,fanart,data_ep,add_p+data_ep+add_n+plot.replace('%27',"'"),original_title,id,season,episode,eng_name,watched,show_original_year,json.dumps(dates),json.dumps(dd)))
        all_folders.append(all_folders_temp)
    dbcur_trk.close()
    dbcon_trk.close()
   
    dbcur.close()
    dbcon.close()
    read_data2=[]
    all_folders=all_folders_temp
    # if len(all_folders)>0:
        # if Addon.getSetting("trakt_access_token")!='' and url_o=='tv':
            # aa=addNolink3( '[COLOR blue][I]---%s---[/I][/COLOR]'%Addon.getLocalizedString(32148), id,180,False,fanart='https://bestdroidplayer.com/wp-content/uploads/2019/06/trakt-what-is-how-use-on-kodi.png', iconimage='https://bestdroidplayer.com/wp-content/uploads/2019/06/trakt-what-is-how-use-on-kodi.png',plot=' ',dont_place=True)
            # all_folders.append(aa)
        # xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_folders,len(all_folders))
    if url_o=='tv' :
        read_data2.append((url_o,match_tv))
    
    #log.warning('ALLDONE TRK')
    if Addon.getSetting("dp")=='true':
        dp.close()
    enc_data=(base64.b64encode(json.dumps(all_f_data).encode("utf-8"))).decode("utf-8")  
    return read_data2,enc_data,all_folders,url_o
def remove_from_trace(name,original_title,id,season,episode):
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()

    if id=='0':
      ok=xbmcgui.Dialog().yesno((Addon.getLocalizedString(32157)),(Addon.getLocalizedString(32159)+name))
    else:
      ok=xbmcgui.Dialog().yesno((Addon.getLocalizedString(32160)),('Unwatched '+name+" ?"))
    if ok:
      if id=='0':
        
        dbcur.execute("DELETE  FROM Lastepisode WHERE original_title = '%s' or original_title = '%s'"%(original_title.replace(' ','%20').replace("'","%27"),original_title.replace('%20',' ').replace("'","%27")))
        
        dbcon.commit()
      else:
      
        if len(episode)==0:
          episode='%20'
        if len(season)==0:
          season='%20'
        episode=episode.replace(" ","%20")
        season=season.replace(" ","%20")
        dbcur.execute("DELETE  FROM  AllData WHERE original_title = '%s'  AND season='%s' AND episode = '%s'"%(original_title,season.replace(" ","%20"),episode.replace(" ","%20")))
       
        
        dbcon.commit()
      dbcur.close()
      dbcon.close()
      cache.clear(['last_view'])
      xbmc.executebuiltin('Container.Refresh')
      if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_trakt")=='true' and len(Addon.getSetting("firebase"))>0:
            table_name='trackt'
            try:
                all_firebase=read_firebase(table_name)
                for items in all_firebase:
                 if all_firebase[items]['original_title']==original_title:
                    delete_firebase(table_name,items)
                    break
            except:pass  
            # xbmc.executebuiltin('Container.Refresh')
def remove_all_from_trace(name,original_title,id,season,episode):

    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()

    if id=='0':
    # yesno((Addon.getLocalizedString(32157)),(Addon.getLocalizedString(32158)+name+Addon.getLocalizedString(32159)))
      ok=xbmcgui.Dialog().yesno(('Anonymous TV'),('האם להסיר את כל הסדרות ממעקב הסדרות?'))
    else:
      ok=xbmcgui.Dialog().yesno((Addon.getLocalizedString(32160)),('Unwatched '+name+" ?"))
    if ok:
      if id=='0':
        dbcur.execute("DELETE FROM Lastepisode")
        
        dbcon.commit()
      else:
      
        if len(episode)==0:
          episode='%20'
        if len(season)==0:
          season='%20'
        episode=episode.replace(" ","%20")
        season=season.replace(" ","%20")
        dbcur.execute("DELETE  FROM  AllData WHERE original_title = '%s'  AND season='%s' AND episode = '%s'"%(original_title,season.replace(" ","%20"),episode.replace(" ","%20")))
       
        
        dbcon.commit()
      dbcur.close()
      dbcon.close()
      cache.clear(['last_view'])
      xbmc.executebuiltin('Container.Refresh')
      if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_trakt")=='true' and len(Addon.getSetting("firebase"))>0:
            table_name='trackt'
            all_firebase=read_firebase(table_name)
            for items in all_firebase:
                    t = Thread(target=delete_firebase, args=(table_name,items,))
                    t.start()
                    # thread=[]
                    # thread.append(Thread(delete_firebase,table_name,items))
                    # thread[0].start()
            # xbmc.executebuiltin('Container.Refresh')
def history_old(url):
    o_url=url
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    
    
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    
    dbcur.execute("SELECT * FROM Lastepisode WHERE type='%s'"%url)

    match = dbcur.fetchall()
    dbcon.commit()
    
    dbcur.close()
    dbcon.close()
    all_d=[]
    
    
    for name,url,icon,fan,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,type in match:
        if o_url=='tv':
            if len(episode)==1:
              episode_n="0"+episode
            else:
               episode_n=episode
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            added='- S%sE%s'%(season_n,episode_n)
        else:
            added=''
        aa=addDir3( name+added, 'history',15, icon,fan,plot,data=year,original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=year,heb_name=original_title)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def s_tracker(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dates,heb_name):
    menu=[]
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
    dbcon.commit()
    
    dbcur.execute("SELECT * FROM playback where tmdb='%s' and season='%s' "%(id,str(season)))
    all_w={}
    match = dbcur.fetchall()
    for n,t,s,e,p,t,f in match:
        ee=str(e)
        all_w[ee]={}
        all_w[ee]['resume']=str(p)
        all_w[ee]['totaltime']=str(t)
    dp = xbmcgui . DialogProgress ( )
    try:
        dp.create('Series Traker','Loading', '','')
        dp.update(0, 'Series Traker','Loading', '' )
    except:
        dp.create('Series Traker'+'\n'+ 'Loading'+'\n'+  '','')
        dp.update(0, 'Series Traker'+'\n'+ 'Loading'+'\n'+  '' )
    menu = Chose_ep(sys.argv[0], original_title,name,id,season,episode,dates,original_title,dp,all_w)
    menu.doModal()
    ret = menu.params
    next_season=menu.nextseason
    original_title=original_title.replace('\u200f','').replace('.',' ')
    del menu
    dp.close()
    #log.warning('ret:'+str(ret))
    if ret!=-1:
        # try:
            # dialog = xbmcgui.DialogBusy()
            # dialog.create()
        # except:
           # xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        try:
            all_d=json.loads(unque(dates))
        except:
            all_d=json.loads(unque(dates))
            
        #log.warning('all_d:'+str(all_d))
        if all_d[2]==0 or all_d[0]==0:
          prev_index=1
        else:
          prev_index=2
          
        #log.warning('prev_index:'+str(prev_index))
        if ret==0 and next_season:
              if next_season:
                season=str(int(season)+1)
                episode='1'
        elif ret==0 and all_d[2]!=0:
          
          episode=str(int(episode)+1)
          from resources.modules.tmdb import get_episode_data
          name,plot,image,season,episode=get_episode_data(id,season,episode)
          o_plot='%s %s %s %s \n'%(Addon.getLocalizedString(32101),season,Addon.getLocalizedString(32102),episode)+plot
        elif ret==prev_index:
          
          if int(episode)>1:
            episode=str(int(episode)-1)
            from resources.modules.tmdb import get_episode_data
            name,plot,image,season,episode=get_episode_data(id,season,episode)
            o_plot='%s %s %s %s \n'%(Addon.getLocalizedString(32101),season,Addon.getLocalizedString(32102),episode)+plot
        elif ret==(prev_index+1):
            
            xbmc.executebuiltin(('Container.update("%s?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode=19",return)'%(sys.argv[0],que(name.replace('%27',"'")),que(url),iconimage,fanart,que(description),show_original_year,original_title,id,season,id,show_original_year,que(heb_name.replace('%27',"'")),'0')))

            return 'ok',[] 
          
        elif ret==(prev_index+2):
            xbmc.executebuiltin(('Container.update("%s?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode=16"),return'%(sys.argv[0],que(name.replace('%27',"'")),que(url),iconimage,fanart,que(description),show_original_year,original_title,id,season,id,show_original_year,que(heb_name.replace('%27',"'")),'0')))
            
            return 'ok',[]
  
        xbmc.executebuiltin(('RunPlugin("%s?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&episode=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode=20",return)'%(sys.argv[0],que(name.replace('%27',"'")),que(url),iconimage,fanart,que(description),show_original_year,original_title,id,season,episode,id,show_original_year,que(heb_name.replace('%27',"'")),'0')))
        
        sys.exit(1)
    else:
        sys.exit(1)
        
def get_movie_data(url):
    
    html=requests.get(url).json()
    return html
def get_trakt():
    input= (Addon.getSetting("trk_user"))

    if input == '':
         Addon.openSettings()
         sys.exit()

    all_d=[]
    from resources.modules.general import call_trakt
    trakt_lists=call_trakt("users/me/lists")
    #trakt_lists=call_trakt('users/me/collection/shows')
  
    my_lists = []
    
    for list in trakt_lists:
        my_lists.append({
            'name': list["name"],
            'user': list["user"]["username"],
            'slug': list["ids"]["slug"]
        })

    for item in my_lists:
        user = item['user']
        slug = item['slug']
        url=user+'$$$$$$$$$$$'+slug
        aa=addDir3(item['name'],url,117,' ',' ',item['name'])
        all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def stop_play():

   return 'forceexit'

def play_trailer(id,tv_movie,plot):
    
    if not os.path.exists(xbmc_tranlate_path("special://home/addons/") + "plugin://inputstream.adaptive/"):
       xbmc.executebuiltin("RunPlugin(plugin://inputstream.adaptive)" )
    if tv_movie=='tv':
        tvshows_append = 'external_ids,videos,credits,content_ratings,alternative_titles,translations'
        url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=%s' % (id, '1248868d7003f60f2386595db98455ef', 'he', tvshows_append)
        data=requests.get(url).json()
        all_trailers = data['videos']['results']
        try:
            video_id = all_trailers[0].get('key')
        except:
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous TV'),'[COLOR %s]הטריילר באנגלית[/COLOR]' % COLOR2)
            url_t='https://api.themoviedb.org/3/tv/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
            # log.warning(url_t)
            html_t=requests.get(url_t).json()
            if len(html_t['results'])==0:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous TV'),'[COLOR %s]אין טריילר[/COLOR]' % COLOR2)
                return 
            if 'results' not in html_t:
                
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous TV'),'[COLOR %s]אין טריילר[/COLOR]' % COLOR2)
                sys.exit()
        
            if len(html_t['results'])>1:
                all_nm=[]
                all_lk=[]
                for items in html_t['results']:
                    all_nm.append(items['name']+","+str(items['size']))
                    all_lk.append(items['key'])
                
                ret = xbmcgui.Dialog().select("Choose trailer", all_nm)
                if ret!=-1:
                    video_id=(all_lk[ret])
                else:
                    s=stop_play()
                    if s=='forceexit':
                        sys.exit(1)
                    else:
                        return 0
            else:
                video_id=(html_t['results'][0]['key'])
    else: 

        movies_append = 'external_ids,videos,credits,release_dates,alternative_titles,translations'
        url = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=%s' % (id ,'1248868d7003f60f2386595db98455ef', 'he', movies_append)
        data=requests.get(url).json()
        try:
            all_trailers = data['videos']['results']
        except Exception as e:
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous TV'),'[COLOR %s]אין טריילר[/COLOR]' % COLOR2)
            log.warning(e)
            sys.exit()
        try:
            video_id = all_trailers[0].get('key')
        except:
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous TV'),'[COLOR %s]הטריילר באנגלית[/COLOR]' % COLOR2)
            url_t="http://api.themoviedb.org/3/movie/%s/videos?api_key=1248868d7003f60f2386595db98455ef"%id
            # log.warning(url_t)
            html_t=requests.get(url_t).json()
            if len(html_t['results'])==0:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous TV'),'[COLOR %s]אין טריילר[/COLOR]' % COLOR2)
                return 
            if 'results' not in html_t:
                
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Anonymous TV'),'[COLOR %s]אין טריילר[/COLOR]' % COLOR2)
                sys.exit()
        
            if len(html_t['results'])>1:
                all_nm=[]
                all_lk=[]
                for items in html_t['results']:
                    all_nm.append(items['name']+","+str(items['size']))
                    all_lk.append(items['key'])
                
                ret = xbmcgui.Dialog().select("Choose trailer", all_nm)
                if ret!=-1:
                    video_id=(all_lk[ret])
                else:
                    s=stop_play()
                    if s=='forceexit':
                        sys.exit(1)
                    else:
                        return 0
            else:
                video_id=(html_t['results'][0]['key'])
    playback_url=''
    if video_id!=None:
      playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
      item = xbmcgui.ListItem(path=playback_url)
      # if plot=='play_now':
      ok=xbmc.Player().play(playback_url,listitem=item,windowed=False)
      # else:
        # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
def progress_trakt(url):
        all_trk_data={}
        all_d=[]
        from resources.modules.general import call_trakt
        if  Addon.getSetting("fav_search_f_tv")=='true' and Addon.getSetting("fav_servers_en_tv")=='true' and len(Addon.getSetting("fav_servers_tv"))>0:
           fav_status='true'
        else:
            fav_status='false'
        if Addon.getSetting("dp")=='true':
                dp = xbmcgui.DialogProgress()
                dp.create("טוען פרקים", "אנא המתן", '')
                dp.update(0)
        import datetime
        start_time = time.time()
        xxx=0
        ddatetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
     
        
        html_g=requests.get(url_g).json()
        #html_g=html_g_tv
        result = call_trakt(url)
     
        items = []
        

        new_name_array=[]
        
        for item in result:
            
            try:
                num_1 = 0
                if 'seasons' in item:
                    for i in range(0, len(item['seasons'])):
                        if item['seasons'][i]['number'] > 0: num_1 += len(item['seasons'][i]['episodes'])
                    num_2 = int(item['show']['aired_episodes'])
                    if num_1 >= num_2: raise Exception()

                    season = str(item['seasons'][-1]['number'])

                    episode = [x for x in item['seasons'][-1]['episodes'] if 'number' in x]
                    episode = sorted(episode, key=lambda x: x['number'])
                    episode = str(episode[-1]['number'])
                else:
                    season = str(item['episode']['season'])
                    episode=str(item['episode']['number'])
                

                tvshowtitle = item['show']['title']
                if tvshowtitle == None or tvshowtitle == '': raise Exception()
                from resources.modules.general import replaceHTMLCodes
                tvshowtitle = replaceHTMLCodes(tvshowtitle)

                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int(ddatetime.strftime('%Y')): raise Exception()

                imdb = item['show']['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0'

                tmdb = item['show']['ids']['tmdb']
                if tmdb == None or tmdb == '': raise Exception()
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                
               
                trakt = item['show']['ids']['trakt']
                if trakt == None or trakt == '': raise Exception()
                trakt = re.sub('[^0-9]', '', str(trakt))
                if 'last_watched_at' in item:
                    last_watched = item['last_watched_at']
                else:
                    last_watched = item['listed_at']
                if last_watched == None or last_watched == '': last_watched = '0'
                items.append({'imdb': imdb, 'tmdb': tmdb, 'tvshowtitle': tvshowtitle, 'year': year, 'snum': season, 'enum': episode, '_last_watched': last_watched})
            
            except Exception as e:
               log.warning(e)
            
            
        result = call_trakt('/users/hidden/progress_watched?limit=1000&type=show')
        result = [str(i['show']['ids']['tmdb']) for i in result]

        items_pre = [i for i in items if not i['tmdb'] in result]

      
        for items in items_pre:
          watched='no'
          not_yet=0
          gone=0
          season=items['snum']
          episode=items['enum']
    
          url='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          #url='http://api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'%(items['tmdb'],season)
          html=cache.get(get_movie_data,time_to_save,url, table='pages')
          plot=' '
          if 'The resource you requested could not be found' not in str(html):
             data=html
            
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               year=str(data['first_air_date'].split("-")[0])
             else:
                if 'release_date' in data:
                  year=str(data['release_date'].split("-")[0])
                else:
                    year=' '
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             f_subs=[]
             
             original_name=data['original_name']
             id=str(data['id'])
             mode=15
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x['id']] for x in data['genres']])
             except:genere=''

   
            
             trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s" % id
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                  if len(f_subs)>0:
                    color='white'
                  else:
                    color='red'
                    
              else:
                 color='white'
              elapsed_time = time.time() - start_time
              if Addon.getSetting("dp")=='true':
                dp.update(int(((xxx* 100.0)/(len(html))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
              xxx=xxx+1
              if int(data['last_episode_to_air']['season_number'])>=int(season):
                if int(data['last_episode_to_air']['episode_number'])>int(episode):
                
                  episode=str(int(episode)+1)
                else:
                 if int(data['last_episode_to_air']['season_number'])>int(season):
                   season=str(int(season)+1)
                   episode='1'
                 else:
                  if (data['next_episode_to_air'])!=None:
                    episode=str(int(episode)+1)
                   
                    not_yet='1'
                  else:
                    gone=1
              else:
                    if (data['next_episode_to_air'])!=None:
                        season=str(int(season)+1)
                        episode='1'
                        not_yet='1'
                    else:
                        gone=1
              video_data={}

              

              video_data['mediatype']='tvshow'
              video_data['OriginalTitle']=new_name
              video_data['title']=new_name



              video_data['year']=year
              video_data['season']=season
              video_data['episode']=episode
              video_data['genre']=genere
              
              if len(episode)==1:
                  episode_n="0"+episode
              else:
                   episode_n=episode
              if len(season)==1:
                  season_n="0"+season
              else:
                  season_n=season
              if Addon.getSetting("trac_trk")=='true':
                addon='\n'+' עונה'+season_n+'-פרק '+episode_n
              else:
                addon=''
              video_data['plot']=plot+addon
              try:
                max_ep=data['seasons'][int(season)-1]['episode_count']
              except Exception as e:
                max_ep=100
            
              if gone==0:
                  if not_yet==0:
                  
                    if episode_n=='01':
                      dates=json.dumps((0,'' ,''))
                    elif max_ep<=int(episode):
                        dates=json.dumps(('','' ,0))
                    else:
                      dates=json.dumps(('','' ,''))
                    all_trk_data[id]={}
                    all_trk_data[id]['icon']=icon
                    all_trk_data[id]['fan']=fan
                    all_trk_data[id]['plot']=plot+addon
                    all_trk_data[id]['year']=year
                    all_trk_data[id]['original_title']=original_name
                    all_trk_data[id]['title']=new_name
                    all_trk_data[id]['season']=season
                    all_trk_data[id]['episode']=episode
                    all_trk_data[id]['eng_name']=original_title
                    all_trk_data[id]['heb_name']=new_name
                    all_trk_data[id]['type']='tv'
                    
                    
                    #log.warning('121')
                    aa=addDir3('[COLOR '+color+']'+new_name+'[/COLOR]'+' S'+season_n+'E'+episode_n,url,mode,icon,fan,plot+addon,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,season=season,episode=episode,eng_name=original_title,tmdbid=id,video_info=video_data,dates=dates,fav_status=fav_status)
                    all_d.append(aa)
                  else:
                   addNolink('[COLOR red][I]'+ new_name+'[/I][/COLOR]'+' S'+season_n+'E'+episode_n, 'www',999,False,iconimage=icon,fanart=fan)
          else:
            
            #log.warning('323')
            responce=call_trakt("shows/{0}".format(items['trakt']), params={'extended': 'full'})
          
           
            addNolink('[COLOR red][I]'+ responce['title']+'[/I][/COLOR]', 'www',999,False)
        #log.warning('424')
        if Addon.getSetting("dp")=='true':
          dp.close()
        #log.warning('H7')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def get_file_data():
    file_data=[]
    if os.path.exists(save_file):
            f = open(save_file, 'r')
            file_data = f.readlines()
            f.close()
    return file_data
def utf8_urlencode(params):
    try:
        import urllib as u
        enc=u.urlencode
    except:
        from urllib.parse import urlencode
        enc=urlencode
    # problem: u.urlencode(params.items()) is not unicode-safe. Must encode all params strings as utf8 first.
    # UTF-8 encodes all the keys and values in params dictionary
    for k,v in list(params.items()):
        # TRY urllib.unquote_plus(artist.encode('utf-8')).decode('utf-8')
        if type(v) in (int, float):
            params[k] = v
        else:
            try:
                params[k.encode('utf-8')] = v.encode('utf-8')
            except Exception as e:
                pass
                #log.warning( '**ERROR utf8_urlencode ERROR** %s' % e )
    
    return enc(params).encode().decode('utf-8')

def get_trk_data(url):
        all_trk_data={}
        from resources.modules.general import call_trakt
        from resources.modules.tmdb import html_g_movie
        # time_to_save=int(Addon.getSetting("save_time"))
        xxx=0
        # if Addon.getSetting("dp")=='true':
        dp = xbmcgui.DialogProgress()
        try:
            dp.create("טוען סרטים", "אנא המתן", '')
            dp.update(0)
        except:
            dp.create("טוען סרטים", "אנא המתן")
            dp.update(0)
        url_g_m=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'

        url_g_tv=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'

        html_g_m=html_g_movie
        start_time = time.time()
        src="tmdb" 
            
        i = (call_trakt('/users/me/watched/movies'))
        
        all_movie_w=[]
        for ids in i:
          all_movie_w.append(str(ids['movie']['ids']['tmdb']))

        if '$$$$$$$$$$$' in url:
            data_in=url.split('$$$$$$$$$$$')
            user = data_in[0]
            slug = data_in[1]
            selected={'slug':data_in[1],'user':data_in[0]}

            responce=call_trakt("/users/{0}/lists/{1}/items".format(user, slug))
        else:
           responce=call_trakt(url)
        new_name_array=[]

        for items in responce:
          
          if 'show' in items:
             slug = 'tv'
             html_g=html_g_tv
          else:
            slug = 'movies'
            html_g=html_g_m
          if slug=='movies':
            url='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['movie']['ids']['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          else:
            url='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['show']['ids']['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          
          html=cache.get(get_movie_data,72,url, table='pages')
          if 'The resource you requested could not be found' not in str(html):
             data=html
             if 'overview' not in data:
                continue
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data :
               if data['first_air_date']==None:
                    year=' '
               else:
                   year=str(data['first_air_date'].split("-")[0])
             else:
                 if 'release_date' in data:
                    if data['release_date']==None:
                        year=' '
                    else:
                        year=str(data['release_date'].split("-")[0])
                 else:
                    year=' '
        
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             f_subs=[]
             if slug=='movies':
               original_name=data['original_title']
               mode=15
               
               id=str(data['id'])
               if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                 f_subs=cache.get(get_subs,9999,'movie',original_name,'0','0',id,year,True, table='pages')
               
               
             else:
               original_name=data['original_name']
               id=str(data['id'])
               mode=16
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x['id']] for x in data['genres']])
             except:genere=''

   
            
             trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s" % id
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                  if len(f_subs)>0:
                    color='white'
                  else:
                    color='red'
                    
              else:
                color='white'
              elapsed_time = time.time() - start_time
              # if Addon.getSetting("dp")=='true':
              try:
                dp.update(int(((xxx* 100.0)/(len(html))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
              except:
                dp.update(int(((xxx* 100.0)/(len(html))) )+'\n'+ ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+'[COLOR'+color+']'+new_name+'[/COLOR]')
              xxx=xxx+1
              watched='no'
              if id in all_movie_w:
                watched='yes'
              '''
              if id in all_tv_w:
                 if season+'x'+episode in all_tv_w[id]:
                  watched='yes'
              '''
              if slug=='movies':
                    fav_search_f=Addon.getSetting("fav_search_f")
                    fav_servers_en=Addon.getSetting("fav_servers_en")
                    fav_servers=Addon.getSetting("fav_servers")
                   
                    google_server= Addon.getSetting("google_server")
                    rapid_server=Addon.getSetting("rapid_server")
                    direct_server=Addon.getSetting("direct_server")
                    heb_server=Addon.getSetting("heb_server")
              else:
                    fav_search_f=Addon.getSetting("fav_search_f_tv")
                    fav_servers_en=Addon.getSetting("fav_servers_en_tv")
                    fav_servers=Addon.getSetting("fav_servers_tv")
                    google_server= Addon.getSetting("google_server_tv")
                    rapid_server=Addon.getSetting("rapid_server_tv")
                    direct_server=Addon.getSetting("direct_server_tv")
                    heb_server=Addon.getSetting("heb_server_tv")
        
   
              if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 or heb_server=='true' or google_server=='true' or rapid_server=='true' or direct_server=='true'):
                    fav_status='true'
              else:
                    fav_status='false'
              all_d=[]
              
              all_trk_data[id]={}
              all_trk_data[id]['icon']=icon
              all_trk_data[id]['fan']=fan
              all_trk_data[id]['plot']=plot
              all_trk_data[id]['year']=year
              all_trk_data[id]['original_title']=original_name
              all_trk_data[id]['title']=new_name
              all_trk_data[id]['season']='%20'
              all_trk_data[id]['episode']='%20'
              all_trk_data[id]['eng_name']=original_name
              all_trk_data[id]['heb_name']=new_name
              all_trk_data[id]['type']='movie'
              addDir4('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status)
              # all_d.append(aa)
          else:
            
            if slug=='movies':
                responce=call_trakt("movies/{0}".format(items['movie']['ids']['trakt']), params={'extended': 'full'})
            else:
                responce=call_trakt("shows/{0}".format(items['show']['ids']['trakt']), params={'extended': 'full'})
           
           
            addNolink('[COLOR red][I]'+ responce['title']+'[/I][/COLOR]', 'www',999,False)

        dp.close()
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
        return all_trk_data
def c_get_one_trk(color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image):
          global all_data_imdb
          import _strptime
          # from  resources.modules.client import  get_html
          data_ep=''
          dates=' '
          fanart=image
          url='https://'+'api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=%s'%(id,season,lang)
         
          html=requests.get(url).json()
          next=''
          ep=0
          f_episode=0
          catch=0
          counter=0
          if 'episodes' in html:
              for items in html['episodes']:
                if 'air_date' in items:
                   try:
                       datea=items['air_date']+'\n'
                       
                       a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                       b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                      
                   
                       if a>b:
                         if catch==0:
                           f_episode=counter
                           
                           catch=1
                       counter=counter+1
                       
                   except:
                         ep=0
          else:
             ep=0
          episode_fixed=int(episode)-1
          try:
              try:
                plot=html['episodes'][int(episode_fixed)]['overview']
              except:
                plot=''
          
              ep=len(html['episodes'])
              try:
                  if (html['episodes'][int(episode_fixed)]['still_path'])==None:
                    fanart=image
                  else:
                    fanart='https://'+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
              except:
                fanart=image
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'עונה '+season+'-פרק '+episode+ '[/COLOR]\n[COLOR yellow] מתוך ' +str(f_episode)  +' פרקים לעונה זו [/COLOR]\n' 
              try:
                  if int(episode)>1:
                    
                    prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
                  else:
                    prev_ep=0
              except:
                prev_ep=0

          

                      
              if int(episode)<ep:

                if (int(episode)+1)>=f_episode:
                  color_ep='white'#color_ep='magenta'
                  next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
                else:
                  
                  next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
              else:
                next_ep=0
              dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              if int(episode)<int(f_episode):
               color='gold'
              else:
               color='white'
               h2=requests.get('https://api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US'%(id)).json()
               last_s_to_air=int(h2['last_episode_to_air']['season_number'])
               last_e_to_air=int(h2['last_episode_to_air']['episode_number'])
              
               if int(season)<last_s_to_air:
      
                 color='lightblue'
            
               if h2['status']=='Ended' or h2['status']=='Canceled':
                color='peru'
               
               
               if h2['next_episode_to_air']!=None:
                 
                 if 'air_date' in h2['next_episode_to_air']:
                  
                  a=(time.strptime(h2['next_episode_to_air']['air_date'], '%Y-%m-%d'))
                  next=time.strftime( "%d-%m-%Y",a)
                  
               else:
                  next=''
                 
          except Exception as e:
              import linecache,sys
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              log.warning('Error :'+ heb_name)
              log.warning('Error :'+ str(e) +',line no:'+str(lineno))
              plot=' '
              color='green'
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'עונה '+season+'-פרק '+episode+ '[/COLOR]\n[COLOR yellow] מתוך ' +str(f_episode)  +' פרקים לעונה זו [/COLOR]\n' 
              dates=' '
              fanart=image
          try:
            f_name=unque(heb_name)
     
          except:
            f_name=name
          if (heb_name)=='':
            f_name=name
          if len(heb_name)<2:
            heb_name=name
          if color=='peru':
            add_p='[COLOR peru][B]סדרה זו הסתיימה או בוטלה[/B][/COLOR]'+'\n'
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n='[COLOR tomato][I]פרק הבא ישודר ב ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]פרק הבא ישודר ב ' +' לא ידוע עדיין '+'[/I][/COLOR]\n'

                next='???'
          
          added_txt=' עונה %s פרק %s '%(season,episode)
          #all_data_imdb.append((color,f_name+' '+added_txt+' '+next,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
          return data_ep,dates,fanart,color,next,color,(f_name+' '+added_txt+' '+next),url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx
def get_one_trk(color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image):
    global all_data_imdb
    #log.warning('Name:%s,season:%s,Episode: %s'%(name,season,episode))
    data_ep,dates,fanart,color,next,color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx=cache.get(c_get_one_trk,999,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image, table='posters')
    all_data_imdb.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
    return data_ep,dates,fanart,color,next

def get_html_data(url):
    
    html=requests.get(url).json()
    return html

def remove_was_i(name,id,season,episode):
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE  FROM playback   where tmdb='%s' and season='%s' and episode='%s'"%(id,str(season).replace('%20','0').replace(' ','0'),str(episode).replace('%20','0').replace(' ','0')))

        dbcon.commit()
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Mamdo', 'הוסר'+name)))
        xbmc.executebuiltin('Container.Refresh')
        dbcur.close()
        dbcon.close()
def sync_trk(removedb=False,show_msg=True):
    #tv
    from resources.modules.general import clean_name
    
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    
    all_tv_prog=progress_trakt('users/me/watched/shows?extended=full',sync=True)
    
    if removedb:
        dbcur.execute("DELETE FROM Lastepisode")
    else:
        dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ")
   
    match_tv = dbcur.fetchall()
   
    
    new_tv={}
    all_local_mv={}
    new_tv_far={}
    for item in match_tv:
      
      
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
     
      all_local_mv[id]={}
      all_local_mv[id]['icon']=icon
      all_local_mv[id]['fan']=image
      all_local_mv[id]['plot']=plot
      all_local_mv[id]['year']=year
      all_local_mv[id]['original_title']=original_title
      all_local_mv[id]['title']=name
      all_local_mv[id]['season']=season
      all_local_mv[id]['episode']=episode
      all_local_mv[id]['eng_name']=eng_name
      all_local_mv[id]['heb_name']=heb_name
      
      all_local_mv[id]['type']='tv'
     
      if id not in all_tv_prog:
       
        new_tv[id]={}
        new_tv[id]['item']=(all_local_mv[id])
        
        new_tv[id]['change_reason']='New'
       
        new_tv[id]['local']=''
        new_tv[id]['trk']=''
      else:
        if season!=all_tv_prog[id]['season']:
            if id not in new_tv:
                new_tv[id]={}
                new_tv[id]['change_reason']=''
            new_tv[id]['item']=(all_tv_prog[id])
            new_tv[id]['change_reason']=new_tv[id]['change_reason']+'$$$$season'
            
            new_tv[id]['local']=season
            new_tv[id]['trk']=all_tv_prog[id]['season']
        if episode!=all_tv_prog[id]['episode']:
            if id not in new_tv:
                new_tv[id]={}
                new_tv[id]['change_reason']=''
            new_tv[id]['item']=(all_tv_prog[id])
            
            new_tv[id]['change_reason']=new_tv[id]['change_reason']+'$$$$episode'
            new_tv[id]['local']=episode
            new_tv[id]['trk']=all_tv_prog[id]['episode']
    for id in all_tv_prog:
      if id not in all_local_mv:
        new_tv_far[id]={}
        new_tv_far[id]['item']=(all_tv_prog[id])
        new_tv_far[id]['change_reason']='New'

        new_tv_far[id]['local']=''
        new_tv_far[id]['trk']=''
      else:
        if all_tv_prog[id]['season']!=all_local_mv[id]['season']:
            if id not in new_tv_far:
                new_tv_far[id]={}
                new_tv_far[id]['change_reason']=''
            new_tv_far[id]['item']=(all_local_mv[id])
            new_tv_far[id]['change_reason']=new_tv_far[id]['change_reason']+'$$$$season'
            
            new_tv_far[id]['local']=all_local_mv[id]['season']
            new_tv_far[id]['trk']=all_tv_prog[id]['season']
        if all_tv_prog[id]['episode']!=all_local_mv[id]['episode']:
            if id not in new_tv_far:
                new_tv_far[id]={}
                new_tv_far[id]['change_reason']=''
            new_tv_far[id]['item']=(all_local_mv[id])
            
            new_tv_far[id]['change_reason']=new_tv_far[id]['change_reason']+'$$$$episode'
            new_tv_far[id]['local']=all_local_mv[id]['episode']
            new_tv_far[id]['trk']=all_tv_prog[id]['episode']
    not_on_trk=[]
    not_on_local=[]
    for id in new_tv:
        if new_tv[id]['change_reason']=='New':
            not_on_trk.append(clean_name(all_local_mv[id]['original_title'],1)+' S%sE%s'%(all_local_mv[id]['season'],all_local_mv[id]['episode'])+'-'+all_local_mv[id]['year'])
    for id in new_tv_far:
        if new_tv_far[id]['change_reason']=='New':
            not_on_local.append(clean_name(all_tv_prog[id]['original_title'],1)+' S%sE%s'%(all_tv_prog[id]['season'],all_tv_prog[id]['episode'])+'-'+all_tv_prog[id]['year'])
    

            
            
    #movie
    all_mv_prog=get_trk_data('users/me/watched/movies')
    
    dbcur.execute("SELECT * FROM Lastepisode WHERE  type='movie'")
    match_tv = dbcur.fetchall()


    new_mv={}
    all_local_mv={}
    new_mv_far={}
    for item in match_tv:
      
      
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
     
      all_local_mv[id]={}
      all_local_mv[id]['icon']=icon
      all_local_mv[id]['fan']=image
      all_local_mv[id]['plot']=plot
      all_local_mv[id]['year']=year
      all_local_mv[id]['original_title']=original_title
      all_local_mv[id]['title']=name
      all_local_mv[id]['season']=season
      all_local_mv[id]['episode']=episode
      all_local_mv[id]['eng_name']=eng_name
      all_local_mv[id]['heb_name']=heb_name
      
      all_local_mv[id]['type']='tv'
      if id not in all_mv_prog:
        new_mv[id]={}
        new_mv[id]['item']=(all_local_mv[id])
        
        new_mv[id]['change_reason']='New'
       
        new_mv[id]['local']=''
        new_mv[id]['trk']=''
    for id in all_mv_prog:
      if id not in all_local_mv:
        new_mv_far[id]={}
        new_mv_far[id]['item']=(all_mv_prog[id])
        new_mv_far[id]['change_reason']='New'

        new_mv_far[id]['local']=''
        new_mv_far[id]['trk']=''
    not_on_trk_mv=[]
    not_on_local_mv=[]
    for id in new_mv:
        if new_mv[id]['change_reason']=='New':
            not_on_trk_mv.append(clean_name(all_local_mv[id]['original_title'],1)+'-'+all_local_mv[id]['year'])
    for id in new_mv_far:
        if new_mv_far[id]['change_reason']=='New':
            not_on_local_mv.append(clean_name(all_mv_prog[id]['original_title'],1)+'-'+all_mv_prog[id]['year'])
    msg='[COLOR yellow][I]%s[/I][/COLOR]\n[COLOR lightblue]not found on TRAKT'%Addon.getLocalizedString(32099)+'\n----------------\n'+'\n'.join(not_on_trk)+'[/COLOR]\n\n[COLOR khaki]only on TRAKT not in local db'+'\n----------------\n'+'\n'.join(not_on_local)+'[/COLOR]'
    msg=msg+'\n\n[COLOR yellow][I]%s[/I][/COLOR]\n[COLOR lightblue]not found on TRAKT'%Addon.getLocalizedString(32100)+'\n----------------\n'+'\n'.join(not_on_trk_mv)+'[/COLOR]\n\n[COLOR khaki]only on TRAKT not in local db'+'\n----------------\n'+'\n'.join(not_on_local_mv)+'[/COLOR]'
    if removedb:
        ok=True
    else:
       ok=TrkBox_help('Changes', msg)
    if ok:
        start_time=time.time()
     
        dp = xbmcgui.DialogProgress()
        try:
            dp.create("Syncing", Addon.getLocalizedString(32072), '')
        except:
            dp.create("Syncing"+'\n'+ Addon.getLocalizedString(32072)+'\n'+ '')
        elapsed_time = time.time() - start_time
        try:
            dp.update(0, Addon.getLocalizedString(32072)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),Addon.getLocalizedString(32093), '')
        except:
            dp.update(0, Addon.getLocalizedString(32072)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+Addon.getLocalizedString(32093)+'\n'+ '')
        xxx=0
        for id in new_tv_far:
           if new_tv_far[id]['change_reason']=='New':
            name=new_tv_far[id]['item']['title']
            url='www'
            icon=new_tv_far[id]['item']['icon']
            image=new_tv_far[id]['item']['fan']
            plot=new_tv_far[id]['item']['plot']
            year=new_tv_far[id]['item']['year']
            original_title=new_tv_far[id]['item']['original_title']
            season=new_tv_far[id]['item']['season']
            episode=new_tv_far[id]['item']['episode']
            eng_name=new_tv_far[id]['item']['eng_name']
            show_original_year=new_tv_far[id]['item']['year']
            heb_name=new_tv_far[id]['item']['heb_name']
            isr='0'
            tv_movie='tv'
            dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'","%27"),url,icon,image,plot.replace("'","%27"),year,original_title.replace("'","%27").replace(" ","%20"),season,episode,id,eng_name.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),isr,tv_movie))
            try:
                dp.update(int(((xxx* 100.0)/(len(new_tv_far))) ), ' Movies '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync DB', name)
            except:
                dp.update(int(((xxx* 100.0)/(len(new_tv_far))) ), ' Movies '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+'Sync DB'+'\n'+ name)
            xxx+=1
        dbcon.commit()
            
        xxx=0
        for id in new_mv_far:
           
           if new_mv_far[id]['change_reason']=='New':
            name=new_mv_far[id]['item']['title']
            url='www'
            icon=new_mv_far[id]['item']['icon']
            image=new_mv_far[id]['item']['fan']
            plot=new_mv_far[id]['item']['plot']
            year=new_mv_far[id]['item']['year']
            original_title=new_mv_far[id]['item']['original_title']
            season=new_mv_far[id]['item']['season']
            episode=new_mv_far[id]['item']['episode']
            eng_name=new_mv_far[id]['item']['eng_name']
            show_original_year=new_mv_far[id]['item']['year']
            heb_name=new_mv_far[id]['item']['heb_name']
            isr='0'
            tv_movie='movie'
            dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'","%27"),url,icon,image,plot.replace("'","%27"),year,original_title.replace("'","%27").replace(" ","%20"),season,episode,id,eng_name.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),isr,tv_movie))
            try:
                dp.update(int(((xxx* 100.0)/(len(new_mv_far))) ), Addon.getLocalizedString(32099)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync DB', name)
            except:
                dp.update(int(((xxx* 100.0)/(len(new_mv_far))) ), Addon.getLocalizedString(32099)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+'Sync DB'+'\n'+ name)
            xxx+=1
        dbcon.commit()
        xxx=0
        for id in new_mv:
          if new_mv[id]['change_reason']=='New':
            i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))
            try:
                dp.update(int(((xxx* 100.0)/(len(new_mv))) ), Addon.getLocalizedString(32100)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync Trakt', id)
            except:
                dp.update(int(((xxx* 100.0)/(len(new_mv))) ), Addon.getLocalizedString(32100)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+'Sync Trakt'+'\n'+ id)
            xxx+=1
        xxx=0
        for id in new_tv:
          if new_tv[id]['change_reason']=='New':
            
            season=new_tv[id]['item']['season']
            episode=new_tv[id]['item']['episode']
            season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
            i = (post_trakt('/sync/watchlist', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
            
            
            i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
            try:
                dp.update(int(((xxx* 100.0)/(len(new_tv))) ), Addon.getLocalizedString(32099)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Sync Trakt', id)
            except:
                dp.update(int(((xxx* 100.0)/(len(new_tv))) ), Addon.getLocalizedString(32099)+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+'Sync Trakt'+'\n'+ id)
            xxx+=1
        if show_msg:
            xbmc.executebuiltin('Container.Refresh')
            xbmcgui.Dialog().ok('Sync','[COLOR aqua][I] %s [/I][/COLOR]'%Addon.getLocalizedString(32112))
    else:
        dbcur.close()
        dbcon.close()
        try:
         dp.close()
        except:
            pass
        sys.exit(1)
    dbcur.close()
    dbcon.close()
    try:
     dp.close()
    except:
        pass
def clear_was_i():
    ok=xbmcgui.Dialog().yesno(("נקה נקודת זמן ניגון "),('האם אתה בטוח?'))
    if ok:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM playback")
        dbcon.commit()
        dbcur.close()
        dbcon.close()
        
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
            table_name='playback'
            try:
                all_firebase=read_firebase(table_name)
                for items in all_firebase:
                        delete_firebase(table_name,items)
                xbmc.executebuiltin('Container.Refresh')
            except Exception as e:
              import linecache,sys
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              log.warning('Error :'+ str(e) +',line no:'+str(lineno))
              match_playtime = self.dbcur.fetchone()
              LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)

        else:
            xbmc.executebuiltin('Container.Refresh')

def ClearCache():
    from resources.modules import cache
    cache.clear(['cookies', 'pages','posters','posters_n'])
   

    

    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]נוקה[/COLOR]' % COLOR2)
def trakt_liked(url,iconImage,fanart):
    from resources.modules.general import call_trakt
    responce=call_trakt(url)
   
            
    for items in responce:
        url=items['list']['user']['username']+'$$$$$$$$$$$'+items['list']['ids']['slug']
        addDir4(items['list']['name'],url,31,iconImage,fanart,items['list']['description'])
def get_genere(link):
   tv_images={u'\u05d0\u05e7\u05e9\u05df \u05d5\u05d4\u05e8\u05e4\u05ea\u05e7\u05d0\u05d5\u05ea': 'http://stavarts.com/wp-content/uploads/2017/10/%D7%A9%D7%99%D7%A9%D7%99-%D7%94%D7%A8%D7%A4%D7%AA%D7%A7%D7%90%D7%95%D7%AA-%D7%AA%D7%A9%D7%A2%D7%B4%D7%97-%D7%A8%D7%90%D7%92%D7%A0%D7%90%D7%A8%D7%95%D7%A7_Page_1.jpg', u'\u05de\u05e1\u05ea\u05d5\u05e8\u05d9\u05df': 'http://avi-goldberg.com/wp-content/uploads/5008202002.jpg', u'\u05d9\u05dc\u05d3\u05d9\u05dd': "https://"+'i.ytimg.com/vi/sN4xfdDwjHk/maxresdefault.jpg', u'\u05de\u05e2\u05e8\u05d1\u05d5\u05df': "https://"+'i.ytimg.com/vi/Jw1iuGaNuy0/hqdefault.jpg', u'\u05e4\u05e9\u05e2': 'http://www.mapah.co.il/wp-content/uploads/2012/09/DSC_1210.jpg', u'\u05e8\u05d9\u05d0\u05dc\u05d9\u05d8\u05d9': 'http://blog.tapuz.co.il/oferD/images/%7B2D0A8A8A-7F57-4C8F-9290-D5DB72F06509%7D.jpg', u'\u05de\u05e9\u05e4\u05d7\u05d4': 'http://kaye7.school.org.il/photos/family.jpg', u'\u05e1\u05d1\u05d5\u05df': 'http://www.myliberty.co.il/media/com_hikashop/upload/2-1.jpg', u'\u05d7\u05d3\u05e9\u05d5\u05ea': "https://"+'shaza10.files.wordpress.com/2010/11/d790d795d79cd7a4d79f-d797d793d7a9-d797d793d7a9d795d7aa-10-d7a6d799d79cd795d79d-d7aad795d79ed7a8-d7a4d795d79cd798d799d79f03.jpg', u'\u05e7\u05d5\u05de\u05d3\u05d9\u05d4': "https://"+'upload.wikimedia.org/wikipedia/he/e/ef/Le_Tout_Nouveau_Testament.jpg', u'\u05d0\u05e0\u05d9\u05de\u05e6\u05d9\u05d4': 'http://www.printime.co.il/image/users/16584/ftp/my_files/smileynumbers1we.jpg', u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9 \u05d5\u05e4\u05e0\u05d8\u05d6\u05d9\u05d4': "https://"+'media.getbooks.co.il/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/s/h/shemharuach_getbooks-copy.jpg', u'\u05d3\u05e8\u05de\u05d4': 'http://www.yorav.co.il/images/moshe+erela/2007/dram.JPG', u'\u05d3\u05d5\u05e7\u05d5\u05de\u05e0\u05d8\u05e8\u05d9': 'http://img.mako.co.il/2017/03/28/704104_I.jpg', u'\u05de\u05dc\u05d7\u05de\u05d4 \u05d5\u05e4\u05d5\u05dc\u05d9\u05d8\u05d9\u05e7\u05d4': "https://"+'dannyorbach.files.wordpress.com/2013/05/berlinsynagoge.jpg', u'\u05d3\u05d9\u05d1\u05d5\u05e8\u05d9\u05dd': 'http://www.news1.co.il/uploadimages/NEWS1-556713283061982.jpg'}
   movie_images={u'\u05de\u05d5\u05e1\u05d9\u05e7\u05d4': 'http://www.blich.ramat-gan.k12.il/sites/default/files/files/music.jpg', u'\u05e1\u05e8\u05d8 \u05d8\u05dc\u05d5\u05d9\u05d6\u05d9\u05d4': 'https://i.ytimg.com/vi/hFc1821MSoA/hqdefault.jpg', u'\u05d4\u05e8\u05e4\u05ea\u05e7\u05d0\u05d5\u05ea': "https://"+'upload.wikimedia.org/wikipedia/he/3/38/%D7%94%D7%A8%D7%A4%D7%AA%D7%A7%D7%90%D7%95%D7%AA_%D7%91%D7%A8%D7%A0%D7%A8%D7%93_%D7%95%D7%91%D7%99%D7%90%D7%A0%D7%A7%D7%94_%D7%9B%D7%A8%D7%96%D7%94_%D7%A2%D7%91%D7%A8%D7%99%D7%AA.png', u'\u05de\u05e1\u05ea\u05d5\u05e8\u05d9\u05df': 'http://avi-goldberg.com/wp-content/uploads/5008202002.jpg', u'\u05de\u05e2\u05e8\u05d1\u05d5\u05df': "https://"+'i.ytimg.com/vi/Jw1iuGaNuy0/hqdefault.jpg', u'\u05de\u05dc\u05d7\u05de\u05d4': 'http://images.nana10.co.il/upload/mediastock/img/16/0/208/208383.jpg', u'\u05e4\u05e9\u05e2': 'http://www.mapah.co.il/wp-content/uploads/2012/09/DSC_1210.jpg', u'\u05e4\u05e0\u05d8\u05d6\u05d9\u05d4': 'http://blog.tapuz.co.il/beinhashurot/images/1943392_142.jpg', u'\u05de\u05e9\u05e4\u05d7\u05d4': 'http://kaye7.school.org.il/photos/family.jpg', u'\u05e7\u05d5\u05de\u05d3\u05d9\u05d4': "https://"+'upload.wikimedia.org/wikipedia/he/e/ef/Le_Tout_Nouveau_Testament.jpg', u'\u05d0\u05e0\u05d9\u05de\u05e6\u05d9\u05d4': 'http://www.printime.co.il/image/users/16584/ftp/my_files/smileynumbers1we.jpg', u'\u05d3\u05e8\u05de\u05d4': 'http://www.yorav.co.il/images/moshe+erela/2007/dram.JPG', u'\u05d4\u05e1\u05d8\u05d5\u05e8\u05d9\u05d4': "https://"+'medicine.ekmd.huji.ac.il/schools/occupationaltherapy/He/about/PublishingImages/%d7%aa%d7%9e%d7%95%d7%a0%d7%94%207.jpg', u'\u05e8\u05d5\u05de\u05e0\u05d8\u05d9': "https://"+'i.ytimg.com/vi/oUon62EIInc/maxresdefault.jpg', u'\u05d3\u05d5\u05e7\u05d5\u05de\u05e0\u05d8\u05e8\u05d9': 'http://img.mako.co.il/2017/03/28/704104_I.jpg', u'\u05d0\u05d9\u05de\u05d4': 'http://up203.siz.co.il/up2/y12o20immdyw.jpg', u'\u05de\u05d5\u05ea\u05d7\u05df': 'http://www.brz.co.il/wp-content/uploads/2014/06/11-350x350.jpg', u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9': "https://"+'upload.wikimedia.org/wikipedia/commons/c/cc/4pen.jpg', u'\u05d0\u05e7\u05e9\u05df': "https://"+'www.renne.co.il/wp-content/uploads/2017/07/actionsign.jpg'}

   images={}
   
   html=requests.get(link).json()
   aa=[]
   image='https://wordsfromjalynn.files.wordpress.com/2014/12/movie-genres-1.png'
   for data in html['genres']:
     if '/movie' in link:
       new_link='http://api.themoviedb.org/3/genre/%s/movies?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(str(data['id']),lang)
     else:
       new_link='http://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&sort_by=popularity.desc&with_genres=%s&language=%s&page=1'%(str(data['id']),lang)
     if data['name'] in tv_images:
       image=tv_images[data['name']]
     elif data['name'] in movie_images:
       image=movie_images[data['name']]
     
     aa.append(addDir3(data['name'],new_link,14,image,image,data['name']))
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),aa,len(aa))


def by_actor(url):
    all=[]
    if url=='www':
        url='1'
    if url=='1':
        aa=addDir3('[COLOR lightblue][I]חפש (באנגלית)[/I][/COLOR]','http://api.themoviedb.org/',126,domain_s+'cellcomtv.cellcom.co.il/globalassets/cellcomtv/content/sratim/pets-secret-life/480x543-template.jpg','http://www.videomotion.co.il/wp-content/uploads/whatwedo-Pic-small.jpg','חפש שחקן')
        all.append(aa)
    if 'themovie' in url:
    
        search_entered=''
        keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
        keyboard.doModal()
        if keyboard.isConfirmed():
               search_entered = keyboard.getText()
               link='https://api.themoviedb.org/3/search/person?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&page=1&include_adult=false'%search_entered
               url='1'
    else:
        link='https://api.themoviedb.org/3/person/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US&page=%s&language=he&sort_by=popularity.desc'%url
    
    headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
    html=requests.get(link,headers=headers).json()
    for items in html['results']:
        icon=items['profile_path']
        if len (items['known_for'])==0:
            
            continue
        if 'backdrop_path' in items['known_for'][0]:
            fanart=items['known_for'][0]['backdrop_path']
        else:
            fanart=' '
        if icon==None:
          icon=' '
        else:
          icon=domain_s+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart=domain_s+'image.tmdb.org/t/p/original/'+fanart
        aa=addDir3(items['name'],str(items['id']),127,icon,fanart,items['name'])
        all.append(aa)
    aa=addDir3('[COLOR aqua][I]עמוד הבא[/COLOR][/I]',str(int(url)+1),126,' ',' ','[COLOR aqua][I]עמוד הבא[/COLOR][/I]')
    all.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def actor_m_cobra(url,plot):

    
    if plot=='shows' or plot=='movie':
        if plot=='shows':
            tv_mode='tv'
        else:
            tv_mode='movie'
    else:
        choise=['סרטים','סדרות']
        ret = xbmcgui.Dialog().select("בחר", choise)
        if ret!=-1:
            if ret==0:
             
             tv_mode='movie'
            else:
             tv_mode='tv'
        else:
          sys.exit()

    if tv_mode=='movie':
       link='https://api.themoviedb.org/3/person/%s?api_key=1180357040a128da71b71716058f6c5c&append_to_response=credits&language=%s&sort_by=popularity.desc'%(url,lang)
    else:
       link='https://api.themoviedb.org/3/person/%s/tv_credits?api_key=1180357040a128da71b71716058f6c5c&append_to_response=credits&language=%s&sort_by=popularity.desc'%(url,lang)
    # from  resources.modules.client import  get_html
    headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
    html=requests.get(link,headers=headers).json()
    if tv_mode=='movie':
        url_g='https://'+'api.themoviedb.org/3/genre/movie/list?api_key=1180357040a128da71b71716058f6c5c&language=%s'%lang
                 
    else:
       url_g='https://'+'api.themoviedb.org/3/genre/tv/list?api_key=1180357040a128da71b71716058f6c5c&language=%s'%lang
    html_g=requests.get(url_g,headers=headers).json()
    if tv_mode=='movie':
      test=html['credits']['cast']
      



      mode=270
    else:
      test=html['cast']
      mode=271
    aa=[]
    i=[]
    try:
      if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
        from resources.modules.general import call_trakt
        i = (call_trakt('/users/me/watched/movies'))
    except Exception as e:
        
        i=[]
    
    all_movie_w=[]
    for ids in i:
      all_movie_w.append(str(ids['movie']['ids']['tmdb']))
    
    
    for items in test:
        watched='no'
        if str(items['id']) in all_movie_w:
           watched='yes'
        
        
        add_n=items['character']
        #log.warning(add_n)
        icon=items['poster_path']
        fanart=items['backdrop_path']
        if icon==None:
          icon=' '
        else:
          icon='https://'+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart='https://'+'image.tmdb.org/t/p/original/'+fanart
        
        plot=items['overview']
        if tv_mode=='movie':
          original_title=items['original_title']
        else:
          original_title=items['original_name']
        id=items['id']
        rating=items['vote_average']
        if tv_mode=='movie':
          title=items['title']
        else:
          title=items['name']
        if 'first_air_date' in items:
           if items['first_air_date']==None:
                    year=' '
           else:
                year=str(items['first_air_date'].split("-")[0])
        else:
            if 'release_date' in items:
              if items['release_date']==None:
                    year=' '
              else:
                year=str(items['release_date'].split("-")[0])
            else:
              year=' '
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
        genere = u' / '.join([genres_list[x] for x in items['genre_ids']])
        #except:genere=''
        
        video_data={}
        video_data['title']=title+' [COLOR blue](%s)[/COLOR]'%add_n
        #video_data['poster']=fanart
        video_data['plot']=plot
        #video_data['icon']=icon
        video_data['genre']=genere
        video_data['rating']=rating
        video_data['year']=year
        trailer = "plugin://%s?mode=171&id=%s&url=%s" % (addon_id,id,tv_movie)
        aa.append(addDir3(title+' [COLOR blue](%s)[/COLOR]'%add_n,'www',mode,icon,fanart,plot,data=year,original_title=original_title,id=str(id),rating=rating,heb_name=title,show_original_year=year,isr=' ',generes=genere,video_info=video_data,trailer=trailer,watched=watched))
    if tv_mode=='movie':
      test=html['credits']['crew']
      mode=270
    else:
      test=html['crew']
      mode=271
    for items in test:
        watched='no'
        if str(items['id']) in all_movie_w:
           watched='yes'
        add_n=items['department']
        icon=items['poster_path']
        fanart=items['backdrop_path']
        if icon==None:
          icon=' '
        else:
          icon='https://'+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart='https://'+'image.tmdb.org/t/p/original/'+fanart
        plot=items['overview']
        if tv_mode=='movie':
          original_title=items['original_title']
        else:
          original_title=items['original_name']
        id=items['id']
        rating=items['vote_average']
        if tv_mode=='movie':
          title=items['title']
        else:
          title=items['name']
        if 'first_air_date' in items:
           if items['first_air_date']==None:
                    year=' '
           else:
                year=str(items['first_air_date'].split("-")[0])
        else:
            if 'release_date' in items:
              if items['release_date']==None:
                    year=' '
              else:
                year=str(items['release_date'].split("-")[0])
            else:
              year=' '
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
        genere = u' / '.join([genres_list[x] for x in items['genre_ids']])
        #except:genere=''
        
        video_data={}
        video_data['title']=title+' [COLOR yellow](%s)[/COLOR]'%add_n
        video_data['plot']=plot
        video_data['genre']=genere
        video_data['rating']=rating
        video_data['year']=year
        trailer = "%s?mode=25&id=%s&url=%s" % (sys.argv,id,tv_mode)
        aa.append(addDir3(title+' [COLOR yellow](%s)[/COLOR]'%add_n,'www',mode,icon,fanart,plot,data=year,original_title=original_title,id=str(id),rating=rating,heb_name=title,show_original_year=year,isr=' ',generes=genere,video_info=video_data,trailer=trailer,watched=watched))
        
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),aa,len(aa))
def actor_m(url,plot):

    
    if plot=='shows' or plot=='movie':
        if plot=='shows':
            tv_mode='tv'
        else:
            tv_mode='movie'
    else:
        choise=['סדרות','סרטים']
        ret = xbmcgui.Dialog().select("בחר", choise)
        if ret!=-1:
            if ret==0:
             tv_mode='tv'
            else:
             tv_mode='movie'
        else:
          sys.exit()

    if tv_mode=='movie':
       link='https://api.themoviedb.org/3/person/%s?api_key=1180357040a128da71b71716058f6c5c&append_to_response=credits&language=%s&sort_by=popularity.desc'%(url,lang)
    else:
       link='https://api.themoviedb.org/3/person/%s/tv_credits?api_key=1180357040a128da71b71716058f6c5c&append_to_response=credits&language=%s&sort_by=popularity.desc'%(url,lang)
    # from  resources.modules.client import  get_html
    headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
    html=requests.get(link,headers=headers).json()
    if tv_mode=='movie':
        url_g='https://'+'api.themoviedb.org/3/genre/movie/list?api_key=1180357040a128da71b71716058f6c5c&language=%s'%lang
                 
    else:
       url_g='https://'+'api.themoviedb.org/3/genre/tv/list?api_key=1180357040a128da71b71716058f6c5c&language=%s'%lang
    html_g=requests.get(url_g,headers=headers).json()
    if tv_mode=='movie':
      test=html['credits']['cast']
      



      mode=15
    else:
      test=html['cast']
      mode=170
    aa=[]
    i=[]
    try:
      if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
        from resources.modules.general import call_trakt
        i = (call_trakt('/users/me/watched/movies'))
    except Exception as e:
        
        i=[]
    
    all_movie_w=[]
    for ids in i:
      all_movie_w.append(str(ids['movie']['ids']['tmdb']))
    
    
    for items in test:
        watched='no'
        if str(items['id']) in all_movie_w:
           watched='yes'
        
        
        add_n=items['character']
        #log.warning(add_n)
        icon=items['poster_path']
        fanart=items['backdrop_path']
        if icon==None:
          icon=' '
        else:
          icon='https://'+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart='https://'+'image.tmdb.org/t/p/original/'+fanart
        
        plot=items['overview']
        if tv_mode=='movie':
          original_title=items['original_title']
        else:
          original_title=items['original_name']
        id=items['id']
        rating=items['vote_average']
        if tv_mode=='movie':
          title=items['title']
        else:
          title=items['name']
        if 'first_air_date' in items:
           if items['first_air_date']==None:
                    year=' '
           else:
                year=str(items['first_air_date'].split("-")[0])
        else:
            if 'release_date' in items:
              if items['release_date']==None:
                    year=' '
              else:
                year=str(items['release_date'].split("-")[0])
            else:
              year=' '
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
        genere = u' / '.join([genres_list[x] for x in items['genre_ids']])
        #except:genere=''
        
        video_data={}
        video_data['title']=title+' [COLOR blue](%s)[/COLOR]'%add_n
        #video_data['poster']=fanart
        video_data['plot']=plot
        #video_data['icon']=icon
        video_data['genre']=genere
        video_data['rating']=rating
        video_data['year']=year
        trailer = "plugin://%s?mode=171&id=%s&url=%s" % (addon_id,id,tv_movie)
        aa.append(addDir3(title+' [COLOR blue](%s)[/COLOR]'%add_n,'www',mode,icon,fanart,plot,data=year,original_title=original_title,id=str(id),rating=rating,heb_name=title,show_original_year=year,isr=' ',generes=genere,video_info=video_data,trailer=trailer,watched=watched))
    if tv_mode=='movie':
      test=html['credits']['crew']
      mode=15
    else:
      test=html['crew']
      mode=16
    for items in test:
        watched='no'
        if str(items['id']) in all_movie_w:
           watched='yes'
        add_n=items['department']
        icon=items['poster_path']
        fanart=items['backdrop_path']
        if icon==None:
          icon=' '
        else:
          icon='https://'+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart='https://'+'image.tmdb.org/t/p/original/'+fanart
        plot=items['overview']
        if tv_mode=='movie':
          original_title=items['original_title']
        else:
          original_title=items['original_name']
        id=items['id']
        rating=items['vote_average']
        if tv_mode=='movie':
          title=items['title']
        else:
          title=items['name']
        if 'first_air_date' in items:
           if items['first_air_date']==None:
                    year=' '
           else:
                year=str(items['first_air_date'].split("-")[0])
        else:
            if 'release_date' in items:
              if items['release_date']==None:
                    year=' '
              else:
                year=str(items['release_date'].split("-")[0])
            else:
              year=' '
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
        genere = u' / '.join([genres_list[x] for x in items['genre_ids']])
        #except:genere=''
        
        video_data={}
        video_data['title']=title+' [COLOR yellow](%s)[/COLOR]'%add_n
        video_data['plot']=plot
        video_data['genre']=genere
        video_data['rating']=rating
        video_data['year']=year
        trailer = "%s?mode=25&id=%s&url=%s" % (sys.argv,id,tv_mode)
        aa.append(addDir3(title+' [COLOR yellow](%s)[/COLOR]'%add_n,'www',mode,icon,fanart,plot,data=year,original_title=original_title,id=str(id),rating=rating,heb_name=title,show_original_year=year,isr=' ',generes=genere,video_info=video_data,trailer=trailer,watched=watched))
        
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),aa,len(aa))
def search_actor():
    search_entered=''
    keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
    keyboard.doModal()
    if keyboard.isConfirmed():
           search_entered = keyboard.getText()
           
           link='https://api.themoviedb.org/3/search/person?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&query=%s&page=1&include_adult=false'%search_entered
           headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
           html=requests.get(link,headers=headers).json()
           for items in html['results']:
                    icon=items['profile_path']
                    fanart=items['known_for'][0]['backdrop_path']
                    if icon==None:
                      icon=' '
                    else:
                      icon=domain_s+'image.tmdb.org/t/p/original/'+icon
                    if fanart==None:
                      fanart=' '
                    else:
                      fanart=domain_s+'image.tmdb.org/t/p/original/'+fanart
                    addDir4(items['name'],str(items['id']),127,icon,fanart,items['name'])

def update_collections():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_d=[]
    collection_cacheFile = os.path.join(tmdb_data_dir, 'collection_data.db')
    dbcon_tmdb = database.connect(collection_cacheFile)
    dbcur_tmdb = dbcon_tmdb.cursor()
    dbcur_tmdb.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""id TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""lang TEXT);"% 'collection')

    try:
        dbcur_tmdb.execute("VACUUM 'collection';")
        dbcur_tmdb.execute("PRAGMA auto_vacuum;")
        dbcur_tmdb.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
        dbcur_tmdb.execute("PRAGMA temp_store=MEMORY ;")
    except:
     pass
    dbcon_tmdb.commit()
    
    import gzip
    from resources.modules.pen_addons import download_file
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(days=1)
    dd=yesterday.strftime("%m_%d_%Y")
    #dd=time.strftime("%m_%d_%Y")
    #log.warning(dd)
    url='http://files.tmdb.org/p/exports/collection_ids_%s.json.gz'%dd
    #log.warning(url)
    download_file(url,user_dataDir)

    with gzip.open(os.path.join(user_dataDir,'fixed_list.txt'), 'rb') as f:
      file_content = (f.read().decode())
    ff='['+file_content.replace('\n',",")+']'
   
    j_file=json.loads(ff.replace(',]',']'))
    zzz=0
    start_time=time.time()
    dp = xbmcgui . DialogProgress ( )
    try:
        dp.create('אנא המתן','מחפש מקורות', '','')
    except:
        dp.create('אנא המתן','מחפש מקורות'+'\n'+ ''+'\n'+'')
    dbcur_tmdb.execute("select id from collection")
    match = dbcur_tmdb.fetchall()
    all_ids=[]
    for ids in match:
        all_ids.append(str(ids[0]))
        
   
    inner_count=0
    for item in j_file:
        
        try:
           if str(item['id']) not in all_ids:
           
            elapsed_time = time.time() - start_time
            
            
            url='https://api.themoviedb.org/3/collection/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=he'%(item['id'])
            
            x=requests.get(url).json()
            #log.warning('32333 '+str(x))
            try:
                if x['poster_path']==None:
                    x['poster_path']=''
            except:pass
            try:
                if x['backdrop_path']==None:
                    x['backdrop_path']=''
            except:pass
            try:
                if len(x['parts'])==0:
                    continue
            except:pass
            try:
                dbcur_tmdb.execute("INSERT INTO collection Values ('%s', '%s', '%s', '%s', '%s','%s');" %  (x['name'].replace("'","%27"),x['id'],x['poster_path'].replace("'","%27"),x['backdrop_path'].replace("'","%27"),x['overview'].replace("'","%27"),x['parts'][0]['original_language']))
                try:
                    dp.update(int(((zzz* 100.0)/(len(j_file))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),x['name'], str(zzz)+'/'+str(len(j_file)))
                except:
                    dp.update(int(((zzz* 100.0)/(len(j_file))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+x['name']+'\n'+ str(zzz)+'/'+str(len(j_file)))
            except:pass
            if dp.iscanceled():
                     break
            inner_count+=1
            if inner_count>100:
                inner_count=0
                dbcon_tmdb.commit()
           zzz+=1
        except Exception as e:
            xbmcgui.Dialog().ok('Error occurred',str(item['id'])+' ' +item['name']+'_'+str(e))
            break
                 
    dp.close()
    dbcon_tmdb.commit()
    dbcur_tmdb.close()
    dbcon_tmdb.close()
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    
def collections(page):
    all_d=[]
    collection_cacheFile = os.path.join(tmdb_data_dir, 'collection_data.db')
    dbcon_tmdb = database.connect(collection_cacheFile)
    dbcur_tmdb = dbcon_tmdb.cursor()
    dbcur_tmdb.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""id TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""lang TEXT);"% 'collection')
    dbcon_tmdb.commit()

    dp = xbmcgui . DialogProgress ( )
    try:
        dp.create('אנא המתן','טוען סרטים', '','')
    except:
        dp.create('אנא המתן','טוען סרטים'+'\n'+ ''+'\n'+'')
    amount_per_page=Addon.getSetting("collection_size")
    dbcur_tmdb.execute("select * from collection where lang='en' LIMIT %s OFFSET %s;"%(amount_per_page,str(int(page)*100)))
    match = dbcur_tmdb.fetchall()
    zzz=0
    start_time=time.time()
    for name,id,icon,fanart,plot,lang in match:
        if Addon.getSetting("collection_dp")=='true':
            elapsed_time = time.time() - start_time
            if Addon.getSetting("collection_dp")=='true':
                try:
                    dp.update(int(((zzz* 100.0)/(len(match))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),name, str(zzz)+'/'+str(len(match)))
                except:
                    pass
            zzz+=1
            if dp.iscanceled():
                     break
        aa=addDir3(name.replace('%27',"'"),id,122,domain_s+'image.tmdb.org/t/p/original/'+icon,domain_s+'image.tmdb.org/t/p/original/'+fanart,plot)
        all_d.append(aa)
    if Addon.getSetting("collection_dp")=='true':
        dp.close()
    dbcur_tmdb.close()
    dbcon_tmdb.close()
    aa=addDir3('[COLOR aqua][I]עמוד הבא[/COLOR][/I]',str(int(page)+1),121,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','[COLOR aqua][I]עמוד הבא[/COLOR][/I]')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def collection_detials(url):
    
    all_d=[]
    url='https://api.themoviedb.org/3/collection/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=he'%url
    x=requests.get(url).json()
    # logging.warning('444441111 '+str(x))
    #html_g=cache.get(cache_genered,72,'movie', table='poster')
    if 'tv' in url:
        html_g=html_g_tv
    else:
        html_g=html_g_movie
    
    for items in x['parts']:
        new_name=items['title']
        if items['poster_path']==None:
            items['poster_path']=''
        if items['backdrop_path']==None:
            items['backdrop_path']=''
                
        icon=domain_s+'image.tmdb.org/t/p/original/'+items['poster_path']
        fan=domain_s+'image.tmdb.org/t/p/original/'+items['backdrop_path']
        if 'release_date' in items:
            year=str(items['release_date'].split("-")[0]) 
        else:
            year=''
        original_name=items['original_title']
        
            
        id=str(items['id'])
        rating=items['vote_average']
        isr='0'
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                        if i['name'] is not None])
        try:genere = u' / '.join([genres_list[x] for x in items['genre_ids']])
        except:genere=''
        plot=items['overview']
        aa=addDir3(new_name,url,15,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
def search_movies(heb_name,original_title,data,iconimage,fanart,tmdb,season,episode,remote=False):
    global silent,selected_index,break_window,play_status
    play_status='מחפש מקורות'

    count=0
    if not os.path.exists(os.path.join(user_dataDir, '4.1.1')):
        
        data={'type':'checklogin',
             'info':''
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        if event['status']==2 or event['status']=='Needs to log from setting':
            tele_source=False
        else:
            tele_source=True
        if tele_source is False:

            DIALOG         = xbmcgui.Dialog()
            choice = DIALOG.yesno('יש להגדיר את חשבון הטלמדיה שלכם', "האם תרצה להגדיר אותו עכשיו?", yeslabel="[B][COLOR white]כן[/COLOR][/B]", nolabel="[B][COLOR white]לא[/COLOR][/B]")
            if choice == 1:
                choice = DIALOG.yesno('הגדרת חשבון','איזה חשבון בדיוק תרצו להגדיר?', yeslabel="[B][COLOR white]חשבון VIP[/COLOR][/B]", nolabel="[B][COLOR white]חשבון שלי אישי[/COLOR][/B]")
                if choice == 1:
                    xbmc.executebuiltin( "RunPlugin(plugin://plugin.program.Settingz-Anon/?mode=302&url=www)" )
                    sys.exit() 
                else:
                    xbmc.executebuiltin( "RunPlugin(plugin://plugin.video.telemedia?mode=5&url=www)" )
                    sys.exit() 
            else:
             xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
             sys.exit() 

    if Addon.getSetting('new_play_window2')=='true':
     if not tmdb=='0':
        tv_movie='movie'
        t = Thread(target=show_new_window, args=(tv_movie, tmdb, season, episode,fanart,))
        t.start()
    else:
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    time_to_save=0
    netflix_mod=Addon.getSetting("netflix_mod")
    c_original_title=original_title

    original_title=original_title.replace('%20',' ')
    if netflix_mod== 'false':
    

            all_links=searchtmdb(tmdb,'all','0$$$0',heb_name,iconimage,fanart,season,episode,no_subs=1,original_title=original_title,dont_return=False,manual=False)

            all_links=all_links+searchtmdb(tmdb,'all','0$$$0',original_title,iconimage,fanart,season,episode,original_title=original_title,dont_return=False,manual=False)
       
            all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
       

    else:
       all_links=searchtmdb(tmdb,'all','0$$$0',heb_name,iconimage,fanart,season,episode,no_subs=1,original_title=original_title,dont_return=False,manual=False)
       
       all_links_eng=searchtmdb(tmdb,'all','0$$$0',original_title,iconimage,fanart,season,episode,original_title=original_title,dont_return=False,manual=False)
       
       all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
    
       all_links_eng=sorted(all_links_eng, key=lambda x: x[4], reverse=False)
    
    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    all_results=[]
    filter_dup=Addon.getSetting("dup_links")
    display=Addon.getSetting("new_source")
    all_t_links=[]
    once=0
    d_save=[]
    menu=[]
    
    for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in all_links:
        fix_name=name.replace('.',' ').replace('_',' ').replace(':','')

        # if heb_name.replace('-',' ').replace(':','') not in fix_name and original_title.replace('-',' ').replace(':','') not in fix_name:
            # continue
        if netflix_mod== 'true':
            if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                   continue
        regex=' ע(.+?) פ(.+?) '
        mmm=re.compile(regex).findall(name)
        if len(mmm)>0:
            continue
        regex='S(.+?)E(.+?)'
        mmm=re.compile(regex).findall(name)
        if len(mmm)>0:
            continue
        regex='ep(.+?)'
        mmm=re.compile(regex).findall(name)
        if len(mmm)>0:
            continue
        if '5.1' in name:
            sound='[COLOR red]5.1[/COLOR]'
        elif '6CH' in name:
            sound='[COLOR red]5.1[/COLOR]'
        elif 'DD5' in name:
            sound='[COLOR red]5.1[/COLOR]'

        else:
            sound=''
        if 'BluRay' in name:
            sou='[COLOR white]BluRay[/COLOR]'
        elif 'Bluray' in name:
            sou='[COLOR white]BluRay[/COLOR]'
        elif 'CD1' in name:
            sou='[COLOR white]חלק 1[/COLOR]'
        elif 'CD2' in name:
            sou='[COLOR white]חלק 2[/COLOR]'
        elif 'CD3' in name:
            sou='[COLOR white]חלק 3[/COLOR]'
        elif 'CD4' in name:
            sou='[COLOR white]חלק 4[/COLOR]'
        elif 'CD5' in name:
            sou='[COLOR white]חלק 5[/COLOR]'
        elif 'חלק_1' in name:
            sou='[COLOR white]חלק 1[/COLOR]'
        elif 'חלק_2' in name:
            sou='[COLOR white]חלק 2[/COLOR]'
        elif 'חלק_3' in name:
            sou='[COLOR white]חלק 3[/COLOR]'
        elif 'חלק_4' in name:
            sou='[COLOR white]חלק 4[/COLOR]'
        elif 'חלק_5' in name:
            sou='[COLOR white]חלק 5[/COLOR]'
        elif 'ח1' in name:
            sou='[COLOR white]חלק 1[/COLOR]'
        elif 'ח2' in name:
            sou='[COLOR white]חלק 2[/COLOR]'
        elif 'ח3' in name:
            sou='[COLOR white]חלק 3[/COLOR]'
        elif 'ח4' in name:
            sou='[COLOR white]חלק 4[/COLOR]'
        elif 'ח5' in name:
            sou='[COLOR white]חלק 5[/COLOR]'
        elif 'חלק 1' in name:
            sou='[COLOR white]חלק 1[/COLOR]'
        elif 'חלק 2' in name:
            sou='[COLOR white]חלק 2[/COLOR]'
        elif 'חלק 3' in name:
            sou='[COLOR white]חלק 3[/COLOR]'
        elif 'חלק 4' in name:
            sou='[COLOR white]חלק 4[/COLOR]'
        elif 'חלק 5' in name:
            sou='[COLOR white]חלק 5[/COLOR]'
        else:
            sou=''
        f_size2.replace('%20',' ')

        if name not in all_t_links or filter_dup==False:
                
                all_t_links.append(name)
                all_results.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title))
                if remote==False:
                    count+=1
                    d_save.append((name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2))
                    link2=('%s?name=%s&mode=3&url=%s&season=%s&episode=%s&original_title=%s&tmdb=%s'%(sys.argv[0],name,link,season,episode,original_title,tmdb))
                    try:
                        listItem=xbmcgui.ListItem(clean_sources(name),iconImage=icon, thumbnailImage=fanart,path=link2)
                    except:
                        listItem=xbmcgui.ListItem(clean_sources(name),path=link2)
                    listItem.setInfo('video', {'Title': name})
                    menu.append([clean_sources(name),'',f_size2,q,sound,sou,'',''])
                    addLink( name, link,mode,False, icon,fan,f_size2,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=c_original_title)
                    
    if netflix_mod== 'true':
        for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in all_links_eng:
            if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                   continue
            regex=' ע(.+?) פ(.+?) '
            mmm=re.compile(regex).findall(name)
            if len(mmm)>0:
                continue
            regex='S(.+?)E(.+?)'
            mmm=re.compile(regex).findall(name)
            if len(mmm)>0:
                continue
            regex='ep(.+?)'
            mmm=re.compile(regex).findall(name)
            if len(mmm)>0:
                continue
            if '5.1' in name:
                sound='[COLOR red]5.1[/COLOR]'
            elif '6CH' in name:
                sound='[COLOR red]5.1[/COLOR]'
            elif 'DD5' in name:
                sound='[COLOR red]5.1[/COLOR]'
            elif 'ח1' in name:
                sound='[COLOR white]חלק 1[/COLOR]'
            elif 'ח2' in name:
                sound='[COLOR white]חלק 2[/COLOR]'
            elif 'ח3' in name:
                sound='[COLOR white]חלק 3[/COLOR]'
            else:
                sound=''
            if 'BluRay' in name:
                sou='[COLOR white]BluRay[/COLOR]'
            elif 'Bluray' in name:
                sou='[COLOR white]BluRay[/COLOR]'
            elif 'CD1' in name:
                sou='[COLOR white]חלק 1[/COLOR]'
            elif 'CD2' in name:
                sou='[COLOR white]חלק 2[/COLOR]'
            elif 'CD3' in name:
                sou='[COLOR white]חלק 3[/COLOR]'
            elif 'CD4' in name:
                sou='[COLOR white]חלק 4[/COLOR]'
            elif 'CD5' in name:
                sou='[COLOR white]חלק 5[/COLOR]'
            elif 'חלק_1' in name:
                sou='[COLOR white]חלק 1[/COLOR]'
            elif 'חלק_2' in name:
                sou='[COLOR white]חלק 2[/COLOR]'
            elif 'חלק_3' in name:
                sou='[COLOR white]חלק 3[/COLOR]'
            elif 'חלק_4' in name:
                sou='[COLOR white]חלק 4[/COLOR]'
            elif 'חלק_5' in name:
                sou='[COLOR white]חלק 5[/COLOR]'
            elif 'ח1' in name:
                sou='[COLOR white]חלק 1[/COLOR]'
            elif 'ח2' in name:
                sou='[COLOR white]חלק 2[/COLOR]'
            elif 'ח3' in name:
                sou='[COLOR white]חלק 3[/COLOR]'
            elif 'ח4' in name:
                sou='[COLOR white]חלק 4[/COLOR]'
            elif 'ח5' in name:
                sou='[COLOR white]חלק 5[/COLOR]'
            elif 'חלק 1' in name:
                sou='[COLOR white]חלק 1[/COLOR]'
            elif 'חלק 2' in name:
                sou='[COLOR white]חלק 2[/COLOR]'
            elif 'חלק 3' in name:
                sou='[COLOR white]חלק 3[/COLOR]'
            elif 'חלק 4' in name:
                sou='[COLOR white]חלק 4[/COLOR]'
            elif 'חלק 5' in name:
                sou='[COLOR white]חלק 5[/COLOR]'
            else:
                sou=''
            f_size2.replace('%20',' ')
            if name not in all_t_links or filter_dup==False:
                
                    all_t_links.append(name)
                    all_results.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title))
                    if remote==False:
                        d_save.append((name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2))

                        menu.append([clean_sources(name),'',f_size2,q,sound,sou,'',''])
                        addLink( name, link,mode,False, icon,fan,f_size2,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=c_original_title)

    if len(d_save)==0:
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אין מקורות[/COLOR]' % COLOR2)
        break_window=True
        sys.exit()
    if display== 'true' and  Addon.getSetting("one_click")=='false' and Addon.getSetting("netflix_mod")=='false':
         menu2 = ContextMenu_new2('plugin.video.telemedia', menu,iconimage,fanart,description,int(count))
         menu2.doModal()
         del menu2
         ret=selected_index
         
         if ret!=-1:
                name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2=d_save[ret]
                play(name,link,data,icon,fan,no_subs,tmdb,season,episode,c_original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='false')
         break_window=True
         sys.exit()
    if Addon.getSetting("one_click")=='true' and remote==False:

            name,link,data,icon,fan,no_subs,tmdb,season,episode,c_original_title,f_size2=d_save[0]
            play(name,link,data,icon,fan,no_subs,tmdb,season,episode,c_original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='false')
            sys.exit()
    if Addon.getSetting("netflix_mod")=='true' and remote==False:

            name,link,data,icon,fan,no_subs,tmdb,season,episode,c_original_title,f_size2=d_save[0]
            play(name,link,data,icon,fan,no_subs,tmdb,season,episode,c_original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='false')
            if Addon.getSetting("sh_one_click")=='true' and display== 'true':
                menu2 = ContextMenu_new2('plugin.video.telemedia', menu,iconimage,fanart,description,int(count))
                menu2.doModal()
                del menu2
                ret=selected_index
                if ret!=-1:
                        name,link,data,icon,fan,no_subs,tmdb,season,episode,c_original_title,f_size2=d_save[ret]
                        play(name,link,data,icon,fan,no_subs,tmdb,season,episode,c_original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='false')
                break_window=True
                sys.exit()
                
            sys.exit()
    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    return all_results

def clear_color(name):
    new_name=name
    if '[COLOR' in name:
        regex='\](.+?)\['
        n_name=re.compile(regex).findall(name)
        if len(n_name)>0:
            new_name=n_name[0]
    return new_name
def get_rest_data(name,url,mode,iconimage,fanart,description,video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=0,generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false'):
        name=name.replace("|",' ')
        description=description.replace("|",' ')
        try:
            te1=sys.argv[0]+"?url="+que(url)+"&mode="+str(mode)
            
            te2="&name="+(name)+"&iconimage="+que(iconimage)+"&fanart="+que(fanart)+"&description="+que(description)+"&heb_name="+(heb_name)+"&dates="+(dates)
            te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
            te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)
        
        
        
        
        
            u=te1 + te2 + te3 + te4+"&fav_status="+fav_status
        except:
           reload(sys)  
           sys.setdefaultencoding('utf8')
           te1=sys.argv[0]+"?url="+que(url)+"&mode="+str(mode)
            
           te2="&name="+(name)+"&iconimage="+que(iconimage)+"&fanart="+que(fanart)+"&description="+que(description)+"&heb_name="+(heb_name)+"&dates="+(dates)
           te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
           te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)
        
           u=te1 + te2 + te3 + te4+"&fav_status="+fav_status
           
        return u
def undo_get_rest_data(full_str):
    params=get_custom_params(full_str)
    for items in params:
        params[items]=params[items].replace(" ","%20")

    url=None
    name=None
    mode=None
    iconimage=None
    fanart=None
    description=' '
    original_title=' '
    fast_link=''
    data=0
    id=' '
    saved_name=' '
    prev_name=' '
    isr=0
    season="%20"
    episode="%20"
    show_original_year=0
    heb_name=' '
    tmdbid=' '
    eng_name=' '
    dates=' '
    data1='[]'
    fav_status='false'
    only_torrent='no'
    only_heb_servers='0'
    new_windows_only=False
    try:
            url=unque(params["url"])
    except:
            pass
    try:
            name=unque(params["name"])
    except:
            pass
    try:
            iconimage=unque(params["iconimage"])
    except:
            pass
    try:        
            mode=int(params["mode"])
    except:
            pass
    try:        
            fanart=unque(params["fanart"])
    except:
            pass
    try:        
            description=unque(params["description"])
    except:
            pass
    try:        
            data=unque(params["data"])
    except:
            pass
    try:        
            original_title=(params["original_title"])
    except:
            pass
    try:        
            id=(params["id"])
    except:
            pass
    try:        
            season=(params["season"])
    except:
            pass
    try:        
            episode=(params["episode"])
    except:
            pass
    try:        
            tmdbid=(params["tmdbid"])
    except:
            pass
    try:        
            eng_name=(params["eng_name"])
    except:
            pass
    try:        
            show_original_year=(params["show_original_year"])
    except:
            pass
    try:        
            heb_name=unque(params["heb_name"])
    except:
            pass
    try:        
            isr=int(params["isr"])
    except:
            pass
    try:        
            saved_name=clean_name(params["saved_name"],1)
    except:
            pass
    try:        
            prev_name=(params["prev_name"])
    except:
            pass
    try:        
            dates=(params["dates"])
    except:
            pass
    try:        
            data1=(params["data1"])
    except:
            pass
    try:        
        
            fast_link=unque(params["fast_link"])
    except:
            pass
    try:        
        
            fav_status=(params["fav_status"])
    except:
            pass
    try:        
        
            only_torrent=(params["only_torrent"])
    except:
            pass
    try:        
        
            only_heb_servers=(params["only_heb_servers"])
    except:
            pass
    try:        
           
            new_windows_only=(params["new_windows_only"])
            new_windows_only = new_windows_only == "true" 
    except:
            pass
    return heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb

def cleantitle(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub(r'\<[^>]*\>','', title)
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\(|\)|\[|\]|\{|\}|\s', '', title).lower()
    return title.lower()
	
def updateSkip(title, seconds=defaultSkip, start=0, service=True):
    with open(skipFile, 'r') as file:
         json_data = json.load(file)
         for item in json_data:
               if cleantitle(item['title']) == cleantitle(title):
                  item['service'] = service
                  item['skip'] = seconds
                  item['start'] = start
    with open(skipFile, 'w') as file:
        json.dump(json_data, file, indent=1)
    if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("skip_intro_s")=='true' and len(Addon.getSetting("firebase"))>0:
        table_name='skipintro'

        all_firebase=read_firebase(table_name)
        write_fire=True
        newIntro = {'title': title, 'service': service, 'skip': seconds, 'start': start}
        for items in all_firebase:
            if all_firebase[items]['data']['title']==title:
                delete_firebase(table_name,items)
                break
        if write_fire:
            write_firebase_intro(newIntro,table_name)
def newskip(title, seconds, start=1):
    if seconds == '' or seconds == None: seconds = defaultSkip
    newIntro = {'title': title, 'service': True, 'skip': seconds, 'start': start}
    try:
        with open(skipFile) as f:
            data = json.load(f)
    except:
        data = []
    for item in data:
        if cleantitle(title) in cleantitle(item['title']):
            updateSkip(title, seconds=seconds, start=start, service=True)
            return
    data.append(newIntro)
    with open(skipFile, 'w') as f:
        json.dump(data, f, indent=2)
    if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("skip_intro_s")=='true' and len(Addon.getSetting("firebase"))>0:
        table_name='skipintro'

        all_firebase=read_firebase(table_name)
        write_fire=True
        for items in all_firebase:
            if all_firebase[items]['data']==newIntro:
                delete_firebase(table_name,items)
                break
        if write_fire:
            write_firebase_intro(newIntro,table_name)

def getSkip(title):
    try:
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("skip_intro_s")=='true' and len(Addon.getSetting("firebase"))>0:

            all_db=read_firebase('skipintro')
            data=[]
            for itt in all_db:
                items=all_db[itt]
                data.append((items['data']))
        else:
            with open(skipFile) as f:
                data = json.load(f)
        skip = [i for i in data if i['service'] != False]
        skip = [i['skip'] for i in skip if cleantitle(i['title']) == cleantitle(title)][0]
    except: 
        skip = defaultSkip
        newskip(title, skip)
    return  skip
	
def checkService(title):
    try:
        with open(skipFile) as f:
            data = json.load(f)
        skip = [i['service'] for i in data if cleantitle(i['title']) == cleantitle(title)][0]
    except: skip = True
    return  skip

def checkStartTime(title):
    try:
        with open(skipFile) as f: data = json.load(f)
        start = [i['start'] for i in data if cleantitle(i['title']) == cleantitle(title)][0]
    except: start = 0
    return  start
	
if not os.path.exists(skipFile): newskip('default', defaultSkip)

def skip_intro():
   try:
        from sqlite3 import dbapi2 as database
   except:
        from pysqlite2 import dbapi2 as database
   cacheFile=os.path.join(user_dataDir,'database.db')
   dbcon = database.connect(cacheFile)
   dbcur = dbcon.cursor()

   dbcur.execute("SELECT * FROM nextup")
   match = dbcur.fetchall()
   dbcur.close()
   dbcon.close()
    
   for dd in match:
        dd_a=dd
   name,data,original_title,id,season,episode,show_original_year,tvdb_id=json.loads(base64.b64decode(dd_a[0]))[0]
   
   timeout=0
   skipped = False
   break_jumpx=1
   time_left=999999
   while timeout<200:
        timeout+=1
        if break_jumpx==0:
            break
        if xbmc.Player().isPlaying():
            break
        xbmc.sleep(100)
   try:

        while xbmc.Player().isPlaying():
            if break_jumpx==0:
                break
            playTime = xbmc.Player().getTime()
            currentShow = original_title
            if currentShow: 

                    if playTime > 250: skipped = True

                    if skipped == False:

                        time.sleep(1)
                        timeNow = xbmc.Player().getTime()
                        status = checkService(original_title)
                        
                        if status == False:
                            skipped = True
                            raise Exception()
                        startTime = checkStartTime(original_title)
                       
                        if int(timeNow) >= int(startTime):
                           if int(timeNow) > int(startTime)+10:
                              
                              break
                           else:
                            if not season=='1' or not episode=='1':
                             Dialog = CustomDialog('script-dialog.xml',Addon.getAddonInfo('path'), show=original_title)
                             Dialog.doModal()
                             skipped = True
                             del Dialog
            print ("CURRENT SHOW PLAYER", currentShow, playTime)
        else: skipped = False
   except: pass
def ep_time(title, seconds, start=1):
    if seconds == '' or seconds == None: seconds = default_ep_Skip
    newIntro = {'title': title, 'service': True, 'skip': seconds, 'start': start}
    try:
        with open(time_ep_File) as f:
            data = json.load(f)
    except:
        data = []
    for item in data:
        if cleantitle(title) in cleantitle(item['title']):
            update_ep_time(title, seconds=seconds, start=start, service=True)
            return
    data.append(newIntro)
    with open(time_ep_File, 'w') as f:
        json.dump(data, f, indent=2)
    if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("time_ep")=='true' and len(Addon.getSetting("firebase"))>0:
        table_name='time_ep'

        all_firebase=read_firebase(table_name)
        write_fire=True
        for items in all_firebase:
            if all_firebase[items]['data']==newIntro:
                delete_firebase(table_name,items)
                break
        if write_fire:
            write_firebase_intro(newIntro,table_name)
def get_ep_time(title):
    try:
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("time_ep")=='true' and len(Addon.getSetting("firebase"))>0:

            all_db=read_firebase('time_ep')
            data=[]
            for itt in all_db:
                items=all_db[itt]
                data.append((items['data']))
        else:
            with open(time_ep_File) as f:
                data = json.load(f)
        skip = [i for i in data if i['service'] != False]
        skip = [i['skip'] for i in skip if cleantitle(i['title']) == cleantitle(title)][0]
    except: 
        skip = default_ep_Skip
        ep_time(title, skip)
    return  skip
def update_ep_time(title, seconds=default_ep_Skip, start=0, service=True):
    with open(time_ep_File, 'r') as file:
         json_data = json.load(file)
         for item in json_data:
               if cleantitle(item['title']) == cleantitle(title):
                  item['service'] = service
                  item['skip'] = seconds
                  item['start'] = start
    with open(time_ep_File, 'w') as file:
        json.dump(json_data, file, indent=1)
    if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("time_ep")=='true' and len(Addon.getSetting("firebase"))>0:
        table_name='time_ep'

        all_firebase=read_firebase(table_name)
        write_fire=True
        newIntro = {'title': title, 'service': service, 'skip': seconds, 'start': start}
        for items in all_firebase:
            if all_firebase[items]['data']['title']==title:
                delete_firebase(table_name,items)
                break
        if write_fire:
            write_firebase_intro(newIntro,table_name)
if not os.path.exists(time_ep_File): ep_time('default', default_ep_Skip)
# heb_name='נמלטים'
def load_test_data(title,icon,fanart,plot,s_title,season,episode,list):
    test_episode = {"episodeid": 0, "tvshowid": 0, "title": title, "art": {}}
    test_episode["art"]["tvshow.poster"] = icon
    test_episode["art"]["thumb"] = icon
    test_episode["art"]["tvshow.fanart"] = fanart
    test_episode["art"]["tvshow.landscape"] =fanart
    test_episode["art"]["tvshow.clearart"] = fanart
    test_episode["art"]["tvshow.clearlogo"] = icon
    test_episode["plot"] = plot
    test_episode["showtitle"] =heb_name+' עונה %s פרק %s '%(season,episode)
    test_episode["playcount"] = 1
    test_episode["season"] =int( season)
    test_episode["episode"] = int(episode)
    test_episode["seasonepisode"] = " עונה %s פרק %s "%(season,episode)
    test_episode["rating"] = None
    test_episode["firstaired"] = ""
    test_episode["list"]=list
    return test_episode
def calculate_progress_steps(period):
                    return (100.0 / int(period)) / 10
# name_n=''
# iconimage=''
# plot_n='דדד'
# season=1
# episode=1
# list='1'
# next_up_page = UpNext("script-upnext-upnext.xml",Addon.getAddonInfo('path'), "DefaultSkin", "1080i")
# ep=load_test_data(name_n,iconimage,iconimage,plot_n,name_n,season,episode,list)

# next_up_page.setItem(ep)

# next_up_page.setProgressStepSize(calculate_progress_steps(30))
# next_up_page.doModal()
# del next_up_page
def search_next(dd,tv_movie,id,heb_name):
   global silent,list_index,str_next,break_jump,sources_searching,clicked,list_index_list
   from resources.modules.general import fix_q
   try:

    if len(str(id))==0:
        return 0
    if str(id)=='%20':
        return 0
    list_index_list=444
    list_index=999
    count_timeout_sources=0
    if tv_movie=='tv':

        # xbmc.sleep(5000)
        str_next=''
        silent=True
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()

        dbcur.execute("SELECT * FROM nextup")
        match = dbcur.fetchall()
        dbcur.close()
        dbcon.close()
        
        for dd in match:
            dd_a=dd
        name,data,original_title,id,season,episode,show_original_year,tvdb_id=json.loads(base64.b64decode(dd_a[0]))[0]

        if len(episode)==1:
          episode_n="0"+episode
        else:
           episode_n=episode
        if len(season)==1:
          season_n="0"+season
        else:
          season_n=season
        

        episode=str(int(episode)+1)
        from resources.modules.tmdb import get_episode_data
        
        name_n,plot_n,image_n,season,episode=get_episode_data(id,season,str(int(episode)),o_name=original_title)
        time_to_save=0
        
        match_a=search_tvep(str(heb_name),str(data),str(original_title),str(data),iconimage,fanart,str(season),str(episode),str(tmdb),False)
        
        dd=[]

        dd.append((heb_name,data,original_title,id,season,episode,show_original_year,tvdb_id))
        all_data=[]
        list=[]
        list2=[]
        all_dd=[]
        filter_lang=Addon.getSetting("filter_non_e")=='true'
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        count=0
        for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,id,original_title in match_a:
                count+=1
                color=''
                if '2160' in q or '4k' in q.lower():
                    color='yellow'
                elif '1080' in q:
                    color='yellow'
                elif '720' in q:
                    color='lightgreen'
                if '[COLOR red]' in name:
                    color='red'
                if '5.1' in name:
                    sound='-[COLOR khaki]5.1[/COLOR]-'
                elif '7.1' in name:
                    sound='-[COLOR khaki]7.1[/COLOR]-'
                else:
                    sound=''
                list.append(['[COLOR %s]%s - [/COLOR]%s[COLOR bisque]%s[/COLOR] %s '%(color,q,sound,str(f_size2),clean_sources_nextep(name))])

                list2.append([clean_sources_nextep(name),q, f_size2,q,'','','',''])
                all_data.append((name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2))

    time_to_save_trk=int(Addon.getSetting("time_to_save"))
    timeout=0
    break_jump=1
    done=0

    if tv_movie=='tv':
      
        if Addon.getSetting("smart_next")=='true':
            time_to_window = int(get_ep_time(original_title))
        else:
            time_to_window=int(Addon.getSetting("window"))
    else:
        time_to_window=int(Addon.getSetting("movie_window"))
    time_left=999999
    while timeout<200:
        timeout+=1
        if break_jump==0:
            break
        if xbmc.Player().isPlaying():
            break
        xbmc.sleep(100)
    play_next=False
    count_ok=0
    while xbmc.Player().isPlaying():
        if break_jump==0:
            break
        try:
            
            vidtime = xbmc.Player().getTime()
        except Exception as e:
            vidtime=0
            pass
        if vidtime>10:
            try:
               
                g_timer=xbmc.Player().getTime()
                g_item_total_time=xbmc.Player().getTotalTime()
                if xbmc.Player().getTotalTime()>10 and xbmc.Player().getTime()>10:
                
                    time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
                
            except Exception as e:
                log.warning('Takt Err:'+str(e))
                pass
            if (time_left<time_to_window) :
                count_ok+=1
            else:
                count_ok=0
            if count_ok>10 :
              play_next=True
              break
        xbmc.sleep(100)
    if break_jump==0:
            return 0

    if play_next:
     
      if tv_movie=='tv':
        from resources.modules.tmdb import get_episode_data
        name_n,plot_n,image_n,season,episode=get_episode_data(id,season,str(int(episode)),o_name=original_title,yjump=True)
        if Addon.getSetting("clean_view")=='true':
          view="‏‏script-upnext-upnext_clean.xml"
        else:
          view="script-upnext-upnext.xml"
        next_up_page = UpNext(view,Addon.getAddonInfo('path'), "DefaultSkin", "1080i")
        ep=load_test_data(name_n,iconimage,iconimage,plot_n,name_n,season,episode,list)

        next_up_page.setItem(ep)

        next_up_page.setProgressStepSize(calculate_progress_steps(30))
        next_up_page.doModal()
        del next_up_page
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup_all_d')
        dbcur.execute("DELETE FROM nextup")
        dbcur.execute("DELETE FROM nextup_all_d")
        dbcur.execute("INSERT INTO nextup Values ('%s')"%(base64.b64encode(json.dumps(dd).encode("utf-8")).decode("utf-8")))
        a=str((all_dd))
        b=base64.b64encode(a.encode("utf-8")).decode("utf-8") 
        dbcur.execute("INSERT INTO nextup_all_d Values ('%s')"%(b))
        dbcon.commit()
        dbcur.close()
        dbcon.close()
        break_window=False
        break_window_rd=False
        global stopnext
        global clear
        
        if list_index!=999 and list_index!=888:
            
            stopnext =True
            xbmc.Player().stop()
            
            # xbmc.sleep(600)
            ret=list_index
            if len(list)==0:
                xbmc.executebuiltin((u'Notification(%s,%s)' % (sys.argv[0], Addon.getLocalizedString(32085))))
                sys.exit()
            else:
                clear= False
                xbmc.executebuiltin('ActivateWindow(busydialognocancel)')

                xbmc.sleep(2500)
                
                name,link,data,icon,fan,no_subs,id,season,episode,original_title,f_size2=all_data[ret]
               
                play(name,link,data,icon,fan,no_subs,id,season,episode,original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true')

        elif list_index_list!=444 and list_index_list!=555:
                
                xbmc.sleep(50)
                stopnext =True
                
                menu2 = ContextMenu_new2('plugin.video.telemedia', list2,iconimage,fanart,description,int(count))
                menu2.doModal()
                stopnext = False
                del menu2
                ret=selected_index
                if ret!=-1:
                    clear= False
                    name,link,data,icon,fan,no_subs,id,season,episode,original_title,f_size2=all_data[ret]  
                    play(name,link,data,icon,fan,no_subs,id,season,episode,original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true')

   except Exception as e:
    import linecache
    sources_searching=False
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    log.warning('ERROR IN Play IN:'+str(lineno))
    log.warning('inline:'+line)
    log.warning('Error:'+str(e))
    if Addon.getSetting("poptele")=='true':
     xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'PlayinLine:'+str(lineno))))
   
    pass

def get_tvdb(id):
    # from  resources.modules.client import  get_html
    url_media='https://api.themoviedb.org/3/%s/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&include_image_language=ru,null&append_to_response=images,external_ids'%('tv',id,lang)
    time_to_save=int(Addon.getSetting("save_time"))
   
    html_media=requests.get(url_media).json()
    try:
      tvdb_id=str(html_media['external_ids']['tvdb_id'])
    except:
      tvdb_id=''
    return tvdb_id
def search_tvep(heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb,remote=False):

    time_to_save=int(Addon.getSetting("save_time"))
    global stopnext
    global namenextupepisode
    display=Addon.getSetting("new_source")
    netflix_mod=Addon.getSetting("netflix_mod")
    heb_name=clear_color(heb_name)
    original_title=original_title.replace('%20',' ')
    global list_index ,playing_file
    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
    once=0
    link_show=Addon.getSetting("fix_link")
    d_save=[]
    exclude=[]
    filter_dup=Addon.getSetting("dup_links")=='true'
    all_links=[]
    all_links_eng=[]
    all_t_links=[]
    all_hebeng=[]
    heb_name=heb_name.replace('...?','').replace('\u200f','').replace(':','').replace('%27',"'").replace('-'," ").replace("’","'")
    c_original=original_title.replace('%20','.').replace(' ','.').replace('%27',"'").replace("'","").replace('%3a',":").replace('...?','').replace('...','').replace('..','')
    tvdb_id= cache.get(get_tvdb,999, id, table='pages') 
    dd=[]
    if netflix_mod=='false':
        options=[heb_name+' ע%s פ%s'%(season,episode),heb_name+' ע%sפ%s'%(season,episode),heb_name+' עונה %s פרק %s'%(season,episode),c_original+'.S%sE%s'%(season_n,episode_n),c_original+'.S%sE%s'%(season,episode)]
    else:
        options_heb=[heb_name+' ע%s פ%s'%(season,episode),heb_name+' ע%sפ%s'%(season,episode),heb_name+' עונה %s פרק %s'%(season,episode)]
        options_eng=[c_original+'.S%sE%s'%(season_n,episode_n),c_original+'.S%sE%s'%(season,episode)]
        
    options2=[' ע%s פ%s'%(season,episode),'ע%s.פ%s'%(season,episode),' ע%sפ%s'%(season,episode),' עונה %s פרק %s'%(season,episode),'.S%sE%s'%(season_n,episode_n),'.S%sE%s'%(season,episode)]
    if netflix_mod=='false':
        for items in options:
            
            all_links=all_links+searchtmdb(tmdb,'all','0$$$0',items.replace(':',''),iconimage,fanart,season,episode,no_subs=1,original_title=original_title,heb_name=heb_name,dont_return=False,manual=False)
    else:
        for items in options_heb:
            
            all_links=all_links+searchtmdb(tmdb,'all','0$$$0',items.replace(':',''),iconimage,fanart,season,episode,no_subs=1,original_title=original_title,heb_name=heb_name,dont_return=False,manual=False)
        for items in options_eng:
            
            all_links_eng=all_links_eng+searchtmdb(tmdb,'all','0$$$0',items.replace(':',''),iconimage,fanart,season,episode,no_subs=1,original_title=original_title,heb_name=heb_name,dont_return=False,manual=False)
    if Addon.getSetting("order_by")=='0':
        
        all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
    else:
        all_links=sorted(all_links, key=lambda x: x[1], reverse=False)
    if netflix_mod=='true':
        all_links_eng=sorted(all_links_eng, key=lambda x: x[4], reverse=False)

    dd.append((heb_name,data,original_title,id,season,episode,show_original_year,tvdb_id))
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
    
    dbcur.execute("DELETE FROM nextup")
    
    try:
       dbcur.execute("INSERT INTO nextup Values ('%s')"%(base64.b64encode(json.dumps(dd).encode("utf-8")).decode("utf-8")))
    except:
        dbcur.execute("DROP TABLE IF EXISTS nextup;")
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
        dbcur.execute("INSERT INTO nextup Values ('%s')"%(base64.b64encode(json.dumps(dd).encode("utf-8")).decode("utf-8")))
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in all_links:
        if name not in all_t_links or filter_dup==False:
            all_t_links.append(name)
            

            ok=False
            o_name=heb_name
            for items in options2:
                    t_items=items.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                    t_name=name.replace('_','.').replace('"',"").replace('  ',' ').lower().replace('-','.').replace(' ','.').replace('[','').replace(']','').replace('_','.').replace(':','').replace("'","").replace('..','.')
                    t_items2=c_original.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                    
                    if (t_items+'.'  in t_name+'.') or (t_items+' '  in t_name+' ') or (t_items+'_'  in t_name+'_') or (t_items.replace('.','_')+'_'  in t_name.replace('.','_')+'_') or (t_items.replace('.','-')+'_'  in t_name.replace('.','-')+'_'):
                       if (o_name in name) or (t_items2 in t_name):
                        ok=True
                        break
            
            if not ok:
                
                exclude.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title))
            else:
                  if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                           continue
                  if once==0:
                    if '5.1' in name:
                        sound='[COLOR red]5.1[/COLOR]'
                    elif '6CH' in name:
                        sound='[COLOR red]5.1[/COLOR]'
                    else:
                        sound=''
                    if 'BluRay' in name:
                        sou='[COLOR blue]BluRay[/COLOR]'
                    else:
                        sou=''
                    if Addon.getSetting("netflix_mod")=='true':
                     heb='ע'
                    else:
                     heb=''
                    d_save.append((name+heb, link,mode,q,loc, icon,fan,f_size2,no_subs,id,original_title))
    for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in all_links_eng:
        if netflix_mod=='true':
            if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                   continue
        if name not in all_t_links or filter_dup==False:
            all_t_links.append(name)
            

            ok=False
            o_name=heb_name
            for items in options2:
                    t_items=items.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                    t_name=name.replace('_','.').replace('"',"").replace('  ',' ').lower().replace('-','.').replace(' ','.').replace('[','').replace(']','').replace('_','.').replace(':','').replace("'","").replace('..','.')
                    t_items2=c_original.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                    
                    if (t_items+'.'  in t_name+'.') or (t_items+' '  in t_name+' ') or (t_items+'_'  in t_name+'_') or (t_items.replace('.','_')+'_'  in t_name.replace('.','_')+'_') or (t_items.replace('.','-')+'_'  in t_name.replace('.','-')+'_'):
                       if (o_name in name) or (t_items2 in t_name):
                        ok=True
                        break
            
            if not ok:
                
                exclude.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title))
            else:
                  if once==0:
                    if '5.1' in name:
                        sound='[COLOR red]5.1[/COLOR]'
                    elif '6CH' in name:
                        sound='[COLOR red]5.1[/COLOR]'

                    else:
                        sound=''
                    if 'BluRay' in name:
                        sou='[COLOR blue]BluRay[/COLOR]'
                    else:
                        sou=''
                    d_save.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,id,original_title))
    d_save.append(('[COLOR orange] ///////////////  מקורות שאולי לא קשורים  /////////////// [/COLOR]','','','','', '','','','','',''))
    for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in exclude:
            if netflix_mod=='true':
                if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                       continue
            if remote==False and link_show=='false':

                if '5.1' in name:
                    sound='[COLOR red]5.1[/COLOR]'
                elif '6CH' in name:
                    sound='[COLOR red]5.1[/COLOR]'
                else:
                    sound=''
                if 'BluRay' in name:
                    sou='[COLOR blue]BluRay[/COLOR]'
                else:
                    sou=''
                d_save.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,id,original_title))
    return d_save

def search_tv(heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb,remote=False):
    global nextepisode,namenextupepisode,stopnext,break_window,play_status
    play_status='מחפש מקורות'
    if not os.path.exists(os.path.join(user_dataDir, '4.1.1')):
        
        data={'type':'checklogin',
             'info':''
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        if event['status']==2 or event['status']=='Needs to log from setting':
            tele_source=False
            
        else:
            tele_source=True

        if tele_source is False:

            DIALOG         = xbmcgui.Dialog()
            choice = DIALOG.yesno('יש להגדיר את חשבון הטלמדיה שלכם', "האם תרצה להגדיר אותו עכשיו?", yeslabel="[B][COLOR white]כן[/COLOR][/B]", nolabel="[B][COLOR white]לא[/COLOR][/B]")
            if choice == 1:
                choice = DIALOG.yesno('הגדרת חשבון','איזה חשבון בדיוק תרצו להגדיר?', yeslabel="[B][COLOR white]חשבון VIP[/COLOR][/B]", nolabel="[B][COLOR white]חשבון שלי אישי[/COLOR][/B]")
                if choice == 1:
                    xbmc.executebuiltin( "RunPlugin(plugin://plugin.program.Settingz-Anon/?mode=302&url=www)" )
                    sys.exit() 
                else:
                    xbmc.executebuiltin( "RunPlugin(plugin://plugin.video.telemedia?mode=5&url=www)" )
                    sys.exit() 
            else:
             xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
             sys.exit() 
    if Addon.getSetting('new_play_window2')=='true':
     if not tmdb=='0':
        tv_movie='tv'
        t = Thread(target=show_new_window, args=(tv_movie, tmdb, season, episode,fanart,))
        t.start()

    else:
       xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    count=0
    display=Addon.getSetting("new_source")
    netflix_mod=Addon.getSetting("netflix_mod")
    heb_name=clear_color(heb_name)
    original_title=original_title.replace('%20',' ')
    global list_index ,playing_file
    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
    time_to_save=0
    tvdb_id= cache.get(get_tvdb,999, id, table='pages') 
    all_links=[]
    all_links_eng=[]
    sep = ':'

    c_original=original_title.replace('%20','.').replace(' ','.').replace('%27',"'").replace('%3a',":").replace('...?',' ').replace('...',' ').replace('..',' ').replace(':','')
    # heb_name = heb_name.split(sep, 1)[0]
    
    heb_name=heb_name.replace('ציידי הטרולים: סיפורי ארקדיה','ציידי הטרולים').replace('מיסטר בין: הסדרה המצוירת','מיסטר בין: הסדרה המצויירת').replace('היי סקול מיוזיקל: המחזמר הסדרה','היי סקול מיוזיקל')
    
    heb_name=heb_name.replace('...?','').replace('\u200f','').replace(':','').replace('%27',"'").replace('-'," ").replace("’","'")#.replace("סיפורי ארקדיה"," ")
    


    if netflix_mod=='false':
        # options=[heb_name+' ע%s פ%s'%(season,episode),heb_name+' ע%sפ%s'%(season,episode),heb_name+' עונה %s פרק %s'%(season,episode),c_original+'.S%sE%s'%(season_n,episode_n),c_original+'.S%sE%s'%(season,episode)]
        
        options=[heb_name+' ע%s פ%s'%(season,episode),heb_name+' ע%sפ%s'%(season,episode),heb_name+' עונה %s פרק %s'%(season,episode),heb_name+' S%sE%s'%(season_n,episode_n),c_original+'.S%sE%s'%(season_n,episode_n),c_original+'.S%sE%s'%(season,episode)]
    else:
        options_heb=[heb_name+' ע%s פ%s'%(season,episode),heb_name+' ע%sפ%s'%(season,episode),heb_name+' עונה %s פרק %s'%(season,episode)]
        options_eng=[c_original+'.S%sE%s'%(season_n,episode_n),c_original+'.S%sE%s'%(season,episode)]

    options2=[' ע%s פ%s'%(season,episode),'ע%s.פ%s'%(season,episode),' ע%sפ%s'%(season,episode),' עונה %s פרק %s'%(season,episode),'.S%sE%s'%(season_n,episode_n),'.S%sE%s'%(season,episode)]

    if netflix_mod=='false':
        for items in options:
            
                all_links=all_links+searchtmdb(tmdb,'all','0$$$0',items.replace(':',''),iconimage,fanart,season,episode,no_subs=1,original_title=original_title,heb_name=heb_name,dont_return=False,manual=False)
    else:
        for items in options_heb:
        
                all_links=all_links+searchtmdb(tmdb,'all','0$$$0',items.replace(':',''),iconimage,fanart,season,episode,no_subs=1,original_title=original_title,heb_name=heb_name,dont_return=False,manual=False)
        for items in options_eng:

                all_links_eng=all_links_eng+searchtmdb(tmdb,'all','0$$$0',items.replace(':',''),iconimage,fanart,season,episode,no_subs=1,original_title=original_title,heb_name=heb_name,dont_return=False,manual=False)

    if Addon.getSetting("order_by")=='0':
        
        all_links=sorted(all_links, key=lambda x: x[4], reverse=False)
    else:
        all_links=sorted(all_links, key=lambda x: x[1], reverse=False)
    if netflix_mod=='true':
        all_links_eng=sorted(all_links_eng, key=lambda x: x[4], reverse=False)
    exclude=[]
    filter_dup=Addon.getSetting("dup_links")=='true'
    all_t_links=[]
    once=0
    d_save=[]
    menu=[]
    dd=[]
    dd.append((heb_name,data,original_title,id,season,episode,show_original_year,tvdb_id))

    from sqlite3 import dbapi2 as database

    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
    
    dbcur.execute("DELETE FROM nextup")
    
    try:
       dbcur.execute("INSERT INTO nextup Values ('%s')"%(base64.b64encode(json.dumps(dd).encode("utf-8")).decode("utf-8")))
    except:
        dbcur.execute("DROP TABLE IF EXISTS nextup;")
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""data TEXT);" % 'nextup')
        dbcur.execute("INSERT INTO nextup Values ('%s')"%(base64.b64encode(json.dumps(dd).encode("utf-8")).decode("utf-8")))

    dbcon.commit()
    dbcur.close()
    dbcon.close()
    if netflix_mod=='false':
        for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in all_links:
            if netflix_mod=='true':
                if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                       continue
            if name not in all_t_links or filter_dup==False:
                all_t_links.append(name)
                # name=name.replace('לולו סרטים','')
                ok=False
                o_name=heb_name
                for items in options2:
                        # name=name.replace('_',' ').replace('.',' ')
                        t_items=items.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()

                        t_name=name.replace('_','.').replace('"',"").replace('  ',' ').lower().replace('-','.').replace(' ','.').replace('[','').replace(']','').replace('_','.').replace(':','').replace("'","").replace('..','.').replace('+',' ').replace('>','').replace('1080P','').replace('WEB','')

                        t_items2=c_original.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                        
                        if (t_items+'.'  in t_name+'.') or (t_items+' '  in t_name+' ') or (t_items+'_'  in t_name+'_') or (t_items.replace('.','_')+'_'  in t_name.replace('.','_')+'_') or (t_items.replace('.','-')+'_'  in t_name.replace('.','-')+'_'):
                            # logging.warning('333o_name3333'+str(o_name))
                            # logging.warning('39993name33999993'+str(name))
                            # logging.warning('tt_items2_itt_items2ems2'+str(t_items2))
                            # logging.warning('tt44444444t_name2'+str(t_name))
                           if (o_name in name.replace('_',' ').replace('.',' ')) or (t_items2 in t_name):
                            ok=True
                            break
                if not ok:
                    exclude.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title))
                else:
                      count+=1
                      if once==0:
                        if '5.1' in name:
                            sound='[COLOR red]5.1[/COLOR]'
                        elif '6CH' in name:
                            sound='[COLOR red]5.1[/COLOR]'
                        else:
                            sound=''
                        if 'BluRay' in name:
                            sou='[COLOR blue]BluRay[/COLOR]'
                        else:
                            sou=''

                        if Addon.getSetting("netflix_mod")=='true':
                         heb='ע'
                        else:
                         heb=''
                        menu.append([name,q, f_size2,q,sound,sou,'',''])
                        d_save.append((name+heb,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2))
                      addLink( name, link,mode,False, icon,fan,f_size2,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
    if netflix_mod=='true':
        for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in all_links_eng:
            if netflix_mod=='true':
                    if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                           continue
            if name not in all_t_links or filter_dup==False:
                all_t_links.append(name)
                

                ok=False
                o_name=heb_name
                for items in options2:
                        t_items=items.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                        t_name=name.replace('_','.').replace('"',"").replace('  ',' ').lower().replace('-','.').replace(' ','.').replace('[','').replace(']','').replace('_','.').replace(':','').replace("'","").replace('..','.')
                        t_items2=c_original.replace('_','.').replace(' ','.').replace(':','').replace("'","").replace('-','.').replace('[','').replace(']','').replace('..','.').lower()
                        
                        if (t_items+'.'  in t_name+'.') or (t_items+' '  in t_name+' ') or (t_items+'_'  in t_name+'_') or (t_items.replace('.','_')+'_'  in t_name.replace('.','_')+'_') or (t_items.replace('.','-')+'_'  in t_name.replace('.','-')+'_'):
                           # if (o_name in name) or (t_items2 in t_name):
                            ok=True
                            break
                if not ok:
                    exclude.append((name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title))
                else:
                      if once==0:
                        count+=1
                        if '5.1' in name:
                            sound='[COLOR red]5.1[/COLOR]'
                        elif '6CH' in name:
                            sound='[COLOR red]5.1[/COLOR]'
                        else:
                            sound=''
                        if 'BluRay' in name:
                            sou='[COLOR blue]BluRay[/COLOR]'
                        else:
                            sou=''
                        menu.append([clean_sources(name),q, f_size2,q,sound,sou,'',''])
                        d_save.append((name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2))
                      addLink( name, link,mode,False, icon,fan,f_size2,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)

    link_show=Addon.getSetting("fix_link")
    for  name, link,mode,q,loc, icon,fan,f_size2,no_subs,tmdb,season,episode,original_title in exclude:
            if netflix_mod=='true':
                if 'CD1' in name or 'CD2' in name or 'CD3' in name or 'CD4' in name or 'CD5' in name or  'חלק_1' in name or 'חלק_2' in name or 'חלק_3' in name or 'חלק_4' in name or 'חלק_5' in name or 'ח1' in name or 'ח2' in name or 'ח3' in name or 'ח4' in name or 'ח5' in name:
                       continue
            if remote==False and link_show=='false':
                addLink( name, link,mode,False, icon,fan,f_size2,no_subs=no_subs,tmdb=tmdb,season=season,episode=episode,original_title=original_title)
                
                if '5.1' in name:
                    sound='[COLOR red]5.1[/COLOR]'
                elif '6CH' in name:
                    sound='[COLOR red]5.1[/COLOR]'
                else:
                    sound=''
                if 'BluRay' in name:
                    sou='[COLOR blue]BluRay[/COLOR]'
                else:
                    sou=''
                menu.append(['[COLOR orange]'+clean_sources(name)+'[/COLOR]','', '',q,sound,sou,'',''])
                d_save.append((name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2))

    if len(d_save)==0:
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אין מקורות[/COLOR]' % COLOR2)
        break_window=True
        sys.exit()
    if display== 'true' and  Addon.getSetting("one_click")=='false' and Addon.getSetting("netflix_mod")=='false':

     menu2 = ContextMenu_new2('plugin.video.telemedia', menu,iconimage,fanart,description,int(count))
     menu2.doModal()
     stopnext = False
     del menu2
     ret=selected_index
     try:
       if ret!=-1:
           name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2=d_save[ret]
           play(name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true')
       break_window=True
     except Exception as e:

           heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb=undo_get_rest_data(fast_link)
           search_tv(heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb,next_ep)
     xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
     sys.exit()

    if Addon.getSetting("one_click")=='true' and remote==False:

            name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2=d_save[0]
            play(name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true')

    if netflix_mod=='true' and remote==False:
            name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2=d_save[0]
            play(name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true')
            if display== 'true' and Addon.getSetting("sh_one_click")=='true' and not stopnext:
                menu2 = ContextMenu_new2('plugin.video.telemedia', menu,iconimage,fanart,description,int(count))
                menu2.doModal()
                stopnext = False
                del menu2
                ret=selected_index
                try:
                   if ret!=-1:
                       
                       name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,f_size2=d_save[ret]
                       play(name,link,data,icon,fan,no_subs,tmdb,season,episode,original_title,heb_name,f_size2,None,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='true')
                   break_window=True
                except Exception as e:
                       heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb=undo_get_rest_data(fast_link)
                       search_tv(heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb,next_ep)
                sys.exit()
            sys.exit()
    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    return all_links 


def clear_all():
    import shutil
    
    data={'type':'logout',
         'info':'quit'
         }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    shutil.rmtree(user_dataDir)
    clear_files()
    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]הכל נוקה[/COLOR]' % COLOR2)
def search_groups(icon_o,fan_o):
        all_d=[]
        from resources.modules.tmdb import get_movies
        search_entered=''
        keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
        keyboard.doModal()
        if keyboard.isConfirmed() :
               query = keyboard.getText()
               if query=='':
                sys.exit()
                

        addNolink( '[COLOR blue][I]---סרטים---[/I][/COLOR]', id,27,False,fan=' ', iconimage=' ',plot=' ')
        get_movies('http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query={0}&language={1}&append_to_response=origin_country&page=1'.format(query,lang),global_s=True)
        
        addNolink( '[COLOR blue][I]---סדרות---[/I][/COLOR]', id,27,False,fan=' ', iconimage=' ',plot=' ')
        get_movies('http://api.themoviedb.org/3/search/tv?api_key=34142515d9d23817496eeb4ff1d223d0&query={0}&language={1}&page=1'.format(query,lang),global_s=True)
        
        
        
        num=random.randint(0,60000)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchPublicChats', 'query': query, '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        dp = xbmcgui.DialogProgress()
        try:
            dp.create('Please Wait...','Adding Groups', '','')
            dp.update(0, 'Please Wait...','Adding Groups', '' )
        except:
            dp.create('Please Wait...','Adding Groups'+'\n'+ ''+'\n'+'')
            dp.update(0, 'Please Wait...'+'\n'+'Adding Groups'+'\n'+ '' )
        counter=0
        counter_ph=10000
        zzz=0
        for items in event['chat_ids']:
            num=random.randint(0,60000)
            data={'type':'td_send',
                     'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':num})
                     }
            event_in=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

            if dp.iscanceled():
                          dp.close()
                         
                          break
            j_enent=(event_in)
            try:
                dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...','Adding Groups', j_enent['@type'] )
            except:
                dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...'+'\n'+'Adding Groups'+'\n'+ j_enent['@type'] )
            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
                icon_id=''
                fan_id=''
                fanart=''
                icon=''
                name=j_enent['title']
             
                color='white'
                if 'is_channel' in j_enent['type']:
                    if j_enent['type']['is_channel']==False:
                        
                        genere='Chat'
                        color='lightblue'
                    else:
                        genere='Channel'
                        color='khaki'
                else:
                     genere=j_enent['type']['@type']
                     color='lightgreen'
                if 'last_message' in j_enent:
                    plot=name
                    pre=j_enent['last_message']['content']
               
                    if 'caption' in pre:
                        plot=j_enent['last_message']['content']['caption']['text']
                    elif 'text' in pre:
                        if 'text' in pre['text']:
                            plot=j_enent['last_message']['content']['text']['text']
                    
                        
                else:
                    plot=name
                try:
                    dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...','Adding Groups', name )
                except:
                    dp.update(int(((zzz* 100.0)/(len(event['chat_ids']))) ), 'Please Wait...'+'\n'+'Adding Groups'+'\n'+ name )
                zzz+=1
             
                # if 'photo' in j_enent:
                   
                   # if 'small' in j_enent['photo']:
                     # counter_ph+=1
                     # icon_id=j_enent['photo']['small']['id']
                     # f_name=str(j_enent['id'])+'_small.jpg'
                     # mv_name=os.path.join(logo_path,f_name)
                     # if os.path.exists(mv_name):
                        # icon=mv_name
                     # else:
                        # icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                   # if 'big' in j_enent['photo']:
                     # counter_ph+=1
                     # fan_id=j_enent['photo']['big']['id']
                     # f_name=str(j_enent['id'])+'_big.jpg'
                     # mv_name=os.path.join(logo_path,f_name)
                     # if os.path.exists(mv_name):
                        # fanart=mv_name
                     # else:
                        # fanart=download_photo(fan_id,counter_ph,f_name,mv_name)
                
                icon='special://home/addons/plugin.video.telemedia/tele/icon.jpg'
                fanart='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                aa=addDir3('[COLOR %s]'%color+name+'[/COLOR]',str(items),2,icon,fanart,plot+'\nfrom_plot',generes=genere,data='0',last_id='0$$$0$$$0$$$0',image_master=icon+'$$$'+fanart,join_menu=True)
                all_d.append(aa)
            
            counter+=1
        if len(all_d)>0:
             
            addNolink( '[COLOR lightblue][I]%s[/I][/COLOR]'%'תוצאות מקבוצות', 'www',99,False,iconimage=icon_o,fan=fan_o)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        dp.close()
               
def join_chan(url):
    
    
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'joinChat', 'chat_id': url, '@extra': num})
             }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    #log.warning(json.dumps(event))
    if event["@type"]=='ok':
        #Joined OK
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32029)))
    else:
        #Error in join
        xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32030)))

def leave_chan(name,url):
    
    
    num=random.randint(0,60000)
    #"Leave Channel"
    #Leave    
    # data={'type':'td_send',
                 # 'info':json.dumps({'@type': 'getOption','name':'my_id', '@extra': num})
                 # }
    # event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    # id=event2['value']
    if Addon.getSetting("vip_login2"):
      LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אפשרות זו חסומה.[/COLOR]' % COLOR2)
      return 
    ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32031),'%s?'%(Addon.getLocalizedString(32032)+name))
    if ok:
        data={'type':'td_send',
             'info':json.dumps({'@type': 'leaveChat', 'chat_id': url, '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        #log.warning(json.dumps(event))
        if event["@type"]=='ok':
            xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32067)))
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmc.executebuiltin(u'Notification(%s,%s)' % ('Telemedia', Addon.getLocalizedString(32068)))
def dis_or_enable_addon(addon_id, enable="true"):
    import json
    addon = '"%s"' % addon_id
    if xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "true":
        return xbmc.log("### Skipped %s, reason = allready enabled" % addon_id)
    elif not xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "false":
        return xbmc.log("### Skipped %s, reason = not installed" % addon_id)
    else:
        do_json = '{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}}' % (addon, enable)
        query = xbmc.executeJSONRPC(do_json)
        response = json.loads(query)
        if enable == "true":
            log.warning("### Enabled %s, response = %s" % (addon_id, response))
        else:
            log.warning("### Disabled %s, response = %s" % (addon_id, response))
    return xbmc.executebuiltin('Container.Update(%s)' % xbmc.getInfoLabel('Container.FolderPath'))
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

def copyDirTree(root_src_dir,root_dst_dir):
    """
    Copy directory tree. Overwrites also read only files.
    :param root_src_dir: source directory
    :param root_dst_dir:  destination directory
    """
    not_copied=[]
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            
        
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                try:
                    os.remove(dst_file)
                except Exception as exc:
                    # import stat
                    # os.chmod(dst_file, stat.S_IWUSR)
                    # os.remove(dst_file)
                    log.warning('Error del:')
                    log.warning(exc)
            try:
                shutil.copy(src_file, dst_dir)
            except:
              if '.dll' not in file_ and '.so' not in file_:
                not_copied.append(file_)
    return not_copied
def install_addon(name,url,silent=False,Delete=True):
    from zipfile import ZipFile
    num=random.randint(0,60000)
    url=json.loads(url)['id']
    if silent:
        ok=True
    else:
        ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32033),(Addon.getLocalizedString(32033)+' %s?'%name))
    if ok:
        if silent==False:
            dp = xbmcgui.DialogProgress()
            dp.create('Telemedia', '[B][COLOR=yellow]Installing[/COLOR][/B]','')
        if Delete:
            try:
                if os.path.exists(addon_path):
                    shutil.rmtree(addon_path)
            except Exception as e:
                logging.warning('error removing folder:'+str(addon_path)+','+str(e))
            if not xbmcvfs.exists(addon_path+'/'):
                os.makedirs(addon_path)
        mv_name=os.path.join(addon_path,name)
        addon=download_photo(url,num,name,mv_name)
        if silent==False:
            dp.update(0,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Extracting[/COLOR][/B]')
        zf = ZipFile(addon)
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0
        for file in zf.infolist():
            extracted_size += file.file_size
            if silent==False:
                dp.update(int((extracted_size*100.0)/uncompress_size),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Extracting[/COLOR][/B]',file.filename)
            
            zf.extract(member=file, path=addon_extract_path)
        zf.close()
        f_o = os.listdir(addon_extract_path)

        filename=os.path.join(addon_extract_path,f_o[0], 'addon.xml')
        if sys.version_info.major > 2:
            do_open = lambda filename: open(filename, encoding='utf-8')
        else:
            do_open = lambda filename: open(filename)
        with do_open(filename) as file:
            file_data= file.read()
            pass
        file.close()
        regex='id=(?:"|\')(.+?)(?:"|\')'
        nm=re.compile(regex).findall(file_data)[0]
        if not xbmc.getCondVisibility("System.HasAddon(%s)" % name.split('-')[0]):
            regex='import addon=(?:"|\')(.+?)(?:"|\')'
            dep=re.compile(regex).findall(file_data)
            missing=[]
            if silent==False:
                dp.update(90,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Dependencies[/COLOR][/B]','')
            zzz=0
            for items in dep:
                if silent==False:
                    dp.update(int((extracted_size*100.0)/len(items)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Dependencies[/COLOR][/B]',items)
                zzz+=1
                if not xbmc.getCondVisibility("System.HasAddon(%s)" % items):
                    missing.append(items)
            if len(missing)>0:
                showText('Missing Dependencies','\n'.join(missing))
                return 0
        addon_p=xbmc_tranlate_path("special://home/addons/")
        files = os.listdir(addon_extract_path)
        try:
            if os.path.exists(os.path.join(addon_p,f_o[0])):
                shutil.rmtree(os.path.join(addon_p,f_o[0]))
        except Exception as e:
         logging.warning('Telemedia Error removing addon')
         pass
        not_copied=copyDirTree(os.path.join(addon_extract_path,f_o[0]),os.path.join( addon_p,f_o[0]))
        if len(not_copied)>0:
            showText('File That was not copied', '\n'.join(not_copied))
        x=xbmc.executebuiltin("UpdateLocalAddons")
        if silent==False:
            dp.update(100,'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Cleaning[/COLOR][/B]','')
        time.sleep(1)
        dis_or_enable_addon(nm)
        shutil.rmtree(addon_path)
        if silent==False:
            dp.close()
        #'Installed'
        #'Installation complete'
        if silent==False:
            xbmcgui.Dialog().ok(Addon.getLocalizedString(32034),Addon.getLocalizedString(32035))


def download_file_loc(id):
        try:
            
            
            path=''
            dp = xbmcgui.DialogProgress()
            dp.create('Telemedia', '[B][COLOR=yellow]Loading[/COLOR][/B]')
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'downloadFile','file_id':int(id), 'priority':1,'offset':0,'limit':0, '@extra': num})
             }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
           
            j_enent_o=(event)
            
           
            
            j_enent_o=(event)
            once=True
            while True:
                data={'type':'td_send',
                 'info':json.dumps({'@type': 'getFile','file_id':int(id), '@extra': num})
                 }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
               
                
                #event = td_receive()
                
                if dp.iscanceled():
                    num=random.randint(0,60000)
                    data={'type':'td_send',
                         'info':json.dumps({'@type': 'cancelDownloadFile','file_id':int(id), '@extra': num})
                         }
                    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                    path=''
                        
                    break
                
                if event:
                    if 'file' in event:
                        size=event['file']['size']
                    else:
                        size=event['size']
                    if event.get('@type') =='error':
                        if Addon.getSetting("poptele")=='true':
                         xbmcgui.Dialog().ok('Error occurred',str(event.get('message')))
                        break
                    
                        
                    
                    if 'expected_size' in event:
                        try:
                            dp.update(int((event['local']['downloaded_size']*100.0)/size),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]Downloading %s/%s[/COLOR][/B]'%(str(event['local']['downloaded_size']),str(size)))
                        except:
                            dp.update(int((event['local']['downloaded_size']*100.0)/size),'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Downloading %s/%s[/COLOR][/B]'%(str(event['local']['downloaded_size'])+'\n'+str(size)))
                        
                        if len(event['local']['path'])>0 and event['local']['is_downloading_completed']==True:
                            size=event['size']
                            path=event['local']['path']
                            break
                xbmc.sleep(100)
            dp.close()
            return path
        except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Main:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))

def kids_tvshow(last_id,icon,fan,chan_id):

        icon_pre=icon
        showdb=Addon.getSetting("showdb")
        fan_pre=fan
        if icon_pre==None:
            icon_pre=''
        if fan_pre==None:
            fan_pre='' 
        num=random.randint(1,1001)

        s_last=1000
        search_filter_arr=['searchMessagesFilterVideo','searchMessagesFilterDocument']
        for search_filter in search_filter_arr:
            try:
                last_id=int(last_id)
            except:
                last_id=0
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':s_last, '@extra': num})
                 }

            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()


            if 'message' in event:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אנא המתן...[/COLOR]' % COLOR2)
                refresh_datatelegram()
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':s_last, '@extra': num})
                     }
               
               

                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

            dp = xbmcgui . DialogProgress ( )
            if showdb == 'true':
             try:
                dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040), '','')
             except:
                dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040)+'\n'+ ''+'\n'+'')
            zzz=0

            for items in event['messages']:  

                if 'document' in items['content']:
                    
                    name=items['content']['document']['file_name']
                    
                    
                    if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name and '.wmv' not in name:
                            continue

                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3
                    if showdb == 'true':
                     if dp.iscanceled():
                        break
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre
                    # name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,999,name,original_title,html_g_movie,icon_pre,fan_pre, table='posters_n')
                    name=clean_name4(name)#name,year,plot,genere,icon,fan,original_name,rating=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    icon='special://home/addons/plugin.video.telemedia/tele/Tv_Show/kids.jpg'
                    # da=''
                    tmdb=''
                    fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                    if showdb == 'true':
                     try:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )
                     except:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...'+'\n'+'Adding'+'\n'+ name )
                    zzz+=1
                    link_data={}
                    link_data['id']=str(items['content']['document']['document']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    if name=='':
                        name='sex '+str(zzz)
                    addLink( name.replace('.',' '),f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    
                    
                if 'video' in items['content']:
                    
                    name=items['content']['video']['file_name']

                    
                    # if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name:
                            # continue
                    #if 'מדובב' not in name and 'hebdub' not in name.lower() and chan_id==str(KIDS_CHAT_ID) :
                    #    continue
                    size=items['content']['video']['video']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3
                    if showdb == 'true':
                     if dp.iscanceled():
                        break
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre
                    # name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,999,name,original_title,html_g_movie,icon_pre,fan_pre, table='posters_n')
                    name=clean_name4(name)#name,year,plot,genere,icon,fan,original_name,rating=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    icon='special://home/addons/plugin.video.telemedia/tele/Tv_Show/kids.jpg'
                    # da=''
                    tmdb=''
                    fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                    if showdb == 'true':
                     try:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )
                     except:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...'+'\n'+'Adding'+'\n'+ name )
                    zzz+=1
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    if name=='':
                        name='sex '+str(zzz)
                    addLink( name.replace('.',' '),f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    

        all_d=[]
        last_id=str(items['id'])
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'[/COLOR]','www',176,icon_pre,fan_pre,Addon.getLocalizedString(32026),data=chan_id,last_id=last_id)
        all_d.append(aa) 
        f_last_id='0$$$0$$$0$$$0'
        #'Search'
        aa=addDir3('[COLOR khaki]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(chan_id),2,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','search',data='0',last_id=f_last_id,image_master=icon_pre+'$$$'+fan_pre)
        all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def tmdb_world2(last_id,icon,fan,chan_id):

        icon_pre=icon
        showdb=Addon.getSetting("showdb")
        fan_pre=fan
        if icon_pre==None:
            icon_pre=''
        if fan_pre==None:
            fan_pre='' 
        num=random.randint(1,1001)

        s_last=1000
        search_filter_arr=['searchMessagesFilterVideo','searchMessagesFilterDocument']
        for search_filter in search_filter_arr:
            try:
                last_id=int(last_id)
            except:
                last_id=0
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':s_last, '@extra': num})
                 }

            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()


            if 'message' in event:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אנא המתן...[/COLOR]' % COLOR2)
                refresh_datatelegram()
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':s_last, '@extra': num})
                     }
               
               

                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

            dp = xbmcgui . DialogProgress ( )
            if showdb == 'true':
             try:
                dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040), '','')
             except:
                dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040)+'\n'+ ''+'\n'+'')
            zzz=0

            for items in event['messages']:  

                if 'document' in items['content']:
                    
                    name=items['content']['document']['file_name']
                    
                    
                    if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name and '.wmv' not in name:
                            continue

                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3
                    if showdb == 'true':
                     if dp.iscanceled():
                        break
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre
                    # name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,999,name,original_title,html_g_movie,icon_pre,fan_pre, table='posters_n')
                    name=clean_name4(name)#name,year,plot,genere,icon,fan,original_name,rating=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    icon='special://home/addons/plugin.video.telemedia/tele/purn.png'
                    # da=''
                    tmdb=''
                    fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                    if showdb == 'true':
                     try:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )
                     except:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...'+'\n'+'Adding'+'\n'+ name )
                    zzz+=1
                    link_data={}
                    link_data['id']=str(items['content']['document']['document']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    if name=='':
                        name='sex '+str(zzz)
                    addLink( name,f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    
                    
                if 'video' in items['content']:
                    
                    name=items['content']['video']['file_name']

                    
                    # if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name:
                            # continue
                    #if 'מדובב' not in name and 'hebdub' not in name.lower() and chan_id==str(KIDS_CHAT_ID) :
                    #    continue
                    size=items['content']['video']['video']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3
                    if showdb == 'true':
                     if dp.iscanceled():
                        break
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre
                    # name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,999,name,original_title,html_g_movie,icon_pre,fan_pre, table='posters_n')
                    name=clean_name4(name)#name,year,plot,genere,icon,fan,original_name,rating=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    icon='special://home/addons/plugin.video.telemedia/tele/purn.png'
                    # da=''
                    tmdb=''
                    fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                    if showdb == 'true':
                     try:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )
                     except:
                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...'+'\n'+'Adding'+'\n'+ name )
                    zzz+=1
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    if name=='':
                        name='sex '+str(zzz)
                    addLink( name,f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    

        all_d=[]
        last_id=str(items['id'])
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'[/COLOR]','www',176,icon_pre,fan_pre,Addon.getLocalizedString(32026),data=chan_id,last_id=last_id)
        all_d.append(aa) 
        f_last_id='0$$$0$$$0$$$0'
        #'Search'
        aa=addDir3('[COLOR khaki]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(chan_id),2,'https://upload.wikimedia.org/wikipedia/he/7/7f/Rich_Sex.jpg','https://upload.wikimedia.org/wikipedia/he/7/7f/Rich_Sex.jpg','search',data='0',last_id=f_last_id,image_master=icon_pre+'$$$'+fan_pre)
        all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

def karaoke_tele(last_id,chan_id):
        all_d2=[]
        num=random.randint(1,1001)
        icon='https://thumbs.dreamstime.com/b/vector-logo-karaoke-design-template-illustration-icon-126463532.jpg'
        fan='https://img.freepik.com/free-vector/karaoke-with-microphones-stars-neon-style_24908-60794.jpg?w=2000'
        s_last=1000
        search_filter_arr=['searchMessagesFilterVideo','searchMessagesFilterDocument']
        #'Search'

        for search_filter in search_filter_arr:
            try:
                last_id=int(last_id)
            except:
                last_id=0
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':s_last, '@extra': num})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if 'message' in event:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אנא המתן...[/COLOR]' % COLOR2)
                refresh_datatelegram()
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':s_last, '@extra': num})
                     }
              
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            zzz=0

            for items in event['messages']:  

                if 'document' in items['content']:
                    
                    name=items['content']['document']['file_name']
                    
                    
                    if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name and '.wmv' not in name:
                            continue
                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3

                    o_name=name
                    name=clean_name4(name)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    tmdb=''
                    link_data={}
                    link_data['id']=str(items['content']['document']['document']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    addLink( name,f_lk,3,False, icon,fan,'[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    
                    
                if 'video' in items['content']:
                    
                    name=items['content']['video']['file_name']

                    size=items['content']['video']['video']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3
                    o_name=name
                    name=clean_name4(name)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    tmdb=''
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    addLink( name,f_lk,3,False, icon,fan,'[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    

        all_d=[]
        last_id=str(items['id'])
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'[/COLOR]','www',257,icon,fan,Addon.getLocalizedString(32026),data=chan_id,last_id=last_id)
        all_d.append(aa) 
        aa=addDir3('[COLOR khaki]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(chan_id),2,icon,fan,'search',data='0',last_id='0$$$0$$$0$$$0',image_master=icon+'$$$'+fan)
        all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def launch_command(command_launch):
    import subprocess
    try:

        external_command = subprocess.call(command_launch, shell = True, executable = '/system/bin/sh')
    except Exception as e:
        try:
            external_command = os.system(command_launch)
        except:
            log.warning('[%s]' % ('ERROR LAUNCHING COMMAND !!!', external_command))

def selectDialog(label, items, pselect=-1, uDetails=False):
    select = xbmcgui.Dialog().select(label, items, preselect=pselect, useDetails=uDetails)
def install_apk(name,url):
    import xbmcvfs
    
    f_id=json.loads(url)['id']
    try:
        num=random.randint(0,60000)
        #Install
        
        ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32033),(Addon.getLocalizedString(32033)+' %s?'%name))
        if ok:
            mv_name=os.path.join(addon_path,name)
            #log.warning('Downloading addon')
            addon=download_photo(f_id,num,name,mv_name)
            #log.warning('addon')
            #log.warning(addon)
            try:
                shutil.move(addon,'/sdcard/Download/application.apk')
            except Exception as e:
                log.warning('File copy err:'+str(e))
                pass
            CUSTOM = (Addon.getSetting("Custom_Manager") or 'com.android.documentsui')
            FMANAGER  = {0:'com.android.documentsui',1:CUSTOM}[0]
            
            xbmc.executebuiltin('StartAndroidActivity(%s,,,"content://%s")'%(FMANAGER,addon))
            
            xbmcgui.Dialog().ok('Done','Complete')
            
    except Exception as e:
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e))
def clean_name2(name,original_title,html_g,icon_pre,fan_pre):
    
    if '@' in name and '.' in name:
        nm=name.split('.')
        ind=0
        for items in nm:
            if '@' in items:
                nm.pop(ind)
            ind+=1
        name='.'.join(nm)
 

    name=name.replace(' ','.').replace('_','.').replace('-','.').replace('%20',' ').replace('5.1','').replace('AAC','').replace('2CH','').replace('.mp4','').replace('.avi','').replace('.mkv','').replace(original_title,'').replace('מדובב','').replace('גוזלן','').replace('BDRip','').replace('BRRip','')

    name=name.replace('1080p','').replace('720p','').replace('480p','').replace('360p','').replace('BluRay','').replace('ח1','').replace('ח2','').replace('נתי.מדיה','').replace('נ.מ.','').replace('..','.').replace('.',' ').replace('WEB-DL','').replace('WEB DL','').replace('נ מדיה','')

    name=name.replace('HDTV','').replace('DVDRip','').replace('WEBRip','')

    name=name.replace('דב סרטים','').replace('לולו סרטים','').replace('דב ס','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('HebDub','').replace('NF','').replace('HDCAM','').replace('@yosichen','')

    name=name.replace('BIuRay','').replace('x264','').replace('Hebdub','').replace('XviD','')

    name=name.replace('Silver007','').replace('Etamar','').replace('iSrael','').replace('DVDsot','').replace('אלי ה סרטים','').replace('PCD1','').replace('PCD2','').replace('CD1','').replace('CD2','').replace('CD3','').replace('Gramovies','').replace('BORip','').replace('200P','').replace('מס1','1').replace('מס2','2').replace('מס3','3').replace('מס4','4').replace('מס 3','3').replace('מס 2','2').replace('מס 1','1')

    name=name.replace('900p','').replace('PDTV','').replace('VHSRip','').replace('UPLOAD','').replace('TVRip','').replace('Heb Dub','').replace('MP3','').replace('AC3','').replace('SMG','').replace('Rip','').replace('6CH','').replace('XVID','')

    name=name.replace('HD','').replace('WEBDL','').replace('DVDrip','')

    #info=(PTN.parse(name))
    regex='.*([1-3][0-9]{3})'
    year_pre=re.compile(regex).findall(name)
    year=0
    if len(year_pre)>0:
        year=year_pre[0]
     
        name=name.replace(year,'')
    pre_year=year
    if year!=0:
        
        url2='http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&year=%s&language=he&append_to_response=origin_country&page=1'%(name,year)
    else:
        url2='http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&append_to_response=origin_country&page=1'%(name)
    #log.warning(url2)
    y=requests.get(url2).json()
    
    
    plot=''
    genere=''
    icon=icon_pre
    fan=fan_pre
    original_name=name
    rating=0
    tmdb=''
    if 'results' in y and len(y['results'])>0:
        res=y['results'][0]
        name=res['title']
        if 'release_date' in res:
           year=str(res['release_date'].split("-")[0])
        if year!=pre_year and len(y['results'])>1:
            for items_in in y['results']:
                if 'release_date' in items_in:
                    year=str(items_in['release_date'].split("-")[0])
                    if year==pre_year:
                        res=items_in
                        name=res['title']
        plot=res['overview']
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres']  if i['name'] is not None])
        try:genere = u' / '.join([genres_list[x] for x in res['genre_ids']])
        except:genere=''
        
        if res['poster_path']==None:
          icon=' '
        else:
           icon='https://image.tmdb.org/t/p/original/'+res['poster_path']
        if 'backdrop_path' in res:
             if res['backdrop_path']==None:
              fan=' '
             else:
              fan='https://image.tmdb.org/t/p/original/'+res['backdrop_path']
        else:
            fan='https://image.tmdb.org/t/p/original/'+html['backdrop_path']
        original_name=res['original_title']
        rating=res['vote_average']
        tmdb=str(res['id'])
    return name,year,plot,genere,icon,fan,original_name,rating,tmdb
    
def clean_name_search(name):

    name=name.replace(' ','.').replace(':','').replace('|','.').replace('%20',' ').replace('5.1','').replace('AAC','').replace('.mp4','').replace('.avi','').replace('.mkv','').replace('מדובב','').replace('כ.ס','').replace('כל סרט','').replace('כל.סרט','').replace('גוזלן','').replace('BDRip','').replace('BRRip','').replace('לולו','')

    name=name.replace('1080p.mp4','1080p').replace('DVD','').replace('BluRay','').replace('Bluray','').replace('נתי מדיה','').replace('נתי.מדיה','').replace('נ.מ','').replace('נ.מ.','').replace('..','.').replace('.',' ').replace('WEB-DL','').replace('WEB DL','').replace('B DL','').replace('WE DL','').replace('נ מדיה','').replace('נ.מדיה','')

    name=name.replace('HDTV','').replace('DVDRip','').replace('WEBRip','').replace('DVDSCR','').replace('HC','').replace('SCR','')

    name=name.replace('@','').replace('BrazzersHype','').replace('Brazzers','').replace('premiumtgnetwork Brazzers','').replace('premiumtgnetwork','').replace('XDADDY','').replace('SurFilms4U_Brazzer','').replace('premiumtgnetwork Bangbros','').replace('דב סרטים','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('HebDub','').replace('NF','').replace('HDCAM','').replace('@yosichen','')

    name=name.replace('BIuRay','').replace('x264','').replace('Hebdub','').replace('XviD','')

    name=name.replace('Silver007','').replace('Etamar','').replace('iSrael','').replace('DVDsot','').replace('אלי ה סרטים','').replace('Gramovies','').replace('BORip','').replace('200P','')

    name=name.replace('900p','').replace('PDTV','').replace('VHSRip','').replace('UPLOAD','').replace('TVRip','').replace('Heb Dub','').replace('MP3','').replace('AC3','').replace('SMG','').replace('Rip','').replace('6CH','').replace('XVID','')

    name=name.replace('HD','').replace('WEBDL','').replace('DVDrip','').replace('WEB-DL','')


    name=name.replace('_','.').replace('-','.').replace('%20',' ').replace('5.1','').replace('AAC','').replace('2CH','').replace('גוזלן','').replace('BDRip','').replace('BRRip','')

    name=name.replace('BluRay','').replace('נתי.מדיה','').replace('נ.מ.','').replace('WEB-DL','').replace('WEB DL','').replace('נ מדיה','')

    name=name.replace('HDTV','').replace('DVDRip','').replace('WEBRip','')

    name=name.replace('דב סרטים','').replace('לולו סרטים','').replace('דב ס','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('NF','').replace('HDCAM','').replace('@yosichen','')

    name=name.replace('BIuRay','').replace('x264','').replace('Hebdub','').replace('XviD','')

    name=name.replace('Silver007','').replace('Etamar','').replace('iSrael','').replace('DVDsot','').replace('אלי ה סרטים','').replace('Gramovies','').replace('BORip','').replace('200P','').replace('.',' ')

    return name
def clean_name4(name):

    name=name.replace(' ','.').replace(':','').replace('|','.').replace('%20',' ').replace('5.1','').replace('AAC','').replace('2CH','').replace('.mp4','').replace('.avi','').replace('.mkv','').replace('מדובב','').replace('כ.ס','').replace('כל סרט','').replace('כל.סרט','').replace('גוזלן','').replace('BDRip','').replace('BRRip','').replace('לולו','')

    name=name.replace('1080p','').replace('1080p.mp4','').replace('720p','').replace('570p','').replace('4K','').replace('DVD','').replace('540p','').replace('480p','').replace('430p','').replace('420p','').replace('270p','').replace('360p','').replace('BluRay','').replace('Bluray','').replace('ח1','').replace('ח2','').replace('נתי מדיה','').replace('נתי.מדיה','').replace('חלק 1','').replace('חלק 2','').replace('חלק 3','').replace('חלק א','').replace('חלק ב','').replace('ח3','').replace('ח4','').replace('ח5','').replace('נ.מ','').replace('נ.מ.','').replace('..','.').replace('.',' ').replace('WEB-DL','').replace('WEB DL','').replace('B DL','').replace('WE DL','').replace('נ מדיה','').replace('נ.מדיה','')

    name=name.replace('HDTV','').replace('DVDRip','').replace('WEBRip','').replace('DVDSCR','').replace('HC','').replace('SCR','')

    name=name.replace('@','').replace('BrazzersHype','').replace('Brazzers','').replace('premiumtgnetwork Brazzers','').replace('premiumtgnetwork','').replace('XDADDY','').replace('SurFilms4U_Brazzer','').replace('premiumtgnetwork Bangbros','').replace('דב סרטים','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('HebDub','').replace('NF','').replace('HDCAM','').replace('@yosichen','')

    name=name.replace('BIuRay','').replace('x264','').replace('Hebdub','').replace('XviD','')

    name=name.replace('Silver007','').replace('Etamar','').replace('iSrael','').replace('DVDsot','').replace('אלי ה סרטים','').replace('PCD1','').replace('PCD2','').replace('CD1','').replace('CD2','').replace('CD3','').replace('Gramovies','').replace('BORip','').replace('200P','').replace('מס1','1').replace('מס2','2').replace('מס3','3').replace('מס4','4').replace('מס 3','3').replace('מס 2','2').replace('מס 1','1')

    name=name.replace('900p','').replace('PDTV','').replace('VHSRip','').replace('UPLOAD','').replace('TVRip','').replace('Heb Dub','').replace('MP3','').replace('AC3','').replace('SMG','').replace('Rip','').replace('6CH','').replace('XVID','')

    name=name.replace('HD','').replace('WEBDL','').replace('DVDrip','').replace('WEB-DL','')





    # all_f=['xvid','EVO1','EVO2','RIp','נועםם','BDRiP','x265','HeBDub',' DivX',' WS','XViD','(',')','אלירן','WEB','H264',' Br','DVDRiP','HEBDUB',' BRrip','DVDRIP','עי יוסי','נתי מ ','ע"י sagi','BDRIP','נתי ','עי אורי המלך','לולו ','כל סרט ','נמ ','H 264','HEVC','  ','לעברית','גזלן']

    name=name.replace('_','.').replace('-','.').replace('%20',' ').replace('5.1','').replace('AAC','').replace('2CH','').replace('.mp4','').replace('.avi','').replace('.mkv','').replace('מדובב','').replace('גוזלן','').replace('BDRip','').replace('BRRip','')

    name=name.replace('1080p','').replace('720p','').replace('480p','').replace('360p','').replace('BluRay','').replace('ח1','').replace('ח2','').replace('נתי.מדיה','').replace('נ.מ.','').replace('WEB-DL','').replace('WEB DL','').replace('נ מדיה','')

    name=name.replace('HDTV','').replace('DVDRip','').replace('WEBRip','')

    name=name.replace('דב סרטים','').replace('לולו סרטים','').replace('דב ס','').replace('()','').replace('חן סרטים','').replace('ק סרטים','').replace('חננאל סרטים','').replace('יוסי סרטים','').replace('נריה סרטים','').replace('HebDub','').replace('NF','').replace('HDCAM','').replace('@yosichen','')

    name=name.replace('BIuRay','').replace('x264','').replace('Hebdub','').replace('XviD','')

    name=name.replace('Silver007','').replace('Etamar','').replace('iSrael','').replace('DVDsot','').replace('אלי ה סרטים','').replace('PCD1','').replace('PCD2','').replace('CD1','').replace('CD2','').replace('CD3','').replace('Gramovies','').replace('BORip','').replace('200P','').replace('מס1','1').replace('מס2','2').replace('מס3','3').replace('מס4','4').replace('מס 3','3').replace('מס 2','2').replace('מס 1','1')

    return name
def tmdb_world(last_id,icon,fan,chan_id):
    # try:
        
        
        from resources.modules.tmdb import get_html_g
        from resources.modules import cache
        html_g_tv,html_g_movie=cache.get(get_html_g,72, table='posters_n')
        icon_pre=icon
        showdb=Addon.getSetting("showdb")
        fan_pre=fan
        if icon_pre==None:
            icon_pre=''
        if fan_pre==None:
            fan_pre='' 
        num=random.randint(1,1001)

        s_last=int(Addon.getSetting("num_vip"))
        try:
            last_id=int(last_id)
        except:
            last_id=0
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':s_last, '@extra': num})
             }
       
       

        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        num=random.randint(1,1001)
        
        if 'message' in event:
            # LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אנא המתן...[/COLOR]' % COLOR2)
            if int(chan_id)==KIDS_CHAT_ID2:
                join_type=0
                chant_id='@NatiMediaHebdub'
            elif int(chan_id)==HEBREW_GROUP:
                invite_link="https://t.me/joinchat/AAAAAEH4beThZwz_zCNQWA"
                join_type=1
                
            elif int(chan_id)==WORLD_GROUP:
                join_type=1
                invite_link="https://t.me/joinchat/AAAAADumPH7RARDHtG0SoA"
            elif int(chan_id)==NATIO_NAL:
                join_type=2
                chant_id="@Nature_Films"
            elif int(chan_id)==DOCU:
                join_type=3
                chant_id="@Docuy"
            elif int(chan_id)==TVSHOW:
                join_type=1
                invite_link="https://telegram.me/joinchat/AAAAAEB-codSLnVIPtovVQ"
            elif int(chan_id)==KIDS:
                join_type=5
                chant_id='@mediachildren'
            elif int(chan_id)==KIDS2:
                join_type=6
                chant_id="@disney_plus_group"
            elif int(chan_id)==KIDS3:
                join_type=7
                chant_id="@Disney_plus_il"
            elif int(chan_id)==WAR:
                join_type=8
                chant_id="@shalom_sratim_WW_2"
            # elif int(chan_id)==WORLD_GROUP2:
                # join_type=9
                # chant_id="@KOL_SERETV"
            elif int(chan_id)==HEBREWTV:
                join_type=1
                invite_link="https://t.me/joinchat/AAAAAEYxRFfUlT_C8fSeIA"
                
                
                
                
                
            num=random.randint(1,1001)
            if 1:#'Chat not found' in event['message']:
                if join_type==1:
                    # LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]יש להתחבר לטלמדיה[/COLOR]' % COLOR2)
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
                     }
                if join_type==0:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@kidsworldglobal', '@extra': num})
                     }
                if join_type==9:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@KOL_SERETV', '@extra': num})
                     }
                if join_type==2:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@Nature_Films', '@extra': num})
                     }
                if join_type==3:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@Docuy', '@extra': num})
                     }
                if join_type==4:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@Sdarot_TV', '@extra': num})
                     }
                if join_type==5:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@mediachildren', '@extra': num})
                     }

                if join_type==6:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@Disney_plus_il', '@extra': num})
                     }
                if join_type==7:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@disney_plus_group', '@extra': num})
                     }
                if join_type==8:
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@shalom_sratim_WW_2', '@extra': num})
                     }

                     
                     
                     
                     
                     
                     
                     
                     
                    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                    data={'type':'td_send',
                     'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
                     }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                num=random.randint(1,1001)
        
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':s_last, '@extra': num})
                     }
               
               

                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': KIDS_CHAT_ID,'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        
        dp = xbmcgui . DialogProgress ( )
        if showdb == 'true':
         try:
            dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040), '','')
         except:
            dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040)+'\n'+ ''+'\n'+'')
        zzz=0
        for items in event['messages']:  
            #log.warning('n itmes')
            #log.warning(items)
           
            if 'document' in items['content']:
                
                name=items['content']['document']['file_name']
                
                
                if '.mkv' not in name and '.mp4' not in name and '.avi' not in name and '.AVI' not in name and '.MKV' not in name and '.MP4' not in name and '.wmv' not in name:
                        continue
                #if 'מדובב' not in name and 'hebdub' not in name.lower() and chan_id==str(KIDS_CHAT_ID) :
                #    continue
                size=items['content']['document']['document']['size']
                f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                
                if 'date' in items:
                    da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
               
                mode=3
                if showdb == 'true':
                 if dp.iscanceled():
                    break
                o_name=name
                icon=icon_pre
                fan=fan_pre
                name=clean_name4(name)
                # name,year,plot,genere,icon,fan,original_name,rating,tmdb=cache.get(clean_name2,999,name,original_title,html_g_movie,icon_pre,fan_pre, table='posters_n')
                # name,year,plot,genere,icon,fan,original_name,rating=clean_name2(name,original_title,html_g_movie,icon_pre,fan_pre)
                plot=''
                year=''
                original_name=''
                genere=''
                rating=''
                if showdb == 'true':
                 try:
                    dp.update(int(((zzz* 100.0)/(len(event['messages']))) ),   Addon.getLocalizedString(32041)+'...','Adding', name )
                 except:
                    dp.update(int(((zzz* 100.0)/(len(event['messages']))) ),   Addon.getLocalizedString(32041)+'...'+'\n'+'Adding'+'\n'+ name )
                zzz+=1
                link_data={}
                link_data['id']=str(items['content']['document']['document']['id'])
                link_data['m_id']=items['id']
                link_data['c_id']=items['chat_id']
                f_lk=json.dumps(link_data)
                addLink( name,f_lk,3,False, icon,fan,'[COLOR blue]'+o_name+'[/COLOR]\n'+f_size2+'\n'+plot,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb)
        all_d=[]
        last_id=str(items['id'])
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'[/COLOR]','www',31,icon_pre,fan_pre,Addon.getLocalizedString(32026),data=chan_id,last_id=last_id)
        all_d.append(aa) 
        f_last_id='0$$$0$$$0$$$0'
        #'Search'
        aa=addDir3('[COLOR khaki]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(chan_id),2,'https://sitechecker.pro/wp-content/uploads/2017/12/search-engines.png','https://www.komando.com/wp-content/uploads/2017/12/computer-search.jpg','search',data='0',last_id=f_last_id,image_master=icon_pre+'$$$'+fan_pre)
        all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    # except:pass
def turkish_data(last_id,icon,fan,chan_id):#dragon and rd
        icon_pre=icon
        showdb=Addon.getSetting("showdb")
        fan_pre=fan
        if icon_pre==None:
            icon_pre=''
        if fan_pre==None:
            fan_pre='' 
        num=random.randint(1,1001)
        s_last=1000
        search_filter_arr=['searchMessagesFilterVideo','searchMessagesFilterDocument','SearchMessagesFilterUrl']
        # for search_filter in search_filter_arr:
        try:
            last_id=int(last_id)
        except:
            last_id=0
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'limit':s_last, '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        if 'message' in event:
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אנא המתן...[/COLOR]' % COLOR2)
            refresh_datatelegram()
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'limit':s_last, '@extra': num})
                 }
           
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        dp = xbmcgui . DialogProgress ( )
        if showdb == 'true':
            dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040)+'\n'+ ''+'\n'+'')
        zzz=0
        rd_link=''
        for items in event['messages']:  
            if 'text' in items['content']:
                name=items['content']['text']['text'].split('\n')
                name=clean_name4(name[0])
                rd_link=items['content']['text']['text']    

                regex='\n(.+?)$'
                rd_link=re.compile(regex).findall(rd_link)
                f_size2=''
                year=''
                original_name=''
                genere=''
                rating=''
                da=''
                tmdb=''
                if 'date' in items:
                    da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                try:
                    rd_link=rd_link[0]
                except:pass
                if 'https' not in rd_link:
                 continue
                
                addLink( name,rd_link,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
            if 'document' in items['content']:
                ok_name=True
                file_name=items['content']['document']['file_name']
                if 'document' in items['content']:
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            if len(items['content']['caption']['text'])>0:
                                name=items['content']['caption']['text']
                                if 'https://' in name:
                                    name=items['content']['caption']['text']
                                    try:rd_link=name.split('\n')[1]
                                    except:rd_link=name
                                    ok_name=True
                                else:
                                    ok_name=False

                    if ok_name:
                        name=file_name
                    
                    c_name=[]
                    if '\n' in name:
                        
                        f_name=name.split('\n')
                        for it in f_name:
                            if '😎' not in it and it!='\n' and len(it)>1 and '💠' not in it:
                                c_name.append(it)
                        name='\n'.join(c_name)
                size=items['content']['document']['document']['size']
                f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                da=''
                if 'date' in items:
                    da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
               
                mode=3
                if showdb == 'true':
                 if dp.iscanceled():
                    break
                o_name=name
                icon=icon_pre
                fan=fan_pre
                name=clean_name4(name)
                plot=''
                year=''
                original_name=''
                f_plot=plot
                genere=''
                rating=''
                
                tmdb=''
                if showdb == 'true':

                    dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )

                zzz+=1
                link_data={}
                link_data['id']=str(items['content']['document']['document']['id'])
                link_data['m_id']=items['id']
                link_data['c_id']=items['chat_id']
                f_lk=json.dumps(link_data)
                if len(rd_link)>0:
                    f_lk='@@@'+'telelink'+f_lk+'rdlink'+rd_link
                addLink( name,f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                
                
            if 'video' in items['content']:
                ok_name=True
                plot=''
                if 'caption' in items['content']:
                    if 'text' in items['content']['caption']:
                        if len(items['content']['caption']['text'])>0:
                            name=items['content']['caption']['text']
                            if 'https://' in name:
                                
                                name=items['content']['caption']['text']
                                try:rd_link=name.split('\n')[1]
                                except:rd_link=name

                                # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', rd_link.split('\n')[1])))
                                ok_name=True
                                
                            else:
                                ok_name=False
                if ok_name:
                    name=items['content']['video']['file_name']
                
                
                if 'caption' in items['content']:
                    plot=items['content']['caption']['text']
                    
                    if '\n' in plot and len(name)<3:
                            name=plot.split('\n')[0]

                    # if not ok_name:

                     # name=plot.split('\n')[0]
                     # regex='\n(.+?)$'
                     # rd_link=re.compile(regex).findall(plot)
    
                     # try:
                        # rd_link=rd_link[0]
                     # except:pass
                     
                size=items['content']['video']['video']['size']
                f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                da=''
                if 'date' in items:
                    da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
               
                mode=3
                if showdb == 'true':
                 if dp.iscanceled():
                    break
                o_name=name
                icon=icon_pre
                fan=fan_pre

                name=clean_name4(name)
                plot=''
                year=''
                original_name=''
                f_plot=plot
                genere=''
                rating=''
                tmdb=''
                if showdb == 'true':

                    dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )

                zzz+=1
                link_data={}
                link_data['id']=str(items['content']['video']['video']['id'])
                link_data['m_id']=items['id']
                link_data['c_id']=items['chat_id']
                f_lk=json.dumps(link_data)
                if name=='':
                    name='sex '+str(zzz)
                if len(rd_link)>0:
                    f_lk='@@@'+'telelink'+f_lk+'rdlink'+rd_link
                addLink( name,f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    

        all_d=[]
        try:
            last_id=str(items['id'])
        except:
            last_id=''
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'---->'+'[/COLOR]','www',263,icon_pre,fan_pre,Addon.getLocalizedString(32026),data=chan_id,last_id=last_id)
        all_d.append(aa) 
        f_last_id='0$$$0$$$0$$$0'
        #'Search'
        # aa=addDir3('[COLOR khaki]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(chan_id),2,'https://upload.wikimedia.org/wikipedia/he/7/7f/Rich_Sex.jpg','https://upload.wikimedia.org/wikipedia/he/7/7f/Rich_Sex.jpg','search',data='0',last_id=f_last_id,image_master=icon_pre+'$$$'+fan_pre)
        # all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def turkish_data2(last_id,icon,fan,chan_id):#my
        icon_pre=icon
        showdb=Addon.getSetting("showdb")
        fan_pre=fan
        if icon_pre==None:
            icon_pre=''
        if fan_pre==None:
            fan_pre='' 
        num=random.randint(1,1001)
        s_last=1000
        search_filter_arr=['searchMessagesFilterVideo','searchMessagesFilterDocument']
        for search_filter in search_filter_arr:
            try:
                last_id=int(last_id)
            except:
                last_id=0
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'filter':{'@type': search_filter},'limit':s_last, '@extra': num})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if 'message' in event:
                LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אנא המתן...[/COLOR]' % COLOR2)
                refresh_datatelegram()
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'searchChatMessages','chat_id':chan_id, 'query': '','from_message_id':int(last_id),'offset':0,'limit':s_last, '@extra': num})
                     }
               
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                try:
                    if 'Chat not found' in event['message']:
                       LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]יש להתחבר לערוץ של הסדרה.[/COLOR]' % COLOR2)
                       
                        
                       return
                except:pass
            dp = xbmcgui . DialogProgress ( )
            if showdb == 'true':
                dp.create(Addon.getLocalizedString(32041)+'...',Addon.getLocalizedString(32040)+'\n'+ ''+'\n'+'')
            zzz=0
            rd_link=''
            for items in event['messages']:  

                if 'document' in items['content']:
                    ok_name=True
                    file_name=items['content']['document']['file_name']
                    if 'document' in items['content']:
                        if 'caption' in items['content']:
                            if 'text' in items['content']['caption']:
                                if len(items['content']['caption']['text'])>0:
                                    name=items['content']['caption']['text']
                                    if 'https://' in name:
                                        name=items['content']['caption']['text']
                                        try:rd_link=name.split('\n')[1]
                                        except:rd_link=name
                                        ok_name=True
                                    else:
                                        ok_name=False

                        if ok_name:
                            name=file_name
                        
                        c_name=[]
                        if '\n' in name:
                            
                            f_name=name.split('\n')
                            for it in f_name:
                                if '😎' not in it and it!='\n' and len(it)>1 and '💠' not in it:
                                    c_name.append(it)
                            name='\n'.join(c_name)
                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    da=''
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3
                    if showdb == 'true':
                     if dp.iscanceled():
                        break
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre
                    name=clean_name4(name)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    
                    tmdb=''
                    if showdb == 'true':

                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )

                    zzz+=1
                    link_data={}
                    link_data['id']=str(items['content']['document']['document']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    if len(rd_link)>0:
                        f_lk='@@@'+'telelink'+f_lk+'rdlink'+rd_link
                    addLink( name,f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    
                    
                if 'video' in items['content']:
                    ok_name=True
                    plot=''
                    if 'caption' in items['content']:
                        if 'text' in items['content']['caption']:
                            if len(items['content']['caption']['text'])>0:
                                name=items['content']['caption']['text']
                                if 'https://' in name:
                                    
                                    name=items['content']['caption']['text']
                                    try:rd_link=name.split('\n')[1]
                                    except:rd_link=name

                                    # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', rd_link.split('\n')[1])))
                                    ok_name=True
                                    
                                else:
                                    ok_name=False
                    if ok_name:
                        name=items['content']['video']['file_name']
                    
                    
                    if 'caption' in items['content']:
                        plot=items['content']['caption']['text']
                        
                        if '\n' in plot and len(name)<3:
                                name=plot.split('\n')[0]

                        # if not ok_name:

                         # name=plot.split('\n')[0]
                         # regex='\n(.+?)$'
                         # rd_link=re.compile(regex).findall(plot)
        
                         # try:
                            # rd_link=rd_link[0]
                         # except:pass
                         
                    size=items['content']['video']['video']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    da=''
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                   
                    mode=3
                    if showdb == 'true':
                     if dp.iscanceled():
                        break
                    o_name=name
                    icon=icon_pre
                    fan=fan_pre

                    name=clean_name4(name)
                    plot=''
                    year=''
                    original_name=''
                    f_plot=plot
                    genere=''
                    rating=''
                    tmdb=''
                    if showdb == 'true':

                        dp.update(int(((zzz* 100.0)/(len(event['messages']))) ), Addon.getLocalizedString(32041)+'...','Adding', name )

                    zzz+=1
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    if name=='':
                        name='sex '+str(zzz)
                    if len(rd_link)>0:
                        f_lk='@@@'+'telelink'+f_lk+'rdlink'+rd_link
                    addLink( name,f_lk,3,False, icon,fan,f_size2,da=da,year=year,original_title=original_name,generes=genere,rating=rating,tmdb=tmdb,no_subs=1)
                    

        all_d=[]
        try:
            last_id=str(items['id'])
        except:
            last_id=''
        aa=addDir3('[COLOR yellow]'+Addon.getLocalizedString(32026)+'---->'+'[/COLOR]','www',275,icon_pre,fan_pre,Addon.getLocalizedString(32026),data=chan_id,last_id=last_id)
        all_d.append(aa) 
        f_last_id='0$$$0$$$0$$$0'
        #'Search'
        # aa=addDir3('[COLOR khaki]'+Addon.getLocalizedString(32027)+'[/COLOR]',str(chan_id),2,'https://upload.wikimedia.org/wikipedia/he/7/7f/Rich_Sex.jpg','https://upload.wikimedia.org/wikipedia/he/7/7f/Rich_Sex.jpg','search',data='0',last_id=f_last_id,image_master=icon_pre+'$$$'+fan_pre)
        # all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def add_to_databaseturkey(url,name,data,iconimage,fanart,description):
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'databaseturkey.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("SELECT * FROM my_fd_groups where id='%s'"%(url))
        match = dbcur.fetchall()
        if len(match)==0:
            dbcur.execute("INSERT INTO my_fd_groups Values ('%s','%s','%s','%s','%s','%s');" %  (name.replace("'","%27"),url,iconimage,fanart,description.replace("'","%27"),' '))
            dbcon.commit()
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),name+' '+Addon.getLocalizedString(32054))
        else:
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Error occurred'),Addon.getLocalizedString(32081))

        
        dbcur.close()
        dbcon.close()
def add_to_databaseturkey2(url,name,data,iconimage,fanart,description):
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/databaseturkey2.db')#os.path.join(user_dataDir,'databaseturkey2.db')
        
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("SELECT * FROM my_fd_groups where id='%s'"%(url))
        match = dbcur.fetchall()
        if len(match)==0:
            dbcur.execute("INSERT INTO my_fd_groups Values ('%s','%s','%s','%s','%s','%s');" %  (name.replace("'","%27"),url,iconimage,fanart,description.replace("'","%27"),' '))
            dbcon.commit()
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),name+' '+Addon.getLocalizedString(32054))
        else:
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'Error occurred'),Addon.getLocalizedString(32081))

        
        dbcur.close()
        dbcon.close()

def download_files(name,url):
    
    try:
        num=random.randint(0,60000)
        new_dest=xbmc_tranlate_path(Addon.getSetting("remote_path"))
        if not os.path.exists(new_dest):
            xbmcgui.Dialog().ok('Error occurred',Addon.getLocalizedString(32089))
            Addon.openSettings()
            return 0
        ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32088),(Addon.getLocalizedString(32088)+' %s?'%name))
        if ok:
            mv_name=os.path.join(new_dest,name)
            addon=download_photo(url,num,name,mv_name)
            
        xbmcgui.Dialog().ok('Error occurred','Err:'+str(e))
    except Exception as e:
        xbmcgui.Dialog().ok(Addon.getLocalizedString(32090),Addon.getLocalizedString(32090))
def clear_search_h():
    ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32093),Addon.getLocalizedString(32094))
    if ok:
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
        dbcon.commit()
        xbmc.executebuiltin('Container.Refresh')
        dbcur.execute("DELETE FROM search")
        dbcon.commit()
        dbcur.close()
        dbcon.close()
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_search")=='true' and len(Addon.getSetting("firebase"))>0:
            table_name='search'
            # try:

            all_firebase=read_firebase(table_name)
            for items in all_firebase:
                    t = Thread(target=delete_firebase, args=(table_name,items,))
                    t.start()
                    # thread=[]
                    
                    # thread.append(Thread(delete_firebase,table_name,items))

                    
                    # thread[0].start()

def groups_join(id,icon_pre,fan_pre):
    
    
    num=random.randint(0,60000)
    m_id=0
    count=0
    #log.warning('Get All groups')
    #log.warning(id)
    all_d=[]
    all_l=[]
    complete_list={}
    complete_list['by_link']=[]
    complete_list['public']=[]
    while count<10:
        count+=1
        #log.warning('m_id')
        #log.warning(m_id)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'getChatHistory','chat_id':id,'from_message_id':m_id,'offset':0,'limit':100,'only_local':False, '@extra':num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
       
        
        counter_ph=num
        
        for msg in event['messages']:
            msg_in=msg['content']
        
            m_id=msg['id']
            icon=icon_pre
            fan=fan_pre
            if 'web_page' in msg_in:
                title=msg_in['web_page']['title']
                
                # if 'photo' in msg_in['web_page']:
                    # counter_ph+=1
                    # icon_id=msg_in['web_page']['photo']['sizes'][0]['photo']['id']
                    # f_name=msg_in['web_page']['photo']['sizes'][0]['photo']['remote']['id']+'.jpg'
                    # mv_name=os.path.join(icons_path,f_name)
                    # if os.path.exists(mv_name):
                        # icon=mv_name
                    # else:
                       # icon=download_photo(icon_id,counter_ph,f_name,mv_name)
                    
                    # counter_ph+=1
                    # loc=msg_in['web_page']['photo']['sizes']
                    # icon_id=msg_in['web_page']['photo']['sizes'][len(loc)-1]['photo']['id']
                    # f_name=msg_in['web_page']['photo']['sizes'][len(loc)-1]['photo']['remote']['id']+'.jpg'
                    # mv_name=os.path.join(fan_path,f_name)
                    # if os.path.exists(mv_name):
                        # fan=mv_name
                    # else:
                       # fan=download_photo(icon_id,counter_ph,f_name,mv_name)
                icon='special://home/addons/plugin.video.telemedia/tele/icon.jpg'
                fan='special://home/addons/plugin.video.telemedia/tele/tv_fanart.png'
                all_l=[]
                all_urls={}
                regex='https://t.me/joinchat/(.+?)\n'
                all_l=re.compile(regex,re.DOTALL).findall(msg_in['web_page']['description']['text'])
                if 'text' in msg_in:
                    all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                
                
                if len(all_l)>0:
                    all_urls['by_link']='$$$'.join(all_l)
                
                complete_list['by_link']+=all_l
                all_l=[]
                regex='@(.+?)(?: |\n|-|$)'
                all_l=re.compile(regex,re.DOTALL).findall(msg_in['web_page']['description']['text'])
                if 'text' in msg_in:
                    all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                    regex='https://t.me/(.+?)(?:/|\n)'
                
                    all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                if len(all_l)>0:
                    all_urls['public']='$$$'.join(all_l)
                complete_list['public']+=all_l
                if not icon:
                    icon=''
                if not fan:
                    fan=''
                aa=addDir3(title,json.dumps(all_urls),39,icon,fan,msg_in['web_page']['description']['text'])
                all_d.append(aa)
            else:
                all_l=[]
                all_urls={}
                regex='https://t.me/joinchat/(.+?)\n'
                if 'text' in msg_in:
                    all_l=re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                
                if 'text' in msg_in:
                    all_l=re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                
                if len(all_l)>0:
                    all_urls['by_link']='$$$'.join(all_l)
                complete_list['by_link']+=all_l
                all_l=[]
                regex='@(.+?)(?: |\n|-|$)'
               
                if 'text' in msg_in:
                    all_l=re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                    regex='https://t.me/(.+?)(?:/|\n)'
                    if 'text' in msg_in:
                        all_l=all_l+re.compile(regex,re.DOTALL).findall(msg_in['text']['text'])
                    
                    if len(all_l)>0:
                        all_urls['public']='$$$'.join(all_l)
                    else:
                        all_urls['public']=''.join(all_l)
                    complete_list['public']+=all_l
                    if not icon:
                        icon=''
                    if not fan:
                        fan=''
                    aa=addDir3(msg_in['text']['text'],json.dumps(all_urls),39,icon,fan,msg_in['text']['text'])
                    all_d.append(aa)
    if not icon:
        icon=''
    if not fan:
        fan=''
    aa=addDir3('[COLOR lightgreen]'+Addon.getLocalizedString(32105)+'[/COLOR]',json.dumps(complete_list),42,icon,fan,Addon.getLocalizedString(32106))
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def join_group(url):
    
    
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':9223372036854775807, 'limit': '100', '@extra': num})
             }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    j_urls=json.loads(url)
    all_j=[]
    dp = xbmcgui.DialogProgress()
            
    dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32062))
    if 'by_link' in j_urls:
      if len(j_urls['by_link'])>0:
       
        by_link_chats=j_urls['by_link']
        if '$$$' in url:
            all_urls=by_link_chats.split('$$$')
        else:
            all_urls=[by_link_chats]
        zzz=0
        for it in all_urls:
          if it!='joinchat':
            if it in all_j:
                continue
            all_j.append(it)
            dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]%s[/COLOR][/B]'%it)
            zzz+=1
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': 'https://t.me/joinchat/'+it, '@extra': num})
             }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

            if 'id' in event:
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': event['id'],'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                
            time.sleep(1)
        
            
    if 'public' in j_urls:
      if len(j_urls['public'])>0:
       
        if '$$$' in j_urls['public']:
            all_links=j_urls['public'].split('$$$')
        else:
            all_links=[j_urls['public']]
        zzz=0
        for items in all_links:
           if items!='joinchat':
            num=random.randint(0,60000)
            
            dp.update(int((zzz*100.0)/len(all_links)),'[B][COLOR=green]Telemedia[/COLOR][/B]', '[B][COLOR=yellow]%s[/COLOR][/B]'%items)
            zzz+=1
            data={'type':'td_send',
             'info':json.dumps({'@type': 'searchPublicChat','username':items, '@extra':num})
             }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            num=random.randint(0,60000)
            if event:
              if 'id' in event:
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
                     }
                event3=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': event['id'],'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    dp.close()
def check_free_space(description,iconImage):
    global break_window,bot
    directory_mod=Addon.getSetting("directory_mod")
    description=description.replace('GB','')
    if directory_mod =='true':

        user_dataDir=str(xbmc_tranlate_path(Addon.getSetting("movie_download_directory")))
    else:


       user_dataDir = xbmc_tranlate_path(Addon.getAddonInfo("profile"))

    if is_hebrew(description) or 'TE' in description or '.mp4' in description or '.mkv' in description or '.avi' in description:
        description=4
    if description==' ':
        description=4
    if xbmc.getCondVisibility('system.platform.android'):
        from os import statvfs
        st = statvfs(user_dataDir)
        free_space = float(st.f_bavail * st.f_frsize)/ (1024*1024*1024) 
    
        try:
            if int(free_space)<int(description):
                    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין מספיק מקום פנוי במכשיר לניגון התוכן'),'[COLOR %s]מנגן דרך הבוט[/COLOR]' % COLOR2)
                    # free_space_window(free_space,iconImage)
                    
                    bot=True#מנגן דרך הבוט באופו אוטומטי במקום ללחוץ דרך חלון מידע על שטח האחסון
                    break_window=True
                    return False
        except:
            if float(free_space)<float(description):
                    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין מספיק מקום פנוי במכשיר לניגון התוכן'),'[COLOR %s]מנגן דרך הבוט[/COLOR]' % COLOR2)
                    # free_space_window(free_space,iconImage)

                    bot=True#מנגן דרך הבוט באופו אוטומטי במקום ללחוץ דרך חלון מידע על שטח האחסון
                    break_window=True
                    return False
        
        # if free_space<2:
            # xbmcgui.Dialog().ok("שגיאה","מקום פנוי %s , נדרש 2 גיגה לפחות"%(str(round(free_space,2))+'Gb'))
            # return False
        return True
        #log.warning('free space:'+ str(free_space)+'Gb')
    elif xbmc.getCondVisibility('system.platform.windows'):
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(user_dataDir), None, None, ctypes.pointer(free_bytes))
        free_space=free_bytes.value / 1024 / 1024/1024

        try:
            if int(free_space)<int(description):

                    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין מספיק מקום פנוי במכשיר לניגון התוכן'),'[COLOR %s]מנגן דרך הבוט[/COLOR]' % COLOR2)
                    # free_space_window(free_space,iconImage)

                    bot=True#מנגן דרך הבוט באופו אוטומטי במקום ללחוץ דרך חלון מידע על שטח האחסון
                    
                    break_window=True
                    return False
        except:
            # logging.warning('2422frep444ace4242')
            # logging.warning(float(free_space))
            # logging.warning(float(description))
            
            # if 1:
            if float(description)>float(free_space):
                    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'אין מספיק מקום פנוי במכשיר לניגון התוכן'),'[COLOR %s]מנגן דרך הבוט[/COLOR]' % COLOR2)
                    # free_space_window(free_space,iconImage)

                    bot=True#מנגן דרך הבוט באופו אוטומטי במקום ללחוץ דרך חלון מידע על שטח האחסון
                    break_window=True
                    return False
        return True
        #log.warning('free space:'+ str(free_bytes.value / 1024 / 1024/1024)+'Gb')
    else:
        return True
def play_remote(url,no_subs,season,episode,original_title,id,saved_name,description,resume,name,heb_name,iconimage,fanart,watched_indicators,plot,rating,genre,year,tag_line,c_id=None,m_id=None,kitana='false'):

    if 'cancel' == resume:
         sys.exit()

    heb_name=heb_name.replace('%20',' ')
    original_title=original_title.replace('%20',' ')

    found=False
    try:
        name=name.replace('%20',' ')
    except:pass
    original_title=original_title.replace('%20',' ')
    saved_name=saved_name.replace('%20',' ')

    num=random.randint(0,60000)
    if 'https://t.me' in url:
        #log.warning('Send')
        data={'type':'td_send',
                 'info':json.dumps({'@type': 'getMessageLinkInfo','url':url, '@extra':num})
                 }
    else:
        
        data={'type':'td_send',
                 'info':json.dumps({'@type': 'getRemoteFile','remote_file_id':url, '@extra':num})
                 }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

    if 'id' in event:
        found=True
        link_o=str(event['id'])
        link_data={}
        link_data['id']=link_o
        link_data['m_id']=m_id
        link_data['c_id']=c_id
    elif 'https://t.me' in url:
        link_data={}
        if 'message' in event:
            if 'document' in event['message']['content']:
                link_o=str(event['message']['content']['document']['document']['id'])
                
                link_data['id']=str(event['message']['content']['document']['document']['id'])
            
            else:
                link_o=str(event['message']['content']['video']['video']['id'])
                
                link_data['id']=str(event['message']['content']['video']['video']['id'])


            link_data['m_id']=event['message']['id']
            link_data['c_id']=event['message']['chat_id']
            found=True
   
        else:
            data={'type':'checklogin',
                 'info':''
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

            if event['status']==2 or event['status']=='Needs to log from setting':
                DIALOG         = xbmcgui.Dialog()
                choice = DIALOG.yesno('יש להגדיר את חשבון הטלמדיה שלכם', "האם תרצה להגדיר אותו עכשיו?", yeslabel="[B][COLOR white]כן[/COLOR][/B]", nolabel="[B][COLOR white]לא[/COLOR][/B]")
                if choice == 1:
                    choice = DIALOG.yesno('הגדרת חשבון','איזה חשבון בדיוק תרצו להגדיר?', yeslabel="[B][COLOR white]חשבון VIP[/COLOR][/B]", nolabel="[B][COLOR white]חשבון שלי אישי[/COLOR][/B]")
                    if choice == 1:
                        xbmc.executebuiltin( "RunPlugin(plugin://plugin.program.Settingz-Anon/?mode=302&url=www)" )
                        sys.exit() 
                    else:
                        xbmc.executebuiltin( "RunPlugin(plugin://plugin.video.telemedia?mode=5&url=www)" )
                        sys.exit() 
                else:
                 xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                 sys.exit() 
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=15&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url,'1','%20','%20',original_title,id,fanart,que(heb_name),iconimage,'',que(description),'',que(heb_name),que(heb_name))
            xbmc.executebuiltin('RunPlugin(%s)'%url)
            # LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]לינק לא זמין, נסה לינק אחר.[/COLOR]' % COLOR2)
             
    if found:
        
        play(name,json.dumps(link_data),fanart,iconimage,'',no_subs,id,season,episode,original_title,heb_name,description,resume,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup='false')

    sys.exit()
def upload_log(backup=False):
   
   
   try:
    
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':9223372036854775807, 'limit': '100', '@extra': num})
             }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    exit_now=0
   
    if 'status' in event:
        xbmcgui.Dialog().ok('Error occurred',event['status'])
        exit_now=1
    if exit_now==0:

        counter=0
        counter_ph=10000
    
        j_enent_o=(event)
        zzz=0
        items=''
        names=[]
        ids=[]
        for items in j_enent_o['chat_ids']:
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':counter})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            order=event['positions'][0]['order']

            j_enent=(event)

            if j_enent['@type']=='chat' and len(j_enent['title'])>1:
                
              
                names.append(j_enent['title'])
                ids.append(items)
    selected_group_id=-1
    if len(names)>0:
        ret = xbmcgui.Dialog().select("Choose", names)
        if ret==-1:
            sys.exit()
        else:
            selected_group_id=ids[ret]
        if selected_group_id!=-1:
            if backup:
                import  zfile as zipfile
                dp = xbmcgui.DialogProgress()
                dp.create('Telemedia', '[B][COLOR=yellow]Backingup[/COLOR][/B]','')
                zip_name = os.path.join(xbmc_tranlate_path("special://temp"), 'data.zip')
                directory_name = user_dataDir
                zf = zipfile.ZipFile(zip_name, "w")
                zzz=0
                for dirname, subdirs, files in os.walk(directory_name): 
                    try:
                        dp.update(int((zzz*100.0)/len(files)),'[B][COLOR=green]Zipping[/COLOR][/B]', dirname)
                    except:
                        pass
                    zzz+=1
                    zf.write(dirname)
                    for filename in files:
                        try:
                            dp.update(int((zzz*100.0)/len(files)),'[B][COLOR=green]Zipping[/COLOR][/B]', filename)
                        except:
                            pass
                        try:
                            zf.write(os.path.join(dirname, filename))
                        except:
                            pass
                zf.close()
                logSelect=[zip_name]
                
                dp.close()
            else:
                db_bk_folder=xbmc_tranlate_path(Addon.getSetting("remote_path"))
                nameSelect=[]
                logSelect=[]
                import glob
                folder = xbmc_tranlate_path('special://logpath')
                
                for file in glob.glob(folder+'/*.log'):
                    try:nameSelect.append(file.rsplit('\\', 1)[1].upper())
                    except:nameSelect.append(file.rsplit('/', 1)[1].upper())
                    logSelect.append(file)
            count=0
            for fi in logSelect:
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'sendMessage','chat_id': selected_group_id,'input_message_content': {'@type':'inputMessageDocument','document': {'@type':'inputFileLocal','path': fi}},'@extra': 1 })
                     }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            try:
                os.remove(zip_name)
            except:
                pass
    xbmcgui.Dialog().ok('Upload Log','Ok')
   except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Upload Log:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))

def join_all_groups(url):
    
    
    num=random.randint(0,60000)

    #log.warning(url)
    
    j_complete_list=json.loads(url)
    #log.warning('j_complete_list:::')
    #log.warning(j_complete_list)
    all_j=[]
    dp = xbmcgui.DialogProgress()
            
    dp.create('Telemedia', '[B][COLOR=yellow]%s[/COLOR][/B]'%Addon.getLocalizedString(32062))
    zzz=0
    for j_urls in j_complete_list['public']:
    
      if len(j_urls)>0:
       
        if '$$$' in j_urls:
            all_links=j_urls.split('$$$')
        else:
            all_links=[j_urls]
        if dp.iscanceled():
                    break
        for items in all_links:
            #log.warning('items:::')
            #log.warning(items)
            if items=='joinchat':
                continue
            num=random.randint(0,60000)
            
            dp.update(int((zzz*100.0)/len(j_complete_list['public'])),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062), '[B][COLOR=yellow]%s[/COLOR][/B]'%items +' , %s/%s'%(str(zzz),str(len(j_complete_list['public']))))
            zzz+=1
            data={'type':'td_send',
             'info':json.dumps({'@type': 'searchPublicChat','username':items, '@extra':num})
             }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if event:
              if 'id' in event :
                
                o_id=event['id']
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'joinChat', 'chat_id': event['id'], '@extra': num})
                     }
                event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                if event:
                  if event.get('@type') =='error':
                    if 'Too Many Requests: retry after' in str(event.get('message')):
                        try:
                            time_to_wait=int(str(event.get('message')).split('Too Many Requests: retry after'))
                        except:
                            continue
                        while( time_to_wait>0):
                            dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062), '[B][COLOR=yellow]Wait for %s sec[/COLOR][/B]'% str(time_to_wait))
                            time_to_wait-=1
                            time.sleep(1)
                
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': o_id,'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
                
                time.sleep(0.1)
               
                
            if dp.iscanceled():
                    break
    for j_urls in j_complete_list['by_link']:
    
    
      if len(j_urls)>0:
       
        by_link_chats=j_urls
        
        if '$$$' in url:
            all_urls=by_link_chats.split('$$$')
        else:
            all_urls=[by_link_chats]
        zzz=0
        for it in all_urls:
          if it!='joinchat':
            if it in all_j:
                continue
            all_j.append(it)

            dp.update(int((zzz*100.0)/len(j_complete_list['by_link'])),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062)+'\n'+ '[B][COLOR=yellow]%s[/COLOR][/B]'%it)
            zzz+=1
            num=random.randint(0,60000)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'checkChatInviteLink', 'invite_link': 'https://t.me/joinchat/'+it, '@extra': num})
             }
                   
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if not event:
                continue
            if 'chat_id' in event:
                continue
            # else:
                # log.warning('Joining:'+'https://t.me/joinchat/'+it)
            data={'type':'td_send',
             'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': 'https://t.me/joinchat/'+it, '@extra': num})
             }
                   
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            if event.get('@type') =='error':
                if 'Too Many Requests: retry after' in str(event.get('message')):
                    time_to_wait=int(str(event.get('message')).split('Too Many Requests: retry after')[1])
                    while( time_to_wait>0):

                        dp.update(int((zzz*100.0)/len(j_urls)),'[B][COLOR=green]%s[/COLOR][/B]'%Addon.getLocalizedString(32062)+'\n'+ '[B][COLOR=yellow]Wait for %s[/COLOR][/B]'% str(time_to_wait))
                        time_to_wait-=1
                        time.sleep(1)
                        if dp.iscanceled():
                            break
            
            if event and 'id' in event:
                num=random.randint(0,60000)
                data={'type':'td_send',
                     'info':json.dumps({'@type': 'addChatToList', 'chat_id': event['id'],'chat_list':{'@type':'chatListArchive'}, '@extra': num})
                     }
                event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            time.sleep(1)
            if dp.iscanceled():
                    break
        if dp.iscanceled():
                    break

    dp.close()
    xbmcgui.Dialog().ok('Telemedia','All Done')
def set_bot_id(name):
   
   
   try:
    if name=='auto':
        ret_bot=1
        if len(Addon.getSetting("update_chat_id"))>0:
            dialog = xbmcgui.Dialog()
            ret_bot = dialog.select(Addon.getLocalizedString(32028), [Addon.getLocalizedString(32125), Addon.getLocalizedString(32126)])
    all_update_bot=[]
    if ',' in Addon.getSetting("update_chat_id"):
        all_update_bot=Addon.getSetting("update_chat_id").split(',')
    elif len(Addon.getSetting("update_chat_id"))>0:
        all_update_bot=[Addon.getSetting("update_chat_id")]
    num=random.randint(0,60000)
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':9223372036854775807, 'limit': '100', '@extra': num})
             }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    exit_now=0
   
    if 'status' in event:
        xbmcgui.Dialog().ok('Error occurred',event['status'])
        exit_now=1
    if exit_now==0:

        counter=0
        counter_ph=10000
    
        j_enent_o=(event)
        zzz=0
        items=''
        names=[]
        ids=[]
        for items in j_enent_o['chat_ids']:
            
            data={'type':'td_send',
                 'info':json.dumps({'@type': 'getChat','chat_id':items, '@extra':counter})
                 }
            event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            order=event['positions'][0]['order']
                          
            j_enent=(event)

            if j_enent['@type']=='chat' and len(j_enent['title'])>1:

                names.append(j_enent['title'])
                ids.append(items)
    selected_group_id=-1
    if len(names)>0:
        ret = xbmcgui.Dialog().select("Choose", names)
        if ret==-1:
            sys.exit()
        else:
            selected_group_id=ids[ret]
        if selected_group_id!=-1:
            if name=='backup':
                
                Addon.setSetting('bot_id',str(ids[ret]))
                
            else:
                if ret_bot==1:
                    Addon.setSetting('update_chat_id',str(ids[ret]))
                else:
                    if str(ids[ret]) not in all_update_bot:
                        Addon.setSetting('update_chat_id',Addon.getSetting("update_chat_id")+','+str(ids[ret]))
    xbmcgui.Dialog().ok('Update bot location','Ok')
   except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            log.warning('ERROR IN Upload Log:'+str(lineno))
            log.warning('inline:'+str(line))
            log.warning(str(e))
            xbmcgui.Dialog().ok('Error occurred','Err:'+str(e)+'Line:'+str(lineno))
def has_addon(name):
    ex=False
    if name=='plugin.program.Settingz':
     name='plugin.program.Settingz-Anon'
    if xbmc.getCondVisibility("System.HasAddon(%s)" % name):
        # log.warning('2')
        ex=True
    else:
        addon_path=os.path.join(xbmc_tranlate_path("special://home"),'addons/')
        # log.warning(addon_path)
        # log.warning(os.listdir(os.path.dirname(addon_path)))
        all_dirs=[]
        for items in os.listdir(os.path.dirname(addon_path)):
            all_dirs.append(items.lower())
        if name.lower() in all_dirs:
            
            ex=True
    ver=''
    if ex:
        ver=((xbmc.getInfoLabel('System.AddonVersion(%s)'%name)))

        addon_path=os.path.join(xbmc_tranlate_path("special://home"),'addons/')
        cur_folder=os.path.join(addon_path,name)
        # log.warning(os.path.join(cur_folder, 'addon.xml'))
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
def joinpack():
            
    import requests,random
    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]מוסיף קבוצות לחשבון[/COLOR]' % COLOR2)
    num=random.randint(1,1001)
 
    # my_movie
    invite_link="https://t.me/+eA6sn8OhyG83NzI0"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            

    # AnonymousTv Update
    id=-1001468271705
    data={'type':'td_send',
     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@anonymoustv_update', '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChat', 'chat_id': id, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    

    # # vip העלאות שלנו
    invite_link="https://t.me/+-sVRNn1HPNNhMjQx"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
            
            

    #ערוץ סרטים מבוגרים
    invite_link="https://t.me/joinchat/AAAAAFK4IYy4YNJdosYR7w"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

def search_result(search_entered):

    from sqlite3 import dbapi2 as database

    dataDir_medovavim =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube.db')
    dbcon = database.connect(dataDir_medovavim)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM kids_movie_ordered where name like '%{0}%'".format(search_entered))
    # logging.warning("SELECT * FROM kids_movie_ordered where name like '%{0}%'".format(search_entered))
    match2 = dbcur.fetchall()
    
    all_w={}
    x=0
    all_l=[]
    from resources.modules.general import replaceHTMLCodes
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match2:
        
        all_l.append(addLink_db(replaceHTMLCodes(name),link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
        x+=1
        
    xbmcplugin.addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))

    dbcur.close()
    dbcon.close()
def heb_mov_letter(iconimage,fanart):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    dataDir_medovavim =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube.db')
    dbcon = database.connect(dataDir_medovavim)
    # logging.warning(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    
    
        
        
    dbcur.execute("SELECT * FROM kids_movie_ordered WHERE substr(name,1,1) NOT LIKE 'א%' and  substr(name,1,1) NOT LIKE 'ב%' and  substr(name,1,1) NOT LIKE 'ג%' and  substr(name,1,1) NOT LIKE 'ד%' and  substr(name,1,1) NOT LIKE 'ה%' and  substr(name,1,1) NOT LIKE 'ו%' and  substr(name,1,1) NOT LIKE 'ז%' and  substr(name,1,1) NOT LIKE 'ח%' and  substr(name,1,1) NOT LIKE 'ט%' and  substr(name,1,1) NOT LIKE 'י%' and  substr(name,1,1) NOT LIKE 'כ%' and  substr(name,1,1) NOT LIKE 'ל%' and  substr(name,1,1) NOT LIKE 'מ%' and  substr(name,1,1) NOT LIKE 'נ%' and  substr(name,1,1) NOT LIKE 'ס%' and  substr(name,1,1) NOT LIKE 'ע%' and  substr(name,1,1) NOT LIKE 'פ%' and  substr(name,1,1) NOT LIKE 'צ%' and  substr(name,1,1) NOT LIKE 'ק%' and  substr(name,1,1) NOT LIKE 'ר%' and  substr(name,1,1) NOT LIKE 'ש%' and  substr(name,1,1) NOT LIKE 'ת%'")
    match_num = dbcur.fetchall()
    
    
    all_l=[]
    exclude=[1503,1498,1509,1501,1507]
    all_l.append(addDir3('1-2'+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match_num)),'0',218,str(iconimage),str(fanart),'סרטים מדובבים'))
    for ch in range(1488,1515): 
        if ch in exclude:
            continue
        dbcur.execute('SELECT * FROM kids_movie_ordered where name like "{0}%"'.format(chr(ch)))
    
        match = dbcur.fetchall()
    
        all_l.append(addDir3(chr(ch)+ ' [COLOR lightblue](%s)[/COLOR] '%str(len(match)),'0',218,str(iconimage),str(fanart),'סרטים מדובבים'))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def heb_mov_dub_letter(name,url):
    o_name=name
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    dataDir_medovavim =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube.db')
    dbcon = database.connect(dataDir_medovavim)
    # logging.warning(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    name=name.split(' [')[0]
    if name=='1-2':
        exclude=[1503,1498,1509,1501,1507]
        all_s=[]
        for ch in range(1488,1515): 
            if ch in exclude:
                continue
            all_s.append("substr(name,1,1) NOT LIKE '{0}%' and ".format(chr(ch)))
        
        dbcur.execute("SELECT * FROM kids_movie_ordered WHERE substr(name,1,1) NOT LIKE 'א%' and  substr(name,1,1) NOT LIKE 'ב%' and  substr(name,1,1) NOT LIKE 'ג%' and  substr(name,1,1) NOT LIKE 'ד%' and  substr(name,1,1) NOT LIKE 'ה%' and  substr(name,1,1) NOT LIKE 'ו%' and  substr(name,1,1) NOT LIKE 'ז%' and  substr(name,1,1) NOT LIKE 'ח%' and  substr(name,1,1) NOT LIKE 'ט%' and  substr(name,1,1) NOT LIKE 'י%' and  substr(name,1,1) NOT LIKE 'כ%' and  substr(name,1,1) NOT LIKE 'ל%' and  substr(name,1,1) NOT LIKE 'מ%' and  substr(name,1,1) NOT LIKE 'נ%' and  substr(name,1,1) NOT LIKE 'ס%' and  substr(name,1,1) NOT LIKE 'ע%' and  substr(name,1,1) NOT LIKE 'פ%' and  substr(name,1,1) NOT LIKE 'צ%' and  substr(name,1,1) NOT LIKE 'ק%' and  substr(name,1,1) NOT LIKE 'ר%' and  substr(name,1,1) NOT LIKE 'ש%' and  substr(name,1,1) NOT LIKE 'ת%' ORDER BY name ASC")
    else:
        dbcur.execute('SELECT * FROM kids_movie_ordered where name like "{0}%" ORDER BY name ASC'.format(name))
    all_l=[]
    match = dbcur.fetchall()
    x=page
    all_w={}
    # if len(Addon.getSetting("firebase"))>0:
            # all_db=read_firebase('last_played_movie_seek_time')
       
            # for itt in all_db:
                # if 'name' not in all_db[itt]:
                    # continue
                # items=all_db[itt]
                # all_w[items['name']]={}
                # all_w[items['name']]['seek_time']=items['seek_time']
                # all_w[items['name']]['total_time']=items['total_time']
    from resources.modules.general import replaceHTMLCodes
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
        if (x>=(page*50) and x<=((page+1)*50)):
            all_l.append(addLink_db(replaceHTMLCodes(name),link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
        x+=1

    if (len(match)-((page+1)*50))>0:
        all_l.append(addDir3(o_name+' [COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),218,'special://home/addons/plugin.video.telemedia/tele/next.png','','סרטים מדובבים'))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def connect_Chat():
    
    
    LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]מוסיף קבוצות לחשבון[/COLOR]' % COLOR2)
    num=random.randint(1,1001)
 
    #ערוץ נתי מדיה סרטים
    invite_link="https://t.me/joinchat/V9QplllGIlPVnoic"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

    #ערוץ נתי מדיה סדרות
    invite_link="https://t.me/joinchat/TwsklSm3Z_oAx8XC"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    #ערוץ סדרות ישראליות
    invite_link="https://t.me/joinchat/AAAAAEYxRFfUlT_C8fSeIA"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
     
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    #ערוץ סרטים ישראלים
    invite_link="https://t.me/joinchat/AAAAAEH4beThZwz_zCNQWA"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
     
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
     #ערוץ קבוצות טלגרם
    id=-1001416235520
    data={'type':'td_send',
     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@MyTelegraMediaGroups', '@extra': num})
     }
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChat', 'chat_id': id, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

    #ערוץ עולם הילדים נתי מדיה
    invite_link="https://t.me/joinchat/AAAAAEqauFWJ4Zar9vPxsg"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
     
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

    #ערוץ בוט קבצים
    id=-1001485772677
    data={'type':'td_send',
     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@allinoneindex', '@extra': num})
     }
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChat', 'chat_id': id, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    
    #ערוץ בוט קבצים2
    id=-1001315491418
    data={'type':'td_send',
     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@allinoneindex1', '@extra': num})
     }
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChat', 'chat_id': id, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()

    #ערוץ סדרות לילדים2 לא זמין כרגע
    id=-1001332295041
    data={'type':'td_send',
     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@shalom_yeladim_1', '@extra': num})
     }
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChat', 'chat_id': id, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    #ערוץ סדרות לילדים
    id=-1001142678650
    data={'type':'td_send',
     'info':json.dumps({'@type': 'searchPublicChat', 'username': '@mediachildren', '@extra': num})
     }
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChat', 'chat_id': id, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    
    #ערוץ סרטים מבוגרים
    invite_link="https://t.me/joinchat/AAAAAFK4IYy4YNJdosYR7w"
    data={'type':'td_send',
     'info':json.dumps({'@type': 'joinChatByInviteLink', 'invite_link': invite_link, '@extra': num})
     }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()



def my_repo():
    
    
    from packaging import version
    id=Addon.getSetting("update_chat_id")
    num=random.randint(0,60000)
    if ',' in Addon.getSetting("update_chat_id"):
        all_ids=Addon.getSetting("update_chat_id").split(',')
    else:
        all_ids=[Addon.getSetting("update_chat_id")]
    try:
        if os.path.exists(addon_path):
            shutil.rmtree(addon_path)
    except Exception as e:
        log.warning('error removing folder:'+str(addon_path)+','+str(e))
    if not xbmcvfs.exists(addon_path+'/'):
        os.makedirs(addon_path)
    all_addons={}
    all_repo_info=[]
    for in_ids in all_ids:

        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':(in_ids), 'query': '','from_message_id':0,'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':100, '@extra': num})
             }

        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        try:
            if 'Chat not found' in event['message']:
               LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]יש להתחבר לערוץ העדכונים[/COLOR]' % COLOR2)
               break
            if 'Have no info about the chat' in event['message']:
               LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]יש להתחבר לערוץ העדכונים[/COLOR]' % COLOR2)
               break
        except: pass
        for items_in in event['messages']:  
              if 'chat_id' in items_in:

                    #log.warning('correct chatid')
                    if 'content' in items_in:
                        items=items_in
                        if 'document' in items_in['content']:
                            #log.warning('correct doc')
                            if 'file_name' in items_in['content']['document']:
                                f_name=items_in['content']['document']['file_name']
                                c_f_name=f_name.split('-')
                                if len(c_f_name)==0:
                                    continue
                                c_f_name=c_f_name[0]
                                if '.xml' in f_name:
                                    mv_name=os.path.join(addon_path,c_f_name)
                                    num=random.randint(0,60000)
                                    try:
                                        addon=download_photo(items_in['content']['document']['document']['id'],num,c_f_name,mv_name)
                                        file = open(addon, 'r') 
                                        file_data= file.read()
                                        file.close()
                                        all_repo_info.append(file_data)
                                    except:
                                        pass
                                if '.zip' not in f_name:
                                    continue
                                
                                #log.warning(f_name)
                                
                                
                                if '-' not in f_name:
                                    continue
                                new_addon_ver=f_name.split('-')[1].replace('.zip','')
                               
                                size=items['content']['document']['document']['size']
                                
                                f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                                idd=str(items_in['content']['document']['document']['id'])
                                ex,cur_version=has_addon(c_f_name)
                                if c_f_name in all_addons:
                                    all_addons[c_f_name].append({'version':new_addon_ver,'ex':ex,'f_name':f_name,'id':idd,'m_id':items_in['id'],'c_id':items_in['id'],'size':str(f_size2)})
                                else:
                                    
                                    all_addons[c_f_name]=[]
                                    all_addons[c_f_name].append({'version':new_addon_ver,'ex':ex,'f_name':f_name,'id':idd,'m_id':items_in['id'],'c_id':items_in['id'],'size':str(f_size2)})

    m=[]
    for tt in all_repo_info:
        regex='setting f_name="(.+?)" "display_name"="(.+?)" icon="(.+?)" fanart="(.+?)" description="(.+?)"'
        m=m+re.compile(regex,re.DOTALL).findall(tt)
    all_data_addon={}

    for f_name,disp_name,icon,fanart,plot in m:
        all_data_addon[f_name]={'disp_name':disp_name,'icon':icon,'fanart':fanart,'plot':plot}
    for items in all_addons:
        link_data={}
        name=items
       
        f_lk=json.dumps(all_addons[items])
        f_size2=all_addons[items][0]['size']
        color='white'
        if all_addons[items][0]['ex']==False:
            color='lightblue'
        title=name
        fan=' '
        icon=' '
        plot=' '
        #log.warning(items)
        if items in all_data_addon:
            
            title=all_data_addon[items]['disp_name']
            icon=all_data_addon[items]['icon']
            fan=all_data_addon[items]['fanart']
            plot=all_data_addon[items]['plot']
        addNolink('[COLOR %s]'%color+ title+'[/COLOR]',f_lk ,47,False, iconimage=icon,fan=fan,generes=f_size2,plot=plot,original_title=json.dumps(all_addons))
def multi_install(name,url,original_title):
    try:
            
        from zfile_18 import ZipFile
    except:
        from zipfile import ZipFile
    
    all_data=json.loads(url)
   
    silent=False
  
    #log.warning(original_title)
    try:
        all_avi_addond=json.loads( urllib.parse.unquote_plus(original_title))
    except:
        all_avi_addond=json.loads(urllib.unquote_plus(original_title))
    try:
        if os.path.exists(addon_path):
            shutil.rmtree(addon_path)
    except Exception as e:
        log.warning('error removing folder:'+str(addon_path)+','+str(e))
    if not xbmcvfs.exists(addon_path+'/'):
        os.makedirs(addon_path)
                
    all_ver=[]
    all_d=[]
    for items in all_data:
        all_ver.append(items['version'])
        all_d.append(items['f_name'])
    
    ret = xbmcgui.Dialog().select("Choose", all_ver)
    if ret==-1:
        sys.exit()
    else:
        url=all_data[ret]['id']
        name=all_d[ret]
        #log.warning(name)
        #log.warning(xbmc.getCondVisibility("System.HasAddon(%s)" % name.split('-')[0]))
        #log.warning(url)
        #log.warning(xbmc.getInfoLabel('System.AddonVersion(%s)'%name.split('-')[0]))
        
        num=random.randint(0,60000)
        #Install
        #log.warning('url::'+url)
        
        if silent:
            ok=True
        else:
            ok=xbmcgui.Dialog().yesno(Addon.getLocalizedString(32033),(Addon.getLocalizedString(32033)+' %s?'%name))
        if ok:
            if silent==False:
                dp = xbmcgui.DialogProgress()
                dp.create('Telemedia', '[B][COLOR=yellow]Installing[/COLOR][/B]'+'\n'+'')
            
            mv_name=os.path.join(addon_path,name)
            #log.warning('Downloading addon')
            addon=download_photo(url,num,name,mv_name)
            xbmc.sleep(1000)
            if silent==False:
                dp.update(0,'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Extracting[/COLOR][/B]')
            zf = ZipFile(addon)

            uncompress_size = sum((file.file_size for file in zf.infolist()))

            extracted_size = 0

            for file in zf.infolist():
                extracted_size += file.file_size
                if silent==False:

                    dp.update(int((extracted_size*100.0)/uncompress_size),'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Extracting[/COLOR][/B]'+'\n'+file.filename)
                zf.extract(member=file, path=addon_extract_path)
            zf.close()
            f_o = os.listdir(addon_extract_path)
            
            filename=os.path.join(addon_extract_path,f_o[0], 'addon.xml')
            if sys.version_info.major > 2:
                do_open = lambda filename: open(filename, encoding='utf-8')
            else:
                do_open = lambda filename: open(filename)

            with do_open(filename) as file:
                file_data= file.read()
                pass

            
            file.close()
            regex='id=(?:"|\')(.+?)(?:"|\')'
            nm=re.compile(regex).findall(file_data)[0]
            if not xbmc.getCondVisibility("System.HasAddon(%s)" % name.split('-')[0]):
                regex='import addon=(?:"|\')(.+?)(?:"|\')'
                dep=re.compile(regex).findall(file_data)
                missing=[]
                if silent==False:

                    dp.update(90,'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Dependencies[/COLOR][/B]'+'\n'+'')
                zzz=0
                for items in dep:
                    if silent==False:

                            dp.update(int((extracted_size*100.0)/len(items)),'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Dependencies[/COLOR][/B]'+'\n'+items)

                    zzz+=1
                    if not xbmc.getCondVisibility("System.HasAddon(%s)" % items):
                        missing.append(items)
                if len(missing)>0:
                    for itemm in missing:
                        if itemm in all_avi_addond:
                            install_addon(itemm,json.dumps(all_avi_addond[itemm][0]),silent=True,Delete=False)
                        else:
                            xbmc.executebuiltin('InstallAddon(%s)'%itemm)
                            zzx=0
                            while not xbmc.getCondVisibility("System.HasAddon(%s)" % itemm):

                                dp.update(int((zzx*100.0)/100),'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Waiting[/COLOR][/B]'+'\n'+itemm)

                                zzx+=1
                                if xbmc .getCondVisibility ("Window.isVisible(yesnodialog)"):
                                        xbmc.executebuiltin('SendClick(11)')
                                if zzx>100:
                                    break
                                xbmc.sleep(1000)

            addon_p=xbmc_tranlate_path("special://home/addons/")
            files = os.listdir(addon_extract_path)
            not_copied=copyDirTree(os.path.join(addon_extract_path,f_o[0]),os.path.join( addon_p,f_o[0]))
            if len(not_copied)>0:
                showText('File That was not copied', '\n'.join(not_copied))
            x=xbmc.executebuiltin("UpdateLocalAddons")
            if silent==False:
                dp.update(100,'[B][COLOR=green]Telemedia[/COLOR][/B]'+'\n'+ '[B][COLOR=yellow]Cleaning[/COLOR][/B]'+'\n'+'')
            time.sleep(1)
            dis_or_enable_addon(nm)
            try:
                shutil.rmtree(addon_path)
            except:
                pass
            if silent==False:
                dp.close()
            #'Installed'
            #'Installation complete'
            if silent==False:
                xbmcgui.Dialog().ok(Addon.getLocalizedString(32034),Addon.getLocalizedString(32035))


def clean_space():
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    dp = xbmcgui.DialogProgress()
            
    dp.create('Telemedia', '[B][COLOR=yellow]Cleaning[/COLOR][/B]','')
    HOME= xbmc_tranlate_path('special://home/')
    USERDATA= os.path.join(HOME,      'userdata')
    ADDONS           = os.path.join(HOME,      'addons')
    
    THUMBS= os.path.join(USERDATA,  'Thumbnails')
    TEMPDIR= xbmc_tranlate_path('special://temp')
    PACKAGES= os.path.join(ADDONS,    'packages')
    remove_all=[THUMBS,TEMPDIR,PACKAGES]
    for items in remove_all:
        dp.update(0, 'Please Wait...','Removing File', items )
        shutil.rmtree(items,ignore_errors=True, onerror=None)
    DATABASE         = os.path.join(USERDATA,  'Database')
    try:
        os.mkdir(THUMBS)
    except:
        pass
    try:
        os.mkdir(TEMPDIR)
    except:
        pass
    try:
        os.mkdir(PACKAGES)
    except:
        pass
    arr = os.listdir(DATABASE)
    
    dp.update(0, 'Please Wait...','Clean DB', '' )
    for items in arr:
        if 'Textures' in items:
            try:
                found=(os.path.join(DATABASE,items))
            except:
                pass
    cacheFile=found
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("DELETE  FROM path")
    dbcur.execute("DELETE  FROM sizes")
    dbcur.execute("DELETE  FROM texture")
    dbcur.execute("DELETE  FROM version")
    dbcon.commit()
    dbcur.close()
    dbcon.close()
    dp.close()
    xbmcgui.Dialog().ok('Clean','Done.')
def get_version():
    
    
    num=random.randint(1,1001)
    data={'type':'td_send',
                 'info':json.dumps({'@type': 'getOption','name':'version', '@extra': num})
                 }
    event2=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    xbmcgui.Dialog().ok('Tdlib Version',event2['value'])
# get_version()
def get_folders(iconimage,fanart):
    
    data={'type':'getfolders',
         'info':''
         }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    #log.warning(json.dumps(event))
    all_d=[]
    for items in event['status']:
        aa=addDir3(event['status'][items],str(items),12,iconimage,fanart,event['status'][items],groups_id=items,last_id='0$$$9223372036854775807')
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def select_file_browser():

            items  = xbmcvfs.listdir('androidapp://sources/apps/')[1]
            select = selectDialog("Select File Explorer",items)
            Addon.setSetting('Custom_Manager',select)
def calendars():
        import datetime
        datetime_get = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        m = "January|February|March|April|May|June|July|August|September|October|November|December".split('|')
        try: months = [(m[0], 'January'), (m[1], 'February'), (m[2], 'March'), (m[3], 'April'), (m[4], 'May'), (m[5], 'June'), (m[6], 'July'), (m[7], 'August'), (m[8], 'September'), (m[9], 'October'), (m[10], 'November'), (m[11], 'December')]
        except: months = []

        d = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday".split('|')
        try: days = [(d[0], 'Monday'), (d[1], 'Tuesday'), (d[2], 'Wednesday'), (d[3], 'Thursday'), (d[4], 'Friday'), (d[5], 'Saturday'), (d[6], 'Sunday')]
        except: days = []
        list=[]
        calendar_link = 'https://api.tvmaze.com/schedule?date=%s'
        for i in range(0, 30):
            if 1:#try:
                name = (datetime_get - datetime.timedelta(days = i))
                name = ("[B]%s[/B] : %s" % (name.strftime('%A'), name.strftime('%d %B')))
                for m in months: name = name.replace(m[1], m[0])
                for d in days: name = name.replace(d[1], d[0])
                try: name = name
                except: pass

                url = calendar_link % (datetime_get - datetime.timedelta(days = i)).strftime('%Y-%m-%d')

                list.append({'name': name, 'url': url, 'image': 'calendar.png', 'action': 'calendar'})
            #except:
            #    pass
        
        return list
def c_get_tv_maze(urls,original_image):
   all_d=[]
   for url in urls:
    #log.warning(url)
    
    from resources.modules.general import base_header
    x=requests.get(url,headers=base_header).json()
    
    for items in x:
        season=str(items['season'])
        if items['number']==None:
            episode='1'
        else:
            episode=str(int(items['number']))
        
        if len(episode)==1:
          episode_n="0"+episode
        else:
           episode_n=episode
        if len(season)==1:
          season_n="0"+season
        else:
          season_n=season
        
        id=items['show']['externals']['thetvdb']
        if id==None:
            id=items['show']['externals']['imdb']
            id='imdb'+str(id)
        else:
            id='tvdb'+str(id)
            
        '''
        url2=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=tvdb_id&language=%s'%(imdb_id,lang)
        #log.warning(items['show']['externals'])
        html_im=requests.get(url2).json()
       
        data=html_im['tv_results']
        if len(data)==0:
            continue
        else:
            data=data[0]
        title=data['name']+' -S%sE%s - '%(season_n,episode_n)
        plot=items['airdate']+'\n'+data['overview']
        if data['poster_path']==None:
            data['poster_path']=''
        if data['backdrop_path']==None:
            data['backdrop_path']=''
        icon='https://image.tmdb.org/t/p/original/'+data['poster_path']
        fan='https://image.tmdb.org/t/p/original/'+data['backdrop_path']
        id=str(data['id'])
        original_name=data['original_name']
        eng_name=original_name
        if 'first_air_date' in data:
           year=str(data['first_air_date'].split("-")[0])
        elif 'release_date' in data:
            year=str(data['release_date'].split("-")[0])
        else:
            year='0'
        '''
        title=items['show']['name']+' -S%sE%s- %s'%(season_n,episode_n,items['name'])
        plot=items['show']['summary']
        if plot==None:
            plot=''
        plot=items['airdate']+'\n'+plot
        icon=' '
        if items['show']['image']==None:
            icon=original_image
        else:
         for it in items['show']['image']:
           icon=items['show']['image'][it]
        fan=icon
       
        original_name=items['show']['name']
        eng_name=items['show']['name']
        if 'premiered' in items:
           year=str(data['premiered'].split("-")[0])
       
        else:
            year='0'
        all_g=[]
        for it in items['show']['genres']:
            all_g.append(it)
        generes=','.join(all_g)
        
        aa=addDir3( title, 'www',20, icon,fan,plot,data=year,generes=generes,original_title=original_name,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=year,heb_name=original_name)
        all_d.append(aa)
   return all_d
def get_tv_maze(url,original_image):
    urls = [i['url'] for i in calendars()][:5]
    #log.warning(urls)
    
    all_d=c_get_tv_maze(urls,original_image)
    
    #time_to_save=int(Addon.getSetting("save_time"))
    #all_d=cache.get(c_get_tv_maze, time_to_save, urls,original_image)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def check_firebase():
        try:
            all_db=read_firebase('table_name')
        except Exception as e:
          import linecache,sys
          exc_type, exc_obj, tb = sys.exc_info()
          f = tb.tb_frame
          lineno = tb.tb_lineno
          log.warning('Error :'+ str(e) +',line no:'+str(lineno))
          match_playtime = self.dbcur.fetchone()
          LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)
          try:
            xbmc.executebuiltin("RunPlugin(plugin://plugin.program.mediasync?mode=9&url=www)")
          except:pass
def  sync_firebase_to_database(notify=False):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))#.decode("utf-8")
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'database.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
    dbcur.execute("DELETE  FROM  playback")
    #המשך צפייה
    try:
        dbcur.execute("SELECT * FROM playback ")
        match = dbcur.fetchall()
    except:pass

    all_db=read_firebase('playback')
    match=[]
    for itt in all_db:
        items=all_db[itt]
        match.append((items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
    for original_title , tmdb, season, episode, playtime,total,free in match:
        dbcur.execute("SELECT * FROM playback ")
        match = dbcur.fetchall()
        if match==None:
           match=-1
        dbcur.execute("INSERT INTO playback Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" %  (original_title.replace("'","%27") , tmdb, season, episode, str(playtime),str(total),' '))
        dbcon.commit()
        
    #חיפוש
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
    dbcur.execute("DELETE  FROM  search")
    try:
        dbcur.execute("SELECT * FROM search ")
        matchsearch = dbcur.fetchall()
    except:pass
    all_db_search=read_firebase('search')
    match_search=[]
    for itt in all_db_search:
        items=all_db_search[itt]
        match_search.append((items['name'],items['free']))
    for name , free in match_search:
        dbcur.execute("SELECT * FROM search ")
        match_search = dbcur.fetchall()
        if match_search==None:
           match_search=-1
        dbcur.execute("INSERT INTO search Values ('%s', '%s');" %  (name.replace("'","%27") , free))
        dbcon.commit()



    #מעקב סדרות
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    dbcur.execute("DELETE  FROM  Lastepisode")
    try:
        dbcur.execute("SELECT * FROM Lastepisode ")
        matchtrackt = dbcur.fetchall()
    except:pass
    all_db_trackt=read_firebase('trackt')
    match_trackt=[]
    for itt in all_db_trackt:
        items=all_db_trackt[itt]
        
        match_trackt.append((items['name'],items['url'],items['iconimage'],items['fanart'],items['overview'],items['year'],items['original_title'],items['season'],items['episode'],items['tmdb'],items['eng_name'],items['show_original_year'],items['heb_name'],items['isr'],items['type']))
    for name , url, iconimage, fanart, overview, year, original_title, season, episode, tmdb, eng_name,show_original_year,heb_name,isr,tv_movie, in match_trackt:
        dbcur.execute("SELECT * FROM Lastepisode ")
        match_trackt = dbcur.fetchall()
        if match_trackt==None:
           match_trackt=-1

        dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (heb_name.replace("'","%27"),url,iconimage,fanart,description.replace("'","%27"),show_original_year,original_title.replace("'","%27"),season,episode,tmdb,original_title.replace("'","%27"),show_original_year,heb_name.replace("'","%27"),'0',tv_movie))

        dbcon.commit()

    if notify:
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'תהנו'),'[COLOR %s]הסנכרון הסתיים[/COLOR]' % COLOR2)


def database_auto():

  if 0:#  Addon.getSetting("sync_mod")=='true' and len(Addon.getSetting("firebase"))>0 and len(Addon.getSetting("firebase"))>0:
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))#.decode("utf-8")
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'database.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
    dbcur.execute("SELECT * FROM playback ")
    match = dbcur.fetchall()

    if len(Addon.getSetting("firebase"))>0:
        t = Thread(target=sync_firebase_to_database, args=())
        t.start()
        # thread=[]
        
        # thread.append(Thread(sync_firebase_to_database))

        # thread[0].start()

    dbcon.commit()
def database_refresh():

    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))#.decode("utf-8")
    tmdb_data_dir = addonPath#os.path.join(addonPath, 'resources', 'tmdb_data')
    tmdb_cacheFile = os.path.join(tmdb_data_dir, 'database.db')
    dbcon = database.connect(tmdb_cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
    dbcur.execute("SELECT * FROM playback ")
    match = dbcur.fetchall()

    if len(Addon.getSetting("firebase"))>0:
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'מסנכרן את היסטוריית הצפייה שלך'),'[COLOR %s]המתן מספר שניות.[/COLOR]' % COLOR2)
        t = Thread(target=sync_firebase_to_database, args=(True,))
        t.start()
        # thread=[]
        
        # thread.append(Thread(sync_firebase_to_database,True))

        # thread[0].start()

    dbcon.commit()
def clean_search(name,clean_all):
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        from sqlite3 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        if clean_all=='false':
            dbcur.execute("DELETE FROM search where name='%s' "%(name.replace('היסטוריית חיפוש: ','').replace("'","%27")))
            dbcon.commit()
        else:
            dbcur.execute("DELETE FROM search")
            dbcon.commit()
        dbcur.close()
        xbmc.executebuiltin('Container.Refresh')
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
def dismark_movie(heb_name,original_title,tmdb):
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')

        from sqlite3 import dbapi2 as database

        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        
        dbcur.execute("DELETE FROM playback where name='%s' and tmdb='%s'"%(original_title.replace("'",""),tmdb))
        dbcur.execute("DELETE FROM playback where name='%s' and tmdb='%s'"%(heb_name.replace("'",""),tmdb))
        dbcon.commit()
        dbcur.close()
        
        
        table_name='playback'
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:

            all_firebase=read_firebase(table_name)
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, heb_name),'[COLOR %s]הוסר[/COLOR]' % COLOR2)
            write_fire=True
            for items in all_firebase:
          
                if all_firebase[items]['original_title']==original_title:

                    # delete_firebase(table_name,items)
                    t = Thread(target=delete_firebase, args=(table_name,items,))
                    t.start()
                    # thread=[]
                    
                    # thread.append(Thread(delete_firebase,table_name,items))

                    
                    # thread[0].start()
                    #write_fire=False
                    break
            for items in all_firebase:
          
                if all_firebase[items]['original_title']==heb_name:
                    t = Thread(target=delete_firebase, args=(table_name,items,))
                    t.start()
                    # delete_firebase(table_name,items)
                    # thread=[]
                    
                    # thread.append(Thread(delete_firebase,table_name,items))

                    
                    # thread[0].start()
                    #write_fire=False
                    break

            xbmc.executebuiltin('Container.Refresh')

        else:
            LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, heb_name),'[COLOR %s]הוסר[/COLOR]' % COLOR2)
            xbmc.executebuiltin('Container.Refresh')
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
def dismark_tv(original_title,tmdb,season,episode):

        from sqlite3 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM playback where name='%s' and tmdb='%s' and season='%s' and episode='%s'"%(original_title.replace("'",""),tmdb,season,episode))
        dbcon.commit()
        dbcur.close()
        xbmc.executebuiltin('Container.Refresh')
        table_name='playback'
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
            all_firebase=read_firebase(table_name)
            write_fire=True
            for items in all_firebase:
          
                if all_firebase[items]['original_title']==original_title:
                 if all_firebase[items]['season']==season:
                  if all_firebase[items]['episode']==episode:
                    # delete_firebase(table_name,items)
                    t = Thread(target=delete_firebase, args=(table_name,items,))
                    t.start()
                    # thread=[]
                    
                    # thread.append(Thread(delete_firebase,table_name,items))

                    
                    # thread[0].start()
                    #write_fire=False
                    break

def mark_movie(original_title,tmdb):

        from sqlite3 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        
        dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (original_title.replace("'",""),tmdb,'','','2','2',' '))
        
        dbcon.commit()
        dbcur.close()
        xbmc.executebuiltin('Container.Refresh')
        table_name='playback'
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
            all_firebase=read_firebase(table_name)
            write_fire=True
            for items in all_firebase:
          
                if all_firebase[items]['original_title']==original_title:

                    # delete_firebase(table_name,items)
                    t = Thread(target=delete_firebase, args=(table_name,items,))
                    t.start()
                    # thread=[]
                    
                    # thread.append(Thread(delete_firebase,table_name,items))

                    
                    # thread[0].start()
                    #write_fire=False
                    break

            if write_fire:
                t = Thread(target=write_firebase, args=(original_title,tmdb,season,episode,'2','2','',table_name,))
                t.start()
                # thread=[]
                
                # thread.append(Thread(write_firebase,original_title,tmdb,season,episode,'2','2','',table_name))

                
                # thread[0].start()
def mark_tv(original_title,tmdb,season,episode):

        from sqlite3 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("INSERT INTO playback Values ('%s','%s','%s','%s','%s','%s','%s');" %  (original_title,tmdb,season,episode,'2','2',' '))
        dbcon.commit()
        dbcur.close()
        xbmc.executebuiltin('Container.Refresh')
        table_name='playback'
        if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
            all_firebase=read_firebase(table_name)
            write_fire=True
            for items in all_firebase:
          
                if all_firebase[items]['original_title']==original_title:
                 if all_firebase[items]['season']==season:
                  if all_firebase[items]['episode']==episode:
                    # delete_firebase(table_name,items)
                    t = Thread(target=delete_firebase, args=(table_name,items,))
                    t.start()
                    # thread=[]
                    
                    # thread.append(Thread(delete_firebase,table_name,items))

                    
                    # thread[0].start()
                    #write_fire=False
                    break

            if write_fire:
            
                t = Thread(target=write_firebase, args=(original_title,tmdb,season,episode,'2','2','',table_name,))
                t.start()
                # thread=[]
                
                # thread.append(Thread(write_firebase,original_title,tmdb,season,episode,'2','2','',table_name))

                
                # thread[0].start()
def download_data_turkey(force=''):#dragon
    from datetime import date, datetime, timedelta
    AUTONEXTRUN    = Addon.getSetting("next_update_turkey")
    AUTOFEQ        = '1'#Addon.getSetting('which_day')
    AUTOFEQ        = int(AUTOFEQ) if AUTOFEQ.isdigit() else 1
    TODAY          = date.today()
    TOMORROW       = TODAY + timedelta(days=1)
    TWODAYS        = TODAY + timedelta(days=2)
    THREEDAYS      = TODAY + timedelta(days=3)
    ONEWEEK        = TODAY + timedelta(days=7)
    service = False
    days = [TODAY, TOMORROW,TWODAYS, THREEDAYS, ONEWEEK]
    feq = int(float(AUTOFEQ))
    
    if AUTONEXTRUN <= str(TODAY) or feq == 0:
        service = True
        next_run = days[feq]
        Addon.setSetting('next_update_turkey', str(next_run))

    if service == True or force=='true':

        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]מעדכן תוכן...[/COLOR]' % COLOR2)
        name =  "turkey"
        buildzip ='https://github.com/drgon1935/2000/blob/main/tur.zip?raw=true'
        dataDir_db =(xbmc_tranlate_path("special://userdata/addon_data/") + 'plugin.video.telemedia/')
        HOME = xbmc_tranlate_path('special://home/')
        ADDONS = os.path.join(HOME,      'addons')
        PACKAGES = os.path.join(ADDONS,    'packages')
        if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
        import urllib
        from urllib.request import urlopen
        from urllib.request import Request
        lib=os.path.join(PACKAGES, '%s_guisettings.zip' % name)
        urllib.request.urlretrieve(buildzip,lib)


        from zipfile import ZipFile
        zf = ZipFile(lib)
        for file in zf.infolist():
            zf.extract(member=file, path=dataDir_db)
        zf.close()

        xbmc.sleep(100)
        try: os.remove(lib)
        except: pass

        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]התוכן עודכן![/COLOR]' % COLOR2)
        xbmc.executebuiltin('Container.Refresh')

def full_data_turkey():
        from sqlite3 import dbapi2 as database
        t = Thread(target=download_data_turkey, args=())
        t.start()
        cacheFile=os.path.join(user_dataDir,'databaseturkey.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("SELECT * FROM my_fd_groups ORDER BY name ASC")
        
        match = dbcur.fetchall()
        all_d=[]
        aa=addLink_db('רענן רשימה',' ',264,False,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','','',video_info='')
        all_d.append(aa)
        aa=addDir3('חיפוש',' ',265,'special://home/addons/plugin.video.telemedia/tele/search.png','','')
        logo_path=os.path.join(user_dataDir, 'logo')

        all_d.append(aa)
        for name,id,icon,fan,plot,free in match:
            try:
                regex='-(.+?)$'
                match=re.compile(regex).findall(icon)
                icon=logo_path+'/-'+match[0]
                match2=re.compile(regex).findall(fan)
                fan=logo_path+'/-'+match2[0]
            except:pass
            aa=addDir3(name.replace('%27',"'"),id,263,icon,fan,plot.replace('%27',"'"),data=id,remove_from_fd_g=True)
            all_d.append(aa)
            
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        
        dbcur.close()
        dbcon.close()
        
def full_data_turkey_2():
        from sqlite3 import dbapi2 as database
        from resources.telemedia import download_data_db
        t = Thread(target=download_data_db, args=())
        t.start()
        cacheFile=(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/databaseturkey2.db')#os.path.join(user_dataDir,'databaseturkey2.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("SELECT * FROM my_fd_groups ORDER BY rowid DESC")
        
        match = dbcur.fetchall()
        all_d=[]
        aa=addLink_db('רענן רשימה',' ',276,False,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','','',video_info='')
        all_d.append(aa)
        aa=addDir3('חיפוש',' ',277,'special://home/addons/plugin.video.telemedia/tele/search.png','','')
        logo_path=os.path.join(user_dataDir, 'logo')

        all_d.append(aa)
        for name,id,icon,fan,plot,free in match:

            try:
                regex='-(.+?)$'
                match=re.compile(regex).findall(icon)
                icon=logo_path+'/-'+match[0]
                match2=re.compile(regex).findall(fan)
                fan=logo_path+'/-'+match2[0]
            except:pass
            aa=addDir3(name.replace('%27',"'"),id,275,icon,fan,plot.replace('%27',"'"),data=id,remove_from_fd_g=True)
            all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        dbcur.close()
        dbcon.close()
def search_result_turkey(search_entered):

    from sqlite3 import dbapi2 as database


    dataDir_turkey =(xbmc_tranlate_path("special://userdata/addon_data/") + 'plugin.video.telemedia/databaseturkey.db')
    dbcon = database.connect(dataDir_turkey)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM my_fd_groups where name like '%{0}%'".format(search_entered))
    match2 = dbcur.fetchall()
    
    
    
    # dataDir_turkey_rd =(xbmc_tranlate_path("special://userdata/addon_data/") + 'plugin.video.telemedia/databaseturkey_rd.db')
    # dbcon_rd = database.connect(dataDir_turkey_rd)
    # dbcur_rd = dbcon_rd.cursor()
    # dbcur_rd.execute("SELECT * FROM my_fd_groups where name like '%{0}%'".format(search_entered))
    # match3 = dbcur_rd.fetchall()
    
   
    x=0
    all_d=[]
    
    for name,id,icon,fan,plot,free in match2:
            try:
                regex='-(.+?)$'

                match=re.compile(regex).findall(icon)
                icon=logo_path+'/-'+match[0]
                match2=re.compile(regex).findall(fan)
                fan=logo_path+'/-'+match2[0]
            except:pass
            aa=addDir3(name.replace('%27',"'"),id,263,icon,fan,plot.replace('%27',"'"),data=id,remove_from_fd_g=True)
            all_d.append(aa)
    # for name,id,icon,fan,plot,free in match3:
            # try:
                # regex='-(.+?)$'

                # match=re.compile(regex).findall(icon)
                # icon=logo_path+'/-'+match[0]
                # match2=re.compile(regex).findall(fan)
                # fan=logo_path+'/-'+match2[0]
            # except:pass
            # aa=addDir3(name.replace('%27',"'"),id,263,icon,fan,plot.replace('%27',"'"),data=id,remove_from_fd_g=True)
            # all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

    dbcur.close()
    dbcon.close()
def search_result_turkey2(search_entered):

    from sqlite3 import dbapi2 as database
    dataDir_turkey =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/databaseturkey2.db')
    dbcon = database.connect(dataDir_turkey)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM my_fd_groups where name like '%{0}%'".format(search_entered))
    match2 = dbcur.fetchall()
    x=0
    all_d=[]
    for name,id,icon,fan,plot,free in match2:
            try:
                regex='-(.+?)$'

                match=re.compile(regex).findall(icon)
                icon=logo_path+'/-'+match[0]
                match2=re.compile(regex).findall(fan)
                fan=logo_path+'/-'+match2[0]
            except:pass
            aa=addDir3(name.replace('%27',"'"),id,263,icon,fan,plot.replace('%27',"'"),data=id,remove_from_fd_g=True)
            all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

    dbcur.close()
    dbcon.close()
def remove_databaseturkey(url,name):
    ok=xbmcgui.Dialog().yesno('הסר תוכן','%s?'%('האם להסיר את: '+name))
    if ok:
        from sqlite3 import dbapi2 as database
        cacheFile=os.path.join(user_dataDir,'databaseturkey.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon.commit()
        dbcur.execute("DELETE  FROM my_fd_groups where id='%s'"%url)
        #log.warning(url)
        dbcon.commit()
        
        cacheFile_rd=(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/databaseturkey2.db')#os.path.join(user_dataDir,'databaseturkey2.db')
        dbcon_rd = database.connect(cacheFile_rd)
        dbcur_rd = dbcon_rd.cursor()
        dbcur_rd.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""id TEXT, ""icon TEXT,""fan TEXT,""plot TEXT, ""free TEXT);" % 'my_fd_groups')
        dbcon_rd.commit()
        dbcur_rd.execute("DELETE  FROM my_fd_groups where id='%s'"%url)
        #log.warning(url)
        dbcon_rd.commit()
        
        
        
        xbmcgui.Dialog().ok('AnonymousTv','הוסר: '+name)
        xbmc.executebuiltin('Container.Refresh')
        
        dbcur.close()
        dbcon.close()
        dbcur_rd.close()
        dbcon_rd.close()
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
        if 'addons_update'==mod:#ערוץ עדכון הרחבות
          # txt='עדכון מהיר'
          # txt='שלח לוג'
            if dragon=='true':
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDU4MDUzMzM1NzpBQUVzTjZPLU5QN05IU1B0eHc2UTZpVnVEa2dhZU1aUU1nOC9zZW5kTWVzc2FnZT9jaGF0X2lkPS0xMDAxNTcwNzQ3MjI0JnRleHQ9').decode('utf-8')
            else:
                error_ad=base64.b64decode('aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDk2Nzc3MjI5NzpBQUhndG1zWEotelVMakM0SUFmNHJKc0dHUlduR09ZaFhORS9zZW5kTWVzc2FnZT9jaGF0X2lkPS0yNzQyNjIzODkmdGV4dD0=').decode('utf-8')

        x=requests.get(error_ad+que(txt)+'\n'+que('שם משתמש: #')+userr+'\n'+que('קוד מכשיר: ')+(HARDWAER)+'\n'+que('מנוי: ')+userdate+'\n'+que('קודי: ')+kodiinfo+'\n'+que('מערכת הפעלה: ')+platform_s()+'\n'+que('שם המערכת: ')+xs+'\n'+que('גירסת ויזארד: ')+version+'\n'+update).json()
        
def search_updates():

    from packaging import version
    num=random.randint(0,60000)
    all_ids=[-1001759184473]
    
    data={'type':'td_send',
             'info':json.dumps({'@type': 'getChats','offset_chat_id':0,'offset_order':0, 'limit': '100','chat_list':{'@type': 'chatListMain'}, '@extra': num})
             }
    
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    for in_ids in all_ids:
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':(in_ids), 'query': '','from_message_id':0,'offset':0,'filter':{'@type': 'searchMessagesFilterDocument'},'limit':100, '@extra': num})
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        if 'messages' not in event:
            # xbmc.executebuiltin('Notification(%s, %s, %d)'%('[COLOR yellow]תקלה נסה שוב מאוחר יותר[/COLOR]',str(json.dumps(event)), 500))
            return ''
        for items_in in event['messages']:  
              if 'chat_id' in items_in:
                    if 'content' in items_in:
                        items=items_in
                        if 'document' in items_in['content']:
                            if 'file_name' in items_in['content']['document']:
                                f_name=items_in['content']['document']['file_name']
                                if '.zip' not in f_name:
                                    continue
                                c_f_name=f_name.split('-')
                                if len(c_f_name)==0:
                                    continue
                                c_f_name=c_f_name[0]
                                if '-' not in f_name:
                                    continue
                                new_addon_ver=f_name.split('-')[1].replace('.zip','')
                                if new_addon_ver=='Anon':
                                    new_addon_ver=f_name.split('-')[2].replace('.zip','')
                                ex,cur_version=has_addon(c_f_name)
                                if ex:
                                   do_update=((version.parse(cur_version)) < (version.parse(new_addon_ver)))
                                   if do_update:
                                    LogNotify('[COLOR yellow]עדכון הרחבה[/COLOR] Ver:%s'%new_addon_ver,c_f_name)
                                    link_data={}
                                    link_data['id']=str(items['content']['document']['document']['id'])
                                    link_data['m_id']=items['id']
                                    link_data['c_id']=items['chat_id']
                                    install_addon(f_name,json.dumps(link_data),silent=True)
                                    LogNotify('[COLOR yellow]הרחבה עודכנה[/COLOR]',f_name.replace('.zip',''))
                                    t = Thread(target=send_info, args=('addons_update','הרחבה עודכנה: '+c_f_name +'\n'+'מגירסה מספר: '+ str(cur_version)+' '+'לגירסה: '+ str(new_addon_ver),))
                                    t.start()

params=get_params()
for items in params:
   params[items]=params[items].replace(" ","%20")
url=None
name=None
mode=None
iconimage=None
fanart=None
resume=None
c_id=None
m_id=None
description=' '
original_title=' '
fast_link=''
data=0
id='0'
saved_name=' '
prev_name=' '
isr=0
no_subs=0
season="%20"
episode="%20"
show_original_year=0
groups_id=0
heb_name=' '
year=' '
tmdbid=' '
eng_name=' '
dates=' '
data1='[]'
file_name=''
fav_status='false'
only_torrent='no'
only_heb_servers='0'
new_windows_only=False
meliq='false'
tv_movie='movie'
last_id='0$$$0$$$0$$$0'
nextup='true'
dd=''
tmdb=''
read_data2=''
all_folders=''
url_o=''
# database_auto()
watched_indicators='0'
kitana='false'
plot=''
rating=''
genre=''
premiered=''
clean_all=''
tag_line=''
try:
     url= unque(params["url"])
except:
     pass
try:
    tag_line = (params['tag_line'])
except:
    pass
try:
     tv_movie=(params["tv_movie"])
except:
        pass
try:
    name=unque(params["name"])
except:
      pass
try:
    iconimage= unque(params["iconimage"])
except:
    pass
try: 
    mode=int(params["mode"])
except:
        pass
try:        
        fanart=unque(params["fanart"])
except:
   pass
try:        
     description=unque(params["description"])
except:
   pass
try:        
    data=unque(params["data"])
except:
   pass
try:        
 
   original_title=unque(params["original_title"])
except:
    pass
try:        
        tmdb=(params["id"])
except:
        pass
try:        
        season=(params["season"])
except:
        pass
try:        
        episode=(params["episode"])
except:
        pass
try:        
        tmdbid=(params["tmdbid"])
except:
        pass
try:        
        eng_name=(params["eng_name"])
except:
        pass
try:        
        show_original_year=(params["show_original_year"])
except:
        pass
try:        
     heb_name= unque(params["heb_name"])
except:
     pass
try:        
        isr=int(params["isr"])
except:
        pass
try:        
        saved_name=clean_name(params["saved_name"],1)
except:
        pass
try:        
        prev_name=(params["prev_name"])
except:
        pass
try:        
        dates=(params["dates"])
except:
        pass
try:        
        no_subs=(params["no_subs"])
except:
        pass
try:        
        image_master= unque(params["image_master"])
except:
    pass
try:        
        last_id= unque(params["last_id"])
except:
    pass
try:        
        resume=(params["resume"])
except:
        pass
try:
    file_name=(params["file_name"])
except:
        pass
try:
    c_id=(params["c_id"])
except:
        pass
try:
    m_id=(params["m_id"])
except:
        pass
try:        
        dd=(params["dd"])
except:
        pass
try:        
        nextup=(params["nextup"])
except:
        pass
try:        
        id=(params["id"]) 
except:
        pass
try:
    groups_id=(params["groups_id"])
except:
        pass
try:
    watched_indicators=(params["watched_indicators"])
except:
    pass
try:
    kitana=(params["kitana"])
except:
    pass
try:
    plot=(params["plot"])
except:
    pass
try:
    rating=(params["rating"])
except:
    pass
try:
    genre=(params["genre"])
except:
    pass
try:
    year=(params["year"])
except:
    pass
try:
    premiered=(params["premiered"])
except:
    pass
try:
    clean_all=(params["clean_all"])
except:
    pass

episode=str(episode).replace('+','%20')
season=str(season).replace('+','%20')
if season=='0':
    season='%20'
if episode=='0':
    episode='%20'
