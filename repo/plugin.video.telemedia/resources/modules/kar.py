 # -*- coding: utf-8 -*-
from resources.modules import public
import re,xbmcplugin,sys,xbmcgui,xbmc
addDir3=public.addDir3
addLink2=public.addLink2
addLink=public.addLink
import xbmcvfs
translatepath=xbmcvfs.translatePath
import sys
path1=translatepath('special://home/addons/script.module.requests/lib')
sys.path.append( path1)
path1=translatepath('special://home/addons/script.module.urllib3/lib')
sys.path.append( path1)
path1=translatepath('special://home/addons/script.module.chardet/lib')
sys.path.append( path1)
path1=translatepath('special://home/addons/script.module.certifi/lib')
sys.path.append( path1)
path1=translatepath('special://home/addons/script.module.idna/lib')
sys.path.append( path1)
path1=translatepath('special://home/addons/script.module.futures/lib')
sys.path.append( path1)
import requests,logging
icon='https://thumbs.dreamstime.com/b/vector-logo-karaoke-design-template-illustration-icon-126463532.jpg'
fan='https://img.freepik.com/free-vector/karaoke-with-microphones-stars-neon-style_24908-60794.jpg?w=2000'
def karaoke_menu():
    all_d=[]
    aa=addDir3('קריוקי VIP','www',257,icon,fan,'קריוקי VIP',data=-1001504420275)
            
    all_d.append(aa)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    

    response = requests.get('https://www.karaoke.co.il/', headers=headers,verify=False).content.decode('utf-8')
    regex='<div class="line"><div class="item_one"><a href="(.+?)">(.+?)<'
    m=re.compile(regex).findall(response)
    
    for lk,nm in m:
        
        aa=addDir3( nm, lk,231, icon,fan,nm)
        all_d.append(aa)
    regex='<div class="item_two"><a href="(.+?)">(.+?)<'
    
    m=re.compile(regex).findall(response)

    for lk,nm in m:
        
        aa=addDir3( nm, lk,231, icon,fan,nm)
        all_d.append(aa)
    aa=addDir3( 'זמרים', 'www',247, icon,fan,'[COLOR lightblue]חיפוש[/COLOR]')
    all_d.append(aa)
    aa=addDir3( '[COLOR lightblue]חיפוש[/COLOR]', 'www',230, icon,fan,'[COLOR lightblue]חיפוש[/COLOR]')
    all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def singer():
    all_d=[]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    

    response = requests.get('https://www.karaoke.co.il/%d7%96%d7%9e%d7%a8%d7%99%d7%9d/', headers=headers,verify=False).content.decode('utf-8', 'ignore')
    import logging
    
    regex='<div class=\"artists_item\"><a href="(.+?)">(.+?)<'
    m=re.compile(regex).findall(response)
    for lk,nm in m:

        aa=addDir3( nm, lk,231, icon,fan,nm)
        all_d.append(aa)

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def play_link_kar(name,url):
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }

   

    response = requests.get(url, headers=headers,verify=False).content.decode('utf-8')
    regex='<div class="song_clip.+?" style="display:none">(.+?)</div>'
    p_m=re.compile(regex,re.DOTALL).findall(response)
   
        
    all_nm=[]
    all_lk=[]
    
    for itt in p_m:

        regex='<h3 class="song_clip_name">(.+?)</h3>'
        m=re.compile(regex,re.DOTALL).findall(itt)[0]
        all_nm.append(m)
        regex='videoplayerframe.php\?id=(.+?)"'
        m=re.compile(regex,re.DOTALL).findall(itt)[0]
        
        all_lk.append(m)
        break
 
    
    
        
    #ret = xbmcgui.Dialog().select('בחר', all_nm)
    #if ret!=-1:
    #    f_lk=all_lk[ret]
    #else:
    #  sys.exit()
    
    x = requests.get('https://www.karaoke.co.il/videoplayerframe.php?id='+all_lk[0], headers=headers,verify=False).content.decode('utf-8')
    regex='src="(.+?)"'
    m=re.compile(regex).findall(x)[0].replace('&time_limit=30','')
    o_link=m
    x = requests.get(m, headers=headers,verify=False).content.decode('utf-8')
    
    regex='"fid".+?"(.+?)"'
    cdn=re.compile(regex).findall(x)[0]
    
    response = requests.post('https://www.karaoke.co.il/api.php', data={'action': 'playbackByCDN',	'cdn': cdn}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'},verify=False)
    
    f_link=(response.json()['data']['playback'].replace('mp3', 'mp4').replace('download', 'show'))
    # logging.warning('url::222'+f_link)
    listItem = xbmcgui.ListItem(name, path=f_link) 
 
    listItem.setInfo(type='Video', infoLabels={'title':name,'plot':''})


    listItem.setProperty('IsPlayable', 'true')

    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
def category(url,iconimage,fanart):
    # log.warning('url::'+url)
    all_d=[]
    
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    

    response = requests.get(url, headers=headers,verify=False).content.decode('utf-8')
    regex='div class="result_image_orig"> <img src="(.+?)" alt=\"(.+?)\" /> <a href="(.+?)" title=\"(.+?)\"'
    m=re.compile(regex).findall(response)
   
    for im,pl,lk,nm in m:
        # aa=addLink2(nm, 'http'+lk.replace('\n','').strip(),175,False,im,im,nm,place_control=True)
        aa=addLink2( nm, lk,232,False, im,im,pl,place_control=True)
        all_d.append(aa)
    regex="<div class=\"line prevnext_links\">(.+?)</div>"
    try:
        m_pre=re.compile(regex,re.DOTALL).findall(response)[0]
        # log.warning(m_pre)
        regex='<a href="(.+?)" class="(.+?)">'
        m=re.compile(regex,re.DOTALL).findall(m_pre)
        for lk,cl in m:
           
           if cl=='next_page':
            
            aa=addDir3( '[COLOR khaki][B]עמוד הבא[/B][/COLOR]', lk.replace('&amp;','&'),231, icon,fan,'[COLOR khaki][B]עמוד הבא[/B][/COLOR]')
            all_d.append(aa)
    except Exception as e:
        logging.warning('def category '+str(e))
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
def kar_search():
    import random,json,xbmcaddon,time
    from resources.modules.general import clean_name
    all_d=[]
    Addon = xbmcaddon.Addon()
    listen_port=Addon.getSetting("port")
    search_entered=''
    keyboard = xbmc.Keyboard(search_entered, 'הכנס חיפוש')
    keyboard.doModal()
    last_id_all='0$$$0$$$0$$$0'
    
    if keyboard.isConfirmed():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        params = (
            ('Sstr', keyboard.getText()),
        )
        try:
            dialog = xbmcgui.DialogBusy()
            dialog.create()
        except:
           xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        last_id_doc=last_id_all.split('$$$')[0]
        num=random.randint(1,1001)
        data={'type':'td_send',
             'info':json.dumps({'@type': 'searchChatMessages','chat_id':(-1001504420275), 'query': keyboard.getText(),'from_message_id':int(last_id_doc),'offset':0,'limit':100, '@extra': num})
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

                    if '.mkv' not in file_name and '.mp4' not in file_name and '.avi' not in file_name and '.AVI' not in file_name and '.MKV' not in file_name and '.MP4' not in file_name and '.wmv' not in file_name:
                        continue
                    size=items['content']['document']['document']['size']
                    f_size2=str(round(float(size)/(1024*1024*1024), 2))+' GB'
                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    regex='.*([1-3][0-9]{3})'
                    year_pre=re.compile(regex).findall(name)
                    year=0
                    if len(year_pre)>0:
                        year=year_pre[0]
                    mode=3
                    o_name=name

                        
                    name=clean_name(name,'')
                    link_data={}
                    link_data['id']=str(items['content']['document']['document']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    addLink( name,f_lk ,mode,False, icon,fan,f_size2,da=da,year=year,original_title=o_name,in_groups=True)
        for items in event['messages']:  
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

                    if 'date' in items:
                        da=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(items['date']))
                    regex='.*([1-3][0-9]{3})'
                    year_pre=re.compile(regex).findall(name)
                    year=0
                    if len(year_pre)>0:
                        year=year_pre[0]
                    name=clean_name(name,'')
                    link_data={}
                    link_data['id']=str(items['content']['video']['video']['id'])
                    link_data['m_id']=items['id']
                    link_data['c_id']=items['chat_id']
                    f_lk=json.dumps(link_data)
                    addLink( name,f_lk,3,False, icon,fan,f_size2+'\n'+plot.replace('\n\n',' - ').replace('סדרות מהלב',''),da=da,year=year,in_groups=True)
        response = requests.get('https://www.karaoke.co.il/searchresults.php', headers=headers, params=params,verify=False).content.decode('utf-8')
        
        regex="div class='result_image_orig'> <img src='(.+?)' alt=\"(.+?)\" /> <a href='(.+?)' title=\"(.+?)\""
        m=re.compile(regex).findall(response)
        
        for im,pl,lk,nm in m:
            
            aa=addLink2( nm, lk,232,False, im,im,pl,place_control=True)
            all_d.append(aa)
    xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))