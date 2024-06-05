# -*- coding: utf-8 -*-
import re,urllib,sys,requests
from resources.modules import log
def auto_trk_auth(key):
        import xbmcgui,xbmcaddon

        Addon = xbmcaddon.Addon()
        dp = xbmcgui . DialogProgress ( )

        try:
            dp.create('אנא המתן','מאשר אנא המתן', key,'')
            dp.update(0, 'אנא המתן','מאשר אנא המתן', key )
        except:
            dp.create('אנא המתן','מאשר אנא המתן'+'\n'+ key+'\n'+'')
            dp.update(0, 'אנא המתן'+'\n'+'מאשר אנא המתן'+'\n'+ key )
        user=Addon.getSetting("trk_user")
        passward=Addon.getSetting("trk_pass")
        cookies = {
            'user_data_version': '3',
        }

        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'utf-8',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        response = requests.get('https://trakt.tv/auth/signin', headers=headers, cookies=cookies)
        regex='name="csrf-token" content="(.+?)"'
        m=re.compile(regex).findall(response.content.decode('utf-8'))[0]
        cookies = {
            'user_data_version': '3',
            
            'webp_supported': 'true',
            'watchnow_country': 'il',
            '_traktsession':response.cookies['_traktsession'],
            
          
        }
        try:
            dp.update(0, 'אנא המתן','נכנס לחשבון', user )
        except:
            dp.update(0, 'אנא המתן'+'\n'+'נכנס לחשבון'+'\n'+ user )
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'https://trakt.tv',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://trakt.tv/auth/signin',
            'Accept-Encoding': 'utf-8',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        data = {
          'utf8': '\u2713',
          'authenticity_token': m,
          'user[login]': user,
          'user[password]': passward,
          'user[remember_me]': '1'
        }

        response = requests.post('https://trakt.tv/auth/signin', headers=headers, cookies=cookies, data=data)
        
        regex='id="meta-username" type="hidden" value="(.+?)"'
        try:
            user_n=re.compile(regex).findall(response.content.decode('utf-8'))[0]
        except:
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('טעות בפרטי התחברות', 'נסה לרשום את שם המשתמש ללא ה @...')))
            Addon.openSettings()
        regex='name="csrf-token" content="(.+?)"'
        m=re.compile(regex).findall(response.content.decode('utf-8'))[0]
        us_token=response.cookies['remember_user_token']
        cookies = {
            'user_data_version': '3',
          
            'webp_supported': 'true',
            'watchnow_country': 'il',
            
            '_gat': '1',
            '_gali': 'new_user',
            'trakt_username': user_n,
            'trakt_userslug': user_n.lower(),
            'remember_user_token':us_token,
            '_traktsession':response.cookies['_traktsession'],
        }

        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://trakt.tv/auth/signin',
            'Accept-Encoding': 'utf-8',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        response = requests.get('https://trakt.tv/activate', headers=headers, cookies=cookies)
        try:
            dp.update(0, 'אנא המתן','מפעיל', user )
        except:
            dp.update(0, 'אנא המתן'+'\n'+'מפעיל'+'\n'+ user )
        m=re.compile(regex).findall(response.content.decode('utf-8'))[0]

        cookies = {
            'user_data_version': '3',
          
            'webp_supported': 'true',
            'watchnow_country': 'il',
           
            '_gat': '1',
            'trakt_username': user_n,
            'trakt_userslug': user_n.lower(),
            'remember_user_token':us_token,
            '_traktsession':response.cookies['_traktsession'],
        }

        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'https://trakt.tv',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://trakt.tv/activate',
            'Accept-Encoding': 'utf-8',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        data = {
          'utf8': '\u2713',
          'authenticity_token': m,
          'code': key,
          'commit': 'Continue'
        }

        response = requests.post('https://trakt.tv/activate', headers=headers, cookies=response.cookies, data=data)
        m=re.compile(regex).findall(response.content.decode('utf-8'))[0]
        


        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'https://trakt.tv',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://trakt.tv/activate/authorize',
            'Accept-Encoding': 'utf-8',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        data = {
          'utf8': '\u2713',
          'authenticity_token': m,
          'commit': 'Yes'
        }

        response = requests.post('https://trakt.tv/activate/authorize', headers=headers, cookies=response.cookies, data=data)
        # logging.warning(response.cookies)
        # logging.warning(response.headers)
        #logging.warning(response.content)
        dp.close()