import os
import itertools
import shutil
from datetime import date, datetime
import platform
from pathlib import Path

current_platfrom = platform.system()


def count_files(path):
    """ Count files in given path. """

    counter = itertools.count(start=0)

    for root, _, files in os.walk(path):
        for _, name in enumerate(files, start=1):
            if os.path.isfile(os.path.join(root, name)):
                next(counter)

    return next(counter)


def generate_file_type(directory, file_type):
    """
    Yield files according to their file extensions. This way,
    images and videos are separated.
    """

    with os.scandir(directory) as it:
        for entry in it:
            mod_time = date.fromtimestamp(os.path.getmtime(entry.path))

            if entry.name.split('.')[1] in file_type:
                yield entry.path, entry.name, mod_time.strftime('%b'), mod_time.strftime('%Y')


existed_files = []


def move_file(yielded_files, dest_root, verbose=False):
    """ Move and sort files according to their modified timestamps. """

    print(f'Moving files into {dest_root}')

    for path, file, mod_month, mod_year in yielded_files:

        year_month = Path(f"{dest_root}/{mod_year}/{mod_month}")
        year_month_file = Path(f"{dest_root}/{mod_year}/{mod_month}/{file}")


        if os.path.exists(year_month):

            if os.path.exists(year_month_file):
                print(f'{file} in {year_month} already exist!')
                # existed_files.append(path)

            else:
                if verbose:
                    print(f'moving {path} --> {year_month}')
                # shutil.move(path, year_month)

        else:
            print(f'making {year_month}')
            # os.makedirs(f'{year_month}', mode=0o777, exist_ok=False)
            if verbose:
                print(f'moving {path} --> {year_month}')
            # shutil.move(path, year_month)


def move_existed_files(dest):
    """ Create timestamp folder and move files into it. """

    time_now = datetime.today()
    folder_name = time_now.strftime('%Y%m%d_%H%M%S')

    dest_folder_name = Path(dest/folder_name)

    os.makedirs(dest_folder_name)

    for file in existed_files:
        shutil.move(file, dest_folder_name)


def add_total_files_in_path(path_1, path_2):
    """ Add total counts from given paths """

    count_path1 = count_files(path_1)
    count_path2 = count_files(path_2)
    total_count = count_path1 + count_path2

    return total_count
