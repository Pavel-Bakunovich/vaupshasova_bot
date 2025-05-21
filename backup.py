from psycopg2 import pool
import datetime
from dotenv import load_dotenv
import os
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from logger import log, log_error
from helpers import get_today_minsk_time

class Database_backup:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv('DATABASE_URL')
        self.DROPBOX_APP_KEY = os.environ['DROPBOX_APP_KEY']
        self.DROPBOX_APP_SECRET = os.environ['DROPBOX_APP_SECRET']
        self.DROPBOX_REFRESH_TOKEN = os.environ['DROPBOX_REFRESH_TOKEN']
        date = get_today_minsk_time()
        self.time_stamp = date.strftime("%b %d, %Y - %H:%M:%S")
        self.date_stamp = date.strftime("%b %d, %Y")
    
    def save_to_dropbox(self, file_name):
        drp = dropbox.Dropbox(app_key=self.DROPBOX_APP_KEY, app_secret=self.DROPBOX_APP_SECRET, oauth2_refresh_token=self.DROPBOX_REFRESH_TOKEN)
        with open(file_name, 'rb') as file:
            drp.files_upload(file.read(), f"/Backup - {self.date_stamp}/{file_name}")    
            log(f"File '{file_name}' uploaded to Dropbox as 'Backup - {self.date_stamp}'")

    def backup_table(self, table_name):
        connection_pool = pool.SimpleConnectionPool(1, 10, self.connection_string)
        if not connection_pool:
            log("Connection pool not created successfully")
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        cur.fetchall()
        file_name = f"{table_name} - {self.time_stamp}.csv"
        with open(file_name,'wt', encoding='utf-8') as file:
            cur.copy_to(file, table_name, sep=',', null='\\N')
        self.save_to_dropbox(file_name)
        os.remove(file_name)
        conn.close()
        connection_pool.putconn(conn)
        connection_pool.closeall()

    def restore_table(self, table_name, backup_file_name, restore_to_connection_string):
        connection_pool = pool.SimpleConnectionPool(1, 10, restore_to_connection_string)
        conn = connection_pool.getconn()
        cur = conn.cursor()
        #cur.execute(f"TRUNCATE TABLE {table_name}")
        
        with open(backup_file_name, 'rt') as backup_file:
            cur.copy_from(backup_file, table_name, sep=',', null='\\N')
        
        conn.commit()
        conn.close()
        connection_pool.putconn(conn)
        connection_pool.closeall()

'''
# Sample code for restoring database from a backup

backuper = Database_backup()
connection_string = "---"
backuper.restore_table("players", "players - May 21, 2025 - 18:25:00.csv", connection_string)
backuper.restore_table("games", "games - May 21, 2025 - 18:25:00.csv", connection_string)
backuper.restore_table("matchday", "matchday - May 21, 2025 - 18:25:00.csv", connection_string)
'''
