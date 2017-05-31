# This python script processes Sourcemod chat logs, created by
# this plugin: https://forums.alliedmods.net/showthread.php?p=1071512
# It will:
#
# (1)copy them
#   from      original_path
#   to        destination_path
#
# (2)sort them into
#   yyyy\yyyy-mm\ folders
#
# (3)rename them to my preferred format
#   dd-mm-yyyy @ [chat].log
#
# For (3) of course it would be easier to just modify the plugin
# itself, but I wanted to practice Python, so here we are.
#
# Cold'er, 29.04.2017

import re
import os
import time
from shutil import copy2

original_path = 'R:\\test\\'
destination_path = 'R:\\test\\2\\'
full_file_list = os.listdir(original_path)

chat_logs_count = 0
count_error_year = 0
error_year_files = []
count_not_moved = 0
files_removed = 0

print()
print('Found', len(full_file_list), 'files... ', end='')

for i in full_file_list:
    file_pattern = re.match('(?:chat)(\d{2})(\d{2})(\d{2})(?:\.log)', i)  # Match chat311299.log
    if not file_pattern:
        continue
    else:
        chat_logs_count += 1
        file_time = os.path.getmtime(original_path + i)
        file_year = str(time.gmtime(file_time)[0])

        if file_year == '20' + file_pattern.group(3):  # ok till 2100, ok
            date = file_pattern.group(1) + '-' + file_pattern.group(2) + '-' + file_year
        else:
            # If getmtime() returns a wrong year cause some dummy
            # modified the file and dates don't match, use '-20'
            date = file_pattern.group(1) + '-' + file_pattern.group(2) + '-20' + file_pattern.group(3)
            count_error_year += 1
            error_year_files.append(file_pattern.group(0))  # Record conflict files

        folder_y = date[6:]
        folder_m = date[3:5]
        folder_path_format = destination_path + folder_y + '\\' + folder_y + '-' + folder_m + '\\'
        file_path_format = destination_path + folder_y + '\\' + folder_y + '-' + folder_m + '\\' + date + ' @ [chat].log'

        if not os.path.exists(folder_path_format):  # Check and create folders
            os.makedirs(folder_path_format)
        if not os.path.exists(file_path_format):  # Check and copy files
            copy2(original_path + i, file_path_format)
        else:
            count_not_moved += 1

print(chat_logs_count, 'of them are chat logs')


def report_moved_files(n):
    '''
    Input the number of files
    '''
    if n == 1:
        w = 'file has been'
    else:
        w = 'files have been'
    print(n, w, 'copied.')


def report_file_state(n, file_state, error_file_list=None):
    '''
    Input the number of files and 'correct'/'incorrect' and [error file list]
    '''
    if n == 1:
        w = 'file'
    else:
        w = 'files'
    print(n, w, 'with', file_state, 'year.')
    if error_file_list:
        print('\t\tConflict files (modification date does not match the date in the file name):\n\t', error_file_list)


# Remove Error Logs
for i in full_file_list:
    file_pattern = re.match('errors_\d{8}\.log', i)  # Match errors_20170422.log
    if not file_pattern:
        continue
    else:
        os.remove(original_path + str(file_pattern.group(0)))
        files_removed += 1


# Output
print()
report_moved_files(chat_logs_count - count_not_moved)
report_file_state(chat_logs_count - count_error_year, 'correct')
report_file_state(count_error_year, 'incorrect', error_year_files)
print('Removed', files_removed, 'error logs.')
os.system('pause')
