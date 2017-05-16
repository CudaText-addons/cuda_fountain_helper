from cudatext import *
import cudatext_cmd as cmds


def get_name_from(s):
    """
    Extraxt name from line, strip () and @ and ^
    """
    n = s.find('(')
    if n>=0:
        s = s[:n]

    if s.endswith('^'):
        s = s[:-1]

    ok = False
    if s.startswith('@'):
        s = s[1:]
        ok = True
    elif s.isupper():
        ok = True

    return (ok, s.strip())


def find_data(lines):
    """
    Find character names in fountain text.
    Also strip brackets from end of name.
    @str is always a name.
    """
    res = []
    for (i, s) in enumerate(lines):
        if not s: continue
        if i==0 or i==len(lines)-1: continue

        ok = lines[i-1]=='' and lines[i+1]!=''
        if not ok: continue

        ok, s = get_name_from(s)
        if ok:
            text = lines[i+1]
            if text.startswith('(') and i+2<len(lines):
                text = lines[i+2]
            res.append({'name': s, 'i': i, 'text': text})
    return res


class Command:
    last_name = ''

    def on_key(self, ed_self, key, state):
        #work on Shift+Enter
        if state=='s' and key==13:
            msg_status('[Fountain Helper] Shift+Enter')
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
        items = find_data(lines)

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
            msg_status('Not ok name: '+name)



    def _find_all_names(self):
        lines = ed.get_text_all().splitlines()
        items = find_data(lines)

        names = [i['name'] for i in items]
        return sorted(list(set(names)))


    def _extract_talks(self, name):
        lines = ed.get_text_all().splitlines()
        items = find_data(lines)

        items = [i['text'] for i in items if i['name'].upper()==name.upper()]
        return items


    def find_talks(self):
        names = self._find_all_names()
        res = dlg_menu(MENU_LIST, '\n'.join(names))
        if res is None: return

        name = names[res]
        items = self._extract_talks(name)

        file_open('')
        ed.set_prop(PROP_TAB_TITLE, 'from '+name)

        text = '\n\n'.join(items)+'\n'
        ed.set_text_all(text)
