import os 
import glob
from pathlib import Path
import arrow
from natsort import natsorted
import shutil
# import tkinter as tk

filesPath = '/Volumes/WormWatcher/WormWatcher'

days_of_backup = 12

backup_path = '/e/WW_backup/WormWatcher'

list_of_required_dirs = [
'backups','CoolTerm Libs','CoolTerm Resources','Dependents','Documents',
'logs','models','old_params_05-Feb-2019_10-28-50','old_params_06-Mar-2019_15-23-58',
'old_params_21-May-2019_12-38-39','ROI_images_24','ROI_images_WM',
'ROI_images_WM_new','Scripts','TestScripts','WormWatcher 1.72',
'WWAnalyzer','WWAnalyzer 2019-06-04 BETA','WWConfig','WWConfigPy','WWCore','WWPythonSupplements','Samples',
]

criticalTime = arrow.now().shift(days=-days_of_backup)

# all_files = glob.glob(os.path.join(filesPath), recursive=True)

# for item in Path(filesPath).glob('/*'):

dir_list = natsorted(glob.glob(os.path.join(filesPath,'*/')))

for item in dir_list:

    item_name = os.path.basename(os.path.dirname(item))

    if item_name not in list_of_required_dirs:
        print(item_name)

        item_path = Path(item)

        list_of_png_paths = list(item_path.glob('**/*.png'))

        if list_of_png_paths:
            
            for count,this_path in enumerate(list_of_png_paths):
                itemTime = arrow.get(this_path.stat().st_mtime)

                if itemTime < criticalTime:
                    this_path_str = str(this_path)
                    move_to = this_path_str.replace(filesPath,backup_path)

                    head,tail = os.path.split(move_to)

                    if os.path.isdir(head):
                        pass
                    else:
                        os.makedirs(head)

                    pass
                else:
                    print(this_path)

        print(len(list_of_png_paths), 'items in',item_path)

        # for path in Path(item).rglob('*.png'):

        #     list_of_png_paths.append(path._str)



# ww_path =

# all_folders = glob.glob(os.path.join(ww_path,'*/'))

# list_of_png_paths = []

# if os.path.isdir(ww_path):

#     for path in Path(ww_path).rglob('*.png'):
#         list_of_png_paths.append(path._str)

# else:
#     print('Not connectect to server')

# print('end')