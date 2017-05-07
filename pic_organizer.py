#!/usr/bin/python2
import os
import time
import pickle
import cv2
import commands

#os.chdir('/run/user/1000/gvfs/')
#os.chdir('/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Juan/')
#home_path = os.getcwd()

#home_path = '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Juan/'
home_path = '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Tavo/Desktop/'

sort_year = 'music'
target_path = '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Tavo/{}/'.format(sort_year)

def mkdir_if_unavailable():
    years = []
    for (dirpath, dirnames, filenames) in os.walk(home_path):
        #pass
        #print(dirpath)
        for filename in filenames:
            #print(filename)
            # makes a list of date of year from filename
            years.append(filename[4:8])


    # finds unique dates 
    unique = reduce(lambda l, x: l if x in l else l+[x], years, [])
    uniques = []

    for element in unique:
        if '201' in element[:3]:
            uniques.append(element[:4])
    cwd = os.getcwd()

    for dirpath, dirnames, filenames in os.walk(cwd):
        for dirname in dirnames:
            for element in uniques:
                if element == dirname:
                    print('yes')
                    continue
                else:
                    try:
                        os.mkdir(element)
                    except Exception as e:
                        continue

#def move_files():
#    cwd = os.getcwd()
#    subdir = '/pictures'
#    os.chdir(cwd+subdir)
#    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
#        for dirname in dirnames:
#            for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
#                for filename in filenames:
#                    print(filename)
#                    time.sleep(.1)
#            print(dirname)
#        for filename in filenames:
#            #print("_____\n{}\n{}\n{}\n_____\n".format(dirpath, dirnames,filename))
#            # check ****2000*** date
#            file_format = filename[-3:]
#            if file_format == '3gp':
#                file_path = os.getcwd()+"/"+filename
#                new_path = home_path+"/cell videos/"+filename
#                print(file_path)
#                #print(new_path)
#                #os.rename(file_path, new_path)
#                time.sleep(1)
#            else:
#                continue
                
def check_dir(this_dir):
    for (dirpath, dirnames, filenames) in os.walk(home_path):
        for dirname in dirnames:
            #print(this_dir, dirname)
            if this_dir == dirname:
                return 1
            else:
                continue

def collect_files(dir_path):
    def read_and_save_collection(save = 0):
        ### container list for paths
        file_paths_collection = []
        for (dirpath, dirnames, filenames) in os.walk(dir_path):
            for filename in filenames:
                # add filepath to collection
                file_paths_collection.append(dirpath+"/"+filename)
        ### Saving list
        if save:
            with open('/home/jj/file_collection.pickle', 'w') as f:
                pickle.dump(file_paths_collection, f)
                print("List saved!")
            print("Collected from: {}".format(dir_path))
        else:
            return file_paths_collection

    def get_file_format(file_format, filepath_list):
        counter = 0
        filepaths_w_format = []
        try:
            for filepath in filepath_list:
                file_format_slice_index = filepath.rfind('.')
                found_file_format = filepath[file_format_slice_index+1:]
                if file_format == found_file_format:
                    counter += 1
                    filepaths_w_format.append(filepath)
                    #print(filepath)
            print("Files found by format [{}]: {}".format(file_format,counter))
            return filepaths_w_format
        except Exception as e:
            print(filepath)
            print(e)

    def load_pickled_file_paths(file_collection_path):
#        with open('/home/jj/file_collection.pickle', 'r') as f:
#            pickled_object = pickle.load(f)
#            print(pickled_object)
        with open(file_collection_path, 'r') as f:
            pickled_object = pickle.load(f)
            #print(pickled_object)

        return pickled_object

    def show_images(file_paths_list):
        for img_path in file_paths_list:
            img = cv2.imread(img_path)
            ### turn to OpenCV format
            #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imshow('frame',img)
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    def sort_list(iter_list, sort_year):
        def sort_by_creation():
            sorted_list = []
            for file_path in iter_list:
                ### slices off file name, leaves dir path
                dir_index = file_path.rfind("/")
                dir_path = file_path[:dir_index+1]
                
                ### cd into working dir
                if os.getcwd() != dir_path:
                    os.chdir(dir_path)
                sorted_list.append(commands.getstatusoutput("ls -ltr | awk '{print $9}'"))
                break

            return sorted_list

        def sort_by_year(sort_year):
            os.chdir(home_path)
            ls_output = commands.getstatusoutput("ls -lc")
            ls_output = ls_output[1].split("\n")

            file_names_by_year = []
            for line_status in ls_output:
                line_status = str(line_status)
                file_year = line_status[35:39]
                file_name = line_status.rfind(" ") + 1
                file_name = line_status[file_name:]
                if sort_year == file_year:
                    file_names_by_year.append(home_path+file_name)

            print("Files found by year [{}]: {}".format(sort_year,len(file_names_by_year)))
            return file_names_by_year
            



        return sort_by_year(sort_year)
            
    def mv_files(filepaths_list, mv_to_path):
        if filepaths_list == []:
            return
        print("Move to: {}".format(mv_to_path))
        raw_input("\nIf moving path looks ok, press Enter otherwise interrupt".upper())
        move_counter = 0
        for file_path in filepaths_list:
            try:
                slash_index = file_path.rfind("/") + 1
                file_name = file_path[slash_index:]
                #print("src:{}\ndest:{}\n".format(file_path, mv_to_path+file_name))
                os.rename(file_path, mv_to_path+file_name)
                move_counter += 1
            except Exception as e:
                print(e)
                continue
        else:
            print("Moved [{}] files".format(move_counter))


    file_paths_list = read_and_save_collection(0)

    #file_paths_list = load_pickled_file_paths('/home/jj/file_collection.pickle')

    specified_format_list = get_file_format('mp3', file_paths_list)

    #sorted_by_year_list = sort_list(file_paths_list, sort_year)

    mv_files(specified_format_list,target_path)
    #mv_files(sorted_by_year_list, target_path)


#    show_images(specified_format_list)




#move_files()
collect_files(home_path)
