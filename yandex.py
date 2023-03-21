#!/usr/bin/env python3

import os, requests, shutil, tarfile, time

from datetime import datetime



ACTIONS = {
    'sites_backup': True,
    'databases_backup': True
}

YANDEX_CONFIG = {
    'yandex_url' : "https://cloud-api.yandex.net/v1/disk/resources",
    'yandex_token' : "yandex_token",
    'yandex_backup_folder' : "/backup/",
}

TEMP_PATH = '/tmp/backup/'

SITES = [
    {"path": "/path/your/file", "arch_name": "arch_name"},
]

DATABASES = [
    {"db_name": "database_name", "login-path": "login-path"},
]



def main():
    if os.path.exists(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)
    os.mkdir(TEMP_PATH)

    # Backup files
    if ACTIONS['sites_backup']:
        print("Backup sites:")
        for site in SITES:
            site_arch_file = backup_file(site)
            if site_arch_file:
                upload_file(site_arch_file)

    # Backup MySQL databases
    if ACTIONS['databases_backup']:
        print("Backup databases:")
        for database in DATABASES:
            dump_arch_file = backup_database(database)
            if dump_arch_file:
                upload_file(dump_arch_file)

    shutil.rmtree(TEMP_PATH)


# Upload file to Yandex Disk
def upload_file(loadfile, replace=False):
    print(f"\tupload {loadfile}")
    """
    savefile: Path on Yandex Disk
    replace: true or false replace file on Yandex Disk
    loadfile: File for upload
    """
    yandex_url = YANDEX_CONFIG['yandex_url']
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f"OAuth {YANDEX_CONFIG['yandex_token']}"}
    savefile = YANDEX_CONFIG['yandex_backup_folder'] + loadfile.split("/")[-1]

    res = requests.get(f'{yandex_url}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file':f})
        except KeyError:
            print(res)


# Create files archive 
def backup_file(site):
    try:
        print(f"\t{site['path']}")
        site_arch_file = TEMP_PATH + site['arch_name'] + datetime.now().strftime("_%Y-%m-%d_%H-%M-%S") + ".tar.gz"
        with tarfile.open(site_arch_file, "w:gz") as tar:
            tar.add(site['path'], arcname=os.path.basename(site['path']))
        tar.close()

        result = site_arch_file

    except:
        result = False

    return result


# Create dump MySQL database
def backup_database(database):
    try:
        print(f"\t{database['db_name']}")
        # create mysqldump
        dump_file = database['db_name'] + ".sql"
        os.popen("mysqldump --login-path=%s %s --no-tablespaces > %s" % (database['login-path'], database['db_name'], TEMP_PATH + dump_file))

        time.sleep(5)

        # Create arch mysqldump
        dump_arch_file = TEMP_PATH + dump_file + datetime.now().strftime("_%Y-%m-%d_%H-%M-%S") + ".tar.gz"
        tar = tarfile.open(dump_arch_file, "w:gz")
        tar.add(TEMP_PATH + dump_file, recursive=False)
        tar.close()

        result = dump_arch_file

    except:
        result = False

    return result



if __name__ == "__main__":
    main()
