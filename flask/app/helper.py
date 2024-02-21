import os, time


def remove_files(directory):
    now = time.time()
    for f in os.listdir(directory):
        if os.stat(os.path.join(directory,f)).st_mtime < now - 3600:
            os.remove(os.path.join(directory, f))

def schedule_file_removal(directory):
    while True:
        remove_files(directory)
        time.sleep(3600)