# -*- encoding: utf-8 -*-

import os
import sys
from xml.dom.minidom import parse
from collections import defaultdict

class Style:
    # .highlight is the wrapper class for highlighting therefore
    # all css rules are prefixed with .highlight
    PREFIX = '.highlight'

    # -----------------------------------------
    #  Params
    #  name: the name of the class
    #  args: each argument is an array.
    #  Each array consists of css properties
    #  that is either a color or font style
    #  ----------------------------------------

    def __init__(self, name, *args):
        self.name = name   # Name of the class
        self.rules = {}   # The css rules
        for arr in args:
            for value in arr:
                # Only define properties if they are already not defined
                # This allows "cascading" if rules to be applied
                if value.startswith('#') and 'color' not in self.rules:
                    self.rules['color'] = value
                else:
                    if 'italic' in value and 'font-style' not in self.rules:
                        self.rules['font-style'] = 'italic'
                    if 'underline' in value and 'text-decoration' not in self.rules:
                        self.rules['text-decoration'] = 'underline'
                    if 'bold' in value and 'font-weight' not in self.rules:
                        self.rules['font-weight'] = 'bold'

    # Helper method for creating the css rule
    def _join_attr(self):
        temp = []
        if(len(self.rules) == 0):
            return ''
        for key in self.rules:
            temp.append(key + ': ' + self.rules[key])
        return '; '.join(temp) + ';'

    def toString(self):
        joined = self._join_attr()
        if joined:
            return "%s .%s { %s }" % (Style.PREFIX, self.name, joined)
        return ''


# Crappy xml parsing function for getting the
# colors and font styles from colortheme file


def get_settings(file_name):
    settings = defaultdict(lambda: [])
    dom = parse(file_name)
    arr = dom.getElementsByTagName('array')[0]
    editor_cfg = arr.getElementsByTagName('dict')[0].getElementsByTagName('dict')[0]
    editor_vals = editor_cfg.getElementsByTagName('string')
    background = editor_vals[0].firstChild.nodeValue
    text_color = editor_vals[2].firstChild.nodeValue
    settings['editor_bg'] = background
    settings['text_color'] = text_color
    for node in arr.childNodes:
        if node.nodeName == "dict":
            try:
                setting = node.getElementsByTagName('string')[1].firstChild.nodeValue
                attrs = []
                values = node.getElementsByTagName('dict')[0].getElementsByTagName('string')
                for v in values:
                    if v.firstChild:
                        a = str(v.firstChild.nodeValue).strip()
                        attrs.append(a)
                for s in setting.split(', '):
                    settings[s] = attrs
            except:
                continue
    return settings


def pygments_from_theme(file):
    settings = get_settings(file)
    styles = []

    #Generic
    styles.append(Style('ge', ['italic']))
    styles.append(Style('gs', ['bold']))

    # Comments
    styles.append(Style('c', settings['comment']))
    styles.append(Style('cp', settings['comment']))
    styles.append(Style('c1', settings['comment']))
    styles.append(Style('cs', settings['comment']))
    styles.append(Style('cm', settings['comment.block'], settings['comment']))

    # Constants
    styles.append(Style('m', settings['constant.numeric'], settings['constant.other'], settings['constant'], settings['support.constant']))
    styles.append(Style('mf', settings['constant.numeric'], settings['constant.other'], settings['constant'], settings['support.constant']))
    styles.append(Style('mi', settings['constant.numeric'], settings['constant.other'], settings['constant'], settings['support.constant']))
    styles.append(Style('mo', settings['constant.numeric'], settings['constant.other'], settings['constant'], settings['support.constant']))
    styles.append(Style('se', settings['constant.language'], settings['constant.other'], settings['constant'], settings['support.constant']))
    styles.append(Style('kc', settings['constant.language'], settings['constant.other'], settings['constant'], settings['support.constant']))

    #Keywords
    styles.append(Style('k', settings['entity.name.type'], settings['support.type'], settings['keyword']))
    styles.append(Style('kd', settings['storage.type'], settings['storage']))
    styles.append(Style('kn', settings['support.function.construct'], settings['keyword.control'], settings['keyword']))
    styles.append(Style('kt', settings['entity.name.type'], settings['support.type'], settings['support.constant']))

    #String
    styles.append(Style('settings', settings['string.quoted.double'], settings['string.quoted'], settings['string']))
    styles.append(Style('sb', settings['string.quoted.double'], settings['string.quoted'], settings['string']))
    styles.append(Style('sc', settings['string.quoted.single'], settings['string.quoted'], settings['string']))
    styles.append(Style('sd', settings['string.quoted.double'], settings['string.quoted'], settings['string']))
    styles.append(Style('s2', settings['string.quoted.double'], settings['string.quoted'], settings['string']))
    styles.append(Style('sh', settings['string']))
    styles.append(Style('si', settings['string.interpolated'], settings['string']))
    styles.append(Style('sx', settings['string.other'], settings['string']))
    styles.append(Style('sr', settings['string.regexp'], settings['string']))
    styles.append(Style('s1', settings['string.quoted.single'], settings['string']))
    styles.append(Style('ss', settings['string']))

    #Name
    styles.append(Style('na', settings['entity.other.attribute-name'], settings['entity.other']))
    styles.append(Style('bp', settings['variable.language'], settings['variable']))
    styles.append(Style('nc', settings['entity.name.class'], settings['entity.other.inherited-class'], settings['support.class']))
    styles.append(Style('no', settings['constant.language'], settings['constant']))
    styles.append(Style('nd', settings['entity.name.class']))
    styles.append(Style('ne', settings['entity.name.class']))
    styles.append(Style('nf', settings['entity.name.function'], settings['support.function']))
    styles.append(Style('nt', settings['entity.name.tag'], settings['keyword']))
    styles.append(Style('nv', settings['variable'], [settings['text_color']]))
    styles.append(Style('vc', settings['variable.language']))
    styles.append(Style('vg', settings['variable.language']))
    styles.append(Style('vi', settings['variable.language']))

    #Operator
    styles.append(Style('ow', settings['keyword.operator'], settings['keyword.operator'], settings['keyword']))
    styles.append(Style('o', settings['keyword.operator'], settings['keyword.operator'], settings['keyword']))

    # Text
    styles.append(Style('n', [settings['text_color']]))
    styles.append(Style('nl', [settings['text_color']]))
    styles.append(Style('nn', [settings['text_color']]))
    styles.append(Style('nx', [settings['text_color']]))
    styles.append(Style('bp', settings['variable.language'], settings['variable'], [settings['text_color']]))
    styles.append(Style('p', [settings['text_color']]))

    css = '.highlight { background-color: ' + settings['editor_bg'] + '; color: ' + settings['text_color'] + '; }\n'
    for st in styles:
        css_style = st.toString()
        if css_style:
            css += css_style + '\n'

    return css

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("Please provide the .tmTheme file!", file=sys.stderr)
        sys.exit(1)

    print(pygments_from_theme(args[0]))
