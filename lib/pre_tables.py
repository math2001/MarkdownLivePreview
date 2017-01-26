# -*- encoding: utf-8 -*-

"""
'pre_tables' transform *html* tables into markdown tables, and put them in some <pre><code> tags
"""

from bs4 import BeautifulSoup

def python_table(s_table):
    """Transform BeautifulSoup table into list of list"""
    rows = []
    for row in s_table.find_all('tr'):
        # rows.append(list(map( lambda td: td.text, row.find_all(['th', 'td']) )))
        rows.append(row.find_all(['th', 'td']))
    return rows

def pre_table(s_table):
    rows = python_table(s_table)
    cols_width = [len(cell) for cell in rows[0]]
    for j, row in enumerate(rows):
        for i, cell in enumerate(row):
            if cols_width[i] < len(cell.text):
                cols_width[i] = len(cell.text)
    text = '<pre class="table"><code>'
    for i, row in enumerate(rows):
        if i == 1:
            for j, cell in enumerate(row):
                text += '|' + '-' * (cols_width[j] + 2)
            text += '|\n'

        for j, cell in enumerate(row):
            text += '| '
            if cell.name == 'th':
                title = ' ' * ((cols_width[j] - len(cell.text)) // 2) \
                        + ''.join(str(node) for node in cell.contents) \
                        + ' ' * int(round((cols_width[j] - len(cell.text)) / 2 ) + 1)
                # + 1 because of the added space before the closing | of each cell
                if cols_width[j] + 1 != len(title):
                    title += ' '
                text += title
            else:
                text += ''.join(str(node) for node in cell.contents) \
                        + ' ' * (cols_width[j] - len(cell.text) + 1)
        text += '|\n'
    text += '</pre></code>'
    return text

def pre_tables(html):
    soup = BeautifulSoup(html, 'html.parser')
    for table in soup.find_all('table'):
        table.replace_with(BeautifulSoup(pre_table(table), 'html.parser'))
    return str(soup)
