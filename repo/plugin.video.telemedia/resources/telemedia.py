# -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,re,xbmcplugin,sys,time,xbmcvfs,json
# from resources.modules import log#,sub
import logging
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
Addon = xbmcaddon.Addon()
addon_id=Addon.getAddonInfo('id')
addonPath = xbmc_tranlate_path(Addon.getAddonInfo("profile"))#.decode("utf-8")
addonPath2 = xbmc_tranlate_path(Addon.getAddonInfo("path"))

tmdb_data_dir = os.path.join(addonPath2, 'resources', 'tmdb_data')

COLOR2='yellow'
COLOR1='white'

ADDONTITLE='Telemedia'
DIALOG         = xbmcgui.Dialog()
global global_var,stop_all#global
global stopnext
global stopnow
stopnow=False
stopnext =False
exit_now=0
global_var=[]

from threading import Thread
import mediaurl
global nextepisode,namenextupepisode
nextepisode=''
namenextupepisode=''
domain_s='https://'
global stopbuffer
stopbuffer=False

from resources.modules import cache as  cache

from resources.modules.public import addNolink,addDir3,lang,user_dataDir,addNolink2,addLink2,addLink_db
listen_port=Addon.getSetting("port")
try:
    import urllib.parse
except:
    import urlparse
que=urllib.parse.quote_plus
url_encode=urllib.parse.urlencode
py2 = False
unque=urllib.parse.unquote_plus
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
def get_params17_18():
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
def get_params(user_params=''):
        param = dict(parse_qsl(user_params.replace('?','')))
        return param    
     

def main_menu():
    all_d=[]
    # if not os.path.exists(os.path.join(xbmc_tranlate_path("special://userdata"),"addon_data", "plugin.video.telemedia/database","td.binlog")):
    import requests
    # log.warning('Start Main')
    data={'type':'checklogin',
         'info':''
         }
    
    try:
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    except:
        xbmcgui.Dialog().ok(Addon.getLocalizedString(32052),'טלמדיה עדיין לא מחובר ... המתן קטנה')
        return ''
    # log.warning(event)
    
    all_d=[]
    if 'status' not in event:
        xbmcgui.Dialog().ok(Addon.getLocalizedString(32052),'שגיאה\n'+str(event))
        return ''

    if event['status']==2 or event['status']=='Needs to log from setting':

        addNolink( '[COLOR lightgreen]%s[/COLOR]'%Addon.getLocalizedString(32001), 'www',5,False,fan="https://www.theseanamethod.com/wp-content/uploads/2017/01/login-570317_1280.jpg", iconimage="https://achieve.lausd.net/cms/lib/CA01000043/Centricity/domain/779/welligentbuttons/login.png")
        addNolink( '[COLOR red]%s[/COLOR]'%Addon.getLocalizedString(32019), 'www',21,False,fan="https://i.ytimg.com/vi/XlzVOc21PgM/maxresdefault.jpg", iconimage="https://pbs.twimg.com/profile_images/557854031930867712/cTa_aSs_.png")
            
    else:

        aa=addDir3(Addon.getLocalizedString(32020),'0',10,'special://home/addons/plugin.video.telemedia/tele/movies.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)

        #Tv Shows
        aa=addDir3(Addon.getLocalizedString(32021),'0',11,'special://home/addons/plugin.video.telemedia/tele/tvshows.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tv Shows')
        all_d.append(aa)

        aa=addDir3('טראקט','https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,'tr'),114,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32046))
        all_d.append(aa)

        aa=addDir3(Addon.getLocalizedString(32027),'0',113,'special://home/addons/plugin.video.telemedia/tele/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Search All',last_id='0$$$0',data='all')
        all_d.append(aa)
        aa=addDir3('המשך צפיה','both',158,'special://home/addons/plugin.video.telemedia/tele/keepwatching.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','TMDB')
        all_d.append(aa)
        #My Groups
        aa=addDir3('קבוצות','0',172,'special://home/addons/plugin.video.telemedia/tele/mygroups.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','My Groups',last_id='0$$$9223372036854775807')
        all_d.append(aa)
        aa=addDir3('סרטים שלנו','movie',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        aa=addDir3('סרטים הודים','movie_hudo',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        aa=addDir3('סדרות שלנו','tvshow',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        aa=addDir3('סדרות בטורקית','tvshow_tur',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        aa=addDir3('סדרות קוריאניות','tvshow_kor',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        aa=addDir3('סדרות הודיות','tvshow_hudo',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        
        
        aa=addDir3('סדרות סיניות','tvshow_chaina',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        aa=addDir3('סדרות אנימה','tvshow_anime',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        
        aa=addDir3('סדרות לילדים שלנו','kids',254,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        all_d.append(aa)
        aa=addDir3('הצגות לילדים','www',261,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001829403114)
        
        all_d.append(aa)
        # aa=addDir3('סרטים VIP','www',213,'special://home/addons/plugin.video.telemedia/tele/keepwatching.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        # all_d.append(aa)
        # aa=addDir3('סרטים מדובבים','www',213,'special://home/addons/plugin.video.telemedia/tele/keepwatching.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        # all_d.append(aa)
        # aa=addDir3('קריוקי','www',229,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        # all_d.append(aa)
        # aa=addDir3(Student Adventures','www',176,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001857582543)
        
        # all_d.append(aa)
        # aa=addDir3('NAKED','www',176,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001903080113)
        
        # all_d.append(aa)
        # aa=addDir3('Adult Movies','www',176,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001443406210)
        
        # all_d.append(aa)
        # aa=addDir3('Adult Movies +18','www',176,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001273898511)
        
        # all_d.append(aa)
        # aa=addDir3('Collection Sex','www',176,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001371048692)

        # all_d.append(aa)
        # aa=addDir3('Хoym Video','www',176,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001488126148)

        # all_d.append(aa)
        # aa=addDir3('קריוקי טלמדיה','www',257,'https://www.sartamedia.com/public/images/logos/SartaLogo.png','https://thumbs.dreamstime.com/b/hollywood-sign-postcard-california-illustration-vintage-hollywood-cinema-logo-design-movie-hollywood-sign-postcard-california-171714267.jpg',Addon.getLocalizedString(32074),data=-1001504420275)
                
        # all_d.append(aa)
        
        
        # aa=addDir3('מבוגרים 2','www',234,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        # all_d.append(aa)
        # aa=addDir3('מבוגרים 3','www',238,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        # all_d.append(aa)
        # aa=addDir3('עידן פלוס','www',251,'special://home/addons/plugin.video.telemedia/tele/keepwatching.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        # all_d.append(aa)
        # aa=addDir3('מוסיקה','www',253,'special://home/addons/plugin.video.telemedia/tele/keepwatching.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Movies')
        # all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    addNolink( '[COLOR red][B]%s[/B][/COLOR]'%Addon.getLocalizedString(32140), 'www',174,False,fan="special://home/addons/plugin.video.telemedia/tele/tv_fanart.png", iconimage="special://home/addons/plugin.video.telemedia/tele/setting.png")

def tv_show_menu():
    import datetime
    all=[]
    now = datetime.datetime.now()
    #Popular
    # aa=addDir3('מעקב סדרות','tv',178,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/sub.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','History')
    
    # all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32057),'https://api.themoviedb.org/3/discover/tv/?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,'en'),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/popular_tv.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32057))
    # aa=addDir3(Addon.getLocalizedString(32057),'http://api.themoviedb.org/3/tv/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/popular_tv.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','TMDB')

    all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32133),'https://api.themoviedb.org/3/tv/on_the_air?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&with_original_language=en&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/on_air.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','TMDB')
    all.append(aa)
    
    
    
    # aa=addDir3('סדרות חדשות',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US&sort_by=popularity.desc&first_air_date_year='+str(now.year)+'&timezone=America%2FNew_York&include_null_first_air_ates=false&language=he&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/new_tv.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','סדרות חדשות')
    
    aa=addDir3('סדרות חדשות','https://api.themoviedb.org/3/discover/tv/?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&first_air_date_year='+str(now.year)+'&with_original_language={1}&language=he&page=1'.format(lang,'en'),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/popular_tv.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','סדרות חדשות')
    
    all.append(aa)
    aa=addDir3('בקרוב בסדרות','upcomingtv&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/years.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    all.append(aa)
    #Genre
    aa=addDir3(Addon.getLocalizedString(32048),'http://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,18,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/genre.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','TMDB')
    all.append(aa)

    aa=addDir3('כתוביות אחרונות','https://www.ktuvit.me/BrowseSeries.aspx?ResultsPerPage=100&Page=1',119,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/sub.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','כתוביות אחרונות')
    all.append(aa)
    #Years
    aa=addDir3(Addon.getLocalizedString(32049),'tv_years&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/years.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','TMDB')
    all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32134),'tv_years&page=1',101,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/network.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','TMDB')
    all.append(aa)
    aa=addDir3(Addon.getLocalizedString(32135),'https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,lang),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/israel.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32135))
    all.append(aa)
    
    #Add Turkish Tv shows
    aa=addDir3(Addon.getLocalizedString(32101),'https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,'tr'),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32046))
    all.append(aa)
    aa=addDir3('סדרות קוריאניות','https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,'ko'),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/turkish.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32046))
    all.append(aa)
    aa=addDir3('לפי שחקן','www',126,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','לפי שחקן')
    all.append(aa)

    aa=addDir3('חיפוש',str(id),167,'special://home/addons/plugin.video.telemedia/tele/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Search All',last_id='0$$$0',data='all')
    all.append(aa)
    aa=addDir3('חיפוש מדויק',str(id),201,'special://home/addons/plugin.video.telemedia/tele/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Search All',last_id='0$$$0',data='all')
    all.append(aa)
    aa=addDir3('חיפוש תוכן מתקדם','advance_tv',14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/advance.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Advance Content selection')
    
    all.append(aa)

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
def movies_menu():
    all_d=[]

    aa=addDir3(Addon.getLocalizedString(32131),'http://api.themoviedb.org/3/movie/now_playing?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/cinema.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')

    all_d.append(aa)
    
    # 'Popular Movies'
    aa=addDir3(Addon.getLocalizedString(32047),'http://api.themoviedb.org/3/movie/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/popular.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    all_d.append(aa)
    # 'Popular Movies'
    aa=addDir3(Addon.getLocalizedString(32049),'movie_years&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/years.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    aa=addDir3('בקרוב בסרטים','upcoming&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/years.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    all_d.append(aa)
    aa=addDir3('כתוביות אחרונות','www',120,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/sub.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','כתוביות אחרונות')
    all_d.append(aa)

    aa=addDir3('הסרטים החמים','http://api.themoviedb.org/3/trending/movie/week?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/hot.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    all_d.append(aa)
    #Genre
    aa=addDir3('סרטים ישראלים','https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format(lang,lang),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/israel.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32135))
    all_d.append(aa)
    aa=addDir3('סרטים הודים','https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language={0}&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language={1}&page=1'.format('he','hi'),14,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/israel.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32135))
    all_d.append(aa)
    aa=addDir3(Addon.getLocalizedString(32048),'http://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%lang,18,'special://home/addons/plugin.video.telemedia/tele/Movies/genre.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    all_d.append(aa)
    #Years
    aa=addDir3(Addon.getLocalizedString(32049),'movie_years&page=1',14,'special://home/addons/plugin.video.telemedia/tele/Movies/years.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    all_d.append(aa)
    aa=addDir3(Addon.getLocalizedString(32132),'movie_years&page=1',112,'special://home/addons/plugin.video.telemedia/tele/Movies/studio.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Tmdb')
    all_d.append(aa)

    aa=addDir3('כל אוספי הסרטים','0',121,'special://home/addons/plugin.video.telemedia/tele/Movies/collection.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','מארזי סרטים')
    all_d.append(aa)
    aa=addDir3('לפי שחקן','www',126,'special://home/addons/plugin.video.telemedia/tele/Tv_Show/actor.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','לפי שחקן')
    all_d.append(aa)

    aa=addDir3('חיפוש',str(id),167,'special://home/addons/plugin.video.telemedia/tele/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Search All',last_id='0$$$0',data='all')
    all_d.append(aa)
    
    aa=addDir3('חיפוש תוכן מתקדם','advance_movie',14,'special://home/addons/plugin.video.telemedia/tele/Movies/movie_search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Advance Content selection')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def groups_menu():
        all_d=[]
        anonymous = xbmcaddon.Addon('plugin.program.Anonymous')
        dragon=anonymous.getSetting('dragon')
        aa=addDir3(Addon.getLocalizedString(32022),'chatListMain',12,'special://home/addons/plugin.video.telemedia/tele/mygroups.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','My Groups',last_id='0$$$9223372036854775807')
        all_d.append(aa)
        aa=addDir3(Addon.getLocalizedString(32138),'chatListArchive',12,'special://home/addons/plugin.video.telemedia/tele/archive.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','My Groups',last_id='0$$$9223372036854775807')
        all_d.append(aa)
        aa=addDir3(Addon.getLocalizedString(32141),'chatListArchive',175,'special://home/addons/plugin.video.telemedia/tele/folder.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','My Folders')
        all_d.append(aa)
        if dragon =='true':
            aa=addDir3('סדרות טורקי','www',33,'special://home/addons/plugin.video.telemedia/tele/info.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32079))
            all_d.append(aa)
        aa=addDir3('סדרות טורקי 2','www',269,'special://home/addons/plugin.video.telemedia/tele/info.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32079))
        all_d.append(aa)
        aa=addDir3('הוסף מאגר קבוצות','www',132,'special://home/addons/plugin.video.telemedia/tele/add_groups.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png',Addon.getLocalizedString(32127))
        
        all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def tv_neworks():
    all_d=[]
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'
    aa=addDir3('[COLOR lightblue]Disney+[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2739&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://lumiere-a.akamaihd.net/v1/images/image_308e48ed.png','https://allears.net/wp-content/uploads/2018/11/wonderful-world-of-animation-disneys-hollywood-studios.jpg','Disney')
    all_d.append(aa)
    aa=addDir3('[COLOR blue]Apple TV+[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2552&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://ksassets.timeincuk.net/wp/uploads/sites/55/2019/03/Apple-TV-screengrab-920x584.png','https://www.apple.com/newsroom/videos/apple-tv-plus-/posters/Apple-TV-app_571x321.jpg.large.jpg','Apple')
    all_d.append(aa)
    aa=addDir3('[COLOR red]NetFlix[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=213&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://art.pixilart.com/705ba833f935409.png','https://i.ytimg.com/vi/fJ8WffxB2Pg/maxresdefault.jpg','NetFlix')
    all_d.append(aa)
    aa=addDir3('[COLOR gray]HBO[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=49&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://filmschoolrejects.com/wp-content/uploads/2018/01/hbo-logo.jpg','https://www.hbo.com/content/dam/hbodata/brand/hbo-static-1920.jpg','HBO')
    all_d.append(aa)
    aa=addDir3('[COLOR lightblue]CBS[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=16&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://cdn.freebiesupply.com/logos/large/2x/cbs-logo-png-transparent.png','https://tvseriesfinale.com/wp-content/uploads/2014/10/cbs40-590x221.jpg','HBO')
    all_d.append(aa)
    aa=addDir3('[COLOR purple]SyFy[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=77&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://cdn.collider.com/wp-content/uploads/syfy-logo1.jpg','https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fewedit.files.wordpress.com%2F2017%2F05%2Fdefault.jpg&w=1100&c=sc&poi=face&q=85','SyFy')
    all_d.append(aa)
    aa=addDir3('[COLOR lightgreen]The CW[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=71&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://www.broadcastingcable.com/.image/t_share/MTU0Njg3Mjc5MDY1OTk5MzQy/tv-network-logo-cw-resized-bc.jpg','https://i2.wp.com/nerdbastards.com/wp-content/uploads/2016/02/The-CW-Banner.jpg','The CW')
    all_d.append(aa)
    aa=addDir3('[COLOR silver]ABC[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=2&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://logok.org/wp-content/uploads/2014/03/abc-gold-logo-880x660.png','https://i.ytimg.com/vi/xSOp4HJTxH4/maxresdefault.jpg','ABC')
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]NBC[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=6&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://designobserver.com/media/images/mondrian/39684-NBC_logo_m.jpg','https://www.nbcstore.com/media/catalog/product/cache/1/image/1000x/040ec09b1e35df139433887a97daa66f/n/b/nbc_logo_black_totebagrollover.jpg','NBC')
    all_d.append(aa)
    aa=addDir3('[COLOR gold]AMAZON[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=1024&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://g-ec2.images-amazon.com/images/G/01/social/api-share/amazon_logo_500500._V323939215_.png','https://cdn.images.express.co.uk/img/dynamic/59/590x/Amazon-Fire-TV-Amazon-Fire-TV-users-Amazon-Fire-TV-stream-Amazon-Fire-TV-Free-Dive-TV-channel-Amazon-Fire-TV-news-Amazon-1010042.jpg?r=1535541629130','AMAZON')
    all_d.append(aa)
    aa=addDir3('[COLOR green]hulu[/COLOR]',domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks=453&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i1.wp.com/thetalkinggeek.com/wp-content/uploads/2012/03/hulu_logo_spiced-up.png?resize=300%2C225&ssl=1','https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwi677r77IbeAhURNhoKHeXyB-AQjRx6BAgBEAU&url=https%3A%2F%2Fwww.hulu.com%2F&psig=AOvVaw0xW2rhsh4UPsbe8wPjrul1&ust=1539638077261645','hulu')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

def search_menu():
    all_d=[]
    all_d2=[]
    aa=addDir3('חיפוש חדש...',str(id),167,'special://home/addons/plugin.video.telemedia/tele/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Search All',last_id='0$$$0',data='all')
    all_d.append(aa)

    # aa=addLink_db('חיפוש - מתי יגיע לרשת?',' ',280,False,'special://home/addons/plugin.video.telemedia/tele/search.png','','',video_info='')
    # all_d.append(aa)
    # aa=addDir3('חיפוש תוכנית...',str(id),273,'special://home/addons/plugin.video.telemedia/tele/search.png','special://home/addons/plugin.video.telemedia/tele/tv_fanart.png','Search All',last_id='0$$$0',data='all')
    # all_d.append(aa)

    from sqlite3 import dbapi2 as database

    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
    dbcon.commit()
        
    dbcur.execute("SELECT * FROM search ORDER BY rowid DESC")
    match_search = dbcur.fetchall()

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    addNolink( '[COLOR red][I]%s[/I][/COLOR]'%'--- היסטוריית חיפוש ---', 'www',99,False,iconimage='special://home/addons/plugin.video.telemedia/tele/search_history.png',fan=fanart)
    
    for nm,fr in match_search:
        if nm=='':
           continue
        
        aa=addDir3(nm.replace('%27',"'"),url,196,'special://home/addons/plugin.video.telemedia/tele/search_history.png',fanart,nm,last_id='0$$$0',data='all')
        all_d2.append(aa)

        
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d2,len(all_d2))
    
    dbcur.close()
    dbcon.close()


def movie_db_menu():

    all_d=[]
    all_d.append(addDir3('סרטים VIP','0',214,'special://home/addons/plugin.video.telemedia/tele/Movies/popular.png','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים VIP'))
    all_d.append(addDir3('סרטים מדובבים עמודים','0',214,'special://home/addons/plugin.video.telemedia/tele/Movies/popular.png','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים'))
    all_d.append(addDir3('סרטים מדובבים אותיות','0',214,'special://home/addons/plugin.video.telemedia/tele/Movies/popular.png','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים מדובבים אותיות'))
    all_d.append(addDir3('סרטים מדובבים שנים','0',214,'special://home/addons/plugin.video.telemedia/tele/Movies/years.png','','לפי שנים'))
    all_d.append(addDir3(' סרטים מדובבים לפי א-ב','0',215,'special://home/addons/plugin.video.telemedia/tele/mygroups.png','','סרטים מדובבים'))
    all_d.append(addDir3('סרטים שנצפו','0',214,'special://home/addons/plugin.video.telemedia/tele/keepwatching.png','https://i.ytimg.com/vi/9FQgg_h_lcQ/maxresdefault.jpg','נצפו','נצפו'))
    
    all_d.append(addDir3('חפש','www',216,'special://home/addons/plugin.video.telemedia/tele/search.png','','חפש'))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

def download_data_db(force=''):
    from datetime import date, datetime, timedelta
    from pyparsing import db
    AUTONEXTRUN    = Addon.getSetting("next_update")
    AUTOFEQ        = Addon.getSetting('which_day')
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
        Addon.setSetting('next_update', str(next_run))

    if service == True or force=='true':
        from resources.default import LogNotify
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]מעדכן תוכן[/COLOR]' % COLOR2)
        name =  "dbkids"
        dataDir_db =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/')
        HOME = xbmc_tranlate_path('special://home/')
        ADDONS = os.path.join(HOME,      'addons')
        PACKAGES = os.path.join(ADDONS,    'packages')
        if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
        import urllib
        from urllib.request import urlopen
        from urllib.request import Request
        lib=os.path.join(PACKAGES, '%s_guisettings.zip' % name)
        urllib.request.urlretrieve(db,lib)


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
def heb_mov_dub(url,description):
    
    t = Thread(target=download_data_db, args=())
    t.start()
    import datetime
    page=int(url)
    from sqlite3 import dbapi2 as database
    all_w={}
    dataDir_medovavim =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube.db')
    dbcon = database.connect(dataDir_medovavim)
    dbcur = dbcon.cursor()
    
    
    dataDir_vip =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube_telemovie.db')
    dbconvip = database.connect(dataDir_vip)
    dbcurvip = dbconvip.cursor()
    
    if 'נצפו' in description:
        try:
            dbcur.execute("SELECT * FROM watched ")
        except:
            download_data_db(force='true')

            dbcur.execute("SELECT * FROM watched ")
        match = dbcur.fetchall()
        all_l=[]
        x=page
        all_array=[]
        count=0
        for name ,link,data,tmdbid,icon, image,free in match:
            all_array.append((count,name ,link,data,tmdbid,icon, image,free))
            count+=1
        all_array=sorted(all_array, key=lambda x: x[0], reverse=True)
        for count,name ,link,data,tmdbid,icon, image,free in all_array:
            if (x>=(page*30) and x<=((page+1)*30)):
                all_l.append(addLink_db(name.replace("%27","'"),link,217,False,icon,image,'',video_info=unque(data),id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),214,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
        
    elif 'שנים' in description:
        try:
            dbcur.execute("SELECT * FROM kids_movie_year ORDER BY year DESC")
        except:
            download_data_db(force='true')
            dbcur.execute("SELECT * FROM kids_movie_year ORDER BY year DESC")
        all_l=[]
        match = dbcur.fetchall()
        x=page
        for name ,link,icon, image,plot,data,tmdbid ,date_added,year in match:
            if (x>=(page*30) and x<=((page+1)*30)):
                all_l.append(addLink_db(name,link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),214,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    elif 'אותיות' in description:
        try:
            dbcur.execute("SELECT * FROM kids_movie_year ORDER BY name ASC")
        except:
            download_data_db(force='true')
            dbcur.execute("SELECT * FROM kids_movie_year ORDER BY name ASC")
        all_l=[]
        match = dbcur.fetchall()
        x=page
        for name ,link,icon, image,plot,data,tmdbid ,date_added,year in match:
            if (x>=(page*30) and x<=((page+1)*30)):
                all_l.append(addLink_db(name,link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),214,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    elif 'VIP' in description:
        try:
            dbcurvip.execute("SELECT * FROM movie_telegram_year ORDER BY year DESC")
        except:
            download_data_db(force='true')
            dbcurvip.execute("SELECT * FROM movie_telegram_year ORDER BY year DESC")
        all_l=[]
        match = dbcurvip.fetchall()
        x=page
        for name ,link,icon, image,plot,data,tmdbid ,date_added,year in match:
            if (x>=(page*30) and x<=((page+1)*30)):
                all_l.append(addLink_db(name,link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),214,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    else:
        try:
            dbcur.execute("SELECT * FROM kids_movie_ordered ORDER BY date_added DESC")
        except:
            download_data_db(force='true')
            dbcur.execute("SELECT * FROM kids_movie_ordered ORDER BY date_added DESC")
        all_l=[]
        match = dbcur.fetchall()
        x=page
        all_data_in=[]
        for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
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
            all_data_in.append((name ,link,icon, image,plot,data,tmdbid ,new_date))
        all_data_in=sorted(all_data_in, key=lambda x: x[7], reverse=True)
        for name ,link,icon, image,plot,data,tmdbid ,date_added in all_data_in:
            if (x>=(page*30) and x<=((page+1)*30)):
                all_l.append(addLink_db(name,link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),214,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def heb_mov(url,description):
    import datetime
    
    page=int(url)

    from sqlite3 import dbapi2 as database

    all_w={}
    dataDir_movieil =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube_m.db')
    dbcon = database.connect(dataDir_movieil)
    dbcur = dbcon.cursor()

    if 'נצפו' in description:
        all_l=[]
        all_l.append(addDir3('חיפוש','www',212,'special://home/addons/plugin.video.telemedia/tele/search.png','','חיפוש'))

        dbcur.execute("SELECT * FROM watched ")
    
        match = dbcur.fetchall()
        
        x=page
        all_array=[]
        count=0
        for name ,link,data,tmdbid,icon, image,free in match:
            all_array.append((count,name ,link,data,tmdbid,icon, image,free))
            count+=1
        all_array=sorted(all_array, key=lambda x: x[0], reverse=True)
        for count,name ,link,data,tmdbid,icon, image,free in all_array:
            if (x>=(page*50) and x<=((page+1)*50)):
                all_l.append(addLink_db(name.replace("%27","'"),link,217,False,icon,image,'',video_info=unque(data),id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),219,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))

    elif 'שנים' in description:
        all_l=[]
        all_l.append(addDir3('חפש','www',212,'special://home/addons/plugin.video.telemedia/tele/search.png','','חפש'))
        # dbcur.execute("SELECT * FROM movie_year ORDER BY year DESC")
        dbcur.execute("SELECT * FROM movie ORDER BY name DESC3")
        match = dbcur.fetchall()
        x=page
        for name ,link,icon, image,plot,data,tmdbid ,date_added,year in match:
            if (x>=(page*50) and x<=((page+1)*50)):
                all_l.append(addLink_db(name,link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),219,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    else:
        all_l=[]
        all_l.append(addDir3('חפש','www',212,'special://home/addons/plugin.video.telemedia/tele/search.png','','חפש'))
        dbcur.execute("SELECT * FROM movie_ordered ORDER BY date_added DESC")
        
        match = dbcur.fetchall()
        x=page
        all_data_in=[]
        for name ,link,icon, image,plot,data,tmdbid ,date_added in match:
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
            if (x>=(page*50) and x<=((page+1)*50)):
            
                all_l.append(addLink_db(name,link,217,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w))
            x+=1
        all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),219,'special://home/addons/plugin.video.telemedia/tele/next.png','',description))
    
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def movie_prodiction():
    all_d=[]
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'
   
    
    aa=addDir3('[COLOR red]Marvel[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=7505&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://yt3.ggpht.com/a-/AN66SAwQlZAow0EBMi2-tFht-HvmozkqAXlkejVc4A=s900-mo-c-c0xffffffff-rj-k-no','https://images-na.ssl-images-amazon.com/images/I/91YWN2-mI6L._SL1500_.jpg','Marvel')
    all_d.append(aa)
    aa=addDir3('[COLOR lightblue]DC Studios[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=9993&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://pmcvariety.files.wordpress.com/2013/09/dc-comics-logo.jpg?w=1000&h=563&crop=1','http://www.goldenspiralmedia.com/wp-content/uploads/2016/03/DC_Comics.jpg','DC Studios')
    all_d.append(aa)
    aa=addDir3('[COLOR lightgreen]Lucasfilm[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=1&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://fontmeme.com/images/lucasfilm-logo.png','https://i.ytimg.com/vi/wdYaG3o3bgE/maxresdefault.jpg','Lucasfilm')
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]Warner Bros.[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=174&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://looking.la/wp-content/uploads/2017/10/warner-bros.png','https://cdn.arstechnica.net/wp-content/uploads/2016/09/warner.jpg','SyFy')
    all_d.append(aa)
    aa=addDir3('[COLOR blue]Walt Disney Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=2&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i.ytimg.com/vi/9wDrIrdMh6o/hqdefault.jpg','https://vignette.wikia.nocookie.net/logopedia/images/7/78/Walt_Disney_Pictures_2008_logo.jpg/revision/latest?cb=20160720144950','Walt Disney Pictures')
    all_d.append(aa)
    aa=addDir3('[COLOR skyblue]Pixar[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=3&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://elestoque.org/wp-content/uploads/2017/12/Pixar-lamp.png','https://wallpapercave.com/wp/GysuwJ2.jpg','Pixar')
    all_d.append(aa)
    aa=addDir3('[COLOR deepskyblue]Paramount[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=4&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://upload.wikimedia.org/wikipedia/en/thumb/4/4d/Paramount_Pictures_2010.svg/1200px-Paramount_Pictures_2010.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/a/a1/Paramount_Pictures_logo_with_new_Viacom_byline.jpg/revision/latest?cb=20120311200405&format=original','Paramount')
    all_d.append(aa)
    aa=addDir3('[COLOR burlywood]Columbia Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=5&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://static.tvtropes.org/pmwiki/pub/images/lady_columbia.jpg','https://vignette.wikia.nocookie.net/marveldatabase/images/1/1c/Columbia_Pictures_%28logo%29.jpg/revision/latest/scale-to-width-down/1000?cb=20141130063022','Columbia Pictures')
    all_d.append(aa)
    aa=addDir3('[COLOR powderblue]DreamWorks[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=7&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://www.dreamworksanimation.com/share.jpg','https://www.verdict.co.uk/wp-content/uploads/2017/11/DA-hero-final-final.jpg','DreamWorks')
    all_d.append(aa)
    aa=addDir3('[COLOR lightsaltegray]Miramax[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=14&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://vignette.wikia.nocookie.net/disney/images/8/8b/1000px-Miramax_1987_Print_Logo.png/revision/latest?cb=20140902041428','https://i.ytimg.com/vi/4keXxB94PJ0/maxresdefault.jpg','Miramax')
    all_d.append(aa)
    aa=addDir3('[COLOR gold]20th Century Fox[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=25&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://pmcdeadline2.files.wordpress.com/2017/03/20th-century-fox-cinemacon1.jpg?w=446&h=299&crop=1','https://vignette.wikia.nocookie.net/simpsons/images/8/80/TCFTV_logo_%282013-%3F%29.jpg/revision/latest?cb=20140730182820','20th Century Fox')
    all_d.append(aa)
    aa=addDir3('[COLOR bisque]Sony Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=34&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Sony_Pictures_Television_logo.svg/1200px-Sony_Pictures_Television_logo.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/2/20/Sony_Pictures_Digital.png/revision/latest?cb=20140813002921','Sony Pictures')
    all_d.append(aa)
    aa=addDir3('[COLOR navy]Lions Gate Films[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=35&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'http://image.wikifoundry.com/image/1/QXHyOWmjvPRXhjC98B9Lpw53003/GW217H162','https://vignette.wikia.nocookie.net/fanon/images/f/fe/Lionsgate.jpg/revision/latest?cb=20141102103150','Lions Gate Films')
    all_d.append(aa)
    aa=addDir3('[COLOR beige]Orion Pictures[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=41&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i.ytimg.com/vi/43OehM_rz8o/hqdefault.jpg','https://i.ytimg.com/vi/g58B0aSIB2Y/maxresdefault.jpg','Lions Gate Films')
    all_d.append(aa)
    aa=addDir3('[COLOR yellow]MGM[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=21&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://pbs.twimg.com/profile_images/958755066789294080/L9BklGz__400x400.jpg','https://assets.entrepreneur.com/content/3x2/2000/20150818171949-metro-goldwun-mayer-trade-mark.jpeg','MGM')
    all_d.append(aa)
    aa=addDir3('[COLOR gray]New Line Cinema[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=12&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://upload.wikimedia.org/wikipedia/en/thumb/0/04/New_Line_Cinema.svg/1200px-New_Line_Cinema.svg.png','https://vignette.wikia.nocookie.net/theideas/images/a/aa/New_Line_Cinema_logo.png/revision/latest?cb=20180210122847','New Line Cinema')
    all_d.append(aa)
    aa=addDir3('[COLOR darkblue]Gracie Films[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=18&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://i.ytimg.com/vi/q_slAJmZBeQ/hqdefault.jpg','https://i.ytimg.com/vi/yGofbuJTb4g/maxresdefault.jpg','Gracie Films')
    all_d.append(aa)
    aa=addDir3('[COLOR goldenrod]Imagine Entertainment[/COLOR]',domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies=23&language=he&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),14,'https://s3.amazonaws.com/fs.goanimate.com/files/thumbnails/movie/2813/1661813/9297975L.jpg','https://www.24spoilers.com/wp-content/uploads/2004/06/Imagine-Entertainment-logo.jpg','Imagine Entertainment')
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
def main_trakt():
   all_d=[]
   aa=addDir3('רשימת סרטים','movie?limit=40&page=1',116,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Lists')
   all_d.append(aa)
   aa=addDir3('רשימת סדרות','tv?limit=40&page=1',116,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Lists')
   all_d.append(aa)
   import datetime
   current_date = adjusted_datetime()
   start = (current_date - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
   finish = 14
        
   aa=addDir3('לוח שידורים','calendars/my/shows/%s/%s?limit=40&page=1'%(start,finish),117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Lists')
   all_d.append(aa)
   aa=addDir3('התקדמות','users/me/watched/shows?extended=full&limit=40&page=1',115,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Progress')
   all_d.append(aa)
   aa=addDir3('פרקים לצפיה','sync/watchlist/episodes?extended=full&limit=40&page=1',115,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Episodes')
   all_d.append(aa)
   aa=addDir3('סדרות לצפיה','users/me/watchlist/episodes?extended=full&limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Series')
   all_d.append(aa)
   aa=addDir3('מארז סדרות','users/me/collection/shows?limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','TV')
   all_d.append(aa)
   aa=addDir3('תוכניות לצפיה','users/me/watchlist/shows?limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Shows')
   all_d.append(aa)
   aa=addDir3('סדרות מומלצות','recommendations/shows?limit=40&ignore_collected=true&page=1',185,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
   all_d.append(aa)
   
   aa=addDir3('רשימת צפיה- סרטים','users/me/watchlist/movies?limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
   all_d.append(aa)
   aa=addDir3('סרטים מומלצים','recommendations/movies?limit=40&ignore_collected=true&page=1',185,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies')
   all_d.append(aa)
   
   aa=addDir3('סרטים שנצפו','users/me/watched/movies?limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched')
   all_d.append(aa)
   aa=addDir3('תוכניות שנצפו','users/me/watched/shows?limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched shows')
   all_d.append(aa)
   aa=addDir3('אוסף סרטים','users/me/collection/movies?limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','collection')
   all_d.append(aa)
   aa=addDir3('רשימת מועדפים','users/likes/lists?limit=40&page=1',118,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Liked lists')
   all_d.append(aa)
   aa=addDir3('המשך צפיה בסרטים','sync/playback/movies?limit=40&page=1',117,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Liked lists')
   all_d.append(aa)
   
   aa=addDir3('המשך צפיה בסדרות','sync/playback/episodes?limit=40&page=1',186,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Liked lists')
   all_d.append(aa)
   
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))

def pre_searches(url,data,last_id,description,iconimage,fanart):
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)
    dbcur = dbcon.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""free TEXT);" % 'search')
    dbcon.commit()
        
    dbcur.execute("SELECT * FROM search ORDER BY rowid DESC")
    # if Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_search")=='true' and len(Addon.getSetting("firebase"))>0:
        # try:
            # all_db=read_firebase('search')
            # match_search=[]
            # for itt in all_db:
                
                # items=all_db[itt]
                # # logging.warning( 'בדיקה'+ str(items))
                # match_search.insert(0,(items['name'],items['free']))
        # except:
          # match_search = dbcur.fetchall()
          # LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, 'בעיה בסנכרון'),'[COLOR %s]מזהה ID שגוי[/COLOR]' % COLOR2)
    # else:
    match_search = dbcur.fetchall()
    
    all_d=[]
    for nm,fr in match_search:
        if nm=='':
         continue
        aa=addDir3(nm,url,196,iconimage,fanart,nm,last_id='0$$$0',data='all')
        all_d.append(aa)
    # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    addNolink( '[COLOR lightgreen]%s[/COLOR]'%Addon.getLocalizedString(32093), 'www',37,False,fan="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/056c5ee1-35c4-4088-bd42-056e3d29a49f/d6r6rsf-a10be578-9677-4191-89f7-94421bec6656.jpg/v1/fill/w_1024,h_578,q_75,strp/gravity_clean_wallpaper_by_iiigerardoiii_d6r6rsf-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NTc4IiwicGF0aCI6IlwvZlwvMDU2YzVlZTEtMzVjNC00MDg4LWJkNDItMDU2ZTNkMjlhNDlmXC9kNnI2cnNmLWExMGJlNTc4LTk2NzctNDE5MS04OWY3LTk0NDIxYmVjNjY1Ni5qcGciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.6h7jn2BgO8JqvQjFL8g9xCNS3d4fWyaQgEVo0NUv794", iconimage="https://15logo.net/wp-content/uploads/2017/03/Clean-Home-800x800.jpg")
        
    dbcur.close()
    dbcon.close()
    
def sex():
    from resources.modules.client import get_html
    from resources.modules.public import addLink
    x=get_html('https://digit.seedhost.eu/kodi/wizard/tv/sex.m3u').content()
    
    regex='tvg-logo="(.+?)".+?group-title=.+?,(.+?)http(.+?)\n'
    m=re.compile(regex,re.DOTALL).findall(x)
    all=[]
    for im,nm,lk in m:
        url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+'http'+lk
        aa=addLink2(nm, 'http'+lk.replace('\n','').strip(),198,False,im,im,nm,place_control=True)
        all.append(aa)
    #log.warning(m)
    

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all,len(all))
    
    
def read_firebase(table_name):
    from resources.modules.firebase import firebase
    firebase = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = firebase.get('/', None)
    if table_name in result:
        return result[table_name]
    else:
        return {}
def delete_firebase(table_name,record):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = fb_app.delete(table_name, record)
    return 'OK'
def write_firebase_search(name,free,table_name):
    from resources.modules.firebase import firebase
    fb_app = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)


    result = fb_app.post(table_name, {'name':name,'free':free})
    return 'OK'
def write_search(query,free,table_name):

            all_firebase=read_firebase(table_name)
            write_fire=True
            for items in all_firebase:
                if all_firebase[items]['name']==query:
                    delete_firebase(table_name,items)
                    break
            if write_fire:
                write_firebase_search(query,free,table_name)

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
        if 'OriginalTitle' in xx:
            f_name=xx['OriginalTitle']
        else:
            f_name=xx['originaltitle']
        trailer = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s" % (tmdbid)
        all_l.append(addLink_db(name,link,256,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w,original_title=f_name,heb_name=name,trailer=trailer))
      x+=1
    all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),199,'special://home/addons/plugin.video.telemedia/tele/next.png','special://home/addons/plugin.video.telemedia/tele/next.png',description))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))

    dbcur.close()
    dbcon.close()
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
            all_l.append(addLink_db(name,link,200,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w,original_title=f_name,heb_name=name,trailer=trailer))
        x+=1
    all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),204,'special://home/addons/plugin.video.telemedia/tele/next.png','special://home/addons/plugin.video.telemedia/tele/next.png',description))

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))
    dbcur.close()
    dbcon.close()
def movie_deco(url,description):#סרטים  vip
    t = Thread(target=download_data_db, args=())
    t.start()
    import datetime
    page=int(url)
    try:
        from sqlite3 import dbapi2 as database
    except:
        from pysqlite2 import dbapi2 as database
    all_w={}
    cacheFile=os.path.join(user_dataDir,'database.db')
    dbcon = database.connect(cacheFile)

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
        all_l.append(addLink_db(name,link,200,False,icon,image,plot,video_info=data,id=tmdbid,all_w=all_w,original_title=f_name,heb_name=name,trailer=trailer))
      x+=1
    all_l.append(addDir3('[COLOR yellow]עמוד הבא[/COLOR]',str(int(page)+1),206,'special://home/addons/plugin.video.telemedia/tele/next.png','special://home/addons/plugin.video.telemedia/tele/next.png',description))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_l,len(all_l))

    dbcur.close()
    dbcon.close()

def resolve_link(url,id,plot,name1,icon,fan):

    if '%%%' in url:
        regex='\[\[(.+?)\]\]'
        match2=re.compile(regex).findall(url)
        if len(match2)>0:
           
            url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
        url=url.split('%%%')[0]
        url_id=url
        fixed_name= bytes(name1, 'utf-8').decode('utf-8', 'ignore')

        
        url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=40&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url_id,'1','%20','%20',original_title,id,fan,url_id,icon,que(fixed_name),que(plot),'',que(name1),que(name1))

    return url

def play_link_db1(name,url,video_info,id,icon,fan,plot,source=False):
    # all_data=json.loads(video_info)
    url=url.replace('[[TE]]','')
    video_data={}
    video_data['title']=name
    video_data['poster']=fan
    video_data['icon']=icon
    video_data['original_title']=name
    video_data['plot']=plot
    video_data[u'mpaa']=('heb')
    listItem = xbmcgui.ListItem(video_data['title'], path=url) 
    listItem.setInfo(type='Video', infoLabels=video_data)
    # ok=xbmc.Player().play(url,windowed=False)
    ok=xbmc.Player().play(url,listitem=listItem,windowed=False)
def play_link_db(name,url,video_info,id,icon,fan,plot,source=False):
    
    OriginalTitle=''
    try:
        all_data=json.loads(video_info)

        
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
    if 0:
       links=url.split('$$$')
       sour_pre=''
       sour=''
       all_s=[]
       for lk in links:
        # if '$$$' in url:
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
                 f_name=f_name.replace('_',' ').replace('TEME','').replace('P','').replace('לולו סרטים','').replace('לולו','').replace('ת.מ','').replace('.mkv','').replace('.avi','').replace('.mp4','').replace('ת מ','').replace('WEBRip','').replace('2021','').replace('חננאל סרטים','').replace("%27","'")
                 
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
                if 'dood' in ty:
                 continue
                if 'drive.google.com' in ty:
                 continue
                if 'www.fembed.com' in ty:
                 continue
                all_f_name.append(f_name)
                sour=sour.replace('openload','vummo')
                ty=ty.replace('tv4kids','streamango').replace('.tk','.com').replace('dood.to','One').replace('dood.la','One').replace('dood.so','One').replace('drive.google.com','Go').replace('www.fembed.com','Xt').replace('720p','720p or 1080p').replace('dood.sh',name).replace('dood.ws',name).replace('Go',name)
                if 'sratim' in ty:
                    ty='str'
                all_s.append(sour.replace('TE','Tele Link')+' - [COLOR yellow]'+ty.replace('letsupload','avlts')+'[/COLOR]')

       # all_s.append('Telemedia All Links')
       # all_s.append('Mando 2 All Links')

       all_s.append('Kitana')
       all_s.append('Torrent')
       all_s.append('נגן טריילר')
       ret = xbmcgui.Dialog().select("בחר", all_s)
       plugin = all_s[ret]
       if ret == -1:
       
            # sys.exit()
            return
       if plugin =='Telemedia All Links':
         try:
            dialog = xbmcgui.DialogBusy()
            dialog.create()
         except:
           xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
         url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=15&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url,'1','%20','%20',OriginalTitle,id,fan,que(name),icon,'',que(plot),'',que(name),que(name))
         xbmc.executebuiltin('RunPlugin(%s)'%url)
       if plugin == 'Kitana':
            url='plugin://plugin.video.cobra/?mode=play_media&media_type=movie&query={0}&tmdb_id={1}'.format(que(name),id)

            xbmc.executebuiltin('RunPlugin(%s)'%url)
            # sys.exit()
            # return 
       # if plugin =='Mando 2 All Links':
                
                # url='plugin://plugin.video.mando/?mode=15&iconimage=%s&fanart=%s&description=%s&url=www&name=%s&heb_name=%s&data=%s&original_title=%s&id=%s&season=%s&episode=%s&tmdbid=%s&eng_name=%s&show_original_year=%s&isr=0&fav_status=false'%(icon,fan,que(plot),que(name),que(name),year,OriginalTitle,id,'%20','%20',id,OriginalTitle,year)
                # xbmc.executebuiltin('RunPlugin(%s)'%url)
       if plugin =='Torrent':

                url='plugin://plugin.video.thorrent/?mode=15&iconimage=%s&fanart=%s&description=%s&url=www&name=%s&heb_name=%s&data=%s&original_title=%s&id=%s&season=%s&episode=%s&tmdbid=%s&eng_name=%s&show_original_year=%s&isr=0&fav_status=false'%(icon,fan,que(plot),que(name),que(name),year,OriginalTitle,id,'%20','%20',id,OriginalTitle,year)
                xbmc.executebuiltin('RunPlugin(%s)'%url)
       if plugin =='נגן טריילר':

                xbmc.executebuiltin('RunPlugin(%s)'%url)
                url = "plugin://plugin.video.telemedia?mode=171&url=www&id=%s&tv_movie=movie&plot=play_now" % (id)
                xbmc.executebuiltin('RunPlugin(%s)'%url)
       if ret!=-1 and not plugin =='Telemedia All Links' and not plugin =='Mando 2 All Links' and not plugin =='Torrent' and not plugin =='Kitana' and not plugin =='נגן טריילר':
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
        try:
                dialog = xbmcgui.DialogBusy()
                dialog.create()
        except:
               xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        regex='\[\[(.+?)\]\]'
        match2=re.compile(regex).findall(url)
        if len(match2)>0:
           
            url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
    o_url=url
    # log.warning('Resolveurl now33:'+o_url)
    try:
        if '[' not in o_url and not 'shift8web' in o_url and 't.me' not in o_url and 'tv4kids' not in o_url :
                
                try:
                        dialog = xbmcgui.DialogBusy()
                        dialog.create()
                except:
                       xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
            
                o_url=o_url.replace('%20','')#.replace('https://dood.so','https://dood.to')
                if 'https://dood' in url:
                        from mediaurl import resolve_doodstream
                        url=url.replace('dood.to','doodstream.com').replace('dood.so','doodstream.com').replace('dood.so','doodstream.com').replace('dood.cx','doodstream.com').replace('%20','')
                        url=resolve_doodstream(url)
                else:
                    url=url.replace('https://dood.so','https://dood.to').replace('%20','')
                    import resolveurl
                    url =resolveurl .HostedMediaFile (url =url ).resolve ()#line:2687

        else:
            
            try:
                    dialog = xbmcgui.DialogBusy()
                    dialog.create()
            except:
                   xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
            url=resolve_link(o_url,id,all_data['plot'],name,icon,fan)
    except:
         url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=15&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url,'1','%20','%20',OriginalTitle,id,fan,que(name),icon,'',que(plot),'',que(name),que(name))
         xbmc.executebuiltin('RunPlugin(%s)'%url)
    
    listItem = xbmcgui.ListItem(all_data['title'], path=url) 
    listItem.setInfo(type='Video', infoLabels=all_data)
    if 'telemedia' in url:
        xbmc.executebuiltin('RunPlugin(%s)'%url)
    else:
      
        listItem.setProperty('IsPlayable', 'true')

        ok=xbmc.Player().play(url,listitem=listItem,windowed=False)
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
def play_link_kids(name,url,video_info,id,icon,fan,plot):
    # log.warning(url)
  # try:
    
    
    from sqlite3 import dbapi2 as database

    dataDir_medovavim =(xbmc_tranlate_path("special://userdata/addon_data/") + 'db/youtube.db')
    dbcon = database.connect(dataDir_medovavim)
    dbcur = dbcon.cursor()
    
    if 'tv_title' in video_info:
        table_name='last_played_tv'
    else:
        table_name='last_played_movie'
    
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%table_name )
    dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""url TEXT,""video_info TEXT,""id TEXT,""icon TEXT,""fan TEXT,""free TEXT);"%'watched' )
    
    dbcur.execute("DELETE FROM "+table_name)
    
    try:
        dbcur.execute("INSERT INTO %s Values ('%s','%s','%s','%s','%s','%s','%s')"%(table_name,name.replace("'","%27"),url,que(video_info),id,icon,fan,plot.replace("'","%27")))
    except:pass
    
    dbcur.execute("SELECT * FROM watched ")
    all_w=[]
    match = dbcur.fetchall()
    all_nw=[]
    for name_w ,link_w,data_w,tmdbid_w,icon_w, image_w,free_w in match:
        all_nw.append(name_w)
    if name.replace("'","%27") not in all_nw and name not in all_nw:
       try:
        dbcur.execute("INSERT INTO watched Values ('%s','%s','%s','%s','%s','%s','%s')"%(name.replace("'","%27"),url,que(video_info),id,icon,fan,plot.replace("'","%27")))
       except:pass
    dbcon.commit()
    dbcur.close()
    dbcon.close()

    try:
        all_data=json.loads(video_info)
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
    OriginalTitle=''
    try:
        try:
            OriginalTitle=all_data['originaltitle']
        except:
            OriginalTitle=all_data['OriginalTitle']
    except:pass
    if OriginalTitle=='':
      OriginalTitle=name
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
                 # log.warning(lk)
                 ff_link=lk
                 f_name=lk.split('%%%')[1].split('_')[1]
                 
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
                sour=sour.replace('openload','vummo').replace('Oren','VIP').replace('TE','TELEMEDIA').replace('RAM','VIP')
                if 'seedhost' in ty:
                    ty='BOT'
                ty=ty.replace('ANVIP','AN-VIP').replace('tv4kids','4TV').replace('.tk','.com').replace('dood.to','TeleBot').replace('dood.la','TeleBot').replace('dood.so','TeleBot').replace('dood.sh','TeleBot').replace('dood.ws','TeleBot').replace('drive.google.com','GDRIVE').replace('www.fembed.com','TeleBot')
                if 'sratim' in ty:
                    ty='str'
                all_s.append('[COLOR lightblue][B]'+sour+'[/B][/COLOR] - [COLOR white]'+ty.replace('letsupload','avlts')+'[/COLOR]')
                

       all_s.append('[COLOR lightblue][B]'+'Telemedia - כל המקורות'+'[/B][/COLOR]')
       ret = xbmcgui.Dialog().select("בחר", all_s)
       plugin = all_s[ret]

       if ret == -1:
            
            sys.exit()
       if plugin =='[COLOR lightblue][B]'+'Telemedia - כל המקורות'+'[/B][/COLOR]':

         xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
               
         icon=icon.replace("'",'').replace("bhttps",'https')
         url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=15&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url,'1','%20','%20',OriginalTitle,id,fan,que(name),icon,'',que(plot),'',que(name),que(name))
         xbmc.executebuiltin('RunPlugin(%s)'%url)

       if ret!=-1 and not plugin =='[COLOR lightblue][B]'+'Telemedia - כל המקורות'+'[/B][/COLOR]':

         xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
         ff_link=links[ret]
        
         regex='\[\[(.+?)\]\]'
         match2=re.compile(regex).findall(links[ret])
         if len(match2)>0:
           if 'TE' in all_s[ret]:
            
            
            ff_link=ff_link
            # log.warning('ff_link2:'+ff_link)
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

        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        regex='\[\[(.+?)\]\]'
        match2=re.compile(regex).findall(url)
        if len(match2)>0:
            
            url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
    o_url=url
    # log.warning('Resolveurl now33:'+o_url)
    try:
    # import logging
    # logging.warning('Resolveurl now33:'+o_url)
        if '[' not in o_url and not 'shift8web' in o_url and 't.me' not in o_url and 'tv4kids' not in o_url and 'seedhost' not in o_url and 'videopress.com' not in o_url : 
                

                xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
            
                o_url=o_url.replace('%20','')#.replace('https://dood.so','https://dood.to')
                if 'https://dood' in url:
                        from resources.default import resolve_doodstream
                        url=url.replace('dood.to','doodstream.com').replace('dood.so','doodstream.com').replace('dood.so','doodstream.com').replace('dood.cx','doodstream.com').replace('%20','')
                        url=resolve_doodstream(url)
                else:
                    # log.warning('11111111:'+str(url))
                    url=url.replace('https://dood.so','https://dood.to').replace('%20','')
                    path=xbmc_tranlate_path('special://home/addons/script.module.resolveurl/lib')
                    sys.path.append( path)
                    path=xbmc_tranlate_path('special://home/addons/script.module.six/lib')
                    sys.path.append( path)
                    path=xbmc_tranlate_path('special://home/addons/script.module.kodi-six/libs')
                    sys.path.append( path)
                    
                    
                    import resolveurl

                    
                    url =resolveurl .HostedMediaFile (url =url ).resolve ()#line:2687
                    # log.warning('ResolveD now:'+str(url))

        else:
            xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
                   
            url=resolve_link(o_url,id,all_data['plot'],name,icon,fan)
    
    except:
         icon=icon.replace("'",'').replace("bhttps",'https')

         url='plugin://plugin.video.telemedia/?url=%s&no_subs=%s&season=%s&episode=%s&mode=15&original_title=%s&id=%s&data=&fanart=%s&url=%s&iconimage=%s&file_name=%s&description=%s&resume=%s&name=%s&heb_name=%s'%(url,'1','%20','%20',OriginalTitle,id,fan,que(name),icon,'',que(plot),'',que(name),que(name))
         xbmc.executebuiltin('RunPlugin(%s)'%url)
    listItem = xbmcgui.ListItem(all_data['title'], path=url) 
    listItem.setInfo(type='Video', infoLabels=all_data)
    listItem.setArt({'icon': icon, 'thumb': fan, 'poster': icon})
    if 'telemedia' in url:
        xbmc.executebuiltin('RunPlugin(%s)'%url)
    else:
      
        listItem.setProperty('IsPlayable', 'true')

        ok=xbmc.Player().play(url,listitem=listItem,windowed=False)
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
        # ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
    # else:
        # regex='\[\[(.+?)\]\]'
        # match2=re.compile(regex).findall(url)
        # if len(match2)>0:
            
            # url=url.replace(match2[0],'').replace('[','').replace(']','').strip()
    # o_url=url
    # try:
        # dialog = xbmcgui.DialogBusy()
        # dialog.create()
    # except:
       # xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    # url=resolve_link(o_url,id,all_data['plot'],name,icon,fan)
    # xbmc.executebuiltin('RunPlugin(%s)'%url)


movie_date=Addon.getSetting('movie_date')
if movie_date=='':
 from datetime import date
 TODAY          = date.today()
 Addon.setSetting('movie_date',str(TODAY))
def refresh_list(user_params,sys_arg_1_data,Addon_id=""):
    global elapsed_time,time_data,sys_arg_1,Addon,use_debrid,description,original_title,iconimage,fanart,dd,url,name,resume,c_id,m_id,fast_link,data,id,saved_name,prev_name,isr,no_subs,season,episode,show_original_year,groups_id,heb_name,year,tmdbid,eng_name,dates,data1,file_name,fav_status,only_torrent,only_heb_servers,new_windows_only,meliq,tv_movie,last_id,nextup,read_data2,tmdb,o_name
    params=get_params(user_params=user_params)

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
    read_data2=''
    tmdb=''
    tmdb_id=''
    video_info={}
    o_name=''
    next_page='0'
    page = 1
    watched_indicators='0'
    tag_line=''
    kitana='false'
    plot=''
    rating=''
    genre=''
    premiered=''
    clean_all=''
    module=''
    try:
        module = (params['module'])
    except:
        pass
    try:
        tag_line = (params['tag_line'])
    except:
        pass
    try:
        clean_all = (params['clean_all'])
    except:
        pass
    try:
        page = int(params['page'])
    except:
        pass
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
     
       o_name=unque(params["o_name"])
    except:
        pass
    try:        
            tmdb=(params["id"])
    except:
            pass
    try:        
            tmdb_id=(params["tmdb_id"])
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
    try:
        next_page=(params["next_page"])
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
    episode=str(episode).replace('+','%20')
    season=str(season).replace('+','%20')

    if season=='0':
        season='%20'
    if episode=='0':
        episode='%20'

    if (mode==None or url==None or len(url)<1) and len(sys.argv)>1:
            
            main_menu()
    elif mode==1:
        
        addon_id='plugin.video.idanplus'
        str_next='ActivateWindow(10025,"%s?iconimage=%s&mode=1&module=%s&moredata&name=%s&url=%s",return)'%("plugin://%s/"%addon_id,iconimage,module,name,url)
        xbmc.executebuiltin(str_next)

    elif mode==2:
        from resources.default import file_list
        file_list(url,data,last_id,description,iconimage,fanart,image_master=image_master,original_title=original_title)
    elif mode==3:
        from resources.default import play
        play(name,url,data,iconimage,fanart,no_subs,tmdb,tmdb_id,season,episode,original_title,heb_name,description,resume,dd,watched_indicators,kitana,plot,rating,genre,year,premiered,tag_line,nextup)
    elif mode==4:
        # import requests
        import requests
        data={'type':'logout',
             'info':''
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
    elif mode==5:
        # import requests
        import requests
        data={'type':'login',
             'info':''
             }
        event=requests.post('http://127.0.0.1:%s/'%listen_port,json=data).json()
        #log.warning(event)
    elif mode==6:
        from resources.default import search
        search(url,data,last_id,description,iconimage,fanart,'0','0',no_subs=0)

    elif mode==9:
        from resources.default import play_link
        play_link(name,url,iconimage,fanart,no_subs,tmdb,season,episode,original_title)

    elif mode==10:
        movies_menu()
    elif mode==11:
        tv_show_menu()
    elif mode==12:
        from resources.default import my_groups
        my_groups(last_id,url,groups_id,next_page)
    elif mode==13:
        from resources.default import search_groups
        search_groups(iconimage,fanart)
    elif mode==14:
        from resources.modules.tmdb import get_movies
        # from resources.modules.tmdb_n import tmdb as  get_movies
        get_movies(url)
    elif mode==15:
        from resources.default import search_movies
        search_movies(heb_name,original_title,data,iconimage,fanart,tmdb,season,episode)
    elif mode==16:
        # import requests
        # if 'tvdb' in id :
            # url2='https://'+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=tvdb_id&language=%s'%(id.replace('tvdb',''),lang)
            # pre_id=requests.get(url2).json()['tv_results']
            
            # if len(pre_id)>0:
                # id=str(pre_id[0]['id'])
        # elif 'imdb' in id:
            # url2='https://'+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=%s'%(id.replace('imdb',''),lang)
           
            # pre_id=requests.get(url2).json()['tv_results']
            
            # if len(pre_id)>0:
                # id=str(pre_id[0]['id'])
        from resources.modules.tmdb import get_seasons
        get_seasons(name,url,iconimage,fanart,description,data,original_title,tmdb,heb_name,isr)
    elif mode==17:
        from resources.default import ClearCache
        ClearCache()
    elif mode==18:
        from resources.default import get_genere
        get_genere(url)
    elif mode==19:
        from resources.modules.tmdb import get_episode
        get_episode(name,url,iconimage,fanart,description,data,original_title,tmdb,season,tmdbid,show_original_year,heb_name)

    elif mode==20:
        from resources.default import search_tv

        search_tv(heb_name,year,original_title,data,iconimage,fanart,season,episode,tmdb)

    elif mode==21:
        from resources.default import clear_all
        clear_all()
    elif mode==22:
        from resources.default import join_chan
        join_chan(url)
    elif mode==23:
        from resources.default import leave_chan
        leave_chan(name,url)
    elif mode==24:
        from resources.default import install_addon
        install_addon(original_title,url)
    elif mode==25:
        from resources.default import install_build
        install_build(original_title,url)
    elif mode==26:
        from resources.modules.tmdb import get_movies
        # from resources.modules.tmdb_n import tmdb as  get_movies
        get_movies(url,local=True)
    elif mode==27:
        # from resources.default import add_tv_to_db
        # add_tv_to_db(name,url,data,iconimage,fanart,description)
        sys.exit()
    elif mode==28:
        my_local_tv()
    elif mode==29:
        from resources.default import remove_my_tv
        remove_my_tv(name,url)
    elif mode==30:
        # from resources.default import pre_searches
        pre_searches(url,data,last_id,description,iconimage,fanart)
    elif mode==31:
        from resources.default import tmdb_world
        tmdb_world(last_id,iconimage,fanart,data)
    elif mode==32:
        from resources.default import install_apk
        install_apk(original_title,url)
    elif mode==33:
        from resources.default import full_data_turkey
        full_data_turkey()
    elif mode==34:
        from resources.default import add_to_databaseturkey
        add_to_databaseturkey(url,name,data,iconimage,fanart,description)
    elif mode==35:
        from resources.default import remove_databaseturkey
        remove_databaseturkey(url,name)
    elif mode==36:
        from resources.default import download_files
        download_files(original_title,url)
    elif mode==37:
        from resources.default import clear_search_h
        clear_search_h()
    elif mode==38:
        from resources.default import groups_join
        groups_join(url,iconimage,fanart)
    elif mode==39:
        from resources.default import join_group
        join_group(url)
    elif mode==40:
        from resources.default import play_remote
        play_remote(url,no_subs,season,episode,original_title,tmdb,tmdb_id,file_name,description,resume,original_title,heb_name,iconimage,fanart,watched_indicators,plot,rating,genre,year,tag_line,c_id=c_id,m_id=m_id,kitana=kitana)
    elif mode==41:
        from resources.default import upload_log
        upload_log()
    elif mode==42:
        from resources.default import join_all_groups
        join_all_groups(url)
    elif mode==43:
        from resources.default import upload_log
        upload_log(backup=True)
    elif mode==44:
        from resources.default import set_bot_id
        set_bot_id(name)
    elif mode==45:
        from resources.default import search_updates
        search_updates()
    elif mode==46:
        from resources.default import my_repo
        my_repo()
    elif mode==47:
        from resources.default import multi_install
        multi_install(name,url,original_title)
    elif mode==48:
        from resources.default import clean_space
        clean_space()
    elif mode==72: 
        from resources.default import by_actor
        by_actor(url)
    elif mode==101:
        tv_neworks()
    elif mode==112:
        movie_prodiction()
    elif mode==113:
        search_menu()
    elif mode==114:
          main_trakt()
    elif mode==115:
        from resources.modules.trakt import progress_trakt
        progress_trakt(url)
    elif mode==116:
        from resources.modules.trakt import get_trakt
        get_trakt(url)
    elif mode==117:
        from resources.modules.trakt import get_trk_data
        get_trk_data(url)
    elif mode==118:
        from resources.modules.trakt import trakt_liked
        trakt_liked(url,iconimage,fanart)
    elif mode==119:
        from resources.default import last_tv_subs
        last_tv_subs(url)
    elif mode==120:
        from resources.default import latest_subs
        latest_subs(url)
    elif mode==121:
        from resources.data import collections
        collections(url)
    elif mode==122:
        from resources.default import collection_detials
        collection_detials(url)
    elif mode==123:
        from resources.default import get_tv_maze
        get_tv_maze(url,iconimage)

    elif mode==126: #72
        from resources.default import by_actor
        by_actor(url)
    elif mode==127: #73
        from resources.default import actor_m
        actor_m(url,description)
    elif mode==128: #74
        from resources.default import search_actor
        search_actor()

    elif mode==131: #74
        from resources.default import joinpack
        joinpack()

    elif mode==134:
        from resources.default import my_repovip
        my_repovip()

    elif mode==136:
        from resources.default import groups_joinautostart
        groups_joinautostart(url,iconimage,fanart)
    elif mode==144:

       last_played()
    elif mode==158:
        from resources.data import was_i
        was_i(url)
    elif mode==159:
        from resources.default import remove_was_i
        remove_was_i(name,id,season,episode)
    elif mode==160:
        from resources.modules.trakt import remove_trk_resume
        remove_trk_resume(name,id,season,episode,data)
    elif mode==162:
        from resources.default import clear_was_i
        clear_was_i()

    elif mode==167:
        search_entered_pre=''
        
        #Enter Search
        keyboard = xbmc.Keyboard(search_entered_pre, '[COLOR blue][I]חיפוש: סרטים - סדרות - עידן פלוס - שחקנים - מדובבים - ערוצים בטלגרם[/I][/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered_pre = keyboard.getText()
        if search_entered_pre=='':
         return
         
        from resources.default import searchallinone
        
        searchallinone(url,data,last_id,search_entered_pre,iconimage,fanart,'0','0',no_subs=1)

    elif mode==168:
        from resources.default import get_cast
        get_cast(url,id,season,episode)
    elif mode==169: 
        from resources.default import actor_m
        actor_m(url,description)
    elif mode==170:
        import requests
        if 'tvdb' in id :
            url2='https://'+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=tvdb_id&language=%s'%(id.replace('tvdb',''),lang)
            pre_id=requests.get(url2).json()['tv_results']
            
            if len(pre_id)>0:
                id=str(pre_id[0]['id'])
        elif 'imdb' in id:
            
            url2='https://'+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=%s'%(id.replace('imdb',''),lang)
           
            pre_id=requests.get(url2).json()['tv_results']
            
            if len(pre_id)>0:
                id=str(pre_id[0]['id'])
        from resources.modules.tmdb import get_seasons
        
        get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr)
          
    elif mode==171:
        from resources.default import play_trailer
        play_trailer(id,url,description)

    elif mode==172:

          groups_menu()
    elif mode==173:
        from resources.default import get_version
        get_version()
    elif mode==174:
        Addon.openSettings()
    elif mode==175:
        from resources.default import get_folders
        get_folders(iconimage,fanart)
    elif mode==176:
        from resources.default import tmdb_world2
        tmdb_world2(last_id,iconimage,fanart,data)
    elif mode==177:
        from resources.default import fast_play
        fast_play(url)
         
    elif mode==178:
        
       from resources.default import read_data2,last_viewed,all_folders,url_o
        # read_data2,enc_data=last_viewed(url)
       read_data2,enc_data,all_folders,url_o=cache.get(last_viewed,24,url, table='last_view')
       # read_data2,enc_data,all_folders,url_o=last_viewed(url)
       aa=[]
       if len(all_folders)>0:
            
            from resources.modules.public import addNolink3
            for name, url,mode, icon,added_res_trakt,all_w,heb_name,fanart,data_ep,plot,original_title,id,season,episode,eng_name,watched,show_original_year,dates,dd in all_folders:
                
                aa.append(addNolink3(heb_name.replace('%27',"'"), url,mode,False, iconimage=icon,all_w_trk=added_res_trakt,all_w=all_w,heb_name=heb_name,fanart=fanart,data=data_ep,plot=plot.replace('%27',"'"),original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,watched=watched,show_original_year=show_original_year,dates=json.dumps(dates),dd=json.dumps(dd),dont_place=True))
                
            # if Addon.getSetting("trakt_access_token")!='' and url_o=='tv':
                # aa.append(addNolink3( '[COLOR blue][I]---%s---[/I][/COLOR]'%Addon.getLocalizedString(32114), id,157,False,fanart='https://bestdroidplayer.com/wp-content/uploads/2019/06/trakt-what-is-how-use-on-kodi.png', iconimage='special://home/addons/plugin.video.telemedia/tele/trakt.png',plot=' ',dont_place=True))
                
            xbmcplugin .addDirectoryItems(int(sys.argv[1]),aa,len(aa))
    elif mode==179:
        from resources.default import s_tracker
        s_tracker(name,url,iconimage,fanart,description,data,original_title,id,season,episode,show_original_year,dates,heb_name)
    elif mode==180:
        from resources.default import sync_trk
        ok=xbmcgui.Dialog().yesno("Override",('%s (%s)'%(Addon.getLocalizedString(32150),Addon.getAddonInfo('name'))))
        remove_db=False
        show_msg=True
        if ok:
            remove_db=True
            show_msg=False
        sync_trk(removedb=False,show_msg=show_msg)
        if remove_db:
            show_msg=True
            sync_trk(removedb=True,show_msg=show_msg)
    elif mode==181:
        from resources.default import remove_from_trace
        remove_from_trace(name,original_title,id,season,episode)
    elif mode==182:
        from resources.default import searchwalltv
        searchwalltv(url,data,last_id,description,iconimage,fanart,'0','0',no_subs=1)
    elif mode==183:
        from resources.default import sync_firebase
        sync_firebase()
    elif mode==184:
        from resources.default import check_firebase
        check_firebase()
    elif mode==185:
        from resources.modules.trakt import get_simple_trk_data
        get_simple_trk_data(url)
    elif mode==186:
        from resources.modules.trakt import resume_episode_list
        resume_episode_list(url)
    elif mode==187:
        from resources.modules.trakt import manager
       
        manager(name, url, data)
    elif mode==188:
        from resources.default import add_remove_trakt
        add_remove_trakt(name,original_title,id,season,episode,o_name)
    elif mode==189:
        from resources.default import clear_files,database_refresh
        if not xbmc.Player().isPlaying():
            clear_files()
        database_refresh()
        
    elif mode==190:
        from resources.default import select_file_browser
        select_file_browser()
    elif mode==191:
        from resources.default import botplaytime
        botplaytime()
    elif mode==192:
        from resources.default import dismark_movie
        dismark_movie(heb_name,original_title,tmdb)
    elif mode==193:
        from resources.default import dismark_tv
        dismark_tv(original_title,tmdb,season,episode)
    elif mode==194:
        from resources.default import mark_movie
        mark_movie(original_title,tmdb)
    elif mode==195:
        from resources.default import mark_tv
        mark_tv(original_title,tmdb,season,episode)
    elif mode==196:
        from resources.default import searchallinone
        searchallinone(url,data,last_id,description,iconimage,fanart,'0','0',no_subs=1)
    elif mode==99:

        xbmc.executebuiltin(url)
    elif mode==197:
        sex()
    elif mode==198:
        listItem = xbmcgui.ListItem(name, path=url) 
        listItem.setInfo(type='Video', infoLabels={'title':name})
        ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
    elif mode==199:
        # from resources.default import heb_mov
        movie_vip(url,description)
    elif mode==200:
        # from data import play_link_db
        play_link_db(name,url,video_info,id,iconimage,fanart,description,source=False)
    elif mode==201:
        search_entered_pre=''
        all_s=[]
        all_s2=[]
        #Enter Search
        keyboard = xbmc.Keyboard(search_entered_pre, Addon.getLocalizedString(32025))
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered_pre = keyboard.getText()
        if search_entered_pre=='':
         sys.exit()

        for year in range(1, 30):
             all_s.append(' עונה '+str(year))
        ret = xbmcgui.Dialog().select("בחר", all_s)
       
        for year in range(1, 30):
             all_s2.append(' פרק '+str(year))

        ret2 = xbmcgui.Dialog().select("בחר", all_s2)
        # plugin = all_s[ret]

        from resources.default import searchallinone
        search_entered_pre=search_entered_pre+all_s[ret]+all_s2[ret2]
        searchallinone(url,data,last_id,search_entered_pre,iconimage,fanart,'0','0',no_subs=1)
        if Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_search")=='true' and len(Addon.getSetting("firebase"))>0:
                query=search_entered_pre
                table_name='search'
                free=''
                t = Thread(target=write_search, args=(query,free,table_name,))
                t.start()
    elif mode==202:
        from resources.data import last_viewed_ep
        t = Thread(target=last_viewed_ep, args=())
        t.start()

    elif mode==203:
        from resources.default import remove_all_from_trace
        remove_all_from_trace(name,original_title,id,season,episode)
    elif mode==204:

        all_movie(url,description)
    elif mode==205:
        if Addon.getSetting("show_movie")=='true':
            from resources.data import movie_notify
            movie_notify(0,description)
    elif mode==206:

        movie_deco(url,description)
    elif mode==207:
        from resources.default import database_auto
        database_auto()
    elif mode==208:
        from resources.default import kids_key
        kids_key(url,name)
    elif mode==209:
        from resources.default import kids_key_remove
        kids_key_remove(url,name)
    elif mode==210:
        from resources.data import last_viewed_ep
        last_viewed_ep(run=True)
    elif mode==211:
        from resources.default import set_botplaytime
        set_botplaytime()
    elif mode==212:
        from resources.default import refresh_datatelegram
        t = Thread(target=refresh_datatelegram, args=())
        t.start()

    elif mode==213:
        movie_db_menu()
    elif mode==214:
        # from resources.default import heb_mov_dub
        heb_mov_dub(url,description)
    elif mode==215:
        from resources.default import heb_mov_letter
        heb_mov_letter(iconimage,fanart)
    elif mode==216:
        search_entered=''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
        keyboard.doModal()
        if keyboard.isConfirmed() :
               search_entered = (keyboard.getText().replace("'","%27"))
               if search_entered!='':
                  from resources.default import search_result
                  search_result(search_entered)
    elif mode==217:
        play_link_kids(name,url,video_info,id,iconimage,fanart,description)

    elif mode==218:
        from resources.default import heb_mov_dub_letter
        heb_mov_dub_letter(name,url)
    elif mode==219:
        # from resources.default import heb_mov
        heb_mov(url,description)
    elif mode==221:
        from resources.default import il_mov_dub
        il_mov_dub(url,description)
        
        
    elif mode==222:
        from resources.data import Satellite_1
        Satellite_1()
    elif mode==223:
        from resources.data import Satellite_2
        Satellite_2()
    elif mode==224:
        from resources.data import tv_all
        tv_all()
    elif mode==225:
        from resources.data import sport_1
        sport_1()
    elif mode==226:
        from resources.data import Satellite_5
        Satellite_5()
    elif mode==227:
        from resources.data import music_ip
        music_ip()
    elif mode==229:
        from resources.modules.kar import karaoke_menu
        karaoke_menu()
    elif mode==230:
        from resources.modules.kar import kar_search
        kar_search()
    elif mode==231:
        from resources.modules.kar import category
        category(url,iconimage,fanart)
    elif mode==232:
        from resources.modules.kar import play_link_kar
        play_link_kar(name,url)
    elif mode==234:
        from resources.modules.empflix import CATEGORIES
        CATEGORIES()
    elif mode==235:
        from resources.modules.empflix import  SORTMETHOD
        SORTMETHOD(url)
    elif mode==236:
        from resources.modules.empflix import  VIDEOLIST
        VIDEOLIST(url, page)
    elif mode==237:
        from resources.modules.empflix import  PLAYVIDEO
        PLAYVIDEO(url)
    elif mode==238:
        from resources.modules.fantasticc import  CATEGORIES
        CATEGORIES()
    elif mode==239:
        from resources.modules.fantasticc import  INDEX
        INDEX(url)
    elif mode==240:
        from resources.modules.fantasticc import  INDEXCOLLECT
        INDEXCOLLECT(url)
    elif mode==241:
        from resources.modules.fantasticc import  INDEXP
        INDEXP(url)
    elif mode==242:
        from resources.modules.fantasticc import  PLAY
        PLAY(url, iconimage)
    elif mode==243:
        from resources.modules.fantasticc import  SEARCH
        SEARCH(url)
    elif mode==244:
        from resources.modules.fantasticc import  SEARCH_RESULTS
        SEARCH_RESULTS(url)
    elif mode==247:
        from resources.modules.kar import singer
        singer()
    elif mode==248:
        from resources.data import idan
        idan()
    elif mode==249:
        from resources.data import Satellite_3
        Satellite_3()
    elif mode==250:
        from resources.data import Satellite_4
        Satellite_4()
        
    elif mode==251:
        from resources.data import idan_chan,idan_menu
        if Addon.getSetting("p_mod")=='false':
            idan_chan()
        else:
            idan_menu()
    elif mode==252:
        if '.fullChan' in description:
            url=resolve_chan(url)
            episode='0'
            season='0'
        video_data={}
        video_data[u'mpaa']=('heb')
        video_data['title']=name
        listItem = xbmcgui.ListItem(name, path=url) 
        listItem.setInfo(type='Video', infoLabels=video_data)
        ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
    elif mode==253:
        from resources.data import music_ip
        music_ip()
    elif mode==254:
        from resources.data import tmdb_upload
        tmdb_upload(url)
    elif mode==255:
        from resources.default import clean_search
        clean_search(name,clean_all)
    elif mode==256:
        # from data import play_link_db
            url='plugin://plugin.video.cobra/?mode=play_media&media_type=movie&query={0}&tmdb_id={1}'.format(que(name),id)

            xbmc.executebuiltin('RunPlugin(%s)'%url)
    elif mode==257:
        from resources.default import karaoke_tele
        karaoke_tele(last_id,data)
    elif mode==258:

        regex='[0-9]+'
        text=re.compile(regex).findall(url)
        id=text[0]
        if 'סרט' in url:
            url='plugin://plugin.video.cobra/?mode=playback.media&media_type=movie&query={0}&tmdb_id={1}'.format(que(name.replace(url,'')),id)
            xbmc.executebuiltin('RunPlugin(%s)'%url)
            # xbmc.executebuiltin('PlayMedia("plugin://plugin.video.cobra/?mode=?get_search_term2&amp;media_type=movie&amp;query=%s")'%que(name.replace(url,'')))
            
        else:
            # url='plugin://plugin.video.cobra/?mode=build_season_lis&tmdb_id={0}'.format(id)
            xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.cobra/?mode=build_season_list&tmdb_id=%s",return)'%id)   
            # xbmc.executebuiltin('ActivateWindow(10025,%s)'%url)
    elif mode==259:
        
        from resources.modules import cache
        cache.clear(['tmdblist'])
        xbmc.executebuiltin('Container.Refresh')

        

        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Anonymous TV', '[COLOR=yellow]בוצע[/COLOR]')))
    elif mode==260:
        from resources.data import update_tmdb
        update_tmdb()
    elif mode==261:
        from resources.default import kids_tvshow
        kids_tvshow(last_id,iconimage,fanart,data)
    elif mode==262:
        from resources.default import joinpack
        joinpack()
        
        
    elif mode==263:
        from resources.default import turkish_data
        turkish_data(last_id,iconimage,fanart,data)
    elif mode==264:
        from resources.default import download_data_turkey
        download_data_turkey('true')
    elif mode==265:
        search_entered=''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
        keyboard.doModal()
        if keyboard.isConfirmed() :
               search_entered = (keyboard.getText().replace("'","%27"))
               if search_entered!='':
                  from resources.default import search_result_turkey
                  search_result_turkey(search_entered)

    elif mode==268:
        from resources.default import add_to_databaseturkey2
        add_to_databaseturkey2(url,name,data,iconimage,fanart,description)
    elif mode==269:
        from resources.default import full_data_turkey_2
        full_data_turkey_2()
    elif mode==270:

            url='plugin://plugin.video.cobra/?mode=playback.media&media_type=movie&query={0}&tmdb_id={1}'.format(que(name.replace(url,'')),id)
            xbmc.executebuiltin('RunPlugin(%s)'%url)
    elif mode==271:
            xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.cobra/?mode=build_season_list&tmdb_id=%s",return)'%id)   
    elif mode==272:
        from resources.default import actor_m_cobra
        actor_m_cobra(url,description)

    elif mode==273:
            xbmc.executebuiltin('ActivateWindow(10025,&quot;plugin://plugin.video.idanplus/?iconimage=https%253A%252F%252Fmedia.reshet.tv%252Fimage%252Fupload%252Fv1641912830%252Fuploads%252F2022%252F902809794.jpg&amp;mode=1&amp;module=reshet&amp;moredata&amp;name=%20%5bCOLOR%20yellow%5d%d7%a8%d7%a9%d7%aa%2013%5b%2fCOLOR%5d%20-%20%5bCOLOR%20orange%5d%5bB%5d%d7%90%d7%91%d7%95%d7%93%d7%99%d7%9d%5b%2fB%5d%5b%2fCOLOR%5d%20&amp;url=https%253A%252F%252F13tv.co.il%252Fall-shows%252Favudim-902985882%252F&quot;,return)')  
            

    elif mode==274:

        addon_id='plugin.video.idanplus'
        str_next='ActivateWindow(10025,"%s?iconimage=%s&mode=2&module=%s&moredata&name=%s&url=%s",return)'%("plugin://%s/"%addon_id,iconimage,module,name,url)
        xbmc.executebuiltin(str_next)
    elif mode==275:
        from resources.default import turkish_data2
        turkish_data2(last_id,iconimage,fanart,data)
    elif mode==276:

        download_data_db(force='true')
    elif mode==277:
        search_entered=''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
        keyboard.doModal()
        if keyboard.isConfirmed() :
               search_entered = (keyboard.getText().replace("'","%27"))
               if search_entered!='':
                  from resources.default import search_result_turkey2
                  search_result_turkey2(search_entered)
                  
    elif mode==278:

            
                
            addon_id='plugin.video.reborn_sdarot'
            str_next='ActivateWindow(10025,"%s?mode=41&url=%s&iconimage=%s&fanart=%s",return)'%("plugin://%s/"%addon_id,url,iconimage,fanart)
            xbmc.executebuiltin(str_next)
    elif mode==279:
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % 'plugin.video.cobra')
    elif mode==280:
        # search_entered_pre=''
        
        # #Enter Search
        # keyboard = xbmc.Keyboard(search_entered_pre, '[COLOR blue][I]חפש באנגלית או בעברית[/I][/COLOR]')
        # keyboard.doModal()
        # if keyboard.isConfirmed():
                # search_entered_pre = keyboard.getText()
        # if search_entered_pre=='':
         # return

        from resources.data import search_MoviesOnlineDates
        search_MoviesOnlineDates(url,name,iconimage,fanart)
  
    if len(sys.argv)>1 and exit_now==0:
        # if mode!=None and mode!=15 and mode!=20 and mode!=199 and mode!=204 and mode!=206 and mode!=14 and mode!=167 and mode!=201 and mode!=196:
            # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATEADDED)
            # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
            # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
            # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
            # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)


        if mode==19 :
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        elif mode==16 :
            xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
        elif mode==33 :
            xbmcplugin.setContent(int(sys.argv[1]), 'studios')
        elif mode==14 :
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        elif mode==254 :
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        elif mode==272 :
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        elif mode==214 :
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous',mode)))

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
# from data import last_viewed_ep
# last_viewed_ep(run=True)
# from resources.data import update_tmdb
# # # movie_notify(0,description)
# update_tmdb()