#!/usr/bin/python2
import os
import time
import pickle
import cv2
import commands

# os.chdir('/run/user/1000/gvfs/')
# os.chdir('/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Juan/')
# home_path = os.getcwd()

# home_path = '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Juan/'
home_path = '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Rachel'
#home_path = '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Rachel//IPad photos from Raquel l/'
# home_path = '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Rachel/'

SORT_YEAR = '2012'

years_with_pics = {}
current_directory_names = []
# mv_to_target_path =
# '/run/user/1000/gvfs/smb-share:server=192.168.0.1,share=root/Tavo/{}/'.format(SORT_YEAR)

# Index slice to find the year
year_s = 35
year_e = 39


def mkdir_if_unavailable():
    global current_directory_names
    os.chdir(home_path)
    print("Checking These directory names:\n{}\n".format(years_with_pics.keys()))

    for year in years_with_pics.keys():
        if check_dir(str(year)):
            print('directory found for {}'.format(year))
        else:
            print("Making directory {}".format(year))
            os.mkdir(str(year))


def check_dir(directory_name):
    # collects dirnames
    if current_directory_names == []:
        print("Gathering Direcotry names first...")
        for (dirpath, dirnames, filenames) in os.walk(home_path):
            for dirname in dirnames:
                current_directory_names.append(dirname)
    # Matched directory name
    for dirname in current_directory_names:
        if directory_name == dirname:
            return 1
        else:
            continue


def collect_files(dir_path):
    def read_and_save_collection(save=0):
        # container list for paths
        file_paths_collection = []
        # collects file names
        for (dirpath, dirnames, filenames) in os.walk(dir_path):
            for filename in filenames:
                # add filepath to collection
                file_paths_collection.append(dirpath + "/" + filename)
        # Saving list
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
                found_file_format = filepath[file_format_slice_index + 1:]
                if file_format == found_file_format:
                    counter += 1
                    filepaths_w_format.append(filepath)
            print("Files found by format [{}]: {}".format(file_format, counter))
            return filepaths_w_format
        except Exception as e:
            print(filepath)
            print(e)

    def load_pickled_file_paths(file_collection_path):
        with open(file_collection_path, 'r') as f:
            pickled_object = pickle.load(f)
        return pickled_object

    def show_images(file_paths_list):
        for img_path in file_paths_list:
            img = cv2.imread(img_path)
            cv2.imshow('frame', img)
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    def sort_list(iter_list, sort_year):
        def sort_by_creation():
            sorted_list = []
            for file_path in iter_list:
                # slices off file name, leaves dir path
                dir_index = file_path.rfind("/")
                dir_path = file_path[:dir_index + 1]

                # cd into working dir
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
                file_year = line_status[year_s:year_e]
                file_name = line_status.rfind(" ") + 1
                file_name = line_status[file_name:]
                try:
                    if int(sort_year) == int(file_year):
                        # print('year Found!')
                        file_names_by_year.append(home_path + file_name)
                    else:
                        # print('Year {} not in:{}'.format(sort_year,line_status))
                        pass
                except:
                    # print("Not a Number:{}".format(file_year))
                    continue

            print("Files found by year [{}]: {}".format(sort_year, len(file_names_by_year)))
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

                # print("src:{}\ndest:{}\n".format(file_path, mv_to_path + file_name))
                os.rename(file_path, mv_to_path + file_name)
                move_counter += 1
            except Exception as e:
                print(e)
                continue
        else:
            print("Moved [{}] files".format(move_counter))

    def find_years_range(sorted_list, start_year, end_year):
        global years_with_pics, current_directory_names

        for i in xrange(end_year - start_year + 1):
            sorted_by_cur_year = sort_list(sorted_list, start_year)
            if len(sorted_by_cur_year) > 0:
                years_with_pics[start_year] = sorted_by_cur_year
            # print("Year:{} Found:{}".format(start_year, len(sorted_by_cur_year)))
            start_year += 1
        current_directory_names = years_with_pics.keys()


    # collects file paths, saves list or not
    file_paths_list = read_and_save_collection(1)

    # loads saved file paths list
    file_paths_list = load_pickled_file_paths('/home/jj/file_collection.pickle')

    # collect files based on format
    specified_format_list = get_file_format('PNG', file_paths_list)

#   for line in specified_format_list:
#       #print(line)
#       dot_i = line.rfind('.') 
#       b_slash = line.rfind('/') + 1
#       file_name = line[b_slash:]
#       file_format = line[dot_i:]
#       new_name = line[:dot_i] + '.png'
#       os.rename(line, new_name)

#   sorted_by_year_list = sort_list(file_paths_list, SORT_YEAR)
#   sorted_by_year_list = sort_list(specified_format_list, SORT_YEAR)
#   find_years_range(specified_format_list, 2008, 2017)


#   mv_files(specified_format_list,mv_to_target_path)
#   mv_files(sorted_by_year_list, mv_to_target_path)



#   show_images(specified_format_list)
    # moves files to its specified directory
    # based on a dictionary containg dirs with a list of full file paths
#   mkdir_if_unavailable()
#   for key in years_with_pics.keys():
#       mv_files(years_with_pics[key], home_path + str(key) + "/")


# move_files()
collect_files(home_path)

