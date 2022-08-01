#!/usr/bin/env python
import requests
import sys
import os
import json
import logging

DEFAULT_TIMEOUT = 30
DEFAULT_CHUNK_SIZE = 256 * 256 * 256

def get_file(url, filename, aria2=False, aria2path=None, timeout=DEFAULT_TIMEOUT):
    logging.info('Retrieving %s from %s' % (filename, url))
    page = requests.get(url, stream=True, verify=False, timeout=timeout)
    if not aria2:
        f = open(filename, 'wb')
        total = 0
        chunk = 0
        for line in page.iter_content(chunk_size=DEFAULT_CHUNK_SIZE):
            chunk += 1
            if line:
                f.write(line)
            total += len(line)
            if chunk % 1000 == 0:
                logging.debug('File %s to size %d' % (filename, total))
        f.close()
    else:
        dirpath = os.path.dirname(filename)
        basename = os.path.basename(filename)
        if len(dirpath) > 0:
            s = "%s --retry-wait=10 -d %s --out=%s %s" % (aria2path, dirpath, basename, url)
        else:
            s = "%s --retry-wait=10 --out=%s %s" % (aria2path, basename, url)
        logging.info('Aria2 command line: %s' % (s))
        os.system(s)
    return filename


def run():
    f = open('data/data.jsonl', 'r', encoding='utf8')
    for l in f:
        r = json.loads(l)
        print('Processing %s (%s)' % (r['packageName'], r['apkUid']))
        filename = os.path.join('apks', r['packageName'] + '.apk')
        if not os.path.exists(filename):
            get_file('https://static.rustore.ru/%s' % (r['apkUid']), filename)
            print('Downloaded %s' % (r['packageName']))
           



if __name__ == "__main__":
    run()