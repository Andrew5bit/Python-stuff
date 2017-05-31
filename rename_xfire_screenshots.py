# My first Python script.
# This will convert file names of Xfire
# screenshots to my preferred format:
# dd-mm-yyyy @ 12h_12m_12s
#
# ...by reading the metadata file:
# _fpsc_metadata.txt
#
# Cold'er, 22.04.2017

import re
import os

fhand = open('R:\\xfire_screens\\_fpsc_metadata.txt')
file_list = []
time_list = []

for line in fhand:
    file_name = re.search('\w+\.jpg(?=\] => Array)', line)
    time_stamp = re.search('(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})', line)
    if file_name:  # build file list
        file_list.append(file_name.group(0))
    if time_stamp:  # format[] and build time list
        time_format = [time_stamp.group(3), time_stamp.group(2), time_stamp.group(1), time_stamp.group(4), time_stamp.group(5), time_stamp.group(6)]
        time_list.append(time_format)

directory = os.listdir('R:\\xfire_screens\\')

for i in directory:
    if i in file_list:
        curr_index = file_list.index(i)
        curr_time = time_list[curr_index]
        os.rename('R:\\xfire_screens\\' + str(i), 'R:\\xfire_screens\\' + str(curr_time[0]) + '-' + str(curr_time[1]) + '-' + str(curr_time[2]) + ' @ ' + str(curr_time[3]) + 'h_' + str(curr_time[4]) + 'm_' + str(curr_time[5]) + 's.jpg')
