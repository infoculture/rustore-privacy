#!/usr/bin/env python
import os, sys
import json
import csv

def process(category=None):    
    repname = category if category else "all"
    f = open('analysis/%s.jsonl' % repname, 'w', encoding='utf8')
    dataset = open('data.jsonl', 'r', encoding='utf8')
    for l in dataset:
        appdata = json.loads(l)
        if category is not None and category not in appdata['categories']: 
            continue
        reppath = os.path.join('reports', appdata['packageName'] + '.json')
        if not os.path.exists(reppath): continue
        print('Processing %s' % (appdata['packageName']))
        repdata = json.load(open(reppath, 'r', encoding='utf8'))
        profile = {'app' : appdata, 'report' : repdata}
        f.write(json.dumps(profile) + '\n')
    f.close()




def load_perms():
    all = []
    f = open('permissions_dangerous.txt', 'r')
    for l in f:
        all.append(l.strip())
    return all
        
PERM_DANG = load_perms()

def report(category=None):
    repname = category if category else "all"

    trackers_table = []
    permissions_table = []
    trackers_all = {}
    full = []

    permissions_all = {}
    for l in open('analysis/%s.jsonl' % repname, 'r', encoding='utf8'):
        o = json.loads(l)
        name = o['app']['packageName']
        n_dang = 0
        perm_dang = []
        perm_normal = []
        for x in o['report']['application']['permissions']:
            v = permissions_all.get(x, {'id' : x,'num' : 0, 'apps' : []})
            v['num'] += 1         
            v['apps'].append(name)
            permissions_all[x] = v
            if x.rsplit('.', 1)[-1] in PERM_DANG:
                n_dang += 1
                perm_dang.append(x)
            else:
                perm_normal.append(x)
        n_tr = len(o['report']['trackers'])
        trackers = [x['name'] for x in o['report']['trackers']]
        for x in o['report']['trackers']:
            v = trackers_all.get(x['id'], {'id' : x['id'], 'name' : x['name'], 'num' : 0})
            v['num'] += 1
            trackers_all[x['id']] = v
        trackers_table.append([name, str(n_tr), ','.join(trackers)])

        permissions_table.append([name, str(len(o['report']['application']['permissions'])), str(n_dang), ','.join(perm_normal), ','.join(perm_dang)])
        full.append([name, o['app']['appName'], o['app']['companyName'], o['app']['shortDescription'], o['app']['versionName'], str(n_tr), ','.join(trackers), str(len(o['report']['application']['permissions'])), str(n_dang), ','.join(perm_normal), ','.join(perm_dang)])


    f = open('analysis/%s_permissions.csv' % repname, 'w', encoding='utf8')
    wr = csv.writer(f, delimiter='\t')
    fieldnames=['id', 'num', 'is_danger', 'apps']
    wr.writerow(fieldnames)
#    wr.writeheader()
    for k, v in permissions_all.items():
        is_danger = True if v['id'].rsplit('.', 1)[-1] in PERM_DANG else False
        wr.writerow([str(v['id']), str(v['num']), str(is_danger), ','.join(v['apps'])])
    f.close()

    f = open('analysis/%s_apps_permissions.csv' % repname, 'w', encoding='utf8')
    wr = csv.writer(f, delimiter='\t')
    fieldnames=['package', 'num', 'num_dang', 'perm_normal', 'perm_dang']
    wr.writerow(fieldnames)
#    wr.writeheader()
    for v in permissions_table:
        wr.writerow(v)
    f.close()

    f = open('analysis/%s_trackers.csv' % repname, 'w', encoding='utf8')
    wr = csv.writer(f, delimiter='\t')
    fieldnames=['id', 'name', 'num']
    wr.writerow(fieldnames)
#    wr.writeheader()
    for k, v in trackers_all.items():
        wr.writerow([str(v['id']), v['name'], str(v['num'])])
    f.close()


    f = open('analysis/%s_apps_trackers.csv' % repname, 'w', encoding='utf8')
    wr = csv.writer(f, delimiter='\t')
    fieldnames=['package', 'num', 'trackers']
    wr.writerow(fieldnames)
#    wr.writeheader()
    for v in trackers_table:
        wr.writerow(v)
    f.close()

    f = open('analysis/%s_full.csv' % repname, 'w', encoding='utf8')
    wr = csv.writer(f, delimiter='\t')
    fieldnames=['package', 'title', 'creator', 'description', 'version', 'trackers_num', 'trackers', 'perm_num_total', 'perm_num_dang', 'perm_normal', 'perm_dang']
    wr.writerow(fieldnames)
#    wr.writeheader()
    for v in full:
        wr.writerow(v)
    f.close()
                               

if __name__ == "__main__":
    category = None
    if len(sys.argv) > 1:
        category=sys.argv[1]
    process(category=category)
    report(category=category)