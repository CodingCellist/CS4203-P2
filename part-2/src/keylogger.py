import csv
from pathlib import Path
import pynput.keyboard as kb
from time import time_ns

# query the user for a location to store the data
csv_file_path = input("Store the data in file: ")
if not csv_file_path.endswith('.csv'):
    csv_file_path += '.csv'

# initialise data fields as empty
travel_data = []
pattern_data = {}
id_pattern = []
pwd_pattern = []
prev_key = ''
# record ID and password in pairs
pwd = False


# path to keep sample count for that data
counter_file = csv_file_path[:-4] + '-counter'
if not Path(counter_file).exists():
    Path(counter_file).touch()
counter_file = open(counter_file, 'r+')
counter_file.seek(0)
try:
    sample_no = int(counter_file.readline())
except ValueError:
    sample_no = 0

# set up the CSV-writer for data storage
csv_file = open(csv_file_path, 'a+', newline='')
pattern_csv = csv.writer(csv_file, delimiter=',', quotechar='"')
if Path(csv_file_path).stat().st_size == 0:
    pattern_csv.writerow(['sample-no', 'input-type', 'char-no', 'time (ns)',
                          'total-time (ns)'])


def log(key):
    global prev_time
    global travel_data
    global id_pattern
    global pwd_pattern
    global pattern_data
    global prev_key
    global sample_no
    global pwd
    elapsed = time_ns() - prev_time
    if key == kb.Key.esc:
        # stop the keylogger
        return False
    elif key != kb.Key.enter:
        travel_data.append((prev_key, str(key), elapsed))
        if pwd:
            # store intervals as password
            pwd_pattern.append(elapsed)
        else:
            # store intervals as user ID
            id_pattern.append(elapsed)
    elif not pwd:
        # if we just got the username, get the password
        pwd = True
    else:
        # record the data
        id_sum = sum(id_pattern)
        pwd_sum = sum(pwd_pattern)
        for i in range(len(id_pattern)):
            pattern_csv.writerow([sample_no, 'id', i, id_pattern[i], id_sum])
        for i in range(len(pwd_pattern)):
            pattern_csv.writerow([sample_no, 'pwd', i, pwd_pattern[i], pwd_sum])
        sample_no += 1
        print('\n', sample_no)
        counter_file.seek(0)
        counter_file.write(str(sample_no) + '\n')
        id_pattern = []
        pwd_pattern = []
        pwd = False
    # print(key, elapsed)
    prev_time = time_ns()
    prev_key = str(key)


# start the keylogger
with kb.Listener(on_press=log) as kb_listener:
    prev_time = time_ns()
    print(sample_no)
    kb_listener.join()
