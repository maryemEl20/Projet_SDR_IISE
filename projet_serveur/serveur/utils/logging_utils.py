import csv
from datetime import datetime
import os

LOG_FILE = 'logs.csv'

def log_event(user_name, status):
    timestamp = datetime.now().isoformat()
    file_exists = os.path.isfile(LOG_FILE)

    if file_exists:
        with open(LOG_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            last_entry = list(reader)[-1]  
            last_timestamp = last_entry[0]
            last_user_name = last_entry[1]
            last_status = last_entry[2]
            
            if user_name == last_user_name and status == last_status:
                return  

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['timestamp', 'user_name', 'status'])  # كتابة رؤوس الأعمدة فقط

        writer.writerow([timestamp, user_name, status])
