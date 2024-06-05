import sys
import re
import json
# from six.moves import  http_cookiejar
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import urllib.request
import urllib.parse as urllib_parse
import http.client as httplib
try:
    import cookielib
except:
    import http.cookiejar
    cookielib = http.cookiejar
xbmcaddon.Addon(id='plugin.video.telemedia')
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib.request.HTTPCookieProcessor(cookiejar)
urllib.request.build_opener(cookie_handler)


def CATEGORIES():
    link = openURL('https://www.empflix.com/categories')
    match = re.compile(r'class="col-6.+?href="([^"]+)">\s*<img.+?src="([^"]+).+?title">([^<]+)', re.DOTALL).findall(link)
    addDir('All', 'https://www.empflix.com/', 235, '', 1)
    for url, thumb, name in match:
        addDir(name,
               url,
               236, thumb, 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def SORTMETHOD(url):
    if url == 'https://www.empflix.com/':
        addDir('Featured', url + 'featured', 236, '', 1)
        addDir('Most Recent', url + 'new', 236, '', 1)
        addDir('Top Rated', url + 'toprated', 236, '', 1)
    else:
        match = re.compile('(https://www.empflix.com/channels/)'
                           '(.*)').findall(url)
        for start, end in match:
            addDir('Being Watched', start + 'watched-' + end, 236, '', 1)
            addDir('Most Recent', start + 'new-' + end, 236, '', 1)
            addDir('Most Viewed', start + 'popular-' + end, 236, '', 1)
            addDir('Top Rated', start + 'rated-' + end, 236, '', 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def VIDEOLIST(url, page):
    link = openURL(url + '/' + str(page))
    match = re.compile(r'data-vid="([^"]+).+?src="([^"]+)"\s*alt="([^"]+).+?tion">([^<]+)',
                       re.DOTALL).findall(link)
    for videourl, thumb, name, duration in match:
        addLink(name + ' (' + duration + ')',
                'https://player.empflix.com/ajax/video-player/' + videourl,
                237,
                thumb.strip())
    if len(match) == 36 or len(match) == 83:
        addDir('Next Page', url, 236, '', page + 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PLAYVIDEO(url):
    video_data={}
    video_data[u'mpaa']=('heb')
    video_data['title']='VIP XXX'
    listItem = xbmcgui.ListItem(video_data['title']) 
    listItem.setInfo(type='Video', infoLabels=video_data)
    link = openURL(url)
    link = json.loads(link).get('html')
    match = re.compile(r'source\s*src="([^"]+)').findall(link)
    xbmc.Player().play(match[0] + '|Referer=https://www.empflix.com/',listitem=listItem)
    


def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + '?url=' + urllib_parse.quote_plus(url) + '&mode=' + str(mode)\
        + '&name=' + urllib_parse.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setArt({'thumb': iconimage, 'icon': 'DefaultFolder.png'})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok


def addDir(name, url, mode, iconimage, page):
    u = sys.argv[0] + '?url=' + urllib_parse.quote_plus(url) + '&mode=' + str(mode) +\
        '&name=' + urllib_parse.quote_plus(name) + '&page=' + str(page)
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setArt({'thumb': iconimage, 'icon': 'DefaultFolder.png'})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
    return ok


def openURL(url):
    xbmc.log("Opening %s" % url)
    req = urllib.request.Request(url)
    req.add_header('Referer', 'https://www.empflix.com/')
    response = urllib.request.urlopen(req)
    link = response.read().decode('utf-8')
    response.close()
    return link


