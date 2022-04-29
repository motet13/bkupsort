from datetime import datetime
import os
from pathlib import Path
import tarfile


### Rename bkup.tar to bkup_[ date ]_[ time ]{ [ num files in tar ]}.tar format ###
def tarname_gen():
    now = datetime.now()
    date = now.date().strftime('%Y%m%d')
    time = now.time().strftime('%H%M%S')

    tarfile_root = Path(os.environ.get("BKUPSORT_TARFILEROOT"))

    original_tarfile = f'{tarfile_root}\\bkup.tar'

    if os.path.exists(original_tarfile):
        with tarfile.open(original_tarfile) as tar:
            for count, _ in enumerate(tar, start=1):
                num_files = count

        new_tarfile_name = f'{tarfile_root}\\bkup_{date}_{time}{{{num_files}}}.tar'
        os.rename(original_tarfile, new_tarfile_name)