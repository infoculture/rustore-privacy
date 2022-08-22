# rustore-privacy
Rustore privacy analysis source code and data

Script update_db.py generates and updates Airtable database table. Require key in file `airtable.key`, obtain it in Airtable API docs.

## Dependencies

* Exodus core. Install `pip3 install exodus-core`. More info https://github.com/Exodus-Privacy/exodus-core
* APIBackuper. Install `pip3 install apibackuper`. More info https://github.com/ruarxive/apibackuper

## Collect API data

1. Switch to `data` dir
2. Use `apibackuper run`

## Export API data
1. Switch to `data` dir
2. Use`apibackuper export data.jsonl`

## Collect APK files
1. Run `python3 run.py`

## Extract permissions and trackers info from APKs
1. Run `python3 run_exodus.py`

## Analyze trackers and permissions

Analyze all applications. Produces all.jsonl and other files with `all` prefix in analysis dir

`python3 analyze.py`


Applications by category. For example 'state' apps. Produces sate.jsonl and other files with `state` prefix in analysis dir

`python3 analyze.py state`


## Exported report data

Folder `export` includes data from report 'Rustore mobile apps privacy' http://rustoreprivacy.infoculture.ru/

Original database available at Airtable https://airtable.com/app5nfpdGUNScgwGV/tblgxkjdS85sjZUfD/viwpqPIhuc8cZdZJi?blocks=hide 

Write infoculture@infoculture.ru for access