# coding: utf-8
from airtable import Airtable
import time
import pprint
import requests
import json

def get_airtable_key(filename):
    f = open(filename, 'r', encoding='utf8')
    key = f.read()
    f.close()
    return key


AIRTABLE_API_DB = 'app5nfpdGUNScgwGV'
AIRTABLE_API_KEY = get_airtable_key('airtable.key')     # airtable.key is a local text file, write key into it
TABLE_APPS = 'Apps'
TABLE_TRACKERS = 'Trackers'
TABLE_PERMISSIONS = 'Permissions'
TABLE_COUNTRIES = 'Countries'
TABLE_COMPANIES = 'Tracking companies'
TABLE_APP_TRACKERS = ''

def load_perms():
    all = []
    f = open('permissions_dangerous.txt', 'r')
    for l in f:
        all.append(l.strip())
    return all
        
PERM_DANG = load_perms()


def write_apps_table():
    f = open('analysis/all.jsonl', 'r', encoding='utf8')
    table_apps = Airtable(AIRTABLE_API_DB, TABLE_APPS, api_key=AIRTABLE_API_KEY)
    for l in f:
        data = json.loads(l)
        record = {}
        for k in ['packageName', 'appId', 'apkUid', 'shortDescription', 'fullDescription', 'versionName']: 
            record[k] = str(data['app'][k])
        record['categories'] = ','.join(data['app']['categories'])
        record['num_trackers'] = len(data['report']['trackers'])
        trackers_ids = []
        for t in data['report']['trackers']:
            trackers_ids.append(str(t['id']))
        record['trackers'] = ','.join(trackers_ids)

        record['num_permissions'] = len(data['report']['application']['permissions'])
        trackers_ids = []
        for t in data['report']['application']['permissions']:
            trackers_ids.append(t)
        record['permissions'] = ','.join(trackers_ids)
        table_apps.insert(record)
        print('Wrote %s' % (record['packageName']))
    f.close()


def write_trackers_table():
    f = open('analysis/all.jsonl', 'r', encoding='utf8')
    table_apps = Airtable(AIRTABLE_API_DB, TABLE_TRACKERS, api_key=AIRTABLE_API_KEY)
    trackers = {}
    for l in f:
        data = json.loads(l)
        for item in data['report']['trackers']: 
            iid = str(item['id'])
            if iid not in trackers.keys():
                trackers[iid] = item
                trackers[iid]['id'] = str(trackers[iid]['id'])
                trackers[iid]['num_apps'] = 1
                trackers[iid]['apps'] = data['app']['packageName']
            else:
                trackers[iid]['num_apps'] += 1
                trackers[iid]['apps'] += ',' + data['app']['packageName']

    for k, v in trackers.items():
        record = v
        table_apps.insert(record)
        print('Wrote %s' % (record['name']))
    f.close()

def write_trac_table():
    f = open('analysis/all.jsonl', 'r', encoding='utf8')
    table_apps = Airtable(AIRTABLE_API_DB, TABLE_TRACKERS, api_key=AIRTABLE_API_KEY)
    trackers = {}
    for l in f:
        data = json.loads(l)
        for item in data['report']['trackers']: 
            iid = str(item['id'])
            if iid not in trackers.keys():
                trackers[iid] = item
                trackers[iid]['id'] = str(trackers[iid]['id'])
                trackers[iid]['num_apps'] = 1
                trackers[iid]['apps'] = data['app']['packageName']
            else:
                trackers[iid]['num_apps'] += 1
                trackers[iid]['apps'] += ',' + data['app']['packageName']

    for k, v in trackers.items():
        record = v
        table_apps.insert(record)
        print('Wrote %s' % (record['name']))
    f.close()

def write_permissions_table():
    f = open('analysis/all.jsonl', 'r', encoding='utf8')
    table_apps = Airtable(AIRTABLE_API_DB, TABLE_PERMISSIONS, api_key=AIRTABLE_API_KEY)
    trackers = {}
    for l in f:
        data = json.loads(l)        
        for item in data['report']['application']['permissions']: 
            iid = item
            if iid not in trackers.keys():
                trackers[iid] = {'id' : item}
                trackers[iid]['num_apps'] = 1
                trackers[iid]['apps'] = data['app']['packageName']
                trackers[iid]['is_danger'] = True if item.rsplit('.', 1)[-1] in PERM_DANG else False
            else:
                trackers[iid]['num_apps'] += 1
                trackers[iid]['apps'] += ',' + data['app']['packageName']

    for k, v in trackers.items():
        record = v
        table_apps.insert(record)
        print('Wrote %s' % (record['id']))
    f.close()

def write_permissions_table():
    f = open('analysis/all.jsonl', 'r', encoding='utf8')
    table_apps = Airtable(AIRTABLE_API_DB, TABLE_PERMISSIONS, api_key=AIRTABLE_API_KEY)
    trackers = {}
    for l in f:
        data = json.loads(l)        
        for item in data['report']['application']['permissions']: 
            iid = item
            if iid not in trackers.keys():
                trackers[iid] = {'id' : item}
                trackers[iid]['num_apps'] = 1
                trackers[iid]['apps'] = data['app']['packageName']
                trackers[iid]['is_danger'] = True if item.rsplit('.', 1)[-1] in PERM_DANG else False
            else:
                trackers[iid]['num_apps'] += 1
                trackers[iid]['apps'] += ',' + data['app']['packageName']

    for k, v in trackers.items():
        record = v
        table_apps.insert(record)
        print('Wrote %s' % (record['id']))
    f.close()


def update_companies_table():
    table_apps = Airtable(AIRTABLE_API_DB, TABLE_TRACKERS, api_key=AIRTABLE_API_KEY)
    companies = {}
    for app in table_apps.get_all():
        fields = app['fields']
        company = fields['company_name']        
        if len(company) == 0: continue
        company = company[0]
        if company not in companies.keys():
            companies[company] = {'name' : company,  'country' : fields['country_name'][0], 'website' : fields['website'], 
            'num_trackers' : 1, 'num_apps' : fields['num_apps']}
        else:
            companies[company]['num_trackers'] += 1
            companies[company]['num_apps'] += fields['num_apps']

    table_comp = Airtable(AIRTABLE_API_DB, TABLE_COMPANIES, api_key=AIRTABLE_API_KEY)
    for comp in table_comp.get_all():
        name = comp['fields']['name']
        if name in companies.keys():
            for k in ['website', 'num_trackers', 'num_apps', 'country']:
                comp['fields'][k] = companies[name][k]
        print('Updated %s' % (name))
        print(comp['fields'])
        table_comp.update(comp['id'], comp['fields'])

def update_countries_table():
    table_comp = Airtable(AIRTABLE_API_DB, TABLE_COMPANIES, api_key=AIRTABLE_API_KEY)
    countries = {}
    for app in table_comp.get_all():
        fields = app['fields']
        country = fields['country_name']        
        if len(country) == 0: continue
        country = country[0]
        if country not in countries.keys():
            countries[country] = {'name' : country, 'num_companies' : 1,
            'num_trackers' :  fields['num_trackers'], 'num_apps' : fields['num_apps']}
        else:
            countries[country]['num_companies'] += 1
            countries[country]['num_trackers'] += fields['num_trackers']
            countries[country]['num_apps'] += fields['num_apps']

    table_count = Airtable(AIRTABLE_API_DB, TABLE_COUNTRIES, api_key=AIRTABLE_API_KEY)
    for count in table_count.get_all():
        name = count['fields']['name']
        if name in countries.keys():
            for k in ['num_companies', 'num_trackers', 'num_apps']:
                count['fields'][k] = countries[name][k]
        print('Updated %s' % (name))
        print(count['fields'])
        table_count.update(count['id'], count['fields'])

def update_apps_table():
    f = open('analysis/all.jsonl', 'r', encoding='utf8')
    packages = {}
    for l in f:
        row = json.loads(l)
        packages[row['app']['packageName']] = row['app']
    f.close()

    table_apps = Airtable(AIRTABLE_API_DB, TABLE_APPS, api_key=AIRTABLE_API_KEY)
    for app in table_apps.get_all():
        fields = app['fields']
        outf = {}
        outf['icon_url'] = packages[fields['packageName']]['iconUrl']
        outf['app_url'] = 'https://apps.rustore.ru/app/' + fields['packageName']        
        table_apps.update(app['id'], outf)
        print('Updated %s' % (fields['packageName']))
#        break

if __name__ == "__main__":
    update_apps_table()
#    update_countries_table()
#    update_companies_table()
#    write_apps_table()
#    write_permissions_table()
#    write_trackers_table()
   