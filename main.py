import os
import time
import threading
import configparser
import subprocess, sys
import psutil



config = configparser.ConfigParser()
config.read(f"START.ini")
file_bat = config['Settings']['file_bat']
stoped_file = config['Settings']['stoped_file']

def launcher(procfile):

    print(f'Процесс: {procfile} запущен...')
    
    start_time = time.time()
    pe = subprocess.Popen([sys.executable, f"{procfile}"],
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT)
    outs, errs = pe.communicate()
    

    close_time = int(time.time() - start_time)

    print(f'Процесс: {procfile} время работы = {close_time} sec.\n{'*' * 20}\n{errs}\n{'*' * 20}\n')

    if 'No such file' not in str(outs) and 'No such file' not in str(errs):
        if stoped_file != '':
            white = []
            for el in psutil.pids():
                try:
                    p = psutil.Process(el)
                    if p.name() == 'python.exe':
                        name_procc = (p.cmdline()[-1])   
                        if name_procc == stoped_file:
                            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=p.pid))
                except:
                    print('Не нашел процесс для убийства. Начинаю перезапуск всех процессов...')
                    subprocess.Popen("taskkill /IM Python.exe /F")

        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pe.pid))
        time.sleep(3)
        return launcher(procfile)

    else:
        print(f'-----------------------------------------{procfile} файл не найден...')
        time.sleep(5)
        subprocess.Popen("taskkill /IM Python.exe /F")




if __name__ == "__main__":

    if file_bat != '':
        file_bat = file_bat.split(';')

        for file in file_bat:
            t = threading.Thread(target = launcher, args = (file.strip(), ))
            t.start()

    else:
        print('Вы не указали файлы запуска...')
        time.sleep(5)

