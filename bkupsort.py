from tkinter import Tk, Label, Button, filedialog, PhotoImage, Canvas, Entry, StringVar, HORIZONTAL, LEFT, Text, INSERT
from tkinter.ttk import Progressbar
import os
from bkup.bkupSort import *
import os.path
from pathlib import Path
import shutil
from bkup.tarname_gen import *


#=========This has been tested and a working program=========
#=========Just need to clean it up=======================

#********* IMPORTANT!!! ****************
#*** RUN THIS ONLY IN THE VIRTUALENV ****
#*** RUN pipenv shell under this directory to activate virtual environment ****

# Automatically rename bkup.tar located in PhoneBackup if exists
tarname_gen()

# Double check PATH before running
photo_path = r'G:\Pictures'
video_path = r'G:\Videos'
var_path = r'G:\var'

total_num_of_files = count_files(var_path)
photo_extensions = ['jpg', 'jpeg', 'png']
video_extensions = ['mp4', '3gp']
picture_files = generate_file_type(var_path, photo_extensions)
video_files = generate_file_type(var_path, video_extensions)
overall_total_file_count = count_files(photo_path) + count_files(video_path)

expected_total = overall_total_file_count + total_num_of_files

print(f'Expected total files: {expected_total}')

window = Tk()
window.config(padx=50, pady=50)
window.title('Bkup Sort')
from_folder_text = StringVar()
from_folder_text.set(f'From: {var_path}')
to_folder_text = StringVar()
to_folder_text.set(f'To: {photo_path}')
total_count_info_text = StringVar()
total_count_info_text.set(f'Files From Destination: {total_num_of_files}')
file_moved_text = StringVar()
file_moved_text.set('File Moved: ')
start_text = StringVar()
start_text.set('Start')
in_progress_text = StringVar()
step = 0
overall_count_text = StringVar()
overall_count_text.set(f'Total Files: {overall_total_file_count}')

Discrepancy_value = 0
Discrepancy_text = StringVar()
Discrepancy_text.set(f'Discrepancy: {Discrepancy_value}')


def count_media_files(path, file_type):
    count = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.split('.')[1] in file_type:
                count += 1

    return count


def move_files(media, extensions, where, what):
    global step

    num_files = count_media_files(var_path, extensions)

    p.config(maximum=total_num_of_files)
    in_progress_text.set(f'Moving: {what}')

    for i in range(num_files):
        this_data = next(media)
        file_src = this_data[0]
        filename = this_data[1]
        file_month = this_data[2]
        file_year = this_data[3]

        destination = Path(f'{where}/{file_year}/{file_month}/{filename}')

        make_destination = '\\'.join(str(destination).split('\\')[:-1])

        p['value'] += 1
        step += 1
        file_moved_text.set(f'File Moved: {step}/{total_num_of_files}')

        try:
            shutil.move(file_src, destination)

        except shutil.Error as alreadyExists:
            print(alreadyExists)

        except FileNotFoundError as notFound:
            os.makedirs(make_destination)
            shutil.move(file_src, destination)

        window.update_idletasks()


def start_sort():
    move_files(picture_files, photo_extensions, photo_path, 'Photos')
    window.update_idletasks()
    to_folder_text.set(f'To: {video_path}')
    move_files(video_files, video_extensions, video_path, 'Videos')

    overall_total_file_count = count_files(photo_path) + count_files(video_path)

    overall_count_text.set(f'Total Files: {overall_total_file_count}')

    if expected_total != overall_total_file_count:
        Discrepancy_value = expected_total - overall_total_file_count
        Discrepancy_text.set(f'Discrepancy: {Discrepancy_value}')

    start_text.set('Done')
    start_btn['state'] = 'disabled'


def nothing():
    pass


canvas = Canvas(width=250, height=250)
logo = PhotoImage(file='./data_200.png')
canvas.create_image(125, 100, image=logo)
canvas.grid(row=0, column=0, columnspan=2)

from_folder = Label(textvariable=from_folder_text,
                    font='Helvetica 10 bold', foreground='#464f5d', width='31', anchor='w')
from_folder.config(padx=10, pady=5)
from_folder.grid(row=6, column=0)

to_folder = Label(textvariable=to_folder_text,
                  font='Helvetica 10 bold', foreground='#464f5d', width='31', anchor='w')
to_folder.config(padx=10, pady=5)
to_folder.grid(row=7, column=0)


none = Label(text='')
none.grid(row=8, column=0)
#464f5d 

overall_count = Label(textvariable=overall_count_text, font='Helvetica 10 bold', foreground='#464f5d', width='31', anchor='w')
overall_count.grid(row=9, column=0)

total_count_info = Label(textvariable=total_count_info_text,
                         font='Helvetica 10 bold', foreground='#3b97d3', width='31', anchor='w')
total_count_info.config(padx=5, pady=2)
total_count_info.grid(row=10, column=0)

file_moved = Label(textvariable=file_moved_text,
                    font='Helvetica 10 bold', foreground='#3b97d3', width='31', anchor='w')
file_moved.config(padx=5, pady=2)
file_moved.grid(row=11, column=0)

Discrepancy = Label(textvariable=Discrepancy_text,
                    font='Helvetica 10 bold', foreground='#3b97d3', width='31', anchor='w')
Discrepancy.config(padx=5, pady=2)
Discrepancy.grid(row=12, column=0)

none = Label(text='')
none.grid(row=13, column=0)

p = Progressbar(orient=HORIZONTAL, length=250, mode='determinate')
p.grid(row=14, column=0, columnspan=2)

in_progress = Label(textvariable=in_progress_text,
                    font='Helvetica 10 bold', foreground='#464f5d')
in_progress.config(padx=10, pady=5)
in_progress.grid(row=15, column=0, columnspan=2)


none = Label(text='')
none.grid(row=16, column=0)

start_btn = Button(textvariable=start_text, width=30, font='Helvetica 10 bold',
                   fg='#464f5d', bg='#67b9cc', command=start_sort)
start_btn.grid(row=17, column=0, columnspan=2)


if total_num_of_files == 0:
    start_text.set('source is empty')
    start_btn.config(command=nothing)
    in_progress_text.set(f'No files to move.')
    in_progress.config(fg='#ff5364')


window.mainloop()
