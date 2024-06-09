################################################################################
#      Copyright (C) 2019 drinfernoo                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc

import os

from resources.libs.common import directory
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common.config import CONFIG


class MaintenanceMenu:

    def get_listing(self):
        directory.add_dir('[B]כלי ניקוי[/B]', {'mode': 'maint', 'name': 'clean'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]כלי הרחבות[/B]', {'mode': 'maint', 'name': 'addon'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]כלי רישום[/B]', {'mode': 'maint', 'name': 'logging'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]תחזוקה שונה[/B]', {'mode': 'maint', 'name': 'misc'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]גיבוי/שחזור[/B]', {'mode': 'maint', 'name': 'backup'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]תיקוני מערכת[/B]', {'mode': 'maint', 'name': 'tweaks'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)

    def clean_menu(self):
        from resources.libs import clear
        from resources.libs.common import tools

        on = '[B][COLOR springgreen]מופעל[/COLOR][/B]'
        off = '[B][COLOR red]כבוי[/COLOR][/B]'

        autoclean = 'true' if CONFIG.AUTOCLEANUP == 'true' else 'false'
        cache = 'true' if CONFIG.AUTOCACHE == 'true' else 'false'
        packages = 'true' if CONFIG.AUTOPACKAGES == 'true' else 'false'
        thumbs = 'true' if CONFIG.AUTOTHUMBS == 'true' else 'false'
        includevid = 'true' if CONFIG.INCLUDEVIDEO == 'true' else 'false'
        includeall = 'true' if CONFIG.INCLUDEALL == 'true' else 'false'

        sizepack = tools.get_size(CONFIG.PACKAGES)
        sizethumb = tools.get_size(CONFIG.THUMBNAILS)
        archive = tools.get_size(CONFIG.ARCHIVE_CACHE)
        sizecache = (clear.get_cache_size()) - archive
        totalsize = sizepack + sizethumb + sizecache

        directory.add_file(
            'ניקוי כולל: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(totalsize)), {'mode': 'fullclean'},
            icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('נקה מטמון: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizecache)),
                           {'mode': 'clearcache'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)') or xbmc.getCondVisibility(
                'System.HasAddon(script.module.resolveurl)'):
            directory.add_file('נקה מטמון פונקציות של פותר', {'mode': 'clearfunctioncache'}, icon=CONFIG.ICONMAINT,
                               themeit=CONFIG.THEME3)
        directory.add_file('נקה חבילות: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizepack)),
                           {'mode': 'clearpackages'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file(
            'נקה תמונות ממוזערות: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizethumb)),
            {'mode': 'clearthumb'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if os.path.exists(CONFIG.ARCHIVE_CACHE):
            directory.add_file('נקה מטמון ארכיון: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(
                tools.convert_size(archive)), {'mode': 'cleararchive'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('נקה תמונות ממוזערות ישנות', {'mode': 'oldThumbs'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('נקה יומני קריסה', {'mode': 'clearcrash'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('נקה מסדי נתונים', {'mode': 'purgedb'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('התחלה מחדש', {'mode': 'freshstart'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

        directory.add_file('ניקוי אוטומטי', fanart=CONFIG.ADDON_FANART, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_file('ניקוי אוטומטי בהפעלה: {0}'.format(autoclean.replace('true', on).replace('false', off)),
                           {'mode': 'togglesetting', 'name': 'autoclean'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if autoclean == 'true':
            directory.add_file(
                '--- תדירות ניקוי אוטומטי: [B][COLOR springgreen]{0}[/COLOR][/B]'.format(
                    CONFIG.CLEANFREQ[CONFIG.AUTOFREQ]),
                {'mode': 'changefreq'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file(
                '--- נקה מטמון בהפעלה: {0}'.format(cache.replace('true', on).replace('false', off)),
                {'mode': 'togglesetting', 'name': 'clearcache'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file(
                '--- נקה חבילות בהפעלה: {0}'.format(packages.replace('true', on).replace('false', off)),
                {'mode': 'togglesetting', 'name': 'clearpackages'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file(
                '--- נקה תמונות ממוזערות ישנות בהפעלה: {0}'.format(thumbs.replace('true', on).replace('false', off)),
                {'mode': 'togglesetting', 'name': 'clearthumbs'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('נקה מטמון וידאו', fanart=CONFIG.ADDON_FANART, icon=CONFIG.ICONMAINT,
                           themeit=CONFIG.THEME1)
        directory.add_file(
            'כלול מטמון וידאו בניקוי מטמון: {0}'.format(includevid.replace('true', on).replace('false', off)),
            {'mode': 'togglecache', 'name': 'includevideo'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

        if includeall == 'true':
            includegaia = 'true'
            includeexodusredux = 'true'
            includethecrew = 'true'
            includeyoda = 'true'
            includevenom = 'true'
            includenumbers = 'true'
            includescrubs = 'true'
            includeseren = 'true'
        else:
            includeexodusredux = 'true' if CONFIG.INCLUDEEXODUSREDUX == 'true' else 'false'
            includegaia = 'true' if CONFIG.INCLUDEGAIA == 'true' else 'false'
            includethecrew = 'true' if CONFIG.INCLUDETHECREW == 'true' else 'false'
            includeyoda = 'true' if CONFIG.INCLUDEYODA == 'true' else 'false'
            includevenom = 'true' if CONFIG.INCLUDEVENOM == 'true' else 'false'
            includenumbers = 'true' if CONFIG.INCLUDENUMBERS == 'true' else 'false'
            includescrubs = 'true' if CONFIG.INCLUDESCRUBS == 'true' else 'false'
            includeseren = 'true' if CONFIG.INCLUDESEREN == 'true' else 'false'

        if includevid == 'true':
            directory.add_file(
                '--- כלול את כל הרחבות הווידאו: {0}'.format(includeall.replace('true', on).replace('false', off)),
                {'mode': 'togglecache', 'name': 'includeall'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.exodusredux)'):
                directory.add_file(
                    '--- כלול את Exodus Redux: {0}'.format(
                        includeexodusredux.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includeexodusredux'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.gaia)'):
                directory.add_file(
                    '--- כלול את Gaia: {0}'.format(includegaia.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includegaia'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.numbersbynumbers)'):
                directory.add_file(
                    '--- כלול את NuMb3r5: {0}'.format(includenumbers.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includenumbers'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.scrubsv2)'):
                directory.add_file(
                    '--- כלול את Scrubs v2: {0}'.format(includescrubs.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includescrubs'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.seren)'):
                directory.add_file(
                    '--- כלול את Seren: {0}'.format(includeseren.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includeseren'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.thecrew)'):
                directory.add_file(
                    '--- כלול את THE CREW: {0}'.format(includethecrew.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includethecrew'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.venom)'):
                directory.add_file(
                    '--- כלול את Venom: {0}'.format(includevenom.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includevenom'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.yoda)'):
                directory.add_file(
                    '--- כלול את Yoda: {0}'.format(includeyoda.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includeyoda'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file('--- הפעל את כל הרחבות הווידאו', {'mode': 'togglecache', 'name': 'true'}, icon=CONFIG.ICONMAINT,
                               themeit=CONFIG.THEME3)
            directory.add_file('--- השבת את כל הרחבות הווידאו', {'mode': 'togglecache', 'name': 'false'}, icon=CONFIG.ICONMAINT,
                               themeit=CONFIG.THEME3)

    def addon_menu(self):
        directory.add_file('הסר הרחבות', {'mode': 'removeaddons'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('הסר נתוני הרחבות', {'mode': 'removeaddondata'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('הפעל/השבת הרחבות', {'mode': 'enableaddons'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        # directory.add_file('Enable/Disable Adult Addons', 'toggleadult', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('רענן את כל המאגרים בכפייה', {'mode': 'forceupdate'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('עדכן את כל ההרחבות בכפייה', {'mode': 'forceupdate', 'action': 'auto'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

   
    def logging_menu(self):
        errors = int(logging.error_checking(count=True))
        errorsfound = str(errors) + ' שגיאה(ות) נמצאה(ו)' if errors > 0 else 'לא נמצאו'
        wizlogsize = ': [COLOR red]לא נמצא[/COLOR]' if not os.path.exists(
            CONFIG.WIZLOG) else ": [COLOR springgreen]{0}[/COLOR]".format(
            tools.convert_size(os.path.getsize(CONFIG.WIZLOG)))
            
        directory.add_file('הפעל/השבת רישום באגים', {'mode': 'enabledebug'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('העלה קובץ יומן', {'mode': 'uploadlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('צפה בשגיאות ביומן: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(errorsfound), {'mode': 'viewerrorlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if errors > 0:
            directory.add_file('צפה בשגיאה האחרונה ביומן', {'mode': 'viewerrorlast'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('צפה בקובץ יומן', {'mode': 'viewlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('צפה בקובץ יומן של הוויזארד', {'mode': 'viewwizlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('נקה את קובץ יומן של הוויזארד: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(wizlogsize), {'mode': 'clearwizlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
   
        
    def misc_menu(self):
        directory.add_file('תיקון קודי 17', {'mode': 'kodi17fix'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('כלי רשת', {'mode': 'nettools'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('הפעל/השבת מקורות לא ידועים', {'mode': 'unknownsources'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('הפעל/השבת עדכוני הרחבות', {'mode': 'toggleupdates'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('טען מחדש סקין', {'mode': 'forceskin'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('טען מחדש פרופיל', {'mode': 'forceprofile'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('סגור את קודי בכפייה', {'mode': 'forceclose'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

    def backup_menu(self):
        directory.add_file('נקה את תיקיית הגיבוי', {'mode': 'clearbackup'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('מיקום גיבוי: [COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.MYBUILDS), {'mode': 'settings', 'name': 'Maintenance'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[גיבוי]: בילד', {'mode': 'backup', 'action': 'build'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[גיבוי]: תיקון Gui', {'mode': 'backup', 'action': 'gui'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[גיבוי]: ערכת נושא', {'mode': 'backup', 'action': 'theme'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[גיבוי]: חבילת הרחבות', {'mode': 'backup', 'action': 'addonpack'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[גיבוי]: נתוני הרחבות', {'mode': 'backup', 'action': 'addondata'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: בילד מקומי', {'mode': 'restore', 'action': 'build'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: תיקון Gui מקומי', {'mode': 'restore', 'action': 'gui'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: ערכת נושא מקומית', {'mode': 'restore', 'action': 'theme'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: חבילת הרחבות מקומית', {'mode': 'restore', 'action': 'addonpack'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: נתוני הרחבות מקומיים', {'mode': 'restore', 'action': 'addondata'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: בילד חיצוני', {'mode': 'restore', 'action': 'build', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: תיקון Gui חיצוני', {'mode': 'restore', 'action': 'gui', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: ערכת נושא חיצונית', {'mode': 'restore', 'action': 'theme', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: חבילת הרחבות חיצונית', {'mode': 'restore', 'action': 'addonpack', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[שחזור]: נתוני הרחבות חיצוניים', {'mode': 'restore', 'action': 'addondata', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

    def tweaks_menu(self):
        directory.add_dir('הגדרות מתקדמות', {'mode': 'advanced_settings'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('סרוק מקורות לקישורים שבורים', {'mode': 'checksources'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('סרוק מאגרים שבורים', {'mode': 'checkrepos'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('הסר שמות קבצים לא ASCII', {'mode': 'asciicheck'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        # directory.add_file('Toggle Passwords On Keyboard Entry', {'mode': 'togglepasswords'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('המר נתיבים ל-special', {'mode': 'convertpath'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('מידע מערכת', {'mode': 'systeminfo'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
