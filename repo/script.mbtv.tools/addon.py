import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import os
import shutil

ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')

def def_iptv():
    xbmc.executebuiltin('Addon.OpenSettings(pvr.iptvsimple)')
    xbmc.sleep(500)
    xbmc.executebuiltin('SetFocus(11)')
    xbmc.executebuiltin('SetFocus(1000)')
    xbmc.executebuiltin('Action(Select)')
    xbmc.executebuiltin('Action(Select)')

def def_debrid():
    message = ("שים לב!\n"
               "כדי להגדיר את חשבון הדבריד שלך יש לבחור במסך הבא באפשרות של Universal Resolvers 2, "
               "ולאחר מכן לבחור בלאמת את חשבון ה-Real-Debrid.\n"
               "אם יש לך ספק דבריד אחר, תוכל לחפש אותו ברשימה ולאמת אותו במקום.")

    dialog = xbmcgui.Dialog()
    choice = dialog.yesno(ADDON_NAME, message, nolabel="בטל", yeslabel="המשך")

    if choice:
        xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.thecrew/?action=ResolveUrlTorrent",return)')

def def_lang():
    xbmc.executebuiltin('ActivateWindow(InterfaceSettings)')
    xbmc.sleep(500)
    xbmc.executebuiltin('SetFocus(5)')  # מספר זה עשוי להשתנות בהתאם לגרסת קודי

def def_font():
    fonts = ['פונט 1', 'פונט 2', 'פונט 3']
    dialog = xbmcgui.Dialog()
    index = dialog.select('בחר פונט', fonts)
    
    if index >= 0:
        confirm = dialog.yesno('אישור שינוי פונט', f'האם אתה בטוח שברצונך להחליף לפונט {fonts[index]}?')
        if confirm:
            # כאן תוכל להוסיף את הקוד לשינוי הפונט בפועל
            xbmcgui.Dialog().ok(ADDON_NAME, f'הפונט הוחלף ל-{fonts[index]}')

def def_cache():
    options = ['ניקוי קאש חלקי', 'ניקוי קאש מלא']
    dialog = xbmcgui.Dialog()
    index = dialog.select('בחר סוג ניקוי', options)
    
    if index >= 0:
        confirm = dialog.yesno('אישור ניקוי קאש', f'האם להמשיך עם {options[index]}?')
        if confirm:
            if index == 0:
                clear_cache()
            else:
                clear_cache_full()

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def clear_cache():
    cache_path = xbmcvfs.translatePath('special://temp')
    initial_size = get_size(cache_path)
    
    if os.path.exists(cache_path):
        for root, dirs, files in os.walk(cache_path):
            for f in files:
                try:
                    os.unlink(os.path.join(root, f))
                except Exception as e:
                    xbmc.log(f"Error deleting file {f}: {str(e)}", xbmc.LOGERROR)
    
    final_size = get_size(cache_path)
    cleared_size = (initial_size - final_size) / (1024 * 1024)  # Convert to MB
    xbmcgui.Dialog().ok(ADDON_NAME, f'ניקוי קאש חלקי הושלם. נמחקו {cleared_size:.2f} MB')

def clear_cache_full():
    cache_paths = [
        xbmcvfs.translatePath('special://temp'),
        xbmcvfs.translatePath('special://home/addons/packages'),
        xbmcvfs.translatePath('special://home/userdata/Thumbnails')
    ]
    total_cleared = 0
    
    for path in cache_paths:
        initial_size = get_size(path)
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except Exception as e:
                        xbmc.log(f"Error deleting file {f}: {str(e)}", xbmc.LOGERROR)
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except Exception as e:
                        xbmc.log(f"Error deleting directory {d}: {str(e)}", xbmc.LOGERROR)
        final_size = get_size(path)
        total_cleared += initial_size - final_size
    
    cleared_size = total_cleared / (1024 * 1024)  # Convert to MB
    xbmcgui.Dialog().ok(ADDON_NAME, f'ניקוי קאש מלא הושלם. נמחקו {cleared_size:.2f} MB')

def main_menu():
    options = ['הגדר IPTV', 'הגדר חשבון דבריד', 'שינוי שפה', 'שינוי פונט', 'ניקוי קאש']
    dialog = xbmcgui.Dialog()
    index = dialog.select('כלי MBTV', options)
    if index == 0:
        def_iptv()
    elif index == 1:
        def_debrid()
    elif index == 2:
        def_lang()
    elif index == 3:
        def_font()
    elif index == 4:
        def_cache()

if __name__ == '__main__':
    main_menu()