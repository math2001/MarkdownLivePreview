# -*- encoding: utf-8 -*-

import re

__all__ = ['escape_amp']

RE_REPLACE_AMPERSAND = re.compile(r'&(\w*)(;)?')

def replace(matchobj):
    if matchobj.group(2):
        return matchobj.group(0)
    else:
        return matchobj.group(0).replace('&', '&amp;')

def escape_amp(text):
    return RE_REPLACE_AMPERSAND.sub(replace, text)

def run_tests():
    tests = [
        ['&amp;', '&amp;'],
        ['&amp', '&amp;amp'],
        ['&', '&amp;'],
        ['& &hello &bonjour;', '&amp; &amp;hello &bonjour;']
    ]
    fails = 0
    for i, (subject, result) in enumerate(tests):
        if RE_REPLACE_AMPERSAND.sub(replace, subject) != result:
            # CSW: ignore
            print('TEST FAIL ({i}): {subject!r} escaped did not match {result!r}'.format(**locals()))
            fails += 1
    if fails == 0:
        # CSW: ignore
        print("SUCCESS: every tests ({}) passed successfully!".format(len(tests)))
    else:
        # CSW: ignore
        print("{} test{} failed".format(fails, 's' if fails > 1 else ''))

if __name__ == '__main__':
    run_tests()
