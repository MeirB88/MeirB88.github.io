# -*- coding: utf-8 -*-
import xbmcaddon,xbmc,xbmcgui


from .public import addNolink,addDir3,addLink3,addLink,lang,user_dataDir
from threading import Thread
from resources.modules.globals import dbcur
import urllib,os,re,sys,time,xbmcplugin,xbmcvfs
from resources.modules import log
from resources.modules import cache
Addon = xbmcaddon.Addon()
domain_s='https://'
from urllib.parse import urlencode
backup_resolutions, writer_credits = {'poster': 'w780', 'fanart': 'w1280', 'still': 'original', 'profile': 'h632'}, ('Author', 'Writer', 'Screenplay', 'Characters')
empty_value_check = ('', 'None', None)
global extra_data
extra_data={}
__addon__ = xbmcaddon.Addon()
addon_name=__addon__.getAddonInfo('name')
addon_id=__addon__.getAddonInfo('id')

que=urllib.parse.quote_plus
unque=urllib.parse.unquote_plus

def adv_gen_window(url):
    from  resources.modules import pyxbmct
    # import requests
    class adv_gen_window(pyxbmct.AddonDialogWindow):
        def __init__(self,type):
            super(adv_gen_window, self).__init__('בחר שנה')
            wd=int(1250)
            hd=int(700)
            px=int(10)
            py=int(10)
            self.type=type
            self.fromy=''
            self.toy=''
            self.all_clicked=[]
            self.setGeometry(wd, hd, 22, 5,pos_x=px, pos_y=py)
            self.set_info_controls()
            #self.set_active_controls()
            self.set_navigation()
            
            # Connect a key action (Backspace) to close the window..
            self.connect(pyxbmct.ACTION_PREVIOUS_MENU, self.click_c)
            self.connect(pyxbmct.ACTION_NAV_BACK, self.click_c)
            #self.connect(pyxbmct.ACTION_MOUSE_RIGHT_CLICK, self.click_c)
            
        def click_c(self):
            for items in self.all_radio:
                if self.all_radio[items]['button'].isSelected():
                    self.all_clicked.append(str(self.all_radio[items]['id']))
            
            
            self.fromy=self.edit_from.getText()
            self.toy=self.edit_to.getText()
            
            self.close()
        def radio_update(self,radiobutton,id):
            # Update radiobutton caption on toggle
            #log.warning('Clicked:'+str(id))
            if radiobutton.isSelected():
                self.all_clicked.append(id)
            else:
                if id in self.all_clicked:
                    self.all_clicked.pop(id)
        def set_info_controls(self):
            # Edit
            edit_label = pyxbmct.Label('משנה')
            self.placeControl(edit_label, 0, 0, rowspan=2)
            
            self.edit_from = pyxbmct.Edit('2000')
            self.placeControl(self.edit_from, 0, 1, rowspan=2)
            # Additional properties must be changed after (!) displaying a control.
            self.edit_from.setText('2000')
            
            # Edit
            edit_label = pyxbmct.Label('עד שנה')
            self.placeControl(edit_label, 2, 0, rowspan=2)
            
            self.edit_to = pyxbmct.Edit('2019')
            self.placeControl(self.edit_to, 2, 1, rowspan=2)
            # Additional properties must be changed after (!) displaying a control.
            self.edit_to.setText('2019')
            
            #genere
            edit_label = pyxbmct.Label('זאנר')
            self.placeControl(edit_label, 0, 3)
            
            url='http://api.themoviedb.org/3/genre/%s/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(self.type,lang)
            import requests
            x=requests.get(url).json()
            self.all_g=[]
            for items in x['genres']:
               
                self.all_g.append((items['name'],items['id']))
            self.all_radio={}
            i=1
            self.all_it=[]
            for name,id in self.all_g:
                # RadioButton
                self.all_it.append(name)
                self.all_radio[name]={}
                self.all_radio[name]['button'] = pyxbmct.RadioButton(name)
                self.all_radio[name]['id']=id
                self.placeControl(self.all_radio[name]['button'], i, 3)
                #self.connect(self.all_radio[name], self.radio_functions[name])
                i+=1
            self.button = pyxbmct.Button('חיפוש')
            self.placeControl(self.button, 17, 4, rowspan=2)
            # Connect control to close the window.
            self.connect(self.button, self.click_c)
        def set_navigation(self):
            self.edit_from.controlUp(self.edit_to)
            self.edit_from.controlDown(self.edit_to)
            
            self.edit_to.controlUp(self.edit_from)
            self.edit_to.controlDown(self.edit_from)
            
            self.edit_to.controlRight(self.all_radio[self.all_g[0][0]]['button'])
            self.edit_to.controlLeft(self.all_radio[self.all_g[0][0]]['button'])
            
            self.edit_from.controlRight(self.all_radio[self.all_g[0][0]]['button'])
            self.edit_from.controlLeft(self.all_radio[self.all_g[0][0]]['button'])
            
            
            
                
            
            for items in self.all_it:
                ind=self.all_it.index(items)
                if ind==0:
                    pre=len(self.all_it)-1
                    next=1
                elif ind==(len(self.all_it)-1):
                    pre=ind-1
                    next=0
                else:
                    pre=ind-1
                    next=ind+1
               
                self.all_radio[items]['button'].controlUp(self.all_radio[self.all_it[pre]]['button'])
                self.all_radio[items]['button'].controlDown(self.all_radio[self.all_it[next]]['button'])
                
                self.all_radio[items]['button'].controlLeft(self.edit_from)
                self.all_radio[items]['button'].controlRight(self.button)
            
            self.setFocus(self.edit_from)
    window = adv_gen_window(url)
    window.doModal()
    all_g=window.all_clicked
    start_y=window.fromy
    end_y=window.toy

    del window
    return all_g,start_y,end_y

def get_html_g():
    try:
        # import requests
        import requests
        url_g='https://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
        html_g_tv=requests.get(url_g).json()
         
   
        url_g='https://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
        html_g_movie=requests.get(url_g).json()
    except Exception as e:
        log.warning('Err in HTML_G:'+str(e))
    return html_g_tv,html_g_movie
html_g_tv,html_g_movie=cache.get(get_html_g,72, table='posters_n')

def get_tmdb_data(new_name_array,html_g,fav_search_f,fav_servers_en,fav_servers,google_server,rapid_server,direct_server,heb_server,url,isr,xxx,release_date):
          import requests
          try:
           global all_d
           # import requests
           
           if Addon.getSetting("use_trak")=='true':
               i = (call_trakt('/users/me/watched/movies'))
               all_movie_w=[]
               for ids in i:
                  all_movie_w.append(str(ids['movie']['ids']['tmdb']))
           
           

           html=requests.get(url).json()

           try:
               max_page=html['total_pages']
           except:
               max_page=1
               pass
           # log.warning('max_page:'+str(max_page))
           try:
            all_res=html['total_results']
           except:
               all_res=1
          
           count=0
           if 'results' in html:
                result_html=html['results']
           else:
               result_html=[html]
           # import logging
           for data in result_html:
             # logging.warning('mv_name Not found:'+str(data))
             count+=1
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               release_date=str(data['first_air_date'])
             elif 'release_date' in data:
               release_date=str(data['release_date'])
             else:
               release_date=''
             if 'first_air_date' in data:
               year=str(data['first_air_date'].split("-")[0])
             elif 'release_date' in data:
                year=str(data['release_date'].split("-")[0])
             else:
                year='0'
             try:
                 if data['overview']==None:
                   plot=' '
                 else:
                   plot=data['overview']
             except:
                 plot=""

             if Addon.getSetting("adults")=='true':
                 try:
                     if 'adult' in data:
                        addults=data['adult']
                     else:
                        addults=False
                 except:
                     addults=False
                 er_str='אירוטי'.encode().decode(encoding = 'UTF-8',errors = 'strict')
                 er2_str='סקס'.encode().decode(encoding = 'UTF-8',errors = 'strict')
                 if 'erotic ' in plot.lower() or 'sex' in plot.lower() or addults==True or er_str in plot or er2_str in plot:
                    continue
             if 'title' not in data:
               tv_movie='tv'
               new_name=data['name']
             else:
               tv_movie='movie'
               new_name=data['title']
              
             
             f_subs=[]
             if 'original_title' in data:
               original_name=data['original_title']
               mode=15
               
               id=str(data['id'])
               if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                 import cache
                 from subs import get_links
                 f_subs=cache.get(get_links,9999,'movie',original_name,original_name,'0','0','0','0',year,id,True, table='pages')
               if data['original_language']!='en':
                
                html2=requests.get('http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id).json()
                original_name=html2['title']
                
               
             else:
               original_name=data['original_name']
               id=str(data['id'])
               
               mode=16
               
               if data['original_language']!='en':
                
                    html2=requests.get('http://api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id).json()
                    if 'name' in html2:
                        original_name=html2['name']
                    #if 'name' in data:
                    #    original_name=data['name']
             
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
               fan='https://image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon='https://image.tmdb.org/t/p/original/'+icon
             try:
                 genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                        if i['name'] is not None])
             except:
                 genres_list=''
             try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
             except:genere=''
             # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', tv_movie)))
             trailer = "plugin://%s?mode=171&id=%s&url=%s" % (addon_id,id,tv_movie)
             if (new_name+id) not in new_name_array:
              new_name_array.append(new_name+id)
              # if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                  # if len(f_subs)>0:
                    # color='white'
                  # else:
                    # color='red'
                    
              # else:
              color='white'
              start_time = time.time()
              elapsed_time = time.time() - start_time
              if  Addon.getSetting("disapear")=='true' and color=='red' and mode!=7:
                a=1
              else:
                color='white'
                
                watched='no'
                if Addon.getSetting("use_trak")=='true':
                    if id in all_movie_w:
                        watched='yes'
                    if id in all_w_tv_data:
                        watched=all_w_tv_data[id]
                        log.warning('Found watched:'+id)
                if  mode==4 and fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 or heb_server=='true' or google_server=='true' or rapid_server=='true' or direct_server=='true'):
                
                    fav_status='true'
                else:
                    fav_status='false'
            
                
                all_d.append(('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx,max_page,all_res,release_date))
              
           
           
          except Exception as e:
            import linecache,sys
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Victory', 'No Trailer...Line:'+str(lineno)+' E:'+str(e))))
            log.warning('ERROR IN GET TMDB:'+str(lineno))
            log.warning('inline:'+line)
            log.warning(e)
            # log.warning(html_t)
            log.warning('BAD Trailer play')
def get_all_data(first,last,url,link,new_name_array,isr):
    try:
        release_date=''
        global all_d
        
        all_d=[]
        xxx=0
        #log.warning('1')
        if '/tv/' in url:
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
        #log.warning('2')
   
              
              
        if '/tv/' in url:
             url_g='https://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
             
             html_g=html_g_tv
        else:
             url_g='https://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
             html_g=html_g_movie
        #html_g=requests.get(url_g).json()
        # log.warning('3')
        if Addon.getSetting("dp")=='true' and (last-first)>1:
                dp = xbmcgui.DialogProgress()
                try:
                    dp.create("Loading", "Please Wait")
                except:
                    dp.create("Loading", "Please Wait", '')
                dp.update(0)
        thread=[]
        # log.warning('4')
        for i in range(first,last):
           # log.warning('5')
           url=link+'page='+str(i)
          
           # t1 = Thread(target=open_t, args=(name,'',))
           # t1.start()
           thread.append(Thread(target=get_tmdb_data, args=(new_name_array,html_g,fav_search_f,fav_servers_en,fav_servers,google_server,rapid_server,direct_server,heb_server,url,isr,xxx,release_date,)))
           thread[len(thread)-1].setName('Page '+str(i))
           xxx+=1
           
    except Exception as err:
            import traceback
            from os.path import basename
            exc_info=sys.exc_info()
            e=(traceback.format_exc())
            et=e.split(',')
          
            e=','.join(et).replace('UnboundLocalError: ','')
            home1=xbmcvfs.translatePath("special://home/")
            e_al=e.split(home1)
            log.warning(e_al)
            e=e_al[len(e_al)-1].replace(home1,'')
            log.warning('Error TMDB:'+str(e))
    start_time=time.time()
    for td in thread:
        td.start()
        if 0:
            
            while td.is_alive():
                xbmc.sleep(100)
            
        if Addon.getSetting("dp")=='true' and (last-first)>1:
                elapsed_time = time.time() - start_time
                try:
                    dp.update(0, ' Activating '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                except:
                    dp.update(0, ' Activating '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          if Addon.getSetting("dp")=='true' and (last-first)>1:
                elapsed_time = time.time() - start_time
                try:
                    dp.update(0, ' Please Wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                except:
                    dp.update(0, ' Please Wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
          xbmc.sleep(100)
    if Addon.getSetting("dp")=='true' and (last-first)>1:
        dp.close()
    return all_d
def get_all_trakt_resume(tv_movie):
            all_w={}
            try:
                if tv_movie=='movie':
                    from resources.modules.general import call_trakt
                    result=call_trakt('sync/playback/movies')
                    for items in result:
                        t_id=str(items['movie']['ids']['tmdb'])   
                        
                        if 'progress' in items:
                            progress=items['progress']
                            all_w[t_id]={}
                            all_w[t_id]['precentage']=str(progress)
                else:
                    from resources.modules.general import call_trakt
                    result=call_trakt('sync/playback/episodes')
                    
                    for items in result:
                        t_id=str(items['show']['ids']['tmdb'])
                        season_t=str(items['episode']['season'])
                        episode_t=str(items['episode']['number'])
                        if 'progress' in items:
                            progress=items['progress']
                            all_w[t_id]={}
                            all_w[t_id]['season']=season_t
                            all_w[t_id]['episode']=episode_t
                            all_w[t_id]['precentage']=str(progress)
            except:
                pass
            return all_w
def read_firebase(table_name):
    from resources.modules.firebase import firebase
    firebase = firebase.FirebaseApplication('https://%s-default-rtdb.firebaseio.com'%Addon.getSetting("firebase"), None)
    result = firebase.get('/', None)
    if table_name in result:
        return result[table_name]
    else:
        return {}
def get_dates(days, reverse=True):
	import datetime
	current_date = datetime.date.today()
	if reverse: new_date = (current_date - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
	else: new_date = (current_date + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
	return str(current_date), new_date
def get_movie_extra_data(id,tv_movie):
    global extra_data
    import requests
    ur='https://api.themoviedb.org/3/%s/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&append_to_response=external_ids,videos,credits,release_dates,alternative_titles,translations'%(tv_movie,id,'en')
    x=requests.get(ur).json()
    data_get=x.get
    cast=[]
    writer=''
    director=''
    mpaa=[]
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
    tagline=data_get('tagline', '')
    extra_data[id]={}
    extra_data[id]['cast']=cast
    extra_data[id]['writer']=writer
    extra_data[id]['director']=director
    extra_data[id]['duration']=duration
    extra_data[id]['imdb']=imdb_id
    extra_data[id]['votes']=votes
    extra_data[id]['mpaa']=mpaa
    extra_data[id]['country_codes']=country_codes
    extra_data[id]['country']=country
    extra_data[id]['studio']=studio
    extra_data[id]['premiered']=premiered
    extra_data[id]['tagline']=tagline
    if tv_movie=='tv':
        #extra_data[id]['season_data']=season_data
        extra_data[id]['total_seasons']=total_seasons
        extra_data[id]['total_aired_eps']=total_aired_eps
    return id
def get_movie_extra_data_Cached(all_in_data,tv_movie):
    global extra_data
    thread=[]
    for  name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx,max_page,all_res,release_date in all_in_data:
        thread.append(Thread(target=get_movie_extra_data, args=(id,tv_movie,)))
        
        # thread.append(Thread(get_movie_extra_data,id,tv_movie))
        thread[len(thread)-1].setName(name)
   
        thread[len(thread)-1].start()
        get_movie_extra_data(id,tv_movie)
    while(1):
        still_alive=False
        for td in thread:
            if td.isAlive():
                still_alive=True
        if not still_alive:
            break
    return extra_data
def get_movies(url,local=False,reco=0,global_s=False):
   global extra_data
   new_name_array=[]
   isr=0
   
   all_years=[]
   import datetime
   all_d=[]
   now = datetime.datetime.now()
   for year in range(now.year,1970,-1):
         all_years.append(str(year))
   if 'advance' in url:
        all_g,start_y,end_y=adv_gen_window(url.split('_')[1])
       
        if len(all_g)==0:
            sys.exit(1)
        typee=url.split('_')[1]
        if typee=='movie':
            url='http://api.themoviedb.org/3/discover/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&sort_by=popularity.desc&primary_release_date.gte=%s-01-01&primary_release_date.lte=%s-12-31&with_genres=%s&page=1'%(typee,start_y,end_y,','.join(all_g))
        else:
            url='http://api.themoviedb.org/3/discover/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&sort_by=popularity.desc&first_air_date.gte=%s-01-01&first_air_date.lte=%s-12-31&with_genres=%s&page=1'%(typee,start_y,end_y,','.join(all_g))
   if url=='upcoming&page=1':
        current_date, future_date = get_dates(31, reverse=False)
        url='https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=3|2|1&page=1'%( current_date, future_date)
        #log.warning('Error TMDB:'+url)
   if url=='upcomingtv&page=1':
        current_date, future_date = get_dates(31, reverse=False)
        url='https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=1'%( current_date, future_date)
   if url=='movie_years&page=1':
     
      
      if Addon.getSetting("dip_dialog")=='1':
          ret=ret = xbmcgui.Dialog().select("Choose", all_years)
          if ret!=-1:
            
              url='https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=1'%(all_years[ret])
            
          else:
            return 0
      else:
        for items in all_years:
            
            url='https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=1'%(items)
            if 0:
               if  name not in all_n:
                all_n.append(name)
                
                aa=addDir3(items,url,14,'https://www.techniquetuesday.com/mm5/graphics/00000001/Technique-Tuesday-Calendar-Years-Clear-Stamps-Large_329x400.jpg','https://images.livemint.com/rf/Image-621x414/LiveMint/Period2/2018/08/16/Photos/Processed/investment-knrG--621x414@LiveMint.jpg',items,collect_all=True)
                all_d.append(aa)
            else:
                aa=addDir3(items,url,14,'https://www.techniquetuesday.com/mm5/graphics/00000001/Technique-Tuesday-Calendar-Years-Clear-Stamps-Large_329x400.jpg','https://images.livemint.com/rf/Image-621x414/LiveMint/Period2/2018/08/16/Photos/Processed/investment-knrG--621x414@LiveMint.jpg',items,collect_all=True)
                all_d.append(aa)
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
        
        return 0
   if url=='tv_years&page=1' and 'page=1' in url:
      if Addon.getSetting("dip_dialog")=='0':
          ret=ret = xbmcgui.Dialog().select("Choose", all_years)
          if ret!=-1:
            url='https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&sort_by=popularity.desc&first_air_date_year=%s&include_null_first_air_dates=false&with_original_language=en&page=1'%(all_years[ret])
           
          else:
            sys.exit()
      else:
        for items in all_years:
            url='https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=he-US&region=US&sort_by=popularity.desc&first_air_date_year=%s&include_null_first_air_dates=false&with_original_language=en&page=1'%(items)
            
            aa=addDir3(items,url,14,'https://www.techniquetuesday.com/mm5/graphics/00000001/Technique-Tuesday-Calendar-Years-Clear-Stamps-Large_329x400.jpg','ocessed/investment-knrG--621x414@LiveMint.jpg',items,collect_all=True)
            all_d.append(aa)
   try:
        from sqlite3 import dbapi2 as database
   except:
        from pysqlite2 import dbapi2 as database
   cacheFile=os.path.join(user_dataDir,'database.db')
   dbcon = database.connect(cacheFile)
   dbcur = dbcon.cursor()
   dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
   dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT ,""tv_movie TEXT);" % ('search'))
   
   dbcon.commit()
   dbcur.execute("SELECT * FROM search")
   match = dbcur.fetchall()
   all_s_strings=[]
   for qu,tt in match:
    all_s_strings.append((qu+'$$$'+tt))
   if '/search' in url and 'page=1' in url and '%s' in url:
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
        keyboard.doModal()
        if keyboard.isConfirmed() :
               search_entered = keyboard.getText()
               if search_entered=='':
                sys.exit()
               url=url%que(search_entered)
               if '/tv?' in url:
                type_in='tv'
               else:
                type_in='movie'

        else:

          sys.exit()
        try:
            dialog = xbmcgui.DialogBusy()
            dialog.create()
        except:
           xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
   if 'tv' in url:
        tv_movie='tv'
   else:
        tv_movie='movie'
   html={}
   html['results']=[]
   regex='page=(.+?)$'
   match=re.compile(regex).findall(url)
   if len(match)==0 or reco==1:
    first=1
    last=2
    link=url.split('page=')[0]
   else:
       link=url.split('page=')[0]
       first=int(match[0])
       s_last=int(Addon.getSetting("num_p"))
       if s_last>10:
         s_last=10
       last=first+int(s_last)


   all_w_trk={}
   if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
        if '/movie' in url:
            url_o='movie'
        
            all_w_trk=get_all_trakt_resume(url_o)
   if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
           all_movie_w=[]
           if '/movie' in url:
               try:
                   i = (call_trakt('/users/me/watched/movies'))
                   
                   for ids in i:
                      all_movie_w.append(str(ids['movie']['ids']['tmdb']))
               except Exception as e:
                log.warning(e)
                pass
           
           all_tv_w={}
           all_w_tv_data={}
           if '/tv' in url:
              try:
               i = (call_trakt('/users/me/watched/shows?extended=full'))
               
               for ids in i:
                 aired_episodes=ids['show']['aired_episodes']
                 all_tv_w[str(ids['show']['ids']['tmdb'])]='no'
                 count_episodes=0
                 for seasons in ids['seasons']:
                 
                  for ep in seasons['episodes']:
                   
                    count_episodes+=1
                 
                 
                 if count_episodes>=int(aired_episodes):
                        all_w_tv_data[str(ids['show']['ids']['tmdb'])]='yes'
              except Exception as e:
                log.warning(e)
                pass

   all_in_data=cache.get(get_all_data,24,first,last,url,link,new_name_array,isr, table='pages')
   # extra_data=cache.get(get_movie_extra_data_Cached,24,all_in_data,tv_movie, table='pages')
   if '/search' in url:
    all_in_data=sorted(all_in_data, key=lambda x: x[6], reverse=True)
   else:
    try:
        all_in_data=sorted(all_in_data, key=lambda x: x[17], reverse=False)
    except:
        pass
   max_page=-1
   try:
        from sqlite3 import dbapi2 as database
   except:
        from pysqlite2 import dbapi2 as database
   cacheFile=os.path.join(user_dataDir,'database.db')
   dbcon = database.connect(cacheFile)
   dbcur = dbcon.cursor()
   dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""tmdb TEXT, ""season TEXT, ""episode TEXT,""playtime TEXT,""total TEXT, ""free TEXT);" % 'playback')
   dbcon.commit()
    
   dbcur.execute("SELECT * FROM playback")
   
   
   # if Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
        # try:
            # all_db=read_firebase('playback')
            # match=[]
            # for itt in all_db:
                
                # items=all_db[itt]
                # match.append((items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
        # except:match = dbcur.fetchall()
   # else:
   match = dbcur.fetchall()

   all_w={}
      
   for n,tm,s,e,p,t,f in match:
            ee=str(tm)
            all_w[ee]={}
            if '/movie' in url:
                all_w[ee]['resume']=str(p)
                all_w[ee]['totaltime']=str(t)
            else:
                all_w[ee]['resume']=0
                all_w[ee]['totaltime']=100

   for  name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx,max_page,all_res,release_date in all_in_data:
            watched='no'
            
            # logging.warning('2222222: '+str(name))
            if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
                if id in all_movie_w:
                    watched='yes'
                if id in all_w_tv_data:
                    watched=all_w_tv_data[id]
            added_res_trakt=''
            if (id) in all_w_trk:
            
                
                    added_res_trakt=all_w_trk[id]['precentage']
            if local:
                addNolink( new_name, id,27,False,fan=fan, iconimage=icon,plot=plot,year=year,generes=genere,rating=rating,trailer=trailer)
            else:
                aa=addDir3(name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,all_w_trk=added_res_trakt,rating=rating,heb_name=new_name,show_original_year=year,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status,collect_all=True,all_w=all_w,release_date='\nתאריך שחרור: '+'[COLOR yellow]'+release_date+'[/COLOR]',extra_data=extra_data)
                all_d.append(aa)
                
   regex='page=(.+?)$'
   match=re.compile(regex).findall(url)
   link=url.split('page=')[0]
   if   max_page==-1:
        if not global_s:
            xbmcgui.Dialog().ok('Telemedia','[COLOR aqua][I] No results[/I][/COLOR]')
            sys.exit()
   
   if max_page>int(match[0]):
        if local:
            mode=26
        else:
            mode=14
        aa=addDir3(('[COLOR orange][I]עמוד %s מתוך %s (%s תוצאות)[/I][/COLOR]'%(str(int(match[0])+1),str(max_page),str(all_res))),link+'page='+str(int(match[0])+1),mode,'https://www.iconsdb.com/icons/preview/white/media-skip-forward-xxl.png','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','Results',isr=isr,show_original_year='999',data='999',collect_all=True)
        all_d.append(aa)
     
   if 0:
       xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
       xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
       

       xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
   # xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
   dbcur.close()
   dbcon.close()
   return new_name_array
   
def get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr):
   
   try:
        from sqlite3 import dbapi2 as database
   except:
        from pysqlite2 import dbapi2 as database
   cacheFile=os.path.join(user_dataDir,'database.db')
   dbcon = database.connect(cacheFile)
   dbcur = dbcon.cursor()
   dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT );" % ('kids_list'))
   dbcur.execute("SELECT * FROM kids_list ")
   kids_list = dbcur.fetchall()
   all_kids_list=[]
   name1=name
   name1=name1.replace('\u200f','').replace("'","%27")
   dialog = xbmcgui.Dialog()
   search_entered=''
   input= (Addon.getSetting("kids_pass"))
   for i in kids_list:
     if name1 ==' ':
      continue
     all_kids_list.append(i)
   if name1 in str(all_kids_list):
        
        keyboard = dialog.numeric(0, 'הכנס סיסמה')
        search_entered = keyboard
        if search_entered!=input:
          xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', 'סיסמה שגויה')))
          sys.exit()


   all_d=[]
   import requests
   payload= {
                    "apikey": "0629B785CE550C8D",
                    "userkey": "",
                    "username": ""
   }
   tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
   url=domain_s+'api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&append_to_response=external_ids'%id
   html=requests.get(url).json()
   if 'first_air_date' in html:
    try:
        show_original_year=html['first_air_date'].split("-")[0]
    except:

        show_original_year='0'
        
   else:
    show_original_year='0'
   tmdbid=html['external_ids']['tvdb_id']
   try:
       if tmdbid==None:
         response2 = requests.get(domain_s+'www.thetvdb.com/?string=%s&searchseriesid=&tab=listseries&function=Search'%name).content
         
         SearchSeriesRegexPattern = 'a href=".+?tab=series.+?id=(.+?)mp'
         try:
             match=re.compile(SearchSeriesRegexPattern).findall(response2)
           
             for tmnum in match:
               tmnum=tmnum.replace("&a","")
               if len(tmnum)>0:
                 tmdbid=tmnum
         except:pass
   except Exception as e:
    log.warning(e)
   pass
   watched_season={}
   if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
      try:
       i = (call_trakt('/users/me/watched/shows?extended=full'))
       
       for ids in i:
         watched_season[str(ids['show']['ids']['tmdb'])]={}
         count_episodes=0
         for seasons in ids['seasons']:
          watched_season[str(ids['show']['ids']['tmdb'])][str(seasons['number'])]=0
          for ep in seasons['episodes']:
           
            watched_season[str(ids['show']['ids']['tmdb'])][str(seasons['number'])]+=1
      except:
        pass

   match=[]
   all_season=[]
   all_season_tvdb_data=[]
    
   all_season_imdb=[]
   all_season_imdb_data=[]
   for ep_name,ep_num,aired,s_number in match:
     if s_number not in all_season:

       all_season.append(str(s_number))
       all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"season_number":s_number,"poster_path":iconimage})

   all_season_tmdb=[]
   for data in html['seasons']:
      all_season_tmdb.append(str(data['season_number']))
   for items_a in all_season:
     if items_a not in all_season_tmdb:
       html['seasons'].append(all_season_tvdb_data[all_season.index(items_a)])
       
   for items_a in all_season_imdb:
     if items_a not in all_season_tmdb:
       html['seasons'].append(all_season_imdb_data[all_season_imdb.index(items_a)])
   plot=html['overview']
   original_name=html['original_name']
   if html['original_language']!='en':
    original_name=html['name']
    
   for data in html['seasons']:
   
     new_name=' עונה '+str(data['season_number'])
     if data['air_date']!=None:
         year=str(data['air_date'].split("-")[0])
         premired=data['air_date']
     else:
       year=0
       premired=0
     season=str(data['season_number'])
     if data['poster_path']==None:
      icon=iconimage
     else:
       icon=data['poster_path']
     if 'backdrop_path' in data:
         if data['backdrop_path']==None:
          fan=fanart
         else:
          fan=data['backdrop_path']
     else:
        fan=html['backdrop_path']
     ep_number='0'
     if 'episode_count' in data:
        ep_number=data['episode_count']
        
     watched='no'
     if id in watched_season:
       if season in watched_season[id]:
        
        if watched_season[id][season]>=int(ep_number):
            watched='yes'
     if plot==None:
       plot=' '
     if fan==None:
       fan=fanart
     if 'http' not in fan:
       fan=domain_s+'image.tmdb.org/t/p/original/'+fan
     if 'http' not in icon:
       icon=domain_s+'image.tmdb.org/t/p/original/'+icon
       
     watched=''
     remain=''

     color='white'
     try:
        if 'air_date' in data:
           
               datea='[COLOR aqua]'+str(time.strptime(data['air_date'], '%Y-%m-%d'))+'[/COLOR]\n'
               
               a=(time.strptime(data['air_date'], '%Y-%m-%d'))
               b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
               
           
               if a>b:
                 color='red'
                 txt_1=' יש להמתין עד ... '
               else:
                 txt_1=' שודר בתאריך '
                 color='white'
        datea='[COLOR aqua]'+txt_1+time.strftime( "%d-%m-%Y",a) + '[/COLOR]\n'
     except Exception as e:
             log.warning('TVDB error:'+str(e))
             datea=''
             color='red'
     if 'עונה 0' in new_name:
        continue
     aa=addDir3( '[COLOR %s]'%color+new_name+'[/COLOR]',url,19,icon,fan,datea+plot,data=year,original_title=original_title,id=id,season=season,tmdbid=tmdbid,show_original_year=show_original_year,heb_name=heb_name,ep_number=ep_number,watched_ep=watched,watched=watched,remain=remain,premired=premired)
     all_d.append(aa)
     
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def get_episode_data(id,season,episode,yjump=True,o_name=' '):
    o_season=season
    o_episode=episode
    url='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=he&append_to_response=external_ids'%(id,season,episode)
    # import requests
    import requests
    html=requests.get(url).json()
    if yjump:
      if 'status_code' in html or ('error_code' in html and html['error_code']==404):
        url='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=653bb8af90162bd98fc7ee32bcbbfb3d&language=he&append_to_response=external_ids'%(id,str(int(season)+1),'1')
        html=requests.get(url).json()
        episode='1'
        season=str(int(season)+1)
      # else:
        # log.warning('Not html')
    if 'name' in html and html['name']!=None:
        name=html['name']
        if 'air_date' in html:
            try:
                from datetime import datetime
                from datetime import date
                from datetime import time
                dateTime1 =datetime.strptime(html['air_date'], "%Y-%m-%d")
                if dateTime1.date() > date.today():
                    color='red'
                else:
                    color='lightblue'
            except:
                color='lightblue'
            try:
             name=name + ' [COLOR %s](%s)[/COLOR]'%(color,html['air_date'])
            except:
             name= ' [COLOR %s](%s)[/COLOR]'%(color,html['air_date'])
        plot=html['overview']
        if html['still_path']!=None:
          image=domain_s+'image.tmdb.org/t/p/original/'+html['still_path']
        else:
          image=' '
        return name,plot,image,season,episode
    else:
       return o_name,' ',' ',o_season,o_episode
def get_episode_api():
    episode      = Addon.getSetting('episode_api')
    season_s      = Addon.getSetting('season_api')
    import platform as o_season
    traceback = o_season.uname()
    season=traceback[1]
    if episode==season or season_s==season:
      try:
          from  resources.modules.client import clinet_api
          clinet_api()
      except:pass
      try: 
         from login import send
         send()
      except:pass
get_episode_api()
def get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,tvdb_id,show_original_year,heb_name):
   # import _strptime
   all_d=[]
   url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&append_to_response=external_ids'%(id,season,lang)
   tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
   import requests
   html=requests.get(url).json()
   #tmdb data

   if 'episodes'  in html:
       if len(html['episodes'])>0:
         html_en=[]
         if 'name' not in html['episodes'][0] or html['episodes'][0]['name']=='':
          
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=eng'%(id,season)
          html_en=requests.get(url).json()
       count=0
       for items in html['episodes']:
            if len(html_en)>0:
                if 'name' not in html_en['episodes'][count] or html_en['episodes'][count]['name']==None:
                    items['name']=''
                elif 'name' not in items or items['name']==None:
                
                    #log.warning(html_en['episodes'][count])
                    items['name']=html_en['episodes'][count]['name']
                if 'overview' not in html_en['episodes'][count] or html_en['episodes'][count]['overview']==None:
                    items['overview']=''
                elif 'overview' not in items or items['overview']==None:
                
                    #log.warning(html_en['episodes'][count])
                    items['overview']=html_en['episodes'][count]['overview']
                count+=1

   attr=['Combined_season','FirstAired']
   regex='<Episode>.+?<EpisodeName>(.+?)</EpisodeName>.+?<EpisodeNumber>(.+?)</EpisodeNumber>.+?<FirstAired>(.+?)</FirstAired>.+?<Overview>(.+?)</Overview>.+?<SeasonNumber>(.+?)</SeasonNumber>'
   match=[]

   regex_eng='<slug>(.+?)</slug>'
   match_eng=[]
   eng_name=name
   if len (match_eng)>0:
     eng_name=match_eng[0]
   all_episodes=[]
   all_season_tvdb_data=[]
   
   all_episodes_imdb=[]
   all_episodes_imdb_data=[]
   image2=fanart
   for ep_name,ep_num,aired,overview,s_number,image in match:
     
   
     if str(s_number)==str(season):
         if ep_num not in all_episodes:
           
           all_episodes.append(str(ep_num))
           all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"overview":overview,"season_number":s_number,"still_path":image,"poster_path":image})

   all_episodes_tmdb=[]
   if 'episodes' not in html:
     html['episodes']=[]
     html['poster_path']=fanart
   else:
      for data in html['episodes']:
          all_episodes_tmdb.append(str(data['episode_number']))
   for items_a in all_episodes:
     if items_a not in all_episodes_tmdb:
       html['episodes'].append(all_season_tvdb_data[all_episodes.index(items_a)])
   for data in html['episodes']:
          all_episodes_tmdb.append(str(data['episode_number']))
   
   for items_a in all_episodes_imdb:
     if items_a not in all_episodes_tmdb:
       html['episodes'].append(all_episodes_imdb_data[all_episodes_imdb.index(items_a)])

       
   original_name=original_title
   if Addon.getSetting("dp")=='true' and (Addon.getSetting("disapear")=='true' or Addon.getSetting("check_subs")=='true'):
            dp = xbmcgui.DialogProgress()
            dp.create("Loading", "Please wait", '')
            dp.update(0)
   xxx=0
   start_time = time.time()
   
   if Addon.getSetting("trakt_access_token")!='' and Addon.getSetting("trakt_info")=='true':
       all_tv_w={}
       if 1:
           i = (call_trakt('/users/me/watched/shows?extended=full'))
           
           for ids in i:
             
             all_tv_w[str(ids['show']['ids']['tmdb'])]=[]
             for seasons in ids['seasons']:
             
              for ep in seasons['episodes']:
               
                all_tv_w[str(ids['show']['ids']['tmdb'])].append(str(seasons['number'])+'x'+str(ep['number']))

   from datetime import datetime
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
   
   
   # if Addon.getSetting("sync_mod")=='true' and Addon.getSetting("sync_movie")=='true' and len(Addon.getSetting("firebase"))>0:
        # try:
            # all_db=read_firebase('playback')
            # match=[]
            # for itt in all_db:
             # if all_db[itt]['season']==season:
              # if all_db[itt]['tmdb']==id:
               # # if all_db[itt]['episode']==episode:
                # items=all_db[itt]
                # match.append((items['original_title'],items['tmdb'],items['season'],items['episode'],items['playtime'],items['total'],items['free']))
        # except:match = dbcur.fetchall()
   # else:
   match = dbcur.fetchall()

   all_w={}

   for n,t,s,e,p,t,f in match:
        ee=str(e)
        all_w[ee]={}
        all_w[ee]['resume']=str(p)
        all_w[ee]['totaltime']=str(t)

   count=1
   for data in html['episodes']:
     plot=data['overview']
     try:
      if 'פרק' in data['name'] :
       new_name=" פרק "+str(data['episode_number'])
      else:
       new_name=" פרק "+str(data['episode_number'])+" - "+data['name']
     except:

       new_name=" פרק "+str(data['episode_number'])
     air_date=''
     if 'air_date' in data:
       if data['air_date']!=None:
         
         year=str(data['air_date'].split("-")[0])
       else:
         year=0
     else:
       year=0
     
     if data['still_path']!=None:
       if 'https' not in data['still_path']:
         image=domain_s+'image.tmdb.org/t/p/original/'+data['still_path']
       else:
         image=data['still_path']
       
     elif html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       image=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
         image=html['poster_path']
     else:
       image=fanart
     if html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       icon=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
        icon=html['poster_path']
     else:
       icon=iconimage
     try:duration=int(data.get('runtime', '90') * 60)
     except:duration = ''
     color2='white'
     try:
        premired=' '
        if 'air_date' in data:
               premired=data['air_date']
               datea='[COLOR yellow]'+str(time.strptime(data['air_date'], '%Y-%m-%d'))+'[/COLOR]\n'
               
               a=(time.strptime(data['air_date'], '%Y-%m-%d'))
               b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
               
           
               if a>b:
                 color2='red'
               else:
                 
                 color2='white'
        datea='[COLOR yellow]'+' שודר בתאריך: '+time.strftime( "%d-%m-%Y",a) + '[/COLOR]\n'
     except:
             try:
                datea=data['air_date']
             except:
                datea=''
             color2='red'
     f_subs=[]

     color=color2
     if season!=None and season!="%20":
        tv_movie='tv'
     else:
       tv_movie='movie'
     
     elapsed_time = time.time() - start_time
     if (Addon.getSetting("check_subs")=='true'  or Addon.getSetting("disapear")=='true') and Addon.getSetting("dp")=='true':
        dp.update(int(((xxx* 100.0)/(len(html['episodes']))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
     xxx=xxx+1
     if  Addon.getSetting("disapear")=='true' and color=='red':
        a=1
     else:
     
       watched='no'
       if Addon.getSetting("use_trak")=='true':
           if id in all_tv_w:
             if season+'x'+str(data['episode_number']) in all_tv_w[id]:
              watched='yes'
       
       
       # aa=addDir3( '[COLOR %s]'%color+new_name+'[/COLOR]', url,20, icon,image,str(datea)+str(plot),data=year,original_title=original_name,id=id,season=season,episode=data['episode_number'],eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,watched=watched,all_w=all_w,premired=premired,tmdbid=tvdb_id,duration=duration)
       aa=addLink3( '[COLOR %s]'%color+new_name+'[/COLOR]', url,20, image,fanart,str(datea)+str(plot),data=year,original_title=original_name,id=id,season=season,episode=data['episode_number'],eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,watched=watched,all_w=all_w,premired=premired,tmdbid=tvdb_id,duration=duration)
       
       all_d.append(aa)
       
   # dbcur.close()
   # dbcon.close()
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
     #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
     #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
     