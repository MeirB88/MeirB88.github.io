# -*- coding: utf-8 -*-
import sys,urllib,json,re
import xbmcgui,xbmcplugin,xbmc,xbmcaddon,xbmcvfs,os
from resources.modules import log
lang=xbmc.getLanguage(0)

Addon = xbmcaddon.Addon()

user_dataDir = xbmcvfs.translatePath(Addon.getAddonInfo("profile"))
try:
    import urllib.parse
except:
    import urlparse

que=urllib.parse.quote_plus
url_encode=urllib.parse.urlencode
save_file=os.path.join(user_dataDir,"fav.txt")
if not xbmcvfs.exists(user_dataDir+'/'):
     os.makedirs(user_dataDir)
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
def meta_get(video_data,item):
    if item=='year' or item=='rating' or item=='votes' or item=='duration':
        return video_data.get(item,'0')
    if item=='country':
        return video_data.get(item,[])
    return video_data.get(item,' ')
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
def addNolink( name, url,mode,isFolder,fan='DefaultFolder.png', iconimage="DefaultFolder.png",plot=' ',year=' ',generes=' ',rating=' ',trailer=' ',original_title=' '):
 

          
            params={}
            params['name']=name
            params['iconimage']=iconimage
            params['fanart']=fan
            params['description']=plot
            params['url']=url
            params['original_title']=original_title
            
            # all_ur=utf8_urlencode(params)
            # u=sys.argv[0]+"?&mode="+str(mode)+'&'+all_ur
            try:
                u=sys.argv[0]+"?&mode="+str(mode)+'&name='+name+'&iconimage='+iconimage+'&fanart='+fan+'&description='+urllib.quote_plus(plot)+'&url='+urllib.quote_plus(url)+'&original_title='+original_title
            except:
                u=sys.argv[0]+"?&mode="+str(mode)+'&name='+name+'&iconimage='+iconimage+'&fanart='+fan+'&description='+urllib.parse.quote_plus(plot)+'&url='+urllib.parse.quote_plus(url)+'&original_title='+original_title
            video_data={}
            video_data['title']=name
            
            
            if year!='':
                video_data['year']=year
            if generes!=' ':
                video_data['genre']=generes
            video_data['rating']=str(rating)
        
            # video_data['poster']=fan
            video_data['plot']=plot
            if trailer!='':
                video_data['trailer']=trailer
            try:
             liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
            except:
             liz = xbmcgui.ListItem( name)
             liz.setArt({'thumb' : iconimage, 'fanart': fan, 'icon': iconimage,'poster': iconimage})
            if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
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
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                
                
            else:
                liz.setInfo( type="Video", infoLabels=video_data)
            liz.setProperty( "Fanart_Image", fan )
            liz.setProperty("IsPlayable","false")
            # art = {}
            # art.update({'poster': iconimage})
            # liz.setArt(art)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################   
def addNolink2( name, url,mode,isFolder,fanart='DefaultFolder.png', iconimage="DefaultFolder.png",plot=' ',year=' ',generes=' ',rating=' ',trailer=' ',original_title=' ',id=' ',season=' ',episode=' ' ,eng_name=' ',show_original_year=' ',dates=' ',dd=' ',dont_place=False):
 


            params={}
            params['name']=name
            params['iconimage']=iconimage
            params['fanart']=fanart
            params['description']=plot.replace("%27","'")
            params['url']=url
            params['original_title']=original_title
            params['id']=id
            params['season']=season
            params['episode']=episode
            params['eng_name']=episode
            params['show_original_year']=show_original_year
            params['dates']=dates
            params['dd']=dd
            menu_items=[]
            
            if mode==146 or mode==15:
                if mode==15:
                    tv_movie='movie'
                else:
                    tv_movie='tv'
                menu_items.append(('[I]Remove from series tracker[/I]', 'RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode=34&name=%s&id=0&season=%s&episode=%s')%(sys.argv[0],original_title,name,season,episode)))
                if len(id)>1:
                    if tv_movie=='tv':
                        tv_mov='tv'
                    else:
                        tv_mov='movie'
                    menu_items.append(('Queue item', 'Action(Queue)' ))
                    menu_items.append(('Trakt manager', 'RunPlugin(%s)' % ('%s?url=%s&mode=150&name=%s&data=%s')%(sys.argv[0],id,original_title,tv_mov) ))
                    menu_items.append(('[I]Trakt watched[/I]', 'RunPlugin(%s)' % ('%s?url=www&original_title=add&mode=65&name=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],tv_movie,id,season,episode))) 
                    
                    menu_items.append(('[I]Trakt unwatched[/I]', 'RunPlugin(%s)' % ('%s?url=www&original_title=remove&mode=65&name=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],tv_movie,id,season,episode))) 
                    
                    type_info='extendedtvinfo'
                    if mode==15:
                        type_info='extendedinfo'
                    menu_items.append(('[I]OpenInfo[/I]','RunScript(script.extendedinfo,info=%s,dbid=,id=%s,name=%s,tvshow=%s,season=%s,episode=%s)'%(type_info,id,original_title,original_title,season,episode)))
            try:
                all_ur=utf8_urlencode(params)
                u=sys.argv[0]+"?&mode="+str(mode)+'&'+all_ur
            except:
                u=sys.argv[0]+"?url="+ urllib.parse.quote_plus(url)+"&name="+name+"&iconimage="+iconimage+"&fanart="+fanart+"&description="+urllib.parse.quote_plus(plot)+"&url="+urllib.parse.quote_plus(url)+"&season="+str(season)+"&episode="+str(episode)+"&mode="+str(mode)+"&original_title="+str(original_title)+"&id="+str(id)+"&dates="+str(dates)
            video_data={}
            video_data['title']=name
            
            
            if year!='':
                video_data['year']=year
            if generes!=' ':
                video_data['genre']=generes
            video_data['rating']=str(rating)
        
            #video_data['poster']=fanart
            video_data['plot']=plot.replace("%27","'")
            if trailer!='':
                video_data['trailer']=trailer
            try:
              liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
            except:
              liz = xbmcgui.ListItem( name)
              liz.setArt({'thumb' : iconimage, 'fanart': fanart, 'icon': iconimage,'poster': iconimage})
            if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
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
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                
                
            else:
                liz.setInfo( type="Video", infoLabels=video_data)
            liz.setProperty( "Fanart_Image", fanart )
            liz.setProperty("IsPlayable","false")
            liz.addContextMenuItems(menu_items, replaceItems=False)
            # art = {}
            # art.update({'poster': iconimage})
            # liz.setArt(art)
            if dont_place:
                return u,liz,False
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)   
def addNolink3( name, url,mode,isFolder,fanart='DefaultFolder.png', iconimage="DefaultFolder.png",plot=' ',all_w_trk='',all_w={},heb_name=' ',data=' ',year=' ',generes=' ',rating=' ',trailer=' ',watched='no',original_title=' ',id=' ',season=' ',episode=' ' ,eng_name=' ',show_original_year=' ',dates=' ',dd=' ',dont_place=False):

            added_pre=''
            if (episode!=' ' and episode!='%20' and episode!=None) :
             
              tv_show='tv'
            else:
                tv_show='movie'
            if '%' in str(episode):
                episode=' '
            if tv_show=='tv':
                ee=str(episode)
            else:
                ee=str(id)
            time_to_save_trk=int(Addon.getSetting("time_to_save"))
            if all_w_trk!='':
                if float(all_w_trk)>=time_to_save_trk:
                    added_pre='  [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
                elif float(all_w_trk)>1:# and float(all_w_trk)<time_to_save_trk:
                    added_pre=' [COLOR yellow][I]'+all_w_trk+'%[/I][/COLOR] \n '
            elif ee in all_w:
                  try:
                    all_w_time=int((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                  except:all_w_time=0
                  if float(all_w_time)>=time_to_save_trk:
                        added_pre=' [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
                  # elif float(all_w_time)>1:# and float(all_w_time)<time_to_save_trk:
                  added_pre=' [COLOR yellow][I]'+str(all_w_time)+'%[/I][/COLOR] \n '
            params={}
            params['name']=name
            params['iconimage']=iconimage
            params['fanart']=fanart
            params['description']=plot.replace("%27","'")
            params['url']=url
            params['data']=data
            params['original_title']=original_title
            params['id']=id
            params['heb_name']=heb_name
            params['season']=season
            params['episode']=episode
            params['eng_name']=original_title
            params['show_original_year']=show_original_year
            params['dates']=dates
            params['dd']=dd
            params['all_w']=json.dumps(all_w)
            menu_items=[]
            
            if mode==179 or mode==20:
                if mode==20:
                    tv_movie='movie'
                else:
                    tv_movie='tv'
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32156), 'RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode=181&name=%s&id=0&season=%s&episode=%s')%(sys.argv[0],que(original_title),que(name),season,episode)))
                menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32163), 'RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode=203&name=%s&id=0&season=%s&episode=%s')%(sys.argv[0],que(original_title),que(name),season,episode)))
                if len(id)>1:
                    if tv_movie=='tv':
                        tv_mov='tv'
                    else:
                        tv_mov='movie'

            all_ur=utf8_urlencode(params)
            u=sys.argv[0]+"?&mode="+str(mode)+'&'+all_ur

            video_data={}
            video_data['title']=name+added_pre.replace('\n','')
            if watched=='yes':
              video_data['playcount']=1
              video_data['overlay']=7
            
            if year!='':
                video_data['year']=year
            if generes!=' ':
                video_data['genre']=generes
            video_data['rating']=str(rating)
        
            #video_data['poster']=fanart
            video_data['plot']=added_pre+plot.replace("%27","'")
            if trailer!='':
                video_data['trailer']=trailer
            liz = xbmcgui.ListItem(name+added_pre.replace('\n',''))
            liz.setArt({'thumb' : iconimage, 'fanart': iconimage, 'icon': iconimage,'poster': iconimage})
            if ee in all_w:
                try:

                    res={}
                    if (float(all_w[ee]['totaltime'])*0.95)<=float(all_w[ee]['resume']):
                         res['wflag']=True
                         
                    else:
                    
                        res['wflag']=False
                    # res['resumetime']=(all_w[ee]['resume'])
                    res['totaltime']=(all_w[ee]['totaltime'])

                    if res:
                        if res['wflag']:
                            video_data['playcount']=1
                            video_data['overlay']=5
                    if res:
                        if not res['wflag']:
                          if res['resumetime']!=None:
                            
                            video_data['playcount']=0
                            video_data['overlay']=0
                            liz.setProperty('ResumeTime', all_w[ee]['resume'])
                            liz.setProperty('TotalTime', all_w[ee]['totaltime'])
                    else:

                      if ee in all_w:
                        liz.setProperty('ResumeTime', all_w[ee]['resume'])
                        liz.setProperty('TotalTime', all_w[ee]['totaltime'])
                except:pass
            '''
            if tv_show=='tv':
                ee=str(episode)
            else:
                ee=str(id)
            if ee in all_w:
            
               liz.setProperty('ResumeTime', all_w[ee]['resume'])
               liz.setProperty('TotalTime', all_w[ee]['totaltime'])
            '''
            if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
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
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                
                
            else:
                liz.setInfo( type="Video", infoLabels=video_data)
            liz.setProperty( "Fanart_Image", fanart )
            liz.setProperty("IsPlayable","false")
            liz.addContextMenuItems(menu_items, replaceItems=False)
            # art = {}
            # art.update({'poster': iconimage})
            # liz.setArt(art)
            if dont_place:
                return u,liz,False
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
def addDir3(name,url,mode,iconimage,fanart,description,premired=' ',image_master='',all_w_trk='',last_id='',video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=0,generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false',collect_all=False,ep_number='',watched_ep='',remain='',groups_id='0',hist='',join_menu=False,menu_leave=False,remove_from_fd_g=False,mark_time=False,all_w={},ct_date='',release_date='',next_page='0',extra_data={},duration=''):
        
        name=name.replace("|",' ')
        description=description.replace("|",' ')
        original_title=original_title.replace("|",' ')
        o_name=name
        if '%' in str(episode):
            episode=' '
        added_pre=''
        if (episode!=' ' and episode!='%20' and episode!=None) :
          tv_movie='tv'
        else:
            tv_movie='movie'
        if '%' in str(episode):
            episode=' '
        if tv_movie=='tv':
            ee=str(episode)
        else:
            ee=str(id)
        time_to_save_trk=int(Addon.getSetting("time_to_save"))
        if all_w_trk!='':
            if float(all_w_trk)>=time_to_save_trk:
                added_pre='  [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
            elif float(all_w_trk)>1:# and float(all_w_trk)<time_to_save_trk:
                added_pre=' [COLOR yellow][I]'+all_w_trk+'%[/I][/COLOR] \n '
        elif ee in all_w:
              try:
               all_w_time=int((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
              except:all_w_time=0
              if mode==20 or mode==15 :
               added_pre='[COLOR yellow][I] - '+str(all_w_time)+'% [/I][/COLOR]\n'

        u=sys.argv[0]+"?mode="+str(mode)+"&iconimage="+iconimage+"&fanart="+fanart+"&description="+ urllib.parse.quote_plus(description)+"&url="+ urllib.parse.quote_plus(url)+"&name="+urllib.parse.quote_plus(name)+"&image_master="+(image_master)+"&heb_name="+urllib.parse.quote_plus(heb_name)+"&last_id="+(last_id)+"&dates="+(dates)+"&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)+"&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)+"&fav_status="+fav_status+"&groups_id="+groups_id+"&next_page="+next_page
        ok=True
        show_sources=True
        
        if mode==20:
            if Addon.getSetting("one_click")=='true':
                if Addon.getSetting("sh_one_click")=='false':
                   show_sources=False
        if mode==15:
            # if Addon.getSetting("one_click")=='true':
                # if Addon.getSetting("sh_one_click")=='false':
                if Addon.getSetting("new_source")=='true':
                   show_sources=False
        if mode==258:
                   show_sources=False
        if mode==270:
                   show_sources=False
        if mode==271:
                   show_sources=False
        if mode==273:
                   show_sources=False
        if mode==274:
                   show_sources=False

        menu_items=[]
        if mode==20 or mode==15:
          menu_items.append(('%s'%'נגן דרך הבוט - חד פעמי', 'RunPlugin(%s?mode=191&url=www)' % sys.argv[0] ))
          menu_items.append(('%s'%'הפעל\בטל - ניגון קבוע דרך הבוט', 'RunPlugin(%s?mode=211&url=www)' % sys.argv[0] ))
        if mode==15:
            menu_items.append(('[I]%s[/I]'%'סמן נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=194&original_title=%s&id=%s')%(sys.argv[0],original_title,id))) 
            menu_items.append(('[I]%s[/I]'%'הסר נצפה / הסר מרשימת הצפיה', 'RunPlugin(%s)' % ('%s?url=www&mode=192&heb_name=%s&original_title=%s&id=%s')%(sys.argv[0],que(heb_name),original_title,id))) 
            menu_items.append(('[I]%s[/I]'%'הוסף לבקרת הורים', 'RunPlugin(%s)' % ('%s?url=%s&mode=208&name=%s')%(sys.argv[0],id,que(name))))
            menu_items.append(('[I]%s[/I]'%'הסר מבקרת הורים', 'RunPlugin(%s)' % ('%s?url=%s&mode=209&name=%s')%(sys.argv[0],id,que(name))))
        if mode==20 :
            menu_items.append(('[I]%s[/I]'%'סמן נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=195&original_title=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],original_title,id,season,episode))) 
            menu_items.append(('[I]%s[/I]'%'הסר נצפה / הסר מרשימת הצפיה', 'RunPlugin(%s)' % ('%s?url=www&mode=193&original_title=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],original_title,id,season,episode))) 
        if mode==196 :
            menu_items.append(('[I]%s[/I]'%'הסר מהיסטוריה', 'RunPlugin(%s)' % ('%s?url=www&mode=255&name=%s&clean_all=%s')%(sys.argv[0],que(name),'false'))) 
            menu_items.append(('[I]%s[/I]'%'הסר את כל ההיסטוריה', 'RunPlugin(%s)' % ('%s?url=www&mode=255&name=%s&clean_all=%s')%(sys.argv[0],que(name),'true'))) 
        if 0:# Addon.getSetting("sync_mod")=='true':
            menu_items.append(('%s'%'רענן סנכרון', 'RunPlugin(%s?mode=189&url=www)' % sys.argv[0] ))
        menu_items.append(('%s'%Addon.getLocalizedString(32063), 'Action(Info)'))
        menu_items.append(('%s'%'הגדרות הרחבה קוברה', 'RunPlugin(%s?mode=279&url=www)' % sys.argv[0] ))
        menu_items.append(('%s'%'הגדרות הרחבה טלמדיה', 'RunPlugin(%s?mode=174&url=www)' % sys.argv[0] ))
        menu_items.append(('[I]%s[/I]'%'מתי יגיע לרשת?', 'RunPlugin(%s)' % ('%s?url=%s&mode=280&name=%s&iconimage=%s&fanart=%s')%(sys.argv[0],id,que(name),iconimage,fanart)))
        # menu_items.append(('%s'%'מתי יגיע לרשת?', 'RunPlugin(%s)' % ('%s?url=%s&mode=280')%(sys.argv[0],que(name))))

        if remove_from_fd_g:
            #Remove from FD groups
           menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32082), 'RunPlugin(%s)' % ('%s?url=%s&mode=35&name=%s')%(sys.argv[0],url,urllib.parse.quote_plus(name))))
        if join_menu:
            #join Channel
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32062), 'RunPlugin(%s)' % ('%s?url=%s&mode=22&name=join')%(sys.argv[0],url)))
        if menu_leave:
            #Leave Channel
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32031), 'RunPlugin(%s)' % ('%s?url=%s&mode=23&name=%s')%(sys.argv[0],url,que(name))))
        
        if mode==16:
            #Remove
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32056), 'RunPlugin(%s)' % ('%s?url=%s&mode=29&name=%s')%(sys.argv[0],url,name)))
        if mode==16:

            menu_items.append(('[I]%s[/I]'%'הוסף לבקרת הורים', 'RunPlugin(%s)' % ('%s?url=%s&mode=208&name=%s')%(sys.argv[0],id,urllib.parse.quote_plus(name))))
            menu_items.append(('[I]%s[/I]'%'הסר מבקרת הורים', 'RunPlugin(%s)' % ('%s?url=%s&mode=209&name=%s')%(sys.argv[0],id,urllib.parse.quote_plus(name))))
        if mode==2:

           menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32080), 'RunPlugin(%s)' % ('%s?url=%s&mode=34&name=%s&data=%s&iconimage=%s&fanart=%s&description=%s')%(sys.argv[0],url,urllib.parse.quote_plus(name),data,iconimage,fanart,urllib.parse.quote_plus(description))))
           menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32164), 'RunPlugin(%s)' % ('%s?url=%s&mode=268&name=%s&data=%s&iconimage=%s&fanart=%s&description=%s')%(sys.argv[0],url,urllib.parse.quote_plus(name),data,iconimage,fanart,urllib.parse.quote_plus(description))))
           
        if mode==263:
           menu_items.append(('%s'%'נגן דרך הבוט - חד פעמי', 'RunPlugin(%s?mode=191&url=www)' % sys.argv[0] ))
           menu_items.append(('%s'%'הפעל\בטל - ניגון קבוע דרך הבוט', 'RunPlugin(%s?mode=211&url=www)' % sys.argv[0] ))

           
           
        if mark_time:
            if Addon.getSetting("remove_resume_time")=='true':
                menu_items.append(('[I]%s[/I]'%'הסר נקודת ניגון', 'RunPlugin(%s)' % ('%s?url=www&mode=160&name=%s&id=%s&season=%s&episode=%s&data=%s')%(sys.argv[0],name,id,season,episode,tv_movie))) 
        if mode==15:
            if tv_movie=='movie':
                se='one_click'
                
            else:
                se='one_click_tv'
            menu_items.append(('[I]%s[/I]'%'הצג רשימת שחקנים', 'ActivateWindow(10025,"%s?mode=168&url=%s&id=%s&season=%s&episode=%s",return)'  % ( sys.argv[0] ,tv_movie,id,season,episode)))
        video_data={}
        video_data['title']=name
        if (episode!=' ' and episode!='%20' and episode!=None) :
          video_data['mediatype']='episode'
          video_data['TVshowtitle']=original_title
          video_data['Season']=int(str(season).replace('%20','0'))
          video_data['Episode']=int(str(episode).replace('%20','0'))
          if premired!=' ':
            video_data['premiered']=premired
          tv_show='tv'
        else:

           video_data['label']=original_title
           video_data['OriginalTitle']=original_title
           video_data['imdbnumber']=id
           video_data['imdbid']=id
           video_data['year']=show_original_year
           video_data['mediatype']='movie'
           video_data['TVshowtitle']=''
           tv_show='movie'
        if  mode==7:
            tv_show='tv'
        video_data['OriginalTitle']=original_title
        if data!=' ':
            video_data['year']=data
        if generes!=' ':
            video_data['genre']=generes
        video_data['rating']=str(rating)
        video_data['plot']=description+ release_date
        release_date2=release_date+' 00:00:00'
        video_data['dateadded']=release_date2
        if ct_date!='':
            video_data['date']=ct_date
        if trailer!=' ':
            video_data['trailer']=trailer
        try:
            str_e1=list(u.encode('utf8'))
            for i in range(0,len(str_e1)):
               str_e1[i]=str(ord(str_e1[i]))
            str_e='$$'.join(str_e1)
        except:pass
        if video_info!={}:
            
            video_data=video_info
        if watched=='yes':
          video_data['playcount']=1
          video_data['overlay']=7
        if ee in all_w:
            name=name.replace('[COLOR white]','[COLOR lightblue]')
            video_data['title']=name+added_pre.replace('\n','') 
        liz=xbmcgui.ListItem(offscreen=True)
        liz.setLabel(name+added_pre.replace('\n',''))
        liz.setArt({'thumb' : iconimage, 'fanart': iconimage, 'icon': iconimage,'poster': iconimage})
        try:
            res={}
            if ee in all_w:
                 if (float(all_w[ee]['totaltime'])*0.95)<=float(all_w[ee]['resume']):
                     res['wflag']=True
                 else:
                    res['wflag']=False
                 res['resumetime']=(all_w[ee]['resume'])
                 res['totaltime']=(all_w[ee]['totaltime'])
            if res:
                if res['wflag']:
                    video_data['playcount']=1
                    video_data['overlay']=5
            if res:
                if not res['wflag']:
                  if res['resumetime']!=None:
                    video_data['playcount']=0
                    video_data['overlay']=0
                    if mode==20:
                        liz.setProperty('ResumeTime', all_w[ee]['resume'])
                    liz.setProperty('TotalTime', all_w[ee]['totaltime'])
            else:
             if ee in all_w:
                liz.setProperty('ResumeTime', all_w[ee]['resume'])
                liz.setProperty('TotalTime', all_w[ee]['totaltime'])
        except:pass
        if ep_number!='':
            liz.setProperty('totalepisodes', str(ep_number))
        if watched_ep!='':
           liz.setProperty('watchedepisodes', str(watched))
        if remain!='':
            liz.setProperty('unwatchedepisodes',str(remain))
        all_v_data=json.dumps(video_data)
        params={}
        params['video_data']=all_v_data
        try:
            all_ur=utf8_urlencode(params)
            u=u+'&'+all_ur
        except:pass
        video_data['title']=video_data['title'].replace("|",' ')
        video_data['plot']=video_data['plot'].replace("|",' ')
        if len(id)>1:
            tt='Video'
        else:
            tt='Files'
        video_data['id']=id
        cast=[]

        if KODI_VERSION>19:
            info_tag = liz.getVideoInfoTag()
            info_tag.setMediaType(meta_get(video_data,'mediatype'))
            info_tag.setTitle(meta_get(video_data,'title'))
            info_tag.setPlot(meta_get(video_data,'plot'))
            try:
                year_info=int(meta_get(video_data,'year'))
                if (year_info>0):
                    info_tag.setYear(year_info)
            except:
                pass
            info_tag.setRating(float(meta_get(video_data,'rating')))
            info_tag.setVotes(int(meta_get(video_data,'votes')))
            info_tag.setMpaa(meta_get(video_data,'mpaa'))
            info_tag.setDuration(int(meta_get(video_data,'duration')))
            info_tag.setCountries(meta_get(video_data,'country'))
            
            info_tag.setTrailer(meta_get(video_data,'trailer'))
            info_tag.setPremiered(meta_get(video_data,'premiered'))
            info_tag.setTagLine(meta_get(video_data,'tagline'))
            info_tag.setStudios((meta_get(video_data,'studio') or '',))
            info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
            info_tag.setGenres(meta_get(video_data,'genre').split(', '))
            info_tag.setWriters(meta_get(video_data,'writer').split(', '))
            info_tag.setDirectors(meta_get(video_data,'director').split(', '))
            # if ee in all_w:
            
                # info_tag.setResumePoint(float(all_w[ee]['resume']),float(all_w[ee]['totaltime']))
        else:
            liz.setInfo( type="Video", infoLabels=video_data)
        liz.setProperty( "Fanart_Image", fanart )
        liz.addContextMenuItems(menu_items, replaceItems=False)
        return u,liz,show_sources

def addLink( name, url,mode,isFolder, iconimage,fanart,description,data='',rating='',generes='',no_subs='0',tmdb='0',season='0',episode='0',original_title='',da='',year=0,all_w={},in_groups=False):
          name=name.replace("|",' ')
          description=description.replace("|",' ')
          menu_items=[]
          params={}
          params['name']=name
          params['iconimage']=iconimage
          params['fanart']=fanart
          params['description']=description
          params['url']=url
          params['no_subs']=no_subs
          params['season']=season
          params['episode']=episode
          params['mode']=mode
          params['original_title']=original_title
          params['id']=tmdb
          # params['dd']=dd
          params['data']=data
          # params['nextup']='false'
          try:
            all_ur=utf8_urlencode(params)

            u=sys.argv[0]+"?"+'&'+all_ur
          except:
            u=sys.argv[0]+"?url="+ urllib.parse.quote_plus(url)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+iconimage+"&fanart="+fanart+"&description="+urllib.parse.quote_plus(description)+"&url="+urllib.parse.quote_plus(url)+"&no_subs="+str(no_subs)+"&season="+str(season)+"&episode="+str(episode)+"&mode="+str(mode)+"&original_title="+str(original_title)+"&id="+str(tmdb)+"&data="+str(data)
 
          video_data={}
          video_data['title']=name
            
            
          if year!='':
                video_data['year']=year
          if generes!='':
                video_data['genre']=generes
          if rating!=0:
            video_data['rating']=str(rating)
        
          # video_data['poster']=fanart
          video_data['plot']=description
          f_text_op=Addon.getSetting("filter_text")
          filer_text=False
          if len(f_text_op)>0:
                filer_text=True
                if ',' in f_text_op:
                    all_f_text=f_text_op.split(',')
                else:
                    all_f_text=[f_text_op]
            
          if filer_text:
            for items_f in all_f_text:
                if items_f.lower() in name.lower():
                    return 0
          #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          try:
           liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
          except:
           liz = xbmcgui.ListItem( name)
           liz.setArt({'thumb' : iconimage, 'fanart': fanart, 'icon': iconimage,'poster': iconimage})
           
           
           menu_items.append(('%s'%'הגדרות הרחבה', 'RunPlugin(%s?mode=174&url=www)' % sys.argv[0] ))
           menu_items.append(('%s'%'נגן דרך הבוט - חד פעמי', 'RunPlugin(%s?mode=191&url=www)' % sys.argv[0] ))
           menu_items.append(('%s'%'הפעל\בטל - ניגון קבוע דרך הבוט', 'RunPlugin(%s?mode=211&url=www)' % sys.argv[0] ))
           
          if in_groups:
              ee=str(name).replace("'","%27")#.encode('base64')
              
             
              if ee in all_w:
                if original_title=='':
                  original_title=name
                video_data['playcount']=0
                video_data['overlay']=0
                video_data['title']='[COLOR lightblue]'+original_title+'[/COLOR]'
                # liz.setProperty('ResumeTime', all_w[ee]['resume'])
                # liz.setProperty('TotalTime', all_w[ee]['totaltime'])
                try:
                    if Addon.getSetting("filter_watched")=='true':
                        time_to_filter=float(Addon.getSetting("filter_watched_time"))
                        pre_time=float((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                        if pre_time>time_to_filter:
                            return 0
                except:
                    pass

          if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
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
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
          else:
                liz.setInfo( type="Video", infoLabels=video_data)
          # art = {}
          # art.update({'poster': iconimage})
          # liz.setArt(art)
          # liz.setProperty("IsPlayable","false")
          # liz.setProperty( "Fanart_Image", fanart )
          
          liz.addContextMenuItems(menu_items, replaceItems=False)
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
def addLink2( name, url,mode,isFolder, iconimage,fanart,description,place_control=False,data='',rating='',generes='',no_subs='0',tmdb='0',season='0',episode='0',original_title='',da='',year=0,all_w={},dd='',in_groups=False):
          name=name.replace("|",' ')
          description=description.replace("|",' ')
          episode=episode.replace('%20',' ')
          season=season.replace('%20',' ')

          params={}
          params['name']=name
          params['iconimage']=iconimage
          params['fanart']=fanart
          params['description']=description
          params['url']=url
          params['no_subs']=no_subs
          params['season']=season
          params['episode']=episode
          params['mode']=mode
          params['original_title']=original_title
          params['id']=tmdb
          params['dd']=dd
          params['data']=data
          params['nextup']='false'
          
          all_ur=utf8_urlencode(params)

          u=sys.argv[0]+"?"+'&'+all_ur
 

          video_data={}
          video_data['title']=name
            
            
          if year!='':
                video_data['year']=year
          if generes!='':
                video_data['genre']=generes
          if rating!=0:
            video_data['rating']=str(rating)
        
          #video_data['poster']=fanart
          video_data['plot']=description
          f_text_op=Addon.getSetting("filter_text")
          filer_text=False
          if len(f_text_op)>0:
                filer_text=True
                if ',' in f_text_op:
                    all_f_text=f_text_op.split(',')
                else:
                    all_f_text=[f_text_op]
            
          if filer_text:
            for items_f in all_f_text:
                if items_f.lower() in name.lower():
                    return 0
          try:
            liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
          except:
            liz = xbmcgui.ListItem( name)
            liz.setArt({'thumb' : iconimage, 'fanart': fanart, 'icon': iconimage})
          menu_items=[]
          if Addon.getSetting("set_view_type")=='true':
            menu_items.append(('[I]Set view type[/I]', 'RunPlugin(%s)' % ('%s?url=%s&mode=167')%(sys.argv[0],str(pre_mode))))
          if mode==170:
            menu_items.append(('[I]Remove from history[/I]', 'RunPlugin(%s)' % ('%s?name=%s&url=www&id=%s&mode=171')%(sys.argv[0],name,tmdb)))
          liz.addContextMenuItems(menu_items, replaceItems=False)
          if in_groups:
              ee=str(name).replace("'","%27")#.encode('base64')
              
             
              if ee in all_w:
                
                video_data['playcount']=0
                video_data['overlay']=0
                video_data['title']='[COLOR lightblue]'+original_title+'[/COLOR]'
                liz.setProperty('ResumeTime', all_w[ee]['resume'])
                liz.setProperty('TotalTime', all_w[ee]['totaltime'])
                try:
                    if Addon.getSetting("filter_watched")=='true':
                        time_to_filter=float(Addon.getSetting("filter_watched_time"))
                        pre_time=float((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
                        if pre_time>time_to_filter:
                            return 0
                except:
                    pass
          if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
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
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                
                
          else:
                liz.setInfo( type="Video", infoLabels=video_data)
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )
          if place_control:
            return u,liz,False
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
def addLink3(name,url,mode,iconimage,fanart,description,premired=' ',image_master='',all_w_trk='',last_id='',video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=0,generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false',collect_all=False,ep_number='',watched_ep='',remain='',groups_id='0',hist='',join_menu=False,menu_leave=False,remove_from_fd_g=False,mark_time=False,all_w={},ct_date='',release_date='',from_seek=False,extra_data={},duration=''):
        # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', release_date)))
        name=name.replace("|",' ')
        description=description.replace("|",' ')
        original_title=original_title.replace("|",' ')
        if '%' in str(episode):
            episode=' '
        added_pre=''
        if (episode!=' ' and episode!='%20' and episode!=None) :
          tv_movie='tv'
        else:
            tv_movie='movie'
        if '%' in str(episode):
            episode=' '
        if tv_movie=='tv':
            ee=str(episode)
        else:
            ee=str(id)
        time_to_save_trk=int(Addon.getSetting("time_to_save"))
        if all_w_trk!='':
            if float(all_w_trk)>=time_to_save_trk:
                added_pre='  [COLOR yellow][I]'+'√'+'[/I][/COLOR] \n '
            elif float(all_w_trk)>1:# and float(all_w_trk)<time_to_save_trk:
                added_pre=' [COLOR yellow][I]'+all_w_trk+'%[/I][/COLOR] \n '
        elif ee in all_w:
              try:
               all_w_time=int((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
              except:all_w_time=0
              if mode==20 or mode==15 :
               added_pre='[COLOR yellow][I] - '+str(all_w_time)+'% [/I][/COLOR]\n'


        u=sys.argv[0]+"?mode="+str(mode)+"&iconimage="+iconimage+"&fanart="+fanart+"&description="+ urllib.parse.quote_plus(description)+"&url="+ urllib.parse.quote_plus(url)+"&name="+urllib.parse.quote_plus(name)+"&image_master="+(image_master)+"&heb_name="+urllib.parse.quote_plus(heb_name)+"&last_id="+(last_id)+"&dates="+(dates)+"&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)+"&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)+"&fav_status="+fav_status+"&groups_id="+groups_id

        ok=True
        show_sources=True
        
        if mode==20:
            if Addon.getSetting("one_click")=='true':
                if Addon.getSetting("sh_one_click")=='false':
                   show_sources=False
        if mode==15:
            # if Addon.getSetting("one_click")=='true':
                # if Addon.getSetting("sh_one_click")=='false':
                if Addon.getSetting("new_source")=='true':
                
                   show_sources=False

        # try:
            # str_e1=list(u.encode('utf8'))
            # for i in range(0,len(str_e1)):
               # str_e1[i]=str(ord(str_e1[i]))
            # str_e='$$'.join(str_e1)
        # except:pass
        menu_items=[]
        if mode==20 or mode==15:
          menu_items.append(('%s'%'נגן דרך הבוט - חד פעמי', 'RunPlugin(%s?mode=191&url=www)' % sys.argv[0] ))
          menu_items.append(('%s'%'הפעל\בטל - ניגון קבוע דרך הבוט', 'RunPlugin(%s?mode=211&url=www)' % sys.argv[0] ))
        if mode==15:
            menu_items.append(('[I]%s[/I]'%'סמן נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=194&original_title=%s&id=%s')%(sys.argv[0],original_title,id))) 
            menu_items.append(('[I]%s[/I]'%'הסר נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=192&original_title=%s&id=%s')%(sys.argv[0],original_title,id))) 
            
        if mode==20 :
            menu_items.append(('[I]%s[/I]'%'סמן נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=195&original_title=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],original_title,id,season,episode))) 
            menu_items.append(('[I]%s[/I]'%'הסר נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=193&original_title=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],original_title,id,season,episode))) 
        if 0:# Addon.getSetting("sync_mod")=='true':
            menu_items.append(('%s'%'רענן סנכרון', 'RunPlugin(%s?mode=189&url=www)' % sys.argv[0] ))
        menu_items.append(('%s'%Addon.getLocalizedString(32063), 'Action(Info)'))
        menu_items.append(('%s'%'הגדרות הרחבה', 'RunPlugin(%s?mode=174&url=www)' % sys.argv[0] ))
        if remove_from_fd_g:
            #Remove from FD groups
           menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32082), 'RunPlugin(%s)' % ('%s?url=%s&mode=35&name=%s')%(sys.argv[0],url,urllib.parse.quote_plus(name))))
        if join_menu:
            #join Channel
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32062), 'RunPlugin(%s)' % ('%s?url=%s&mode=22&name=join')%(sys.argv[0],url)))
        if menu_leave:
            #Leave Channel
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32031), 'RunPlugin(%s)' % ('%s?url=%s&mode=23&name=%s')%(sys.argv[0],url,que(name))))
        
        if mode==16:
            #Remove
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32056), 'RunPlugin(%s)' % ('%s?url=%s&mode=29&name=%s')%(sys.argv[0],url,name)))
        if mode==16:
            #add to my TV
            menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32069), 'RunPlugin(%s)' % ('%s?url=%s&mode=27&name=%s&data=%s&iconimage=%s&fanart=%s&description=%s')%(sys.argv[0],id,name,data,iconimage,fanart,description)))
        if mode==2:
           menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32080), 'RunPlugin(%s)' % ('%s?url=%s&mode=34&name=%s&data=%s&iconimage=%s&fanart=%s&description=%s')%(sys.argv[0],url,urllib.parse.quote_plus(name),data,iconimage,fanart,urllib.parse.quote_plus(description))))
           menu_items.append(('[I]%s[/I]'%Addon.getLocalizedString(32164), 'RunPlugin(%s)' % ('%s?url=%s&mode=268&name=%s&data=%s&iconimage=%s&fanart=%s&description=%s')%(sys.argv[0],url,urllib.parse.quote_plus(name),data,iconimage,fanart,urllib.parse.quote_plus(description))))
        if mark_time:
            if Addon.getSetting("remove_resume_time")=='true':
                menu_items.append(('[I]%s[/I]'%'הסר נקודת ניגון', 'RunPlugin(%s)' % ('%s?url=www&mode=160&name=%s&id=%s&season=%s&episode=%s&data=%s')%(sys.argv[0],name,id,season,episode,tv_movie))) 
        if mode==15:
            if tv_movie=='movie':
                se='one_click'
                
            else:
                se='one_click_tv'
            # menu_items.append(('[I]הוספה לסרטים שלי[/I]', 'RunPlugin(%s)' % ('%s?url=www&description=%s&mode=164')%(sys.argv[0],str_e)))
            menu_items.append(('[I]%s[/I]'%'הצג רשימת שחקנים', 'ActivateWindow(10025,"%s?mode=168&url=%s&id=%s&season=%s&episode=%s",return)'  % ( sys.argv[0] ,tv_movie,id,season,episode)))
        video_data={}

        # info = {'title': id, 'season': season, 'episode': episode}
        video_data['title']=name
        
        if (episode!=' ' and episode!='%20' and episode!=None) :
          video_data['mediatype']='episode'
          video_data['TVshowtitle']=original_title
          video_data['Season']=int(str(season).replace('%20','0'))
          video_data['Episode']=int(str(episode).replace('%20','0'))
          if premired!=' ':
            video_data['premiered']=premired
          tv_show='tv'
        if mode==19 or mode==16:
         tv_show='tv'
         video_data['year']=show_original_year

        else:

           video_data['label']=original_title
           video_data['OriginalTitle']=original_title
           video_data['imdbnumber']=id
           video_data['imdbid']=id
           video_data['year']=show_original_year
           video_data['mediatype']='movie'
           video_data['TVshowtitle']=''
           tv_show='movie'
        
        if  mode==7:
            tv_show='tv'
        video_data['OriginalTitle']=original_title
        if data!=' ':
            video_data['year']=data
        if generes!=' ':
            video_data['genre']=generes
        video_data['rating']=str(rating)
        # video_data['period']='02:50:00'
        # video_data['poster']=str(fanart)
        # if mode==15 or mode==16:
          # datetime=' \n[COLOR yellow]תאריך שחרור: [/COLOR]'+ release_date
        # else :
         # datetime=''
        video_data['plot']=description+ release_date
        release_date2=release_date+' 00:00:00'
        video_data['dateadded']=release_date2
        if ct_date!='':
            video_data['date']=ct_date
        if trailer!=' ':
            video_data['trailer']=trailer
        try:
            str_e1=list(u.encode('utf8'))
            for i in range(0,len(str_e1)):
               str_e1[i]=str(ord(str_e1[i]))
            str_e='$$'.join(str_e1)
        except:pass
        if video_info!={}:
            
            video_data=video_info
        if watched=='yes':
          video_data['playcount']=1
          video_data['overlay']=7
        if ee in all_w:

            name=name.replace('[COLOR white]','[COLOR lightblue]')
            video_data['title']=name+added_pre.replace('\n','')
        try:
            liz=xbmcgui.ListItem(name+added_pre.replace('\n',''), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        except:

            liz=xbmcgui.ListItem(offscreen=True)
            liz.setLabel(name+added_pre.replace('\n',''))
            liz.setArt({'thumb' : iconimage, 'fanart': fanart, 'icon': iconimage,'poster': iconimage})
        try:

            res={}
            if ee in all_w:
                 if (float(all_w[ee]['totaltime'])*0.95)<=float(all_w[ee]['resume']):
                     res['wflag']=True
                     
                 else:
                
                    res['wflag']=False
                 # res['resumetime']=(all_w[ee]['resume'])
                 # res['totaltime']=(all_w[ee]['totaltime'])

            if res:
                if res['wflag']:
                    video_data['playcount']=1
                    video_data['overlay']=5
            if res:
                if not res['wflag']:
                  if res['resumetime']!=None:
                    
                    video_data['playcount']=0
                    video_data['overlay']=0
                    if mode==20:
                     liz.setProperty('ResumeTime', all_w[ee]['resume'])
                    liz.setProperty('TotalTime', all_w[ee]['totaltime'])
            else:

             if ee in all_w:
                liz.setProperty('ResumeTime', all_w[ee]['resume'])
                liz.setProperty('TotalTime', all_w[ee]['totaltime'])
        except:pass

        if ep_number!='':
            # log.warning('ep_number:'+str(ep_number))
            liz.setProperty('totalepisodes', str(ep_number))

        if watched_ep!='':
           # log.warning('watched_ep:'+ str(watched))
           liz.setProperty('watchedepisodes', str(watched))
                
        
        if remain!='':
            # log.warning('remain:'+ str(remain))
            liz.setProperty('unwatchedepisodes',str(remain))
        all_v_data=json.dumps(video_data)
        params={}
        params['video_data']=all_v_data
        try:
            all_ur=utf8_urlencode(params)
            u=u+'&'+all_ur
        except:pass
        # art = {}
        # art.update({'poster': iconimage})
        
        # liz.setArt(art)
        video_data['title']=video_data['title'].replace("|",' ')
        video_data['plot']=video_data['plot'].replace("|",' ')
        # video_streaminfo = {'codec': 'h264'}
                
        if len(id)>1:
            
            tt='Video'
        else:
            tt='Files'
        video_data['id']=id
        cast=[]
        imdb_id=''
        total_seasons, total_aired_eps ='',''
        if (extra_data!={}):
            meta_ge=extra_data[id].get
            total_seasons, total_aired_eps = meta_ge('total_seasons'), meta_ge('total_aired_eps')
            extra_data[id]['total_seasons']=''
            extra_data[id]['total_aired_eps']=''
            imdb_id=extra_data[id]['imdb']
            cast=extra_data[id]['cast']
            extra_data[id]['cast']=[]
            video_data.update(extra_data[id])
        video_data.pop('imdb', None)
        video_data.pop('id', None)
        video_data.pop('total_aired_eps', None)
        video_data.pop('country_codes', None)
        video_data.pop('total_seasons', None)
        if duration!='':
            video_data['duration']=duration

        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "id", id )
        liz.setCast(cast)
        liz.setUniqueIDs({'imdb': imdb_id, 'tmdb': str(id)})
        if total_aired_eps!='':
            liz.setProperty('totalepisodes', str(total_aired_eps))
        if total_seasons!='':
            liz.setProperty('totalseasons', str(total_seasons))
        if len(id)>1:
         
            if '/tv' in url or '/shows' in url:
                tv_mov='tv'
            else:
                tv_mov='movie'

            if Addon.getSetting("trakt_manager")=='true':
                menu_items.append(('ניהול טרקאט', 'RunPlugin(%s)' % ('%s?url=%s&mode=187&name=%s&data=%s')%(sys.argv[0],id,original_title,tv_mov) ))
            if Addon.getSetting("trakt_watched")=='true':
                menu_items.append(('[I]%s[/I]'%'נצפה טראקט', 'RunPlugin(%s)' % ('%s?url=www&original_title=add&mode=188&name=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],tv_show,id,season,episode))) 
            if Addon.getSetting("trakt_unwatched")=='true':
                menu_items.append(('[I]%s[/I]'%'לא נצפה טראקט', 'RunPlugin(%s)' % ('%s?url=www&original_title=remove&mode=188&name=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],tv_show,id,season,episode))) 
        if KODI_VERSION>19:
            info_tag = liz.getVideoInfoTag()
            info_tag.setMediaType(meta_get(video_data,'mediatype'))
            info_tag.setTitle(meta_get(video_data,'title'))
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
            info_tag.setTagLine(meta_get(video_data,'tagline'))
            info_tag.setStudios((meta_get(video_data,'studio') or '',))
            info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
            info_tag.setGenres(meta_get(video_data,'genre').split(', '))
            info_tag.setWriters(meta_get(video_data,'writer').split(', '))
            info_tag.setDirectors(meta_get(video_data,'director').split(', '))
            
            
        else:
            liz.setInfo( type=tt, infoLabels=video_data)
        liz.setProperty( "Fanart_Image", fanart )
        # all_v_data=json.dumps(video_data)
        liz.addContextMenuItems(menu_items, replaceItems=False)
        return u,liz,False
def addLink_db( name, url,mode,isFolder, iconimage,fanart,description,data='',trailer=' ',video_info={},id='',all_w={},original_title='',heb_name=''):
          added_pre=''
          unque=urllib.parse.unquote_plus
          ee=str(id)

          try:
            iconimage=iconimage.strip()
          except:
            iconimage=str(iconimage)

          try:
            fanart=fanart.strip()
          except:
            fanart=str(fanart)
            
          menu_items=[]
          menu_items.append(('%s'%'נגן דרך הבוט - חד פעמי', 'RunPlugin(%s?mode=191&url=www)' % sys.argv[0] ))
          menu_items.append(('%s'%'הפעל\בטל - ניגון קבוע דרך הבוט', 'RunPlugin(%s?mode=211&url=www)' % sys.argv[0] ))
          menu_items.append(('[I]%s[/I]'%'סמן נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=194&original_title=%s&id=%s')%(sys.argv[0],original_title,id))) 
          menu_items.append(('[I]%s[/I]'%'הסר נצפה', 'RunPlugin(%s)' % ('%s?url=www&mode=192&original_title=%s&id=%s')%(sys.argv[0],original_title,id))) 
          menu_items.append(('%s'%'רענן סנכרון', 'RunPlugin(%s?mode=189&url=www)' % sys.argv[0] ))
          menu_items.append(('%s'%Addon.getLocalizedString(32063), 'Action(Info)'))
          menu_items.append(('%s'%'הגדרות הרחבה', 'RunPlugin(%s?mode=174&url=www)' % sys.argv[0] ))
          menu_items.append(('[I]%s[/I]'%'הוסף לבקרת הורים', 'RunPlugin(%s)' % ('%s?url=%s&mode=208&name=%s')%(sys.argv[0],id,urllib.parse.quote_plus(name))))
          menu_items.append(('[I]%s[/I]'%'הסר מבקרת הורים', 'RunPlugin(%s)' % ('%s?url=%s&mode=209&name=%s')%(sys.argv[0],id,urllib.parse.quote_plus(name))))
            
          u=sys.argv[0]+"?mode="+str(mode)+"&iconimage="+iconimage+"&fanart="+fanart+"&description="+ urllib.parse.quote_plus(description)+"&url="+ urllib.parse.quote_plus(url)+"&name="+urllib.parse.quote_plus(name)+"&heb_name="+urllib.parse.quote_plus(heb_name)+"&original_title="+(original_title)+"&id="+(id)+"&video_info="+(video_info)
          liz=xbmcgui.ListItem(name)
          liz.setArt({'thumb' : iconimage, 'fanart': iconimage, 'icon': iconimage})
          if ee in all_w:
              try:
               all_w_time=int((float(all_w[ee]['resume'])*100)/float(all_w[ee]['totaltime']))
              except:all_w_time=0
              # if mode==20 or mode==15 :
              added_pre='[COLOR yellow][I] - '+str(all_w_time)+'% [/I][/COLOR]'
              # xbmc.executebuiltin((u'Notification(%s,%s)' % ('Kodi Anonymous', added_pre)))
          if video_info!={}:
                
                try:
                    video_data=json.loads(video_info)
                    dateadded=video_data['dateadded']
                    # rating=video_data['rating']
                    regex='.+?-.+?-.+? '
                    date_pre=re.compile(regex).findall(str(dateadded))
                    video_data['trailer']=trailer
                    try:
                        ddd='\nהסרט נוסף בתאריך: '+'[COLOR yellow]'+str(date_pre[0])+'[/COLOR]'
                    except:
                        ddd=''
                    # ddd2='\nציון: '+'[COLOR yellow]'+str(rating)+'[/COLOR]'
                    video_data['plot']=description.replace("%27","'")+ddd#+ddd2
                    video_data['mediatype']='movie'
                    
                    
                    res={}
                    if ee in all_w:
                             if (float(all_w[ee]['totaltime'])*0.95)<=float(all_w[ee]['resume']):
                                 res['wflag']=True
                             else:
                                res['wflag']=False
                    if res:
                            if res['wflag']:
                                video_data['playcount']=1
                                video_data['overlay']=5

                    liz=xbmcgui.ListItem(offscreen=True)
                    liz.setLabel(name+added_pre.replace('\n',''))
                    liz.setArt({'thumb' : iconimage, 'fanart': fanart, 'icon': iconimage,'poster': iconimage})
                except:
                    video_data={ "Title": unque( name), "Plot": description   }
                    video_data['mediatype']='movie'
          else:
            video_data={ "Title": unque( name), "Plot": description   }
            video_data['mediatype']='movie'
            liz=xbmcgui.ListItem(offscreen=True)
            liz.setLabel(name+added_pre.replace('\n',''))
            liz.setArt({'thumb' : iconimage, 'fanart': fanart, 'icon': iconimage,'poster': iconimage})
          remove_keys=['fanart','icon','original_title','tv_title','fast','heb title','imdb','poster','studios','tmdb']
          for key in remove_keys:
              if key in video_data:
                del video_data[key]
          liz.addContextMenuItems(menu_items, replaceItems=False)
          if KODI_VERSION>19:
                info_tag = liz.getVideoInfoTag()
                info_tag.setMediaType(meta_get(video_data,'mediatype'))
                info_tag.setTitle(meta_get(video_data,'title'))
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
                # info_tag.setVotes(int(meta_get(video_data,'votes')))
                info_tag.setMpaa(meta_get(video_data,'mpaa'))
                info_tag.setDuration(int(meta_get(video_data,'duration')))
                info_tag.setCountries(meta_get(video_data,'country'))
                
                info_tag.setTrailer(meta_get(video_data,'trailer'))
                info_tag.setPremiered(meta_get(video_data,'premiered'))
                info_tag.setTagLine(meta_get(video_data,'tagline'))
                info_tag.setStudios((meta_get(video_data,'studio') or '',))
                info_tag.setUniqueIDs({'imdb': meta_get(video_data,'imdb'), 'tmdb':meta_get(video_data,'tmdb')})
                info_tag.setGenres(meta_get(video_data,'genre').split(', '))
                info_tag.setWriters(meta_get(video_data,'writer').split(', '))
                info_tag.setDirectors(meta_get(video_data,'director').split(', '))
                
                
          else:
                liz.setInfo( type="Video", infoLabels=video_data)
          # art = {}
          # art.update({'poster': iconimage})
          # liz.setArt(art)
          # liz.setProperty("IsPlayable","true")
          # liz.setProperty("IsPlayable","false")
          # liz.setProperty( "Fanart_Image", fanart )
          # liz.addContextMenuItems(menu_items, replaceItems=False)
          #xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
          return u,liz,False