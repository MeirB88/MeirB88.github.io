# -*- coding: utf-8 -*-
import xbmcaddon,xbmc,xbmcgui,xbmcplugin,re,sys,time,xbmcvfs
from .public import addDir3,lang
from threading import Thread
from resources.modules import log
from resources.modules import cache
Addon = xbmcaddon.Addon()
addon_id=Addon.getAddonInfo('id')

def get_html_g():
    try:
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
           html=requests.get(url).json()

           try:
               max_page=html['total_pages']
           except:
               max_page=1
               pass
           try:
            all_res=html['total_results']
           except:
               all_res=1
          
           count=0
           if 'results' in html:
                result_html=html['results']
           else:
               result_html=[html]
           for data in result_html:
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
             if 'title' not in data:
               tv_movie='tv'
               new_name=data['name']
             else:
               tv_movie='movie'
               new_name=data['title']
             f_subs=[]
             if 'original_title' in data:
               original_name=data['original_title']
               mode=270
               
               id=str(data['id'])
               if data['original_language']!='en':
                    html2=requests.get('http://api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id).json()
                    original_name=html2['title']
             else:
                   original_name=data['original_name']
                   id=str(data['id'])
                   mode=271
                   if data['original_language']!='en':
                        html2=requests.get('http://api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id).json()
                        if 'name' in html2:
                            original_name=html2['name']
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
             trailer = "plugin://%s?mode=171&id=%s&url=%s" % (addon_id,id,tv_movie)
             if (new_name+id) not in new_name_array:
              new_name_array.append(new_name+id)
              color='white'
              start_time = time.time()
              elapsed_time = time.time() - start_time
              if  Addon.getSetting("disapear")=='true' and color=='red' and mode!=7:
                a=1
              else:
                color='white'
                watched='no'
                fav_status='false'
                all_d.append((new_name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx,max_page,all_res,release_date))

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
        fav_search_f=''
        fav_servers_en=''
        fav_servers=''
        google_server=''
        rapid_server=''
        direct_server=''
        heb_server=''
        if '/tv/' in url:
             url_g='https://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
             
             html_g=html_g_tv
        else:
             url_g='https://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language='+lang
             html_g=html_g_movie
        thread=[]
        for i in range(first,last):
           url=link+'page='+str(i)
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
            
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          xbmc.sleep(100)
    if Addon.getSetting("dp")=='true' and (last-first)>1:
        dp.close()
    return all_d

def get_movies(url,local=False,reco=0,global_s=False):

   new_name_array=[]
   isr=0
   all_d=[]
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
   all_in_data=cache.get(get_all_data,24,first,last,url,link,new_name_array,isr, table='pages')
   for  name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx,max_page,all_res,release_date in all_in_data:


            aa=addDir3(name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,generes=genere,trailer=trailer,fav_status=fav_status,collect_all=True,release_date='\nתאריך שחרור: '+'[COLOR yellow]'+release_date+'[/COLOR]')
            all_d.append(aa)
   xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
