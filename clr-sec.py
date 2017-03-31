import datetime
import os
import shutil
import time

def del_dir():
    home = os.listdir(os.getcwd())
    if 'sec-imgs' in home:
        print(os.getcwd()+'/sec-imgs')
        shutil.rmtree('./sec-imgs')
        os.mkdir('sec-imgs')
    else:
        os.mkdir('sec-imgs')

    print('\nsec-imgs cleared!')

def del_yesterday(folder):
    today = datetime.datetime.now().strftime('%F')
    day = today[-2:]
    day = int(day)
    yesterday = day - 1
    yest_date = today[:-2]+str(yesterday)

    yesterdays_counter = 0
    todays_counter = 0
    
    # iterates through passed folders files
    for file_ in os.listdir(os.getcwd()+'/sec-imgs/{}'.format(folder)):
        files_date = file_[16:26]
        if files_date == yest_date:
            os.remove(os.getcwd()+'/sec-imgs/'+folder+'/'+file_)
            yesterdays_counter += 1
        else:
            todays_counter += 1

    print('\n{} yesterday files deleted'.format(yesterdays_counter))
    print('{} Todays files\n'.format(todays_counter))
    time.sleep(1)

# iterate through sec-imgs folder and delete yesterday's files



while True:
    answer = raw_input('[A] for del yesterday , [L] for del dir\n')
    if answer == 'a':
        folder = raw_input("Folder Name:\n")
        del_yesterday(folder)
    elif answer == 'l':
        del_dir()
    else:
        exit()

