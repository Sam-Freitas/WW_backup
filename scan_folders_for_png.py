import os 
import glob
from pathlib import Path
import arrow
from natsort import natsorted
import shutil
# import tkinter as tk


# path to the main working WormWatcher folder
filesPath = '/Volumes/WormWatcher/WormWatcher'

# number of days want to store as a on computer backup
# default 10
days_of_backup = 10

# generally:    3 sessions/day -> ~675MB/day
#               81 plates/day -> 54.675GB/day
#               10 days of backup -> 546.75GB stored on computer

# path to the backup folder, probably on a seperate hard drive
backup_path = '/e/WW_backup/WormWatcher'

def move_to_backup(move_to,this_path_str):

    # find head and tail (path and name) of where file is going
    head,tail = os.path.split(move_to)

    # if path already to where its going already exists 
    if os.path.isdir(head):
        # if the file doesnt already exist in the backup
        if not os.path.isfile(move_to):
            # move file from this_path_str to move_to 
            shutil.move(this_path_str,move_to)
        # if the file already exists in the backup 
        else:
            # then you can just remove the file as its already backed up
            os.remove(this_path_str)
    # if need to make the path 
    else:
        # recursively make the dirs to where its going
        os.makedirs(head)
        # move file from this_path_str to move_to 
        shutil.move(this_path_str,move_to)

    return 0 

def copy_to_backup(move_to,this_path_str):

    # find head and tail (path and name) of where file is going
    head,tail = os.path.split(move_to)
    # if path already to where its going already exists 
    if os.path.isdir(head):
        # copy file from this_path_str to move_to 
        # unless it already exists in the folder
        if not os.path.isfile(move_to):
            shutil.copy2(this_path_str,move_to)
    else:
        # recursively make the dirs to where its going
        os.makedirs(head)
        # move file from this_path_str to move_to 
        shutil.copy2(this_path_str,move_to)

    return 0


# list of required dirs 
list_of_required_dirs = [
'backups','CoolTerm Libs','CoolTerm Resources','Dependents','Documents','Logs',
'logs','models','old_params_05-Feb-2019_10-28-50','old_params_06-Mar-2019_15-23-58',
'old_params_21-May-2019_12-38-39','ROI_images_24','ROI_images_WM',
'ROI_images_WM_new','Scripts','TestScripts','WormWatcher 1.72',
'WWAnalyzer','WWAnalyzer 2019-06-04 BETA','WWConfig','WWConfigPy','WWCore','WWPythonSupplements','Samples',
]

# find X days before current time
criticalTime = arrow.now().shift(days=-days_of_backup)

# get all the directories from the working directory
dir_list = natsorted(glob.glob(os.path.join(filesPath,'*/')))

# iterate through each dir in the glob list
for item in dir_list:

    # find the basename
    item_name = os.path.basename(os.path.dirname(item))

    # if the basename is NOT included in the required dirs
    if item_name not in list_of_required_dirs:
        print('')
        print(item_name)

        # get the pathlib.Path of this dir
        item_path = Path(item)

        # recursively go through item_path and list all .pngs (Can be changed to whatever storage medium)
        # takes a while
        list_of_png_paths = list(item_path.glob('**/*.png'))

        # number of items moved to backup
        move_file_counter = 0
        copy_file_counter = 0

        # if not empty
        if list_of_png_paths:
            
            # iterate through each png
            for _,this_path in enumerate(list_of_png_paths):
                # find how old the file is
                itemTime = arrow.get(this_path.stat().st_mtime)
                # covnert the path to a str (easier to work with)
                this_path_str = str(this_path)
                # get where the file is going
                move_to = this_path_str.replace(filesPath,backup_path)

                # if the file is older than X days
                if itemTime < criticalTime:
                    # then move it to the backup (removes file)
                    move_to_backup(move_to,this_path_str)
                    move_file_counter = move_file_counter + 1
                
                # if the file is younger than X days
                else:
                    # then copy it to the backup (keeps file)
                    copy_to_backup(move_to,this_path_str)
                    copy_file_counter = copy_file_counter + 1


        print(len(list_of_png_paths), 'items in',item_path)
        print(move_file_counter, 'items moved')
        print(copy_file_counter, 'items copied')


print('end of script')
