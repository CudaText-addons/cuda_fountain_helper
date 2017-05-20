import os
from cudatext import *
import cudatext_cmd as cmds
from .fo_proc import *


def msg(s):
    msg_status('[Fountain] '+s)


class Command:
    last_name = ''

    def on_key(self, ed_self, key, state):
        #work on Shift+Enter
        if state=='s' and key==13:
            msg('Shift+Enter')
            carets = ed.get_carets()
            if len(carets)>1: return
            y = carets[0][1]
            s = ed.get_text_line(y)
            s = s.upper()
            ed.set_text_line(y, s)
            ed.cmd(cmds.cCommand_KeyEnter)
            return False #block


    def _find_name(self, name_init):
        lines = ed.get_text_all().splitlines()
        items = find_names(lines)

        while True:
            name = dlg_input('Character name (case ignored):', name_init)
            if not name: return
            items = [i for i in items if i['name'].upper()==name.upper()]
            if items:
                self.last_name = name
                break
            else:
                msg_box('Name "%s" not found, try another name'%name, MB_OK+MB_ICONWARNING)

        items_m = ['['+str(i['i']+1)+'] '+i['text'] for i in items]
        res = dlg_menu(MENU_LIST, '\n'.join(items_m))
        if res is None: return
        #print(items[res])
        y = items[res]['i']
        ed.set_caret(0, y, -1, -1)


    def find_name(self):
        names = self._find_all_names()
        if not names:
            msg('No characters found')
            return

        res = dlg_menu(MENU_LIST, '\n'.join(names))
        if res is None: return
        self._find_name(names[res])


    def find_name_caret(self):
        carets = ed.get_carets()
        if len(carets)>1: return
        y = carets[0][1]
        ok, name = get_name_from(ed.get_text_line(y))
        if ok:
            self._find_name(name)
        else:
            msg('Not ok name: '+name)



    def _find_all_names(self):
        lines = ed.get_text_all().splitlines()
        items = find_names(lines)

        names = [i['name'] for i in items]
        return sorted(list(set(names)))


    def _extract_talks(self, name):
        lines = ed.get_text_all().splitlines()
        items = find_names(lines)

        items = [i['text'] for i in items if i['name'].upper()==name.upper()]
        return items


    def extract_talks(self):
        names = self._find_all_names()
        if not names:
            msg('No characters found')
            return

        res = dlg_menu(MENU_LIST, '\n'.join(names))
        if res is None: return

        name = names[res]
        items = self._extract_talks(name)

        text_filename = os.path.basename(ed.get_filename())
        text_caption = 'This file contains all dialogue spoken by "%s" extracted from "%s".'\
            % (name, text_filename)

        file_open('')
        ed.set_prop(PROP_TAB_TITLE, 'from '+name)

        text = '\n\n'.join([text_caption]+items)+'\n'
        ed.set_text_all(text)


    def find_scene(self):
        lines = ed.get_text_all().splitlines()
        items = find_scenes(lines)
        if not items:
            msg('No scenes found')
            return

        items_m = [i['s'] for i in items]
        res = dlg_menu(MENU_LIST, '\n'.join(items_m))
        if res is None: return

        y = items[res]['i']
        ed.set_caret(0, y, -1, -1)


    def on_complete(self, ed_self):
        carets = ed.get_carets()
        if len(carets)>1: return

        x, y, x1, y1 = carets[0]
        s = ed.get_text_line(y)
        len_rt = len(s)-x
        s = s[:x]

        ok, s = get_name_from(s)
        if not ok:
            print('Not a character: '+s)
            return

        names = self._find_all_names()
        #print('names', names)

        res = []
        for name in names:
            if name.startswith(s) and name!=s:
                res.append(name)
        #print('res', res)

        text = '\n'.join(['name|%s|'%name for name in res])
        ed.complete(text, len(s), len_rt, 0, False)
        return True
