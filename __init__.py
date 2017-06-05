import os
from cudatext import *
import cudatext_cmd as cmds
from .fo_proc import *


SIDE_TITLE = 'Dialogs'

def msg(s):
    msg_status('[Fountain] '+s)


class Command:
    last_name = ''
    id_list = None
    filename = ''

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


    def fill_side_panel(self, extract_items, name):

        app_proc(PROC_SIDEPANEL_ADD, SIDE_TITLE+',-1,listbox,output.png')
        app_proc(PROC_SIDEPANEL_ACTIVATE, SIDE_TITLE)
        self.id_list = app_proc(PROC_SIDEPANEL_GET_CONTROL, SIDE_TITLE)

        listbox_proc(self.id_list, LISTBOX_DELETE_ALL)
        listbox_proc(self.id_list, LISTBOX_ADD, index=-1, text='(from %s)'%name, tag=-1)

        for i in extract_items:
            text = '%d: ' % (i['i']+1) + i['text']
            listbox_proc(self.id_list, LISTBOX_ADD, index=-1, text=text, tag=i['i'])


    def _extract_talks(self, name):

        lines = ed.get_text_all().splitlines()
        items = find_names(lines)
        items = [i for i in items if i['name'].upper()==name.upper()]

        self.filename = ed.get_filename()
        self.fill_side_panel(items, name)

        return [i['text'] for i in items]


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


    def on_panel(self, ed_self, id_control, id_event):

        if id_control != self.id_list: return

        if id_event=='on_sel':
            sel = listbox_proc(self.id_list, LISTBOX_GET_SEL)
            if sel is None: return
            item = listbox_proc(self.id_list, LISTBOX_GET_ITEM, index=sel)
            if item is None: return
            tag = item[1]
            if tag<0: return

            file_open(self.filename)
            ed.set_caret(0, tag, -1, -1)
            msg_status('Gone to line %d'%tag)
