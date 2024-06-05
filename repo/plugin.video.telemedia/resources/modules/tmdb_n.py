#!/usr/bin/env python3
# countasync.py


#('https://api.themoviedb.org/3/movie/603?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US',verify=False).json()


import time,sys,random,os
from concurrent.futures import wait
from  resources.modules.public import addNolink,addDir3,addLink,lang,user_dataDir
import json
from  resources.modules.client import get_html
from resources.modules import cache
import concurrent.futures
import xbmcplugin,xbmcgui
from urllib.parse import urlencode
from resources.modules import log
from  resources.modules.general import addon_id
cacheFile=os.path.join(user_dataDir,'database.db')
import xbmcaddon
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
Addon = xbmcaddon.Addon()
window=xbmcgui.Window(10000)
backup_resolutions, writer_credits = {'poster': 'w780', 'fanart': 'w1280', 'still': 'original', 'profile': 'h632'}, ('Author', 'Writer', 'Screenplay', 'Characters')

def get_html_g():
    try:
        url_g='https://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
        html_g_tv=get_html(url_g).json()
         
   
        url_g='https://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
        html_g_movie=get_html(url_g).json()
    except Exception as e:
        log.warning('Err in HTML_G:'+str(e))
    return html_g_tv,html_g_movie
html_g_tv,html_g_movie=cache.get(get_html_g,72, table='posters')

class tmdb:
    def __init__(self,url):
        Addon = xbmcaddon.Addon()
        self.all_results={}
        self.all_lists=[]
        if '/movie' in url:
            self.tv_movie='movie'
        else:
            self.tv_movie='tv'
        self.all_ids=[]
        self.main_data={}
        self.url=url
        self.all_d={}
        self.all_results,self.all_ids,self.main_data=self.local_cache(self.build_data,24,self.url)
        
        self.add_dir()
        
    def set_PRAGMAS(self, dbcon):
        
        
        dbcur = dbcon.cursor()
        dbcur.execute('''PRAGMA synchronous = OFF''')
        dbcur.execute('''PRAGMA journal_mode = OFF''')
        
        return dbcur
    def get_property(self,prop):
        return window.getProperty(prop)
    def set_property(self,prop,value):
        return window.setProperty(prop,value)
        
    def local_cache(self,function,timeout,url):
        
        cachedata = self.get_property(url)
        if cachedata:
            self.all_results,self.all_ids,self.main_data,saved_time=eval(cachedata)
            self.all_results=json.loads(self.all_results)
            self.all_ids=json.loads(self.all_ids)
            self.main_data=json.loads(self.main_data)
            t1 = int(saved_time)
            t2 = int(time.time())

            update = (abs(t2 - t1) / 3600) >= int(timeout)
            
            if update == True:
               
                t=time.time()
                self.all_results,self.all_ids,self.main_data=function(url)
                c= (json.dumps(self.all_results), json.dumps(self.all_ids), json.dumps(self.main_data),t)
                c = self.set_property(url,repr(c))
                
                
                
  
        if not cachedata or self.all_ids==[]:
            log.warning('Not mem')
           
            dbcon = database.connect(cacheFile)
            dbcur=self.set_PRAGMAS(dbcon)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""url TEXT, ""all_results TEXT, ""all_ids TEXT, ""main_data TEXT,""added TEXT, ""free TEXT);" % 'local_cache')
            
            dbcur.execute("SELECT * FROM local_cache WHERE url = '%s'" % (url))
            match = dbcur.fetchone()
            
            t = int(time.time())
            if match!=None:
                self.all_results,self.all_ids,self.main_data=json.loads(match[1]),json.loads(match[2]),json.loads(match[3])
                
                t1 = int(match[4])
                t2 = int(time.time())
                update = (abs(t2 - t1) / 3600) >= int(timeout)
                if update == True:
                    self.all_results,self.all_ids,self.main_data=function(url)
                    cachedata = (json.dumps(self.all_results), json.dumps(self.all_ids), json.dumps(self.main_data),t)
                    cachedata = self.set_property(url,repr(cachedata))
                    
                    
                    dbcur.execute("INSERT INTO local_cache Values (?, ?, ?, ?, ?, '')" , (url, json.dumps(self.all_results), json.dumps(self.all_ids), json.dumps(self.main_data),t))
                    dbcon.commit()
                
                return self.all_results,self.all_ids,self.main_data
                        
            else:
                
                self.all_results,self.all_ids,self.main_data=function(url)
                
                cachedata = (json.dumps(self.all_results), json.dumps(self.all_ids), json.dumps(self.main_data),t)
                cachedata = self.set_property(url,repr(cachedata))
                
                
                dbcur.execute("INSERT INTO local_cache Values (?, ?, ?, ?, ?, '')" , (url, json.dumps(self.all_results), json.dumps(self.all_ids), json.dumps(self.main_data),t))
                dbcon.commit()
            dbcur.close()
            dbcon.close()
        return self.all_results,self.all_ids,self.main_data
    def get_more_meta(self,id,iconimage,fanart):
      try:
        all_clear_art=[]
        all_n_fan=[]
        all_banner=[]
        r_banner=''
        r_back=''
        r_art=''
        r_logo=''
        art={'fanart':fanart,'iconimage':iconimage,'clearlogo':r_logo,'clearart':r_art,'icon': iconimage, 'thumb': fanart, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage,'banner': r_banner, 'landscape': r_back, 'discart': iconimage}
    
        user = 'cf0ebcc2f7b824bd04cf3a318f15c17d'

        headers = {'api-key': 'a7ad21743fd710fccb738232f2fbdcfc'}

        headers.update({'client-key': user})
       
        m_type='movies'
        f_id=id
        
        full_art=get_html('http://webservice.fanart.tv/v3/%s/%s'%(m_type,f_id),headers=headers).json()

        logo=full_art.get('hdmovielogo','')
        if len(logo)>0:
            all_logo=[]
            for itt in logo:
              if itt['lang']=='en':
                all_logo.append(itt['url'])
            random.shuffle(all_logo)
            r_logo=all_logo[0]
        if 'hdmovieclearart' in full_art:
            for itt in full_art['hdmovieclearart']:
               if itt['lang']=='en':
                all_clear_art.append(itt['url'])
            
        if len(all_clear_art)>0:
            random.shuffle(all_clear_art)
            r_art=all_clear_art[0]
        if 'moviebackground' in full_art:
            for itt in full_art['moviebackground']:
               if itt['lang']=='en':
                all_n_fan.append(itt['url'])
        
        if len(all_n_fan)>0:
            random.shuffle(all_n_fan)
            r_back=all_n_fan[0]
        if 'moviebanner' in full_art:
            for itt in full_art['moviebanner']:
               if itt['lang']=='en':
                all_banner.append(itt['url'])
        
        if len(all_n_fan)>0:
            random.shuffle(all_n_fan)
            r_banner=all_clear_art[0]
        art={'fanart':fanart,'iconimage':iconimage,'clearlogo':r_logo,'clearart':r_art,'icon': iconimage, 'thumb': fanart, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage,'banner': r_banner, 'landscape': r_back, 'discart': iconimage}

        return art
      except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
           
            log.warning('ERROR IN GET Art:'+str(lineno))
            log.warning('inline:'+line)
            log.warning(e)
            return art
    def get_response(self,req_url, timeout=10):
            return get_html(req_url, timeout=timeout,verify=False).json()
    def collect_meta(self,req_url, timeout=10):
        response = cache.get(self.get_response,24,req_url, table='posters')
       
        iconimage='https://image.tmdb.org/t/p/original/'+(response.get('poster_path','') or "")
        fanart='https://image.tmdb.org/t/p/original/'+(response.get('backdrop_path','') or "")
        self.all_results[response['id']]={}
        self.all_results[response['id']]['result']=response
        if self.tv_movie=='movie':
            self.all_results[response['id']]['art']=self.get_more_meta(response['id'],iconimage,fanart)
        else:
            self.all_results[response['id']]['art']={'fanart':fanart,'iconimage':iconimage,'icon': iconimage, 'thumb': fanart, 'poster': iconimage}
        return self.all_results
    def build_data(self,url):
        
        data=cache.get(self.get_response,24,self.url, table='posters') 
        
        all_urls = ["https://api.themoviedb.org/3/%s/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=en&append_to_response=external_ids,videos,credits,release_dates,alternative_titles,translations"%(self.tv_movie,i['id']) for i in data['results']]
        
        self.all_ids=[i['id'] for i in data['results']]
        self.main_data={}
        x=0
        for i in data['results']:
            id=str(i.get('id'))
            self.main_data[id]={}
            self.main_data[id]['results']=i
            self.main_data[id]['main']=data
            self.main_data[id]['order']=x
            x+=1
        if Addon.getSetting("extra_data")=='true':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for url in all_urls:
                    futures.append(executor.submit(self.collect_meta, req_url=url))
                wait(futures)
        return self.all_results,self.all_ids,self.main_data
        
    def get_main_data(self,id):
       try:
        
        video_data={}
        remove_record=False
        html=self.main_data[id]['main']
        data=self.main_data[id]['results']
        max_page=html['total_pages']
        all_res=html['total_results']
        
        rating=data.get('vote_average',0)
        
        plot=data.get('overview','')
           
        if Addon.getSetting("adults")=='true':
             
            addults=data.get('adult',False)
             
                
            er_str='אירוטי'.encode().decode(encoding = 'UTF-8',errors = 'strict')
            er2_str='סקס'.encode().decode(encoding = 'UTF-8',errors = 'strict')
            if 'erotic ' in plot.lower() or 'sex' in plot.lower() or addults==True or er_str in plot or er2_str in plot:
                remove_record=True
            
        if 'title' not in data:
           tv_movie='tv'
           new_name=data['name']
           html_g=html_g_tv
        else:
           tv_movie='movie'
           new_name=data['title']
           html_g=html_g_movie
          
        
         
        if 'original_title' in data:
           original_name=data['original_title']
        else:
           original_name=data['original_name']
        iconimage='https://image.tmdb.org/t/p/original/'+data.get('poster_path','')
        fanart='https://image.tmdb.org/t/p/original/'+html.get('backdrop_path','')
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                if i['name'] is not None])
        try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
        except:genere=''
         
        trailer = "plugin://%s?mode=171&id=%s&url=%s" % (addon_id,id,tv_movie)
        
        if 'first_air_date' in data:
           year=str(data['first_air_date'].split("-")[0])
        elif 'release_date' in data:
            year=str(data['release_date'].split("-")[0])
        else:
            year='0'
  
        video_data['title']=new_name
        video_data['mediatype']='movie'
        video_data['TVshowtitle']=''
        
        video_data['season']=' '
        video_data['episode']=' '
        video_data['OriginalTitle']=original_name
        
        video_data['year']=year
        
        video_data['genre']=genere
        video_data['rating']=str(rating)
        video_data['trailer']=trailer

        video_data['plot']=plot
     
        #video_data['iconimage']=iconimage
        #video_data['fanart']=fanart
        
        return video_data
       except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
           
            log.warning('ERROR IN Main Data:'+str(lineno))
            log.warning('inline:'+line)
            log.warning(e)
            return video_data
    def get_watched(self):
        
        cacheFile=os.path.join(user_dataDir,'database.db')
        dbcon = database.connect(cacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')

       
        dbcon.commit()
   
        dbcur.execute("SELECT * FROM playback")
        match = dbcur.fetchall()
        dbcur.close()
        dbcon.close()
        all_w={}
          
        for n,tm,s,e,p,t,f in match:
                ee=str(tm)
                all_w[ee]={}
                if self.tv_movie=='movie':
                    all_w[ee]['resume']=str(p)
                    all_w[ee]['totaltime']=str(t)
                else:
                    all_w[ee]['resume']=0
                    all_w[ee]['totaltime']=100
        return all_w
    def add_items(self,data_pre,tv_movie,order):
       try:
        if 'result' in data_pre:
            data_get=data_pre['result'].get 
        else:
            data_get=data_pre['results'].get 
        id=str(data_get('id'))
       
        
        
       
        
        
        
        video_data=self.get_main_data(id)
        #log.warning(video_data['title']+', '+id+','+added_pre)
        
        heb_name=video_data['title']
        cast=[]
        writer=''
        director=''
        mpaa=[]
        total_aired_eps=''
        total_seasons=''
        if Addon.getSetting("extra_data")=='true':
            
            
            
            tmdb_id, imdb_id = data_get('id', ''), data_get('imdb_id', '')
            votes = data_get('vote_count', '')
            if tv_movie=='movie':
                
                try: duration = int(data_get('runtime', '90') * 60)
                except: duration = 90 * 60
                
            else:
                try: duration = min(data_get('episode_run_time'))*60
                except: duration = 30*60
                season_data, total_seasons, total_aired_eps = data_get('seasons'), data_get('number_of_seasons'), data_get('number_of_episodes')
            credits = data_get('credits')
            if credits:
                all_cast = credits.get('cast', None)
                if all_cast:
                    try: cast = [{'name': i['name'], 'role': i['character'], 'thumbnail': 'https://image.tmdb.org/t/p/%s%s' % (backup_resolutions['profile'], i['profile_path'])if i['profile_path'] else ''}\
                                for i in all_cast]
                    except Exception as e:
                        log.warning(e)
                crew = credits.get('crew', None)
                if crew:
                    try: writer = ', '.join([i['name'] for i in crew if i['job'] in writer_credits])
                    except: pass
                    try: director = [i['name'] for i in crew if i['job'] == 'Director'][0]
                    except: pass
            release_dates = data_get('release_dates')
            if release_dates:
                try: mpaa = [x['certification'] for i in release_dates['results'] for x in i['release_dates'] \
                            if i['iso_3166_1'] == 'US' and x['certification'] != '' and x['note'] == ''][0]
                except: mpaa=[]
            if tv_movie=='movie':
                premiered =  data_get('release_date', '')
            else:
                premiered =  data_get('first_air_date', '')
            companies = data_get('production_companies')
            studio=[]
            if tv_movie=='tv':
                networks = data_get('networks', None)
                if networks:
                    if len(networks) == 1: studio = [i['name'] for i in networks][0]
                    else:
                        try: studio = [i['name'] for i in networks if i['logo_path'] not in empty_value_check][0] or [i['name'] for i in networks][0]
                        except: pass
            else:
                if companies:
                    if len(companies) == 1: studio = [i['name'] for i in companies][0]
                    else:
                        try: studio = [i['name'] for i in companies if i['logo_path'] not in empty_value_check][0] or [i['name'] for i in companies][0]
                        except: pass
            production_countries = data_get('production_countries', None)
            country_codes=[]
            country=[]
            if production_countries:
                country = [i['name'] for i in production_countries]
                country_codes = [i['iso_3166_1'] for i in production_countries]
            iconimage='https://image.tmdb.org/t/p/original/'+(data_get('poster_path','') or "")
            fanart='https://image.tmdb.org/t/p/original/'+(data_get('backdrop_path','') or "")
            tagline=data_get('tagline', '')
            
            
            #video_data['cast']=cast
            video_data['writer']=writer
            video_data['director']=director
            video_data['duration']=duration
            #video_data['imdb']=imdb_id
            video_data['votes']=votes
            video_data['mpaa']=mpaa
            #video_data['country_codes']=country_codes
            video_data['country']=country
            video_data['studio']=studio
            video_data['premiered']=premiered
        else:
            iconimage='https://image.tmdb.org/t/p/original/'+(data_get('poster_path','') or "")
            fanart='https://image.tmdb.org/t/p/original/'+(data_get('backdrop_path','') or "")
            imdb_id=id
            data_pre['art']={'fanart':fanart,'iconimage':iconimage,'clearlogo':'','clearart':'','icon': iconimage, 'thumb': fanart, 'poster': iconimage,'tvshow.poster': iconimage, 'season.poster': iconimage,'banner': '', 'landscape': ''}
                
               
            
                    
        link=self.url.split('page=')[0]
        page_no=self.url.split('page=')[1]

        params={}
        params['iconimage']=iconimage
        params['fanart']=fanart
        params['description']=video_data['plot']
        params['url']=link+'page='+str(int(page_no)+1)
        params['name']=video_data['title']
        params['season']=' '
        params['episode']=' '
        params['heb_name']=heb_name
        params['original_title']=video_data['OriginalTitle']
        if self.tv_movie=='movie':
            
            params['mode']=15
            isfolder=False
        else:
            params['mode']=16
            isfolder=True
        params['id']=id
 
        params['tmdbid']=id
        params['eng_name']=video_data['title']
        params['show_original_year']=video_data['year']
        params['data']=video_data['year']
        url_params = 'plugin://plugin.video.telemedia/?' + urlencode(params) 
        self.all_d[id]={}
        self.all_d[id]['url_params']=url_params
        self.all_d[id]['video_data']=video_data
        self.all_d[id]['cast']=cast
        self.all_d[id]['data_pre']=data_pre
        
        self.all_d[id]['total_aired_eps']=total_aired_eps
        self.all_d[id]['total_seasons']=total_seasons
        
        self.all_d[id]['imdb_id']=imdb_id
        
        self.all_d[id]['order']=order
        #self.all_lists.append((url_params, listitem, isfolder,order))
       except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
           
            log.warning('ERROR IN GET TMDB:'+str(lineno))
            log.warning('inline:'+line)
            log.warning(e)
    def thread_all_data(self,url):
        if Addon.getSetting("extra_data")=='true':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                i=0
                for id in self.all_ids:
                    if id not in self.all_results:
                        id=str(id)
                   
                    
                    futures.append(executor.submit(self.add_items, data_pre=self.all_results[id],tv_movie=self.tv_movie,order=i))
                    i+=1
                wait(futures)
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                i=0
                for id in self.all_ids:
                    if id not in self.all_results:
                        id=str(id)
                   
                    
                    futures.append(executor.submit(self.add_items, data_pre=self.main_data[id],tv_movie=self.tv_movie,order=i))
                    i+=1
                wait(futures)
        return self.all_d,{},{}
    def get_added_pre(self,id,all_w):
        added_pre=''
        ee=id
        time_to_save_trk=int(Addon.getSetting("time_to_save"))
        all_w_trk=''
        if all_w_trk!='':
            if float(all_w_trk)>=time_to_save_trk:
                added_pre='  [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
            elif float(all_w_trk)>1:# and float(all_w_trk)<time_to_save_trk:
                added_pre=' [COLOR yellow][I]'+str(int(float(all_w_trk)))+'%[/I][/COLOR] \n '
        elif ee in all_w:
              
              if '%' in str(all_w[ee]['resume']):
                all_w_time=all_w[ee]['resume'].replace('%','')
              else:
                try:
                    all_w_time=int((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                except:
                    all_w_time=''
              if float(all_w_time)>=time_to_save_trk:
                    added_pre=' [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
              elif float(all_w_time)>1:# and float(all_w_time)<time_to_save_trk:
               added_pre=' [COLOR yellow][I]'+str(all_w_time)+'%[/I][/COLOR] \n '
        return added_pre
    def get_menu_items(self,video_data,id):
        menu_items=[]
        tv_show=tv_movie=self.tv_movie
        season='%20'
        episode='%20'
        
        if Addon.getSetting("cast")=='true':
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32248), 'ActivateWindow(10025,"%s?mode=177&url=%s&id=%s&season=%s&episode=%s",return)'  % ( "plugin://%s/"%addon_id ,self.tv_movie,id,'%20','%20')))
        menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32166), 'Action(Info)'))
        if Addon.getSetting("play_trailer")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32167), 'PlayMedia(%s)' % video_data['trailer']))
        if Addon.getSetting("settings_content")=='true':
            menu_items.append(('%s'%Addon.getLocalizedString(32168), 'RunPlugin(%s?mode=151&url=www)' % "plugin://%s/"%addon_id ))
        if Addon.getSetting("queue_item")=='true':
            menu_items.append(('%s'%Addon.getLocalizedString(32169), 'Action(Queue)' ))
        if Addon.getSetting("trakt_manager")=='true':
            menu_items.append((Addon.getLocalizedString(32170), 'RunPlugin(%s)' % ('%s?url=%s&mode=150&name=%s&data=%s')%("plugin://%s/"%addon_id,id,video_data['OriginalTitle'],tv_movie) ))
        if Addon.getSetting("trakt_watched")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32171), 'RunPlugin(%s)' % ('%s?url=www&original_title=add&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_show,id,season,episode))) 
        if Addon.getSetting("trakt_unwatched")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32172), 'RunPlugin(%s)' % ('%s?url=www&original_title=remove&mode=65&name=%s&id=%s&season=%s&episode=%s')%("plugin://%s/"%addon_id,tv_show,id,season,episode))) 
        if Addon.getSetting("clear_Cache")=='true':
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32176), 'RunPlugin(%s)' % ('%s?url=www&mode=35')%("plugin://%s/"%addon_id)))
        return menu_items
    def add_dir(self):
        '''
        for id in self.all_ids:
            if id not in self.all_results:
                log.warning('False: '+str(id))
            else:
                log.warning('True: '+str(id))
        '''
        start=time.time()
        self.all_d,dummy1,dummy2=self.local_cache(self.thread_all_data,24,'data'+self.url)
        all_w=self.get_watched()
        
               
        
        for ids in self.all_d:
            url_params=self.all_d[ids]['url_params']
            video_data=self.all_d[ids]['video_data']
            cast=self.all_d[ids]['cast']
            data_pre=self.all_d[ids]['data_pre']
            total_aired_eps=self.all_d[ids]['total_aired_eps']
            total_seasons=self.all_d[ids]['total_seasons']
            order=self.all_d[ids]['order']
            #added_pre=self.all_d[ids]['added_pre']
            imdb_id=self.all_d[ids]['imdb_id']
            added_pre=self.get_added_pre(ids,all_w)
            if added_pre!='':

                video_data['title']='[COLOR lightblue]'+video_data['title']+'[/COLOR]'
            video_data['title']=added_pre.replace('\n','')+video_data['title']
            menu_items=self.get_menu_items(video_data,ids)
            
            listitem=xbmcgui.ListItem(offscreen=True)
            
            listitem.setContentLookup(False)
            listitem.setLabel(added_pre+video_data['title'])
            
            
            listitem.setCast(cast)
            listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': str(id)})

            listitem.setArt(data_pre.get('art',[]))
            listitem.setInfo('Video', infoLabels=video_data)
            listitem.addContextMenuItems(menu_items, replaceItems=False)
            isfolder=False
            if self.tv_movie=='tv':
                isfolder=True
                #video_data['season_data']=season_data
                if total_aired_eps!='':
                    listitem.setProperty('totalepisodes', str(total_aired_eps))
                if total_seasons!='':
                    listitem.setProperty('totalseasons', str(total_seasons))
            self.all_lists.append((url_params, listitem, isfolder,order))  
        self.all_lists=sorted(self.all_lists, key=lambda x: x[3], reverse=False)
        
        listitem=xbmcgui.ListItem(offscreen=True)
        listitem.setLabel('[COLOR aqua][I]עמוד הבא[/I][/COLOR]')
        
        
        listitem.setInfo('Video', infoLabels={'title':'[COLOR aqua][I]עמוד הבא[/I][/COLOR]'})
        listitem.setArt({'fanart':'https://static.bimago.pl/mediacache/catalog/product/cache/8/6/117168/image/750x1120/77f2bbb90b9f6398dc4944625b9e3c2c/117168_1.jpg','iconimage':'https://previews.123rf.com/images/alekseyvanin/alekseyvanin1801/alekseyvanin180100900/93405059-next-page-line-icon-outline-vector-sign-linear-style-pictogram-isolated-on-white-arrow-right-symbol-.jpg'})
        
        link=self.url.split('page=')[0]
        page_no=self.url.split('page=')[1]
        params={}
    
        params['description']=''
        params['url']=link+'page='+str(int(page_no)+1)
        params['name']='[COLOR aqua][I]עמוד הבא[/I][/COLOR]'
        import xbmc
        params['heb_name']='[COLOR aqua][I]עמוד הבא[/I][/COLOR]'

        params['mode']=14
        params['eng_name']='[COLOR aqua][I]עמוד הבא[/I][/COLOR]'
     

        url_params = 'plugin://plugin.video.telemedia/?' + urlencode(params) 
        
        self.all_lists.append((url_params, listitem, True))
        
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),self.all_lists,len(self.all_lists))
        if self.tv_movie=='movie':
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        else:
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        log.warning(time.time()-start)


