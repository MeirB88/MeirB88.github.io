'''
    Copyright (C) 2014-2016 ddurdle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''
import xbmc,time


import urllib

import urllib.parse
que=urllib.parse.quote_plus
url_encode=urllib.parse.urlencode
py2 = False
#
#
#
class mediaurl:
    # CloudService v0.2.4

    ##
    ##
    def __init__(self, url, qualityDesc, quality, order, title=''):
        self.url = url
        self.qualityDesc = qualityDesc
        self.quality = quality
        self.order = order
        self.title = title
        self.offline = False


    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__,
                                  self.order)

    def __cmp__(self, other):
        if hasattr(other, 'order'):
            return self.order.__cmp__(other.order)

    def getKey(self):
        return self.order

def html_decode (O0O0OO0O0OOO00OO0 ):#line:2481
    ""#line:2486
    OOOOOO0OOO00OO0OO =(("'",'&#39;'),('"','&quot;'),('>','&gt;'),('<','&lt;'),('-','&#8211;'),('&','&amp;'))#line:2494
    for O0O00OOOO000OOO00 in OOOOOO0OOO00OO0OO :#line:2495
        O0O0OO0O0OOO00OO0 =O0O0OO0O0OOO00OO0 .replace (O0O00OOOO000OOO00 [1 ],O0O00OOOO000OOO00 [0 ])#line:2496
    return O0O0OO0O0OOO00OO0 #line:2497
def dood_decode( data):
    import string,random
    t = string.ascii_letters + string.digits
    return data + ''.join([random.choice(t) for _ in range(10)])
def resolve_doodstream(url):
    import re

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        
        'Connection': 'keep-alive',
        
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
    from resources.modules import cfscrape
    uri=url.replace('/d/','/e/').replace('dood.cx','dood.so').replace('dood.la','dood.so').replace('resolveurl','').replace('dood.sh','dood.so')
    counter=0
    match=None
    while not match:
        
        scraper = cfscrape.create_scraper()
        
    
        html=scraper.get(uri,headers=headers).content.decode('utf-8')
        
        match = re.search(r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''', html, re.DOTALL)

        if match:
            
            break
        else:
            xbmc.sleep(50)
        counter+=1
        if counter>10:
            break
    if match:
        token = match.group(2)
        url = 'https://dood.so' + match.group(1)
        headers.update({'Referer': 'https://dood.so/'})
        html = scraper.get(url, headers=headers).content.decode('utf-8')
        head=url_encode(headers)
        f_url=dood_decode(html) + token + str(int(time.time() * 1000)) +"|"+head

        return f_url

