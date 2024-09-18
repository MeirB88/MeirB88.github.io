import routing
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
import json
import xbmc
import os

plugin = routing.Plugin()
addon = xbmcaddon.Addon()

JSON_URL = "http://mbtv.site/movies_and_tvshows.json"

def get_icon_path(icon_name):
    return os.path.join(addon.getAddonInfo('path'), 'resources', 'icons', icon_name)

def get_content():
    try:
        xbmc.log(f"Fetching content from URL: {JSON_URL}", level=xbmc.LOGINFO)
        response = requests.get(JSON_URL)
        response.raise_for_status()
        content = json.loads(response.text)
        return content
    except Exception as e:
        xbmc.log(f"Error fetching or parsing content: {str(e)}", level=xbmc.LOGERROR)
        return {"movies": [], "tvshows": []}

@plugin.route('/')
def index():
    movies_item = xbmcgui.ListItem("סרטים")
    movies_item.setArt({'icon': get_icon_path('movies.png')})
    
    tvshows_item = xbmcgui.ListItem("סדרות")
    tvshows_item.setArt({'icon': get_icon_path('tvshows.png')})
    
    search_item = xbmcgui.ListItem("חיפוש")
    search_item.setArt({'icon': get_icon_path('search.png')})

    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_movies), movies_item, True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_tvshows), tvshows_item, True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(search_menu), search_item, True)
    
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/movies')
def show_movies():
    content = get_content()
    for movie in content.get('movies', []):
        list_item = xbmcgui.ListItem(label=movie['title'])
        
        video_info = list_item.getVideoInfoTag()
        video_info.setTitle(movie['title'])
        video_info.setPlot(movie.get('description', ''))
        
        if movie.get('poster'):
            list_item.setArt({'poster': movie['poster'], 'icon': movie['poster']})
        
        list_item.setProperty('IsPlayable', 'true')
        
        url = movie.get('url', '')
        
        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, False)
    
    xbmcplugin.setContent(plugin.handle, 'movies')
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/tvshows')
def show_tvshows():
    content = get_content()
    for show in content.get('tvshows', []):
        list_item = xbmcgui.ListItem(label=show['title'])
        
        video_info = list_item.getVideoInfoTag()
        video_info.setTitle(show['title'])
        video_info.setPlot(show.get('description', ''))
        
        if show.get('poster'):
            list_item.setArt({'poster': show['poster'], 'icon': show['poster']})
        
        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_seasons, show_title=show['title']), list_item, True)
    
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/show/<show_title>')
def show_seasons(show_title):
    content = get_content()
    show = next((s for s in content.get('tvshows', []) if s['title'] == show_title), None)
    if show and 'seasons' in show:
        for season in show['seasons']:
            list_item = xbmcgui.ListItem(label=f"עונה {season['season_number']}")
            if show.get('poster'):
                list_item.setArt({'poster': show['poster'], 'icon': show['poster']})
            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_episodes, show_title=show_title, season_number=season['season_number']), list_item, True)
    xbmcplugin.setContent(plugin.handle, 'seasons')
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/show/<show_title>/season/<season_number>')
def show_episodes(show_title, season_number):
    content = get_content()
    show = next((s for s in content.get('tvshows', []) if s['title'] == show_title), None)
    if show:
        season = next((s for s in show.get('seasons', []) if str(s['season_number']) == season_number), None)
        if season:
            for episode in season.get('episodes', []):
                list_item = xbmcgui.ListItem(label=episode['title'])
                video_info = list_item.getVideoInfoTag()
                video_info.setTitle(episode['title'])
                if show.get('poster'):
                    list_item.setArt({'poster': show['poster'], 'icon': show['poster']})
                list_item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(plugin.handle, episode.get('url', ''), list_item, False)
    xbmcplugin.setContent(plugin.handle, 'episodes')
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/search')
def search_menu():
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(search, category='all'), xbmcgui.ListItem(label="חיפוש כללי"), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(search, category='movies'), xbmcgui.ListItem(label="חיפוש סרטים"), True)
    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(search, category='tvshows'), xbmcgui.ListItem(label="חיפוש סדרות"), True)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/search/<category>')
def search(category):
    search_string = xbmcgui.Dialog().input("הזן מילות חיפוש", type=xbmcgui.INPUT_ALPHANUM)
    if not search_string:
        return
    
    content = get_content()
    results = []
    
    if category in ['all', 'movies']:
        results.extend([movie for movie in content.get('movies', []) if search_string.lower() in movie['title'].lower()])
    
    if category in ['all', 'tvshows']:
        results.extend([show for show in content.get('tvshows', []) if search_string.lower() in show['title'].lower()])
    
    for item in results:
        list_item = xbmcgui.ListItem(label=item['title'])
        video_info = list_item.getVideoInfoTag()
        video_info.setTitle(item['title'])
        video_info.setPlot(item.get('description', ''))
        
        if item.get('poster'):
            list_item.setArt({'poster': item['poster'], 'icon': item['poster']})
        
        if 'seasons' in item:  # This is a TV show
            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_seasons, show_title=item['title']), list_item, True)
        else:  # This is a movie
            list_item.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(plugin.handle, item.get('url', ''), list_item, False)
    
    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.endOfDirectory(plugin.handle)

if __name__ == '__main__':
    plugin.run()