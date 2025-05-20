from psycopg2 import pool
import datetime
from dotenv import load_dotenv
import os
import dropbox
from logger import log, log_error
from helpers import get_today_minsk_time

class Database_backup:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv('DATABASE_URL')
        self.DROPBOX_TOKEN = os.environ['DROPBOX_TOKEN']
        date = get_today_minsk_time()
        self.time_stamp = date.strftime("%b %d, %Y - %H:%M:%S")
        self.date_stamp = date.strftime("%b %d, %Y")

    def save_to_dropbox(self, file_name):
        try:
            drp = dropbox.Dropbox(self.DROPBOX_TOKEN)
            with open(file_name, 'rb') as file:
                drp.files_upload(file.read(), f"/Backup - {self.date_stamp}/{file_name}")    
                log(f"File '{file_name}' uploaded to Dropbox as 'Backup - {self.date_stamp}'")
        except dropbox.exceptions.ApiError as err:
            log(f"API error: {err}")
        except Exception as e:
            log(f"Error: {e}") 

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



