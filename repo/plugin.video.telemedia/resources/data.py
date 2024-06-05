# -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,re,xbmcplugin,sys,time,xbmcvfs,json,base64
from resources.modules import log
import xbmcvfs
xbmc_tranlate_path=xbmcvfs.translatePath
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc_tranlate_path(__addon__.getAddonInfo('path'))
Addon = xbmcaddon.Addon()

addon_id=__addon__.getAddonInfo('id')
addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))#.decode("utf-8")
addonPath2 = xbmc_tranlate_path(Addon.getAddonInfo("path"))


tmdb_data_dir = os.path.join(addonPath2, 'resources', 'tmdb_data')
ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108

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
COLOR2='yellow'
COLOR1='white'
ADDONTITLE='Telemedia'
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path=dir_path.replace('resources','')
telemaia_icon=os.path.join(dir_path,'icon.png')
DIALOG         = xbmcgui.Dialog()
def LogNotify(title, message, times=2000, icon=telemaia_icon,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)
try:
  cond=xbmc.abortRequested
except:
   cond=xbmc.Monitor().abortRequested()
global global_var,stop_all#global
global stopnext
global stopnow
stopnow=False
stopnext =False
exit_now=0
global_var=[]

from threading import Thread
import mediaurl
update='עדכון מהיר זמין עבורכם'
global nextepisode,namenextupepisode
nextepisode=''
namenextupepisode=''
domain_s='https://'
global stopbuffer
stopbuffer=False
# from resources.modules.globals import *
from resources.modules import cache as  cache
from resources.modules.public import addNolink,addDir3,lang,user_dataDir,addNolink2,addLink2,addLink_db
# from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,cloudflare_request,fix_q,call_trakt,post_trakt,reset_trakt,cloudflare_request,base_header
from pyparsing import my1,my2,my3,my4,my5,sport,tvall,music   
listen_port=Addon.getSetting("port")
try:
    logo_path=os.path.join(user_dataDir, 'logo')

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
try:
    import urllib.parse
except:
    import urlparse

que=urllib.parse.quote_plus
url_encode=urllib.parse.urlencode
py2 = False

unque=urllib.parse.unquote_plus
def replaceHTMLCodes(txt):
    try:
        import HTMLParser
        html_parser = HTMLParser.HTMLParser()
       
    except:
        import html as html_parser
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = html_parser.unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.replace("&#8211", "-")
    txt = txt.replace("&#8217", "'")
    txt = txt.strip()
    return txt
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



def read_firebase(table_name):
    from resources.modules.firebase import firebase
    firebase = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = firebase.get('/', None)
    if table_name in result:
        return result[table_name]
    else:
        return {}
def read_firebase_tmdb(table_name):
    
    from resources.modules.firebase import firebase
    
    firebase = firebase.FirebaseApplication('https://tmdbkodi-default-rtdb.firebaseio.com', None)
    
    result = firebase.get('/', None)
    
    if table_name in result:
        return result[table_name]
    else:
        return {}

def collections(page):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_d=[]
    collection_cacheFile = os.path.join(tmdb_data_dir, 'collection_data.db')
    dbcon_tmdb = database.connect(collection_cacheFile)
    dbcur_tmdb = dbcon_tmdb.cursor()
    dbcur_tmdb.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""id TEXT,""icon TEXT,""fanart TEXT,""plot TEXT,""lang TEXT);"% 'collection')
    dbcon_tmdb.commit()

    amount_per_page=50
    dbcur_tmdb.execute("select * from collection where lang='en' LIMIT %s OFFSET %s;"%(amount_per_page,str(int(page)*50)))
    match = dbcur_tmdb.fetchall()
    # zzz=0
    # start_time=time.time()
    for name,id,icon,fanart,plot,lang in match:
        
        addNolink(name.replace('%27',"'"), id,122,True,fan=domain_s+'image.tmdb.org/t/p/original/'+fanart, iconimage=domain_s+'image.tmdb.org/t/p/original/'+icon,plot=plot.replace('%27',"'"))

    dbcur_tmdb.close()
    dbcon_tmdb.close()
    aa=addDir3('[COLOR aqua][I]עמוד הבא[/COLOR][/I]',str(int(page)+1),121,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','[COLOR aqua][I]עמוד הבא[/COLOR][/I]')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

def adjusted_datetime(string=False, dt=False):
    from datetime import datetime, timedelta
    d = datetime.utcnow() + timedelta(hours=int(72))
    if dt: return d
    d = datetime.date(d)
    if string:
        try: d = d.strftime('%Y-%m-%d')
        except ValueError: d = d.strftime('%Y-%m-%d')
    else: return d

def get_html_data(url):
    import requests
    # import requests
    html=requests.get(url).json()
    return html
def was_i(url):
    addNolink2('[COLOR red][I][B]נקה היסטוריה[/B][/I][/COLOR]','www',162,False,iconimage='https://keepingitclean.ca/images/social/keep-it-clean-social-sharing.jpg',fanart='https://the-clean-show.us.messefrankfurt.com/content/dam/messefrankfurt-usa/the-clean-show/2021/images/kv/Cleanshow%20websideheader_tropfen_2560x1440px_01.jpg')
    try:
        page=int(url)
    except:
        page=0
        
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()

    try:
     dbcur.execute("SELECT * FROM playback ORDER BY rowid DESC")
     dbcon.commit()
    except:pass
    
    if 0:# Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
        try:
            all_db=read_firebase('playback')
            match=[]
            for itt in all_db:
                
                items=all_db[itt]
                match.insert(0,(items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
            
        except:
             LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)
             match = dbcur.fetchall()
             
    else:
        match = dbcur.fetchall()
    # if Addon.getSetting("dp")=='true':
    # dp = xbmcgui . DialogProgress ( )
    # try:
        # dp.create('אנא המתן','מבצע איסוף', '','')
        # dp.update(0, 'אנא המתן','מבצע איסוף', '' )
    # except:
        # dp.create('אנא המתן','מבצע איסוף'+'\n'+ ''+'\n'+'')
        # dp.update(0, 'אנא המתן'+'\n'+'מבצע איסוף'+'\n'+ '' )
    zzz=0
    tmdbKey='653bb8af90162bd98fc7ee32bcbbfb3d'
    all_d=[]
    all_w={}
    x=page
    for name,tmdb,season,episode,playtime,totaltime,free in match:

      # if str(season)!=None and str(season)!="%20" and str(season)!="0":
          # for n,tm,s,e,p,t,f in match:
                    # ee=str(e)
                    # all_w[ee]={}
                    # all_w[ee]['resume']=str(p)
                    # all_w[ee]['totaltime']=str(t)
      
      # else:
          # for n,tm,s,e,p,t,f in match:
                    # ee=str(tm)
                    # all_w[ee]={}
                    # all_w[ee]['resume']=str(p)
                    # all_w[ee]['totaltime']=str(t)
      # all_db=read_firebase('playback')

      # for itt in all_db:
            
            # items=all_db[itt]
            # all_w[items['tmdb']]={}
            # all_w[items['tmdb']]['playtime']=items['playtime']
            # all_w[items['tmdb']]['total']=items['total']

      if float(totaltime)==0:
        continue
        
      if (int((float(playtime)*100)/float(totaltime)))<90:
        try:
        
            a=int(tmdb)
            
        except:
            if 'tt' in free:
             url='https://'+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=%s'%(free,lang)
             import requests
             html_im=requests.get(url).json()
             if season=='0':
                 if len(html_im['movie_results'])>0:
                    tmdb=str(html_im['movie_results'][0]['id'])
             else:
                if len(html_im['tv_results'])>0:
                    tmdb=str(html_im['tv_results'][0]['id'])
             try:
        
                a=int(tmdb)
                
             except:
                continue
            else:
                continue
        
        if season!='0' and season!='' and season!='%20':
         if (x>=(page*12) and x<=((page+1)*12)):
          url_t='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=%s&append_to_response=external_ids'%(tmdb,season,episode,lang)
          html_t=cache.get(get_html_data,9999,url_t, table='posters')
          if 'status_code' in html_t:
            continue
          if 'still_path' in html_t:
            if html_t['still_path']==None:
                html_t['still_path']=''
          else:
            html_t['still_path']=''
          fan='https://'+'image.tmdb.org/t/p/original/'+html_t['still_path']
          time_play='[COLOR yellow][I] '+str(int((float(playtime)*100)/float(totaltime)))+'%'+'[/I][/COLOR]'
          plot=html_t['overview']
          url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=external_ids'%(tmdb,tmdbKey,lang)
          html=cache.get(get_html_data,9999,url2, table='posters')
          if 'poster_path' in html:
              if html['poster_path']==None:
                html['poster_path']=''
          else:
            html['poster_path']=''
          icon='https://'+'image.tmdb.org/t/p/original/'+html['poster_path']
          new_name=html['name']+ ' עונה %s  פרק %s '%(season,episode)+time_play
          url='www'
          if 'air_date' in html_t:
           if html_t['air_date']!=None:
             
             year=str(html_t['air_date'].split("-")[0])
           else:
            year='0'
          else:
            year='0'
          if 'first_air_date' in html:
           if html['first_air_date']!=None:
             
             data=str(html['first_air_date'].split("-")[0])
           else:
            data='0'
          else:
            data='0'
          original_name=html['original_name']
          rating=html['vote_average']
          heb_name=html['name']
          isr='0'
          genres_list=[]
          if 'genres' in html:
            for g in html['genres']:
                  genres_list.append(g['name'])
            
            try:genere = u' / '.join(genres_list)
            except:genere=''
          trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s&tv_movie=%s" % (tmdb,'tv')
          all_d.append(addDir3(new_name,url,20,icon,fan,plot,data=year,original_title=original_name,id=tmdb,rating=rating,heb_name=heb_name,show_original_year=data,isr=isr,generes=genere,trailer=trailer,season=season,episode=episode,all_w=all_w,hist='true'))
         x+=1
        else:
         if (x>=(page*12) and x<=((page+1)*12)):
          url_t='http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s'%(tmdb,lang)
          
          
          #log.warning(url_t)
          html=cache.get(get_html_data,9999,url_t, table='poster')
          if 'status_code' in html:
            continue
          if 'backdrop_path' in html:
              if html['backdrop_path']==None:
                html['backdrop_path']=''
          else:
            html['backdrop_path']=''
          fan=domain_s+'image.tmdb.org/t/p/original/'+html['backdrop_path']
          time_play='[COLOR yellow][I] '+str(int((float(playtime)*100)/float(totaltime)))+'%'+'[/I][/COLOR]'
          if 'overview' not in html:
            continue
          plot=html['overview']
          if 'poster_path' in html:
              if html['poster_path']==None:
                html['poster_path']=''
          else:
            html['poster_path']=''
          icon=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']

          new_name=html['title']+' '+time_play

          url='www'
          if 'release_date' in html:
           if html['release_date']!=None:
             
             year=str(html['release_date'].split("-")[0])
           else:
            year='0'
          else:
            year='0'
          original_title=html['original_title']
          rating=html['vote_average']
          heb_name=html['title']
          isr='0'
          genres_list=[]
          if 'genres' in html:
            for g in html['genres']:
                  genres_list.append(g['name'])
            
            try:
                genere = u' / '.join(genres_list)
            except:
                genere=''
          else:
              genere=''
          trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s&tv_movie=%s" % (tmdb,'tv')
          all_d.append(addDir3(new_name,url,15,icon,fan,plot,episode=' ',season=' ',data=year,original_title=original_title,id=tmdb,rating=rating,heb_name=heb_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,all_w=all_w,hist='true'))
         x+=1
        # if Addon.getSetting("dp")=='true':
        # try:
            # dp.update(int(((zzz* 100.0)/(len(match))) ), 'אנא המתן','טוען', new_name )
        # except:
            # dp.update(int(((zzz* 100.0)/(len(match))) ), 'אנא המתן'+'\n'+'טוען'+'\n'+ new_name )
        
        # zzz+=1
        # if dp.iscanceled():
           # dp.close()
           # break
    # if Addon.getSetting("dp")=='true':
    all_d.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),158,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    # dp.close()
    dbcur.close()
    dbcon.close()
    
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    



def movie_vip(url,description):#סרטים  vip
    import datetime
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_w={}
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur5 = dbcon.cursor()
    try:
     dbcur5.execute("SELECT * FROM playback")
     dbcon.commit()
    except:pass
    match_playback = dbcur5.fetchall()

    for n,tm,s,e,p,t,f in match_playback:
            ee=str(tm)
            all_w[ee]={}
            all_w[ee]['resume']=str(p)
            all_w[ee]['totaltime']=str(t)
    dataDir_movievip =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube_telemovie.db')
    dbcon = database.connect(dataDir_movievip)
    dbcur = dbcon.cursor()

    all_l=[]
    dbcur.execute("SELECT * FROM movie_telegram_ordered ORDER BY date_added DESC")
    match = dbcur.fetchall()
    x=page
    all_data_in=[]
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
        new_date=''
        try:
            try:
                  
                  new_date=datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                  
                  new_date=datetime.datetime(*(time.strptime(date_added, "%Y-%m-%d %H:%M:%S")[0:6]))
                  
        except:
            new_date=new_date
        all_data_in.append((name ,link,icon, image,plot,data,tmdbid ,new_date))
    all_data_in=sorted(all_data_in, key=lambda x: x[7], reverse=True)
    
    for name ,link,icon, image,plot,data,tmdbid ,date_added in all_data_in:

      if (x>=(page*25) and x<=((page+1)*25)):
        xx=json.loads(unque(data))
        f_name=xx['OriginalTitle']
        trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s" % (tmdbid)
        all_l.append(addLink_db(replaceHTMLCodes(name),link,200,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w,original_title=f_name,heb_name=replaceHTMLCodes(name),trailer=trailer))
      x+=1
    all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),199,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))

    dbcur.close()
    dbcon.close()
def idan_menu():
    all_d=[]
    aa=addDir3('לויין 1','www',222,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    all_d.append(aa)
    aa=addDir3('לויין 2','www',223,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    all_d.append(aa)
    # aa=addDir3('לויין 3','www',249,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    # all_d.append(aa)
    # aa=addDir3('לויין 4','www',250,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    # all_d.append(aa)
    # aa=addDir3('לויין 5','www',218,BASE_LOGO+'movies.png',all_fanarts['32024'],'Movies')
    # all_d.append(aa)
    # aa=addDir3('לויין 5','www',226,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    # all_d.append(aa)
    # aa=addDir3('ספורט','www',225,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    # all_d.append(aa)
    aa=addDir3('כל הערוצים מכל העולם','www',224,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    all_d.append(aa)
    aa=addDir3('עידן פלוס','www',248,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def Satellite1():
    base_header={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',

                'Pragma': 'no-cache',
                
               
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                }
    from resources.modules.client import get_html
    x=get_html('https://www.pesekzman.com/',headers=base_header).content()
   
           
    regex='<section class="sidebar" id="sidebar">(.+?)</ul>'
    m=re.compile(regex,re.DOTALL).findall(x)
    
    regex='<a href="(.+?)"><li class="(.+?)"><img src="(.+?)" /><p>(.+?)</p></li></a>'
    m2=re.compile(regex).findall(m[0])
    all_d=[]
    for url,nm,img,name in m2:
             # aa=addLink2('[I]%s[/I]'%Addon.getLocalizedString(32022), url,6,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,tmdb=id,year=show_original_year,place_control=True)
             # all_d.append(aa)
        all_d.append(addLink2(name,url,215,False,img,img,name,description))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def Satellite2(img_o):
    all_d=[]
    all_channels,headers=cache.get(get_fchan, 5,table='pages')

    for items in all_channels:
        name=items
        url=all_channels[items]['url']
        img=all_channels[items]['logo']

        if 'http' not in img:
            img=img_o
        aa=addLink2(name,url+'$$$'+json.dumps(headers),252,False,img,img,name+'.fullChan',description)
        all_d.append(aa)

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def idan():
    all_d=[]
    from resources.modules.client import get_html
    # xx=get_html('https://raw.githubusercontent.com:443/RGdevz/RGDevz.github.io/master/test.txt').content()
    xx=get_html('https://digit.seedhost.eu/kodi/wizard/tv/simple.m3u').content()
    regex='tvg-logo="(.+?)".+?group-title=.+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        # if not 'm3u8' in lk or not 'm3u' in lk:
            # continue
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm, 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def Satellite_3():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(my3).content()
    
    regex='tvg-name="(.+?)".+?tvg-logo="(.+?)".+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,nm2,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm2.replace('#EXTGRP:Израиль | ישראלי',''), 'http'+lk.replace('\n','').strip(),252,False,nm,nm,nm2,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def Satellite_4():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(my4).content()
    
    regex='tvg-rec="(.+?)".+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm, 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def Satellite_1():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(my1).content()
    regex='tvg-rec="(.+?)".+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm.replace('#EXTGRP:Израиль | ישראלי',''), 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def Satellite_2():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(my2).content()
    regex='tvg-logo="(.+?)".+?group-title=.+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm.replace('#EXTGRP:ישראלי',''), 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def tv_all():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(tvall).content()
    regex='tvg-rec="(.+?)".+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm.replace('#EXTGRP:Израиль | ישראלי','').replace('#EXTGRP:',''), 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def idan_chan():
    from  resources.modules.client import get_html
    # x=get_html('https://raw.githubusercontent.com:443/RGdevz/RGDevz.github.io/master/test.txt').content()
    x=get_html('https://digit.seedhost.eu/kodi/wizard/tv/simple.m3u').content()

    regex='tvg-logo="(.+?)".+?group-title=.+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(x)
    all=[]
    for im,nm,lk in m:
        # if 'm3u' not in lk or 'm3u8' not in lk:
         # continue
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm, 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all.append(aa)

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def sport_1():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(sport).content()
    
    regex='tvg-logo="(.+?)".+?group-title=.+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm, 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def Satellite_5():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(my5).content()
    
    regex='tvg-name="(.+?)",.+?(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(im, 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def music_ip():
    all_d=[]
    from resources.modules.client import get_html
    xx=get_html(music).content()
    
    regex='tvg-logo="(.+?)".+?group-title=.+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(xx)

    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm, 'http'+lk.replace('\n','').strip(),252,False,im,im,nm,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def all_movie(url,description):#סרטים מכל הזמנים
    import datetime
    
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_w={}
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur5 = dbcon.cursor()
    try:
     dbcur5.execute("SELECT * FROM playback")
     dbcon.commit()
    except:pass
    match_playback = dbcur5.fetchall()

    for n,tm,s,e,p,t,f in match_playback:
            ee=str(tm)
            all_w[ee]={}
            all_w[ee]['resume']=str(p)
            all_w[ee]['totaltime']=str(t)
    dataDir_allmovie =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube_tele_all_movie.db')
    dbcon = database.connect(dataDir_allmovie)
    dbcur = dbcon.cursor()
    all_l=[]
    dbcur.execute("SELECT * FROM movie_telegram_ordered ORDER BY date_added DESC")
    match = dbcur.fetchall()
    x=page
    all_data_in=[]
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
        new_date=''
        try:
            try:
                  
                  new_date=datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                  
                  new_date=datetime.datetime(*(time.strptime(date_added, "%Y-%m-%d %H:%M:%S")[0:6]))
                  
        except:
            new_date=new_date
        all_data_in.append((name ,link,icon, image,plot,data,tmdbid ,new_date))
    all_data_in=sorted(all_data_in, key=lambda x: x[7], reverse=True)
    
    for name ,link,icon, image,plot,data,tmdbid ,date_added in all_data_in:
        if (x>=(page*25) and x<=((page+1)*25)):
            xx=json.loads(unque(data))
            f_name=xx['OriginalTitle']
            trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s" % (tmdbid)
            all_l.append(addLink_db(replaceHTMLCodes(name),link,200,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w,original_title=f_name,heb_name=replaceHTMLCodes(name),trailer=trailer))
        x+=1
    all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),204,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def movie_deco(url,description):#סרטים  vip
    import datetime
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_w={}
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur5 = dbcon.cursor()
    try:
     dbcur5.execute("SELECT * FROM playback")
     dbcon.commit()
    except:pass
    match_playback = dbcur5.fetchall()

    for n,tm,s,e,p,t,f in match_playback:
            ee=str(tm)
            all_w[ee]={}
            all_w[ee]['resume']=str(p)
            all_w[ee]['totaltime']=str(t)
    dataDir_doco =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube_tele_deco_movie.db')
    dbcon = database.connect(dataDir_doco)
    dbcur = dbcon.cursor()

    all_l=[]

    dbcur.execute("SELECT * FROM movie_telegram_ordered ORDER BY date_added DESC")
    match = dbcur.fetchall()
    x=page
    all_data_in=[]
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
        new_date=''
        try:
            try:
                  
                  new_date=datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                  
                  new_date=datetime.datetime(*(time.strptime(date_added, "%Y-%m-%d %H:%M:%S")[0:6]))
                  
        except:
            new_date=new_date
        all_data_in.append((name ,link,icon, image,plot,data,tmdbid ,new_date))
    all_data_in=sorted(all_data_in, key=lambda x: x[7], reverse=True)
    
    for name ,link,icon, image,plot,data,tmdbid ,date_added in all_data_in:

      if (x>=(page*25) and x<=((page+1)*25)):
        xx=json.loads(unque(data))
        f_name=xx['OriginalTitle']
        trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s" % (tmdbid)
        all_l.append(addLink_db(replaceHTMLCodes(name),link,200,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w,original_title=f_name,heb_name=replaceHTMLCodes(name),trailer=trailer))
      x+=1
    all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),206,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))

    dbcur.close()
    dbcon.close()
def movie_notify(url,description):
    import datetime
    
    movie_date=Addon.getSetting('movie_date')

    menu=[]
    d_save=[]
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_w={}
    count=0
    dataDir_medovavim =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube.db')
    dataDir_movievip =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube_telemovie.db')
    dataDir_doco =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube_tele_deco_movie.db')

    #סרטים VIP
    dbcon = database.connect(dataDir_movievip)
    dbcur = dbcon.cursor()
    #סרטים מכל הזמנים
    #סרטים מדובבים
    dbcon4 = database.connect(dataDir_medovavim)
    dbcur4 = dbcon4.cursor()
    all_l=[]
    try:
        dbcur.execute("SELECT * FROM movie_telegram_ordered ORDER BY date_added DESC")
    except:
        pass

    try:
        dbcur4.execute("SELECT * FROM kids_movie_ordered ORDER BY date_added DESC")
    except:
        pass
    #סרטים VIP
    match = dbcur.fetchall()
    x=page
    all_data_in=[]
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
        new_date=''
        try:
            try:
                  
                  new_date=datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                  
                  new_date=datetime.datetime(*(time.strptime(date_added, "%Y-%m-%d %H:%M:%S")[0:6]))
                  
        except:
            new_date=new_date
        
        all_data_in.append((name ,link,icon, image,plot,data,tmdbid ,new_date))
    all_data_in=sorted(all_data_in, key=lambda x: x[7], reverse=True)
    
    for name ,link,icon, image,plot,data,tmdbid ,date_added in all_data_in:

        count+=1
        if count>7:
            continue
        xx=json.loads(unque(data))
        year=xx['year']
        d_save.append((replaceHTMLCodes(name),link,data,tmdbid,icon,image,plot))
        menu.append([replaceHTMLCodes(name),year,'',icon,image,plot.replace('TEME','').replace('%27',"'"),'',''])
    
    #סרטים מדובבים
    match4 = dbcur4.fetchall()
    x=page
    all_data_in4=[]
    menu.append(['','','','','','','','סרטים מדובבים'])
    d_save.append(('סרטים מדובבים','','','','','',''))
    for name ,link,icon, image,plot,data,tmdbid ,date_added in match4:
        
        try:
            try:
                  new_date=datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                  new_date=datetime.datetime(*(time.strptime(date_added, "%Y-%m-%d %H:%M:%S")[0:6]))
        except:
           try:
            try:
                  new_date=datetime.datetime.strptime(date_added, '%d/%m/%Y %H:%M:%S')
            except TypeError:
                  new_date=datetime.datetime(*(time.strptime(date_added, "%d/%m/%Y %H:%M:%S")[0:6]))
           except:
            new_date=new_date
        all_data_in4.append((name ,link,icon, image,plot,data,tmdbid ,new_date))
    all_data_in4=sorted(all_data_in4, key=lambda x: x[7], reverse=True)
    count=0
    for name ,link,icon, image,plot,data,tmdbid ,date_added in all_data_in4:

        count+=1
        if count>15:
            continue
        try:
            xx=json.loads(unque(data))
            year=xx['year']
        except:
            year=''
        d_save.append((replaceHTMLCodes(name),link,data,tmdbid,icon,image,'connect'))
        menu.append([replaceHTMLCodes(name),year,'',icon,image,plot.replace('TEME','').replace('%27',"'"),'',''])

    menu2 = ContextMenu_new_vip('plugin.video.telemedia', menu,icon,image,'')
    menu2.doModal()
    del menu2
    ret=selected_index
    
    if ret!=-1:
            if 'סרטים מדובבים' in d_save[ret]:
             return
            if 'connect' in d_save[ret]:
                name,link,data,tmdbid,icon,image,plot=d_save[ret]
                url='plugin://plugin.video.mando/?mode=207&name=%s&url=%s&video_info=%s&id=%s&iconimage=%s&fanart=%s&description=%s'%(que(name),link,data,tmdbid,icon,image,que(plot))
                xbmc.executebuiltin('RunPlugin(%s)'%url)
                return
            
            name,link,data,tmdbid,icon,image,plot=d_save[ret]
            
            play_link_db(name,link,data,tmdbid,icon,image,plot,True)
    dbcur.close()
    dbcon.close()

def update_tmdb_cache():
    xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    t_match=[]

    all_db=read_firebase_tmdb('tmdb')
    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    for itt in all_db:
        items=all_db[itt]
        t_match.insert(0,(items['name'],items['tv_movie'],items['aa'],items['bb'],items['cc'],items['dd'],items['year'],items['genere'],items['rating']))

    return t_match
def tmdb_upload(type_t):
    
    telemaia_fan=os.path.join(dir_path,'fanart.jpg')
    d_save=[]
    menu=[]
    t_match=cache.get(update_tmdb_cache,1, table='tmdblist')
    count=0
    all=[]
    # aa=addLink2('רענן רשימה','0',259,True,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','','',place_control=True)
    aa=addLink_db('רענן רשימה',' ',259,False,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','','',video_info='')
    all.append(aa)
    for name,tv_movie,icon,bb,cc,dd,year,genere,rating in t_match:

        
        video_data={}

        video_data['genre']=genere
        video_data['rating']=rating
        video_data['year']=year
        video_data['dateadded']=''
        


        if 'סדרה' == tv_movie and type_t=='tvshow' :

            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            all.append(aa)
        if 'סדרה מדובבת' == tv_movie and type_t=='kids' :
            
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            all.append(aa)
        if 'סדרה טורקית' == tv_movie and type_t=='tvshow_tur' :
            
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            all.append(aa)
        if 'סדרה קוריאנית' == tv_movie and type_t=='tvshow_kor' :
            
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            all.append(aa)
        if 'סדרה הודית' == tv_movie and type_t=='tvshow_hudo' :
            
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            all.append(aa)
        if 'סדרה אנימה' == tv_movie and type_t=='tvshow_anime' :
            
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            all.append(aa)
        if 'סדרה סינית' == tv_movie and type_t=='tvshow_chaina' :
            
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            all.append(aa)
        if 'סרט' == tv_movie and type_t=='movie' :
            # aa=addDir3(name,tv_movie+str(dd),258,icon,bb,cc)
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            # aa=addLink2(name+' - '+tv_movie,tv_movie+str(dd),258,False,icon,bb,cc,place_control=True)
            all.append(aa)
        if 'סרט הודי' == tv_movie and type_t=='movie_hudo' :
            # aa=addDir3(name,tv_movie+str(dd),258,icon,bb,cc)
            aa=addLink_db(name,tv_movie+str(dd),258,False,icon,bb,cc,video_info=json.dumps(video_data))
            # aa=addLink2(name+' - '+tv_movie,tv_movie+str(dd),258,False,icon,bb,cc,place_control=True)
            all.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
            
            
def update_tmdb():
    telemaia_fan=os.path.join(dir_path,'fanart.jpg')
    d_save=[]
    menu=[]
    t_match=cache.get(update_tmdb_cache,1, table='pages')
    count=0
    for name,tv_movie,icon,bb,cc,dd,year,genere,rating in t_match:
        count+=1
        if count>150:
            continue
        d_save.append((name,tv_movie))
        menu.append([name+' - '+tv_movie,'','',icon,'','','',''])
    menu2 = new_update_tmdb('plugin.video.telemedia', menu,'icon',telemaia_fan,'תכנים שנוספו לאחרונה')

    menu2.doModal()
    del menu2
    ret=selected_index

    if ret!=-1:
        name,tv_movie=d_save[ret]

        if 'סרט' in tv_movie:

            xbmc.executebuiltin('PlayMedia("plugin://plugin.video.cobra/?mode=?get_search_term2&amp;media_type=movie&amp;query=%s")'%que(name))

        else:
            xbmc.executebuiltin('PlayMedia("plugin://plugin.video.cobra/?mode=?get_search_term2&amp;media_type=tv&amp;query=%s")'%que(name))
def resolve_link(url,id,plot,name1,icon,fan):

    if '%%%' in url:
        regex='\[\[(.+?)\]\]'
        match2=re.compile(regex).findall(url)
        if len(match2)>0:
           
            url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
        url=url.split('%%%')[0]
        url_id=url

        fixed_name= bytes(name1, 'utf-8').decode('utf-8', 'ignore')

        url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=40&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url_id,'1','%20','%20',que(fixed_name),id,fan,url_id,icon,que(fixed_name),plot,'',name1,name1)

    return url

def play_link_db(name,url,video_info,id,icon,fan,plot,source=False):
    try:
        all_data=json.loads(video_info)

        OriginalTitle=''
        try:
            try:
                OriginalTitle=all_data['originaltitle']
            except:
                OriginalTitle=all_data['OriginalTitle']
        except:pass
        year=all_data['year']
        try:
          all_data[u'mpaa']=unicode('heb')
        except:
          all_data[u'mpaa']=('heb')
    except:
        all_data={}
        all_data['title']=name
        all_data['plot']=plot
        try:
          all_data[u'mpaa']=unicode('heb')
        except:
          all_data[u'mpaa']=('heb')
    all_f_name=[]
    if 1:
       links=url.split('$$$')
       sour_pre=''
       sour=''
       all_s=[]
       for lk in links:
           f_name=''
           regex='\[\[(.+?)\]\]'
           match=re.compile(regex).findall(str(lk))
           if len(match)==0:
               if 'TEME' in lk:
                 ff_link=lk
                 f_name=lk.split('%%%')[1].split('_')[1]
                 
                 ff_link=fn.replace(match2[0],'').replace('[','').replace(']','')
                 match=[('TE',f_name)]
               else:
                    regex='//(.+?)/'
                     
                    match_ser=re.compile(regex).findall(str(lk))
            
                    if len(match_ser)>0:
                         match=[]
                         match.append((sour,match_ser[0]))
                    else:
                        match=[]
                        match.append((sour,'Direct'))
           else:
                if 'TEME' in lk:
                 #log.warning(lk)
                 ff_link=lk

                 f_name=lk.split('%%%')[1]#.split('_')[1]
                 f_name=f_name.replace('_',' ').replace('TEME','').replace('P','').replace('לולו סרטים','').replace('לולו','').replace('ת.מ','').replace('.mkv','').replace('.avi','').replace('.mp4','').replace('ת מ','').replace('WEBRip','').replace('2021','').replace('חננאל סרטים','')
                 
                 plot=plot.replace('TEME','')
                 # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', plot)))
                 # if not source:
                     # if '1080' not in f_name and ' ' in plot  :
                      # continue
                 match=[('TE',f_name.replace('%20',' '))]
                 
                else:
                    regex='\[\[(.+?)\]\].+?//(.+?)/'
                    match=re.compile(regex).findall(str(lk))
                if len(match)==0:
                    if 'TEME' in lk:
                     ff_link=lk
                     f_name=lk.split('%%%')[1].split('_')[1]
                     
                     match=[('TE',f_name)]
                     
                    else:
                        regex='\[\[(.+?)\]\]'
                        sour=re.compile(regex).findall(str(lk))[0]
                        match=[]
                        match.append((sour,'Direct'))
           
           for sour,ty in match:
                all_f_name.append(f_name)
                sour=sour.replace('openload','vummo')
                ty=ty.replace('tv4kids','streamango').replace('.tk','.com').replace('dood.to','One').replace('dood.la','One').replace('dood.so','One').replace('drive.google.com','Go').replace('www.fembed.com','Xt').replace('720p','720p or 1080p')
                if 'sratim' in ty:
                    ty='str'
                all_s.append(sour.replace('TE','Tele Link')+' - [COLOR yellow]'+ty.replace('letsupload','avlts')+'[/COLOR]')

       all_s.append('Telemedia All Links')
       all_s.append('Mando 2 All Links')
       all_s.append('Torrent 2 All Links')
       ret = xbmcgui.Dialog().select("בחר", all_s)
       plugin = all_s[ret]
       if ret == -1:
       
            return
            
       if plugin =='Telemedia All Links':
         try:
            dialog = xbmcgui.DialogBusy()
            dialog.create()
         except:
           xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
         url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=15&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url,'1','%20','%20',OriginalTitle,id,icon,que(name),icon,'',que(plot),'',que(name),que(name))
         xbmc.executebuiltin('RunPlugin(%s)'%url)

       if plugin =='Mando 2 All Links':

                url='plugin://plugin.video.mando/?mode=15&iconimage=%s&fanart=%s&description=%s&url=www&name=%s&heb_name=%s&data=%s&original_title=%s&id=%s&season=%s&episode=%s&tmdbid=%s&eng_name=%s&show_original_year=%s&isr=0&fav_status=false'%(icon,fan,que(plot),que(name),que(name),year,OriginalTitle,id,'%20','%20',id,OriginalTitle,year)
                xbmc.executebuiltin('RunPlugin(%s)'%url)
       if plugin =='Torrent 2 All Links':

                url='plugin://plugin.video.thorrent/?mode=15&iconimage=%s&fanart=%s&description=%s&url=www&name=%s&heb_name=%s&data=%s&original_title=%s&id=%s&season=%s&episode=%s&tmdbid=%s&eng_name=%s&show_original_year=%s&isr=0&fav_status=false'%(icon,fan,que(plot),que(name),que(name),year,OriginalTitle,id,'%20','%20',id,OriginalTitle,year)
                xbmc.executebuiltin('RunPlugin(%s)'%url)
       if ret!=-1 and not plugin =='Telemedia All Links' and not plugin =='Mando 2 All Links' and not plugin =='Torrent 2 All Links':
         #log.warning(links)
         #log.warning(ret)
         ff_link=links[ret]
         
         regex='\[\[(.+?)\]\]'
         match2=re.compile(regex).findall(links[ret])
         if len(match2)>0:
           if 'TE' in all_s[ret]:
            
            
            ff_link=ff_link
            #log.warning('ff_link2:'+ff_link)
           if 'http' in ff_link or 'TE' in all_s[ret]:
            ff_link=ff_link.replace(match2[0],'').replace('[','').replace(']','')
           else:
            ff_link=ff_link.replace(match2[0],'')
         else:
            try:
                if 'http' in ff_link:
                    ff_link=ff_link.replace(match2[0],'').replace('[','').replace(']','')
                else:
                    ff_link=ff_link.replace(match2[0],'')
            except:
                pass
         # log.warning('ff_link:'+ff_link)
        
         if 'TE' in all_s[ret]:
            
            
            heb_name=all_f_name[ret]
            saved_name=all_f_name[ret]
            original_title=all_f_name[ret]
            season='%20'
            
         url=ff_link.strip()
       else:
         sys.exit()
    else:
        regex='\[\[(.+?)\]\]'
        match2=re.compile(regex).findall(url)
        if len(match2)>0:
            
            url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
    o_url=url
    try:
        dialog = xbmcgui.DialogBusy()
        dialog.create()
    except:
       xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    url=resolve_link(o_url,id,all_data['plot'],name,icon,fan)
    xbmc.executebuiltin('RunPlugin(%s)'%url)
def c_get_one_trk_epinfo(color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image):
          
          global all_data_imdb
          import _strptime
          import requests
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
                  color_ep='magenta'
                  next_ep=time.strftime( "%Y-%m-%d",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d')))
                else:
                  
                  next_ep=time.strftime( "%Y-%m-%d",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
              else:
                next_ep=0
              # dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              dates=next_ep
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
                  next=time.strftime( "%Y-%m-%d",a)
                  
               else:
                  next=''
                 
          except Exception as e:
              import linecache,sys
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              #log.warning('Error :'+ heb_name)
              #log.warning('Error :'+ str(e) +',line no:'+str(lineno))
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
            add_p=''
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n=next#'[COLOR tomato][I]פרק הבא ישודר ב ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]פרק הבא ישודר ב ' +' לא ידוע עדיין '+'[/I][/COLOR]\n'

                next='???'
          
          added_txt=' עונה %s פרק %s '%(season,episode)

          return data_ep,dates,fanart,color,next,color,(f_name+' '+added_txt+' '+next),url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx
def get_one_trk(color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image):
    global all_data_imdb
    
    data_ep,dates,fanart,color,next,color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx=cache.get(c_get_one_trk_epinfo,999,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image, table='posters')
    all_data_imdb.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
    
    return data_ep,dates,fanart,color,next
class ContextMenu_new_ep(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID, menu,icon,fan,txt):
        FILENAME='info_ep.xml'
        return super(ContextMenu_new_ep, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID, menu,icon,fan,txt):
        global playing_text,selected_index
        #log.warning('Init')
        super(ContextMenu_new_ep, self).__init__()
        self.menu = menu
        self.auto_play=0
        selected_index=-1
        self.params    = 666666
        self.imagecontrol=101
        # self.bimagecontrol=5001
        # self.txtcontrol=2
        self.tick_label=6001
        self.icon=icon
        self.fan=fan
        self.text=txt
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


    def fill_table(self,all_his_links):
        #log.warning('Start Fill')
        count=0
        self.paramList = []
        all_liz_items=[]
        # try:
        for item in self.menu:
            count+=1
            self.paramList.append(item[6])
            title =item[0]
            season='עונה '+item[1]
            episode='פרק '+item[2]
            icon=item[3]
            fanart=item[4]
            plot=item[5]
            date_episode=item[6]
            Addon.setSetting('noteid',str(date_episode))
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('season', season)
            liz.setProperty('episode',episode)
            liz.setProperty('plot', plot)
            liz.setProperty('image',icon)
            all_liz_items.append(liz)
        self.list.addItems(all_liz_items)
        
        self.setFocus(self.list)
        # except Exception as e:
            # log.warning('Fill error:'+str(e))
        self.setFocusId(self.dismiss)
    def onInit(self):
        self.dismiss     = 3001
        self.nevershow     = 3002

        all_his_links=[]
        t = Thread(target=self.fill_table, args=(all_his_links,))
        t.start()
        line   = 38
        spacer = 20
        delta  = 0 

        nItem = len(self.menu)
        if nItem > 16:
            nItem = 16
            delta = 1
        self.getControl(self.imagecontrol).setImage(self.fan)
        self.getControl(self.tick_label).setLabel(str(self.text)+str(' פרקים חדשים יצאו'))

        height = (line+spacer) + (nItem*line)
        height=570
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
        if controlId == 3002:

            Addon.setSetting('show_ep2','false')

            self.close()
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
        # Addon.setSetting('notify','false')
    def close_now(self):
        global done1_1
        #log.warning('Close:8')
        self.params = 888
        self.done=1
        # xbmc.executebuiltin( "Action(Fullscreen)" )
        # xbmc.sleep(1000)
        #log.warning('Close now CLosing')
        done1_1=3
        self.close()
    def onFocus(self, controlId):
        pass
class ContextMenu_new_vip(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID, menu,icon,fan,txt):
        FILENAME='info_movie.xml'
        return super(ContextMenu_new_vip, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID, menu,icon,fan,txt):
        global playing_text,selected_index
        #log.warning('Init')
        super(ContextMenu_new_vip, self).__init__()
        self.menu = menu
        self.auto_play=0
        selected_index=-1
        self.params    = 666666
        self.imagecontrol=101
        # self.bimagecontrol=5001
        # self.txtcontrol=2
        self.tick_label=6001
        self.icon=icon
        self.fan=fan
        self.text=txt
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


    def fill_table(self,all_his_links):
        #log.warning('Start Fill')
        count=0
        self.paramList = []
        all_liz_items=[]
        # try:
        for item in self.menu:
            count+=1
            self.paramList.append(item[6])
            title =item[0]
            season=item[1]
            episode=item[2]
            icon=item[3]
            fanart=item[4]
            plot=item[5]
            date_episode=item[6]
            # year=item[7]
            seperit=item[7]
            # Addon.setSetting('noteid',date_episode)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('season', str(season))
            liz.setProperty('episode',episode)
            liz.setProperty('plot', plot)
            liz.setProperty('image',icon)
            # liz.setProperty('year',year)
            liz.setProperty('seperit',seperit)
            all_liz_items.append(liz)
        self.list.addItems(all_liz_items)
        
        self.setFocus(self.list)
        # except Exception as e:
            # log.warning('Fill error:'+str(e))
        self.setFocusId(self.dismiss)
    def onInit(self):
        self.dismiss     = 3001
        self.nevershow     = 3002
        all_his_links=[]

        t = Thread(target=self.fill_table, args=(all_his_links,))
        t.start()


        line   = 38
        spacer = 20
        delta  = 0 

        nItem = len(self.menu)
        if nItem > 16:
            nItem = 16
            delta = 1
        try:
            self.getControl(self.imagecontrol).setImage(self.fan)
        except:pass
        self.getControl(self.tick_label).setLabel(str(self.text)+str(' תכנים חדשים נכנסו'))

        height = (line+spacer) + (nItem*line)
        height=570
        self.list = self.getControl(3000)
        # self.list.setHeight(height)
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
        if controlId == 3002:

            # Addon.setSetting('show_movie','false')

            self.close()
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
        # Addon.setSetting('notify','false')
    def close_now(self):
        global done1_1
        #log.warning('Close:8')
        self.params = 888
        self.done=1
        xbmc.executebuiltin( "Action(Fullscreen)" )
        xbmc.sleep(1000)
        #log.warning('Close now CLosing')
        done1_1=3
        self.close()
    def onFocus(self, controlId):
        pass
class new_update_tmdb(xbmcgui.WindowXMLDialog):
    def __new__(cls, addonID, menu,icon,fan,txt):
        # FILENAME='new_update_tmdb.xml'
        FILENAME='search_movie.xml'
        return super(new_update_tmdb, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
    def __init__(self, addonID, menu,icon,fan,txt):
        global playing_text,selected_index
        super(new_update_tmdb, self).__init__()
        self.menu = menu
        selected_index=-1
        self.params    = 666666
        self.imagecontrol=101   
        self.bimagecontrol=102   
        self.tick_label=6001
        self.icon=icon
        self.fan=fan
        self.text=txt
    def fill_table(self,all_his_links):
        all_liz_items=[]
        for item in self.menu:
            title =item[0]
            icon=item[1]
            fanart=item[2]
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('image',icon)
            all_liz_items.append(liz)
        self.list.addItems(all_liz_items)
        self.setFocus(self.list)
        self.setFocusId(self.dismiss)
    def onInit(self):
        self.dismiss     = 3000 #onfocus
        self.nevershow     = 3002
        all_his_links=[]

        self.getControl(self.imagecontrol).setImage(self.fan)
        self.getControl(self.bimagecontrol).setImage(self.icon)
        self.getControl(self.tick_label).setLabel(str(self.text))
        height=570
        self.list = self.getControl(3000)
        newY = 360 - (height/2)
        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)
        t = Thread(target=self.fill_table, args=(all_his_links,))
        t.start()
    def onAction(self, action):  
        global done1_1,selected_index
        actionId = action.getId()
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = 888
            selected_index=-1
            self.close()
        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK,ACTION_NAV_BACK]:
            self.params = 888
            selected_index=-1
            self.close()
    def onClick(self, controlId):
        global selected_index
        if controlId == 3002:
            self.close()
        if controlId != 3001:
            index = self.list.getSelectedPosition()        
            try:    
                self.params = index
            except:
                self.params = None
            selected_index=self.params
            self.close()
        else:
            selected_index=-1
            self.close()
    def onFocus(self, controlId):
        pass
def search_MoviesOnlineDates(id,name,iconimage,fanart):
    
    import random,requests
    num=random.randint(0,60000)
    all_d2=[]
    # name = name.split(':', 1)[0]
    data={'type':'td_send',
         'info':json.dumps({'@type': 'searchChatMessages','chat_id':(-1001783189378), 'query': name,'from_message_id':0,'offset':0,'limit':100, '@extra': num})
         }
    event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    counter=0
    zzz=0
    msg=False
    d_save=[]
    menu=[]
    import logging
    for items in event['messages']:  
        # logging.warning(items)
        if 'caption' in items['content']:
            msg=items['content']['caption']['text']
            msg=msg.replace('הצטרפו אלינו:','').replace('⭐⭐','').replace('ערוץ: @MoviesOnlineDates','').replace('קבוצה: @MoviesOnlineDatesChat','').replace('קבוצת הדיונים ובקשת תאריכים: @MoviesOnlineDatesChat','').replace('\n\n','\n').replace('\n\n\n','\n').replace('🇮🇱','ישראל').replace('🇺🇸','ארצות הברית').replace('✅','').replace('🎬','')
            
            if 'סרטים שצפויים להגיע החודש' in msg:
                continue
            if name not in msg:

                continue

            # regex='- (.+?) '
            # mmm=re.compile(regex).findall(msg)
            # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', mmm)))
            d_save.append((id,name))
            menu.append([msg,iconimage,fanart])

        if 'text' in items['content']:
            msg=True
            msg=items['content']['text']['text']
            
            msg=msg.replace('הצטרפו אלינו:','').replace('⭐⭐','').replace('ערוץ: @MoviesOnlineDates','').replace('קבוצה: @MoviesOnlineDatesChat','').replace('קבוצת הדיונים ובקשת תאריכים: @MoviesOnlineDatesChat','').replace('\n\n','\n').replace('\n\n\n','\n').replace('🇮🇱','ישראל').replace('🇺🇸','ארצות הברית').replace('✅','').replace('🎬','')
            if name not in msg:

                continue
            d_save.append((id,name))
            
            menu.append([msg,iconimage,fanart])
            
    if msg:
        menu2 = new_update_tmdb('plugin.video.telemedia', menu,iconimage,fanart,'מתי יגיע לרשת?')
        menu2.doModal()
        del menu2
        ret=selected_index
        if ret!=-1:
            id,name=d_save[ret]
            url='plugin://plugin.video.cobra/?mode=playback.media&media_type=movie&query={0}&tmdb_id={1}'.format(que(name),id)
            xbmc.executebuiltin('RunPlugin(%s)'%url)
    else:
        LogNotify("[COLOR %s]%s[/COLOR]" % ('gold', 'Anonymous TV'),'[COLOR %s]לא נמצאו תוצאות[/COLOR]' % 'white')
        
        
# def last_viewed_ep(isr=' ',run=False):

    # if run==True:
        # xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    # AUTONEXTRUN    = Addon.getSetting("next_sync")
    # from datetime import date, timedelta
    # TODAY          = date.today()
    # ONEWEEK        = TODAY + timedelta(days=7)

    # if AUTONEXTRUN <= str(TODAY):
        # next_run = ONEWEEK
        # Addon.setSetting('next_sync', str(next_run))

    # url_o='tv'
    # global all_data_imdb
    # all_data_imdb=[]
    # all_folders=[]
    # all_f_data=[]
    # match_list=[]
    # import datetime
    # from resources.modules.general import clean_name
    # try:
        # from sqlite3 import dbapi2 as database
    # except:
        # from pysqlite2 import dbapi2 as database
    # cacheFile_trk = os.path.join(user_dataDir, 'cache_play_trk.db')
    # dbcon_trk = database.connect(cacheFile_trk)
    # dbcur_trk  = dbcon_trk.cursor()
    # dbcur_trk.execute("CREATE TABLE IF NOT EXISTS %s ( ""data_ep TEXT, ""dates TEXT, ""fanart TEXT,""color TEXT,""id TEXT,""season TEXT,""episode TEXT, ""next TEXT,""plot TEXT);" % 'AllData4')
    
    # dbcon_trk.commit()
    # cacheFile=os.path.join(user_dataDir,'database.db')
    # dbcon = database.connect(cacheFile)
    # dbcur = dbcon.cursor()
    # dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
    # dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
    # dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""id TEXT, ""season TEXT, ""episode TEXT);" % 'subs')#mando ok
    # dbcon.commit()
    # all_w_trk={}
    # all_tv_w={}
    # all_movie_w={}
    # if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
        # all_w_trk,all_tv_w,all_movie_w=get_all_trakt_resume(url_o)
    # strptime = datetime.datetime.strptime
    # start_time=time.time()
    # color='white'
    # if url_o=='tv':
        # dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ")
    # else:
       # dbcur.execute("SELECT * FROM Lastepisode WHERE  type='movie'")
    # match_tv = dbcur.fetchall()
    # xxx=0
    # all_data_imdb=[]
    # thread=[]
    # for item in match_tv:
      # name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
      # dates=' '
      # next=''
      # data_ep=''
      # fanart=image
      # xxx+=1
      # done_data=0
      # if url_o=='tv' :
          # try:
              # dbcur_trk.execute("SELECT  * FROM AllData4 WHERE  id='%s' AND season='%s' AND episode='%s'"%(id,season,episode))
              # match2 = dbcur_trk.fetchone()
              # if match2!=None:
                # data_ep,dates,fanart,color,i,j,k,next,plot=match2
                # dates=json.loads(dates)
                # if color=='white' :
                    
                    # thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                    # thread[len(thread)-1].setName(clean_name(original_title,1))
                    # done_data=1
              # else:
                # thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                # thread[len(thread)-1].setName(clean_name(original_title,1))
                # done_data=1
          # except:
            # thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
            # thread[len(thread)-1].setName(clean_name(original_title,1))
            # done_data=1
      # added_txt=''
      
      # if done_data==0:
          # try:
            # f_name=unque(heb_name)
          # except:
            # f_name=name
          # if (heb_name)=='':
            # f_name=name
          # if len(heb_name)<2:
            # heb_name=name
          # if color=='peru':
            # add_p='[COLOR peru][B]סדרה זו הסתיימה או בוטלה[/B][/COLOR]'+'\n'
          # else:
            # add_p=''
          # add_n=''
          # if color=='white' and url_o=='tv' :
              # if next !='':
                # add_n=next
              # else:
                # add_n=''
                # next='???'
          # if url_o=='tv' :
            # added_txt=' עונה %s פרק %s '%(season,episode)
            
          # all_data_imdb.append((color,f_name+' '+added_txt+' '+next,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
    # for td in thread:
        # td.start()
        # # if len(thread)>38:
            # # xbmc.sleep(255)
        # # else:
            # # xbmc.sleep(10)
    # # while 1:
          # # still_alive=0
          # # all_alive=[]
          # # for yy in range(0,len(thread)):
            
            # # if  thread[yy].is_alive():
              
              # # still_alive=1
              # # all_alive.append(thread[yy].name)
          # # if still_alive==0:
            # # break
          # # xbmc.sleep(100)
    # menu=[]
    # thread=[]
    # d_save=[]
    # dateep=[]
    # count=0
    # dbcur.execute("SELECT * FROM playback ")
    # match_play = dbcur.fetchall()

    # week=Addon.getSetting('next_sync')
    # for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx in all_data_imdb:
        # heb_name=heb_name.replace('%27',"'")
        # episode=str(int(episode)+1)
        # from resources.modules.tmdb import get_episode_data
        # name,plot,image,season,episode=get_episode_data(id,season,episode)
        # if run==False:
            # if str(TODAY) not in str(dates):
                # continue
            # count+=1
            # dateep.append(str(dates))
            # menu.append([heb_name,season,episode,icon,fanart,plot,dates,''])
            # d_save.append((heb_name,year,original_title,data_ep,icon,fanart,season,episode,id))
        # else:
            # # xxxs='2021-12-05'

            # all_t_links=[]
            # for name1,tmdb1,season1,episode1,playtime1,totaltime1,free1 in match_play:
             
             # try:
                # episode1=str(int(episode1)+1)
             # except:pass
             # if id == tmdb1:
              # if season == season1:
               # if not episode == episode1:
                # continue
               # if str(TODAY) < str(dates):
                # continue
               # if float(totaltime1)==0:
                # continue
               # if str(dates)=='0':
                # continue
               # if not (int((float(playtime1)*100)/float(totaltime1)))<90 :
                # if heb_name not in all_t_links:

            # # if str(week) > str(dates):
                # # continue
                 # count+=1
                 # dateep.append(str(dates))
                 # all_t_links.append(heb_name)
                 # menu.append([heb_name,season,episode,icon,fanart,plot,dates,''])
                 # d_save.append((heb_name,year,original_title,data_ep,icon,fanart,season,episode,id))
    # xxxs='2021-09-02'
    # noteid=Addon.getSetting('noteid')
    # eps=False
    # for ep in dateep:
      # if str(TODAY) in ep:#ep:
        # eps=True

      # if noteid < ep:
          # Addon.setSetting('notify','true')
    # if Addon.getSetting("notify")=='true' and eps==True or run==True:
        # if menu==[]:
           # xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
           # LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]אין פרקים לצפיה[/COLOR]' % COLOR2)
           # sys.exit()
        # xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
        # menu2 = ContextMenu_new_ep('plugin.video.telemedia', menu,icon,fanart,int(count))
        # menu2.doModal()
        # Addon.setSetting('notify','false')
        # del menu2
        # from resources.default import search_tv
        # ret=selected_index
        # if ret!=-1:
                
                # heb_name,year,original_title,data_ep,icon,fanart,season,episode,id=d_save[ret]
                # search_tv(heb_name,year,original_title,data_ep,icon,fanart,season,episode,id,'')
    # dbcur_trk.close()
    # dbcon_trk.close()
    # dbcur.close()
    # dbcon.close()


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
original_title=None
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
read_data2=''
tmdb=''
video_info={}


try:
     url= unque(params["url"])
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
    video_info=unque(params["video_info"])
except:
        pass
episode=str(episode).replace('+','%20')
season=str(season).replace('+','%20')
# movie_notify(0,description)
if season=='0':
    season='%20'
if episode=='0':
    episode='%20'
