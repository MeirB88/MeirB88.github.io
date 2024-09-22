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
import xbmcgui
import xbmcvfs

import glob
import os
import re

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.gui import window


def parse(file, foldername):
    getid = tools.parse_dom(file, 'addon', ret='id')
    getname = tools.parse_dom(file, 'addon', ret='name')
    addid = foldername if len(getid) == 0 else getid[0]
    title = foldername if len(getname) == 0 else getname[0]
    temp = title.replace('[', '<').replace(']', '>')
    temp = re.sub('<[^<]+?>', '', temp)

    return temp, addid


def whitelist(do):
    addonnames = []
    addonids = []
    addonfolds = []

    dialog = xbmcgui.Dialog()
    
    if do == 'edit':
        fold = glob.glob(os.path.join(CONFIG.ADDONS, '*/'))
        for folder in sorted(fold, key=lambda x: x):
            foldername = os.path.split(folder[:-1])[1]
            if foldername in CONFIG.EXCLUDES:
                continue
            elif foldername in CONFIG.DEFAULTPLUGINS:
                continue
            elif foldername == 'packages':
                continue
            xml = os.path.join(folder, 'addon.xml')
            if os.path.exists(xml):
                a = tools.read_from_file(xml)
                temp, addid = parse(a, foldername)
                addonnames.append(temp)
                addonids.append(addid)
                addonfolds.append(foldername)
        fold2 = glob.glob(os.path.join(CONFIG.ADDON_DATA, '*/'))
        for folder in sorted(fold2, key=lambda x: x):
            foldername = os.path.split(folder[:-1])[1]
            if foldername in addonfolds:
                continue
            if foldername in CONFIG.EXCLUDES:
                continue
            xml = os.path.join(CONFIG.ADDONS, foldername, 'addon.xml')
            xml2 = os.path.join(CONFIG.XBMC, 'addons', foldername, 'addon.xml')
            if os.path.exists(xml):
                a = tools.read_from_file(xml)
            elif os.path.exists(xml2):
                a = tools.read_from_file(xml2)
            else:
                continue
            temp, addid = parse(a, foldername)
            addonnames.append(temp)
            addonids.append(addid)
            addonfolds.append(foldername)
        selected = []
        tempaddonnames = ["-- לחץ כאן להמשך --"] + addonnames
        currentWhite = whitelist(do='read')
        for item in currentWhite:
            logging.log(str(item))
            try:
                name, id, fold = item
            except Exception as e:
                logging.log(str(e))
            if id in addonids:
                pos = addonids.index(id)+1
                selected.append(pos-1)
                tempaddonnames[pos] = "[B][COLOR {0}]{1}[/COLOR][/B]".format(CONFIG.COLOR1, name)
            else:
                addonids.append(id)
                addonnames.append(name)
                tempaddonnames.append("[B][COLOR {0}]{1}[/COLOR][/B]".format(CONFIG.COLOR1, name))
        choice = 1
        while choice not in [-1, 0]:
            choice = dialog.select("{0}: בחר את התוספים שברצונך להוסיף לרשימה הלבנה.".format(CONFIG.ADDONTITLE), tempaddonnames)
            if choice == -1:
                break
            elif choice == 0:
                break
            else:
                choice2 = (choice-1)
                if choice2 in selected:
                    selected.remove(choice2)
                    tempaddonnames[choice] = addonnames[choice2]
                else:
                    selected.append(choice2)
                    tempaddonnames[choice] = "[B][COLOR {0}]{1}[/COLOR][/B]".format(CONFIG.COLOR1, addonnames[choice2])
        white_list = []
        if len(selected) > 0:
            for addon in selected:
                white_list.append("['%s', '%s', '%s']" % (addonnames[addon], addonids[addon], addonfolds[addon]))
            writing = '\n'.join(white_list)
            tools.write_to_file(CONFIG.WHITELIST, writing)
        else:
            try:
                os.remove(CONFIG.WHITELIST)
            except:
                pass
        logging.log_notify(CONFIG.ADDONTITLE,
                           "[COLOR {0}]{1} תוספים ברשימה הלבנה[/COLOR]".format(CONFIG.COLOR2, len(selected)))
    elif do == 'read':
        white_list = []
        if os.path.exists(CONFIG.WHITELIST):
            lines = tools.read_from_file(CONFIG.WHITELIST).split('\n')
            for item in lines:
                try:
                    name, id, fold = eval(item)
                    white_list.append(eval(item))
                except:
                    pass
        return white_list
    elif do == 'view':
        list = whitelist(do='read')
        if len(list) > 0:
            msg = "להלן רשימת הפריטים ברשימה הלבנה שלך, פריטים אלה (יחד עם התלותים) לא יוסרו בעת ביצוע אתחול מחדש או כאשר נתוני המשתמש יוחלפו בהתקנת בנייה.[CR][CR]"
            for item in list:
                try:
                    name, id, fold = item
                except Exception as e:
                    logging.log(str(e))
                msg += "[COLOR {0}]{1}[/COLOR] [COLOR {2}]\"{3}\"[/COLOR][CR]".format(CONFIG.COLOR1, name, CONFIG.COLOR2, id)
            window.show_text_box("צפייה בפריטים ברשימה הלבנה", msg)
        else:
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]אין פריטים ברשימה הלבנה[/COLOR]".format(CONFIG.COLOR2))
    elif do == 'import':
        source = dialog.browse(1, '[COLOR {0}]בחר את קובץ הרשימה הלבנה לייבוא[/COLOR]'.format(CONFIG.COLOR2),
                               'files', '.txt', False, False, CONFIG.HOME)
        logging.log(str(source))
        if not source.endswith('.txt'):
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]הייבוא בוטל![/COLOR]".format(CONFIG.COLOR2))
            return
        current = whitelist(do='read')
        idList = []
        count = 0
        for item in current:
            name, id, fold = item
            idList.append(id)
        lines = tools.read_from_file(xbmcvfs.File(source)).split('\n')
        with open(CONFIG.WHITELIST, 'a') as f:
            for item in lines:
                try:
                    name, id, folder = eval(item)
                except Exception as e:
                    logging.log("Error Adding: '{0}' / {1}".format(item, str(e)), level=xbmc.LOGERROR)
                    continue
                logging.log("{0} / {1} / {2}".format(name, id, folder))
                if id not in idList:
                    count += 1
                    writing = "['{0}', '{1}', '{2}']".format(name, id, folder)
                    if len(idList) + count > 1:
                        writing = "\n%s" % writing
                    f.write(writing)
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]{1} פריטים נוספו[/COLOR]".format(CONFIG.COLOR2, count))
    elif do == 'export':
        source = dialog.browse(3,
                               '[COLOR {0}]בחר היכן ברצונך לייצא את קובץ הרשימה הלבנה[/COLOR]'.format(CONFIG.COLOR2),
                               'files', '.txt', False, False, CONFIG.HOME)
        logging.log(str(source))
        try:
            xbmcvfs.copy(CONFIG.WHITELIST, os.path.join(source, 'whitelist.txt'))
            dialog.ok(CONFIG.ADDONTITLE,
                      "[COLOR {0}]הרשימה הלבנה יוצאה ל:[/COLOR]".format(CONFIG.COLOR2)
                      +'\n'+"[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, os.path.join(source, 'whitelist.txt')))
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]הרשימה הלבנה יוצאה[/COLOR]".format(CONFIG.COLOR2))
        except Exception as e:
            logging.log("שגיאת ייצוא: {0}".format(str(e)), level=xbmc.LOGERROR)
            if not dialog.yesno(CONFIG.ADDONTITLE,
                                "[COLOR {0}]המיקום שבחרת אינו ניתן לכתיבה. האם ברצונך לבחור מיקום אחר?[/COLOR]".format(CONFIG.COLOR2),
                                yeslabel="[B][COLOR springgreen]שנה מיקום[/COLOR][/B]",
                                nolabel="[B][COLOR red]לא בטל[/COLOR][/B]"):
                logging.log_notify(CONFIG.ADDONTITLE,
                                   "[COLOR {0}]ייצוא הרשימה הלבנה בוטל[/COLOR]".format(CONFIG.COLOR2, e))
            else:
                whitelist(do='export')
    elif do == 'clear':
        if not dialog.yesno(CONFIG.ADDONTITLE,
                            "[COLOR {0}]האם אתה בטוח שברצונך לנקות את הרשימה הלבנה שלך?".format(CONFIG.COLOR2)
                            +'\n'+"תהליך זה אינו ניתן לביטול.[/COLOR]",
                            yeslabel="[B][COLOR springgreen]כן הסר[/COLOR][/B]",
                            nolabel="[B][COLOR red]לא בטל[/COLOR][/B]"):
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]ניקוי הרשימה הלבנה בוטל[/COLOR]".format(CONFIG.COLOR2))
            return
        try:
            os.remove(CONFIG.WHITELIST)
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]הרשימה הלבנה נוקתה[/COLOR]".format(CONFIG.COLOR2))
        except:
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]שגיאה בניקוי הרשימה הלבנה![/COLOR]".format(CONFIG.COLOR2))