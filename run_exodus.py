#!/usr/bin/env python
import os, sys

def run():
    apks = os.listdir('apks')
    for a in apks:
        so = 'exodusa -j -o "%s" "%s"' % (os.path.join('reports', a.rsplit('.', 1)[0] + '.json'), os.path.join('apks', a))
        print(so)
        os.system(so)
                               

if __name__ == "__main__":
    run()