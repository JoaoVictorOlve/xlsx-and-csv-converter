import os, time

now = time.time()

def remove_files(directory, created_at):
    print("Não tem arquivo")
    for f in os.listdir(directory):
        print("removido")
        if os.stat(os.path.join(directory,f)).st_mtime < now - created_at:
            os.remove(os.path.join(directory, f))
            print("arquivo removido")
    print("verificado")

def schedule_file_removal(directory, created_at):
    while True:
        print("looping passando")
        remove_files(directory, created_at)
        time.sleep(2)