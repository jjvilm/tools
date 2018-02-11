import subprocess 
import os 

""" An IPFS object manager with python """

class IpfsHash():
    def __init__(self, csv_file="ipfs_hash_objects.csv"):
        self.csv_file = csv_file
        self.named_hash = {}
        self.found_hash = self.find_recursive_hash()
        self.loaded_hash = self.load_hash()


    def find_recursive_hash(self):
        # recommended way after 3.5 python to run a command in shell, converts bytes output to string 
        res = subprocess.run(["ipfs", "pin", "ls", "-t", "recursive"], stdout=subprocess.PIPE).stdout.decode('utf-8')

        # splits it by line to iterate
        res = res.split('\n')

        recursives = []
        for line in res:
            try:
                recursives.append(line[:46])
            except:
                pass
        # returns iter hashes
        return recursives

    def display_hash(self, hash_list, named_dic=''):
        """ enumerates passed hash list """
        # converting to dic hash is key, 
        if named_dic != '':
            hash_list.sort()
            for i, hash_name in enumerate(hash_list):
                print("{}\t{}".format(i+1, hash_name))
        else:
            for i, hash_str in enumerate(self.named_hash.keys()):
                i + 1
                print("{}\t{} {}".format(i, hash_str, self.named_hash[hash_str]))

    # saves to csv file as: hash,name
    def save_hash2csv(self):
        try:
            with open(self.csv_file, 'w') as f:
                for key in self.named_hash.keys():
                    f.write("{},{}\n".format(key, self.named_hash[key]))
                print("{} Saved!".format(self.csv_file))
        except Exception as e:
            print("error in save_hash2csv", e)

    
    def load_hash(self):
        """ Will try to open file, else will return 0 """
        try:
            with open(self.csv_file, 'r') as f:
                self.loaded_hash = f.readlines()
            # remove new line  `\n` at the end of each line
            self.loaded_hash =  [x.strip() for x in self.loaded_hash]

            # load to self.named_hash
            for hash_name in self.loaded_hash:
                if len(hash_name) > 46:
                    #separates hash and name into dictionary
                    self.named_hash[hash_name[:46]] = hash_name[47:]
            return self.loaded_hash

        except Exception as e:
            # if unable to load file then sets default list 
            print("Setting self.loaded_hash == self.found_hash")
            self.loaded_hash = self.found_hash
            print(e)

        

    def give_name(self, new_hash_list, passed_name=None):
        # Automatic naming, runs after add2ipfs 
        try:
            if passed_name != None:
                hash_str =  passed_name[6:52]
                hash_name = passed_name[53:-1]
                self.named_hash[hash_str] = hash_name
                print("ADDed {} {}".format(hash_str, hash_name))
                # appends to self.csv_file
                self.save_hash2csv()
            
            # manually asks to rename found hashes 
            else:
                try:
                    answer = input("\nWould you like to rename NEW FOUND hash?\n[Y][N] [R]remove\t[O] Open  in WebBrowser\n")
                    # asks name for each found hash
                    if answer.lower() == 'y':
                        for hash_name in new_hash_list:
                            given_name = input("\n{}\nRename To:".format(hash_name))
                            self.named_hash[hash_name] = str(given_name)
                            print('Named! and file saved...\n')
                        self.save_hash2csv()
                    elif answer.lower() == 'o':
                        self.open_hash(new_hash_list[0])
                    elif answer.lower() == 'r':
                        self.rmPinned(new_hash_list[0])
                except Exception as e:
                    print("Some error\n{}".format(e))

        except Exception as e:
            print(e, "\nIn give_name()")
            
    def open_hash(self, hash_str='', webbrowser='chromium'):
        """ Opens hash in passed webbrowser, first will try local gateway then ipfs.io """
        if hash_str == '':
            hash_str = input("Enter Hash: ")
        print('Opening:\n{}'.format(hash_str))
        try:
            print("opening with local gateway")
            subprocess.run(["{}".format(webbrowser), "127.0.0.1:8080/ipfs/{}".format(hash_str)])
        except Exception as e:
            print(e)
            try:
                print('Trying with: ipfs.io')
                subprocess.run(["{}".format(webbrowser), "ipfs.io/ipfs/{}".format(hash_str)])
            except Exception as e:
                print("Could not open ipfs.io")
                print(e)

    def rmPinned(self, hash_str=''):
        """ removes passed hash string from local IPFS repo """
        # lets to input if none passed
        if hash_str == '':
            typed_hash = input("IPFS Hash to REMOVE: ")
            try:
                subprocess.run(["ipfs", "pin", "rm", "{}".format(typed_hash)])
                del self.named_hash[typed_hash]
                self.save_hash2csv()
            except Exception as e:
                print(e)
        else:
            subprocess.run(["ipfs", "pin", "rm", "{}".format(hash_str)])
            del self.named_hash[typed_hash]
            self.save_hash2csv()



    def find_new_hash(self):
        """ Returns list of new hases not given a name """
        new_ipfshash_name = []
        new_ipfshash_counter = 0
        # strip name away to comapre hash
        for hazh in self.found_hash:
            # skips empty names
            if hazh == '':
                continue
            if hazh not in self.named_hash.keys():
                print("NEW {}".format(hazh))
                new_ipfshash_name.append(hazh)
                new_ipfshash_counter += 1
        # asks to rename and save list
        if new_ipfshash_counter:
            self.give_name(new_ipfshash_name)
        else:
            print("Nothing new!")

            
    def reset_hash_list(self):
        """ Finds all recursive ipfs objects and saves the hash string withou file names """
        with open('ipfs_hash_objects.csv', 'w') as f:
            for line in self.found_hash:
                f.write(line+'\n')

    def back_up_csv_file(self):
        """ creates a backup of file """
        from shutil import copyfile
        new_name = self.csv_file[:-3] + "bak"
        #creates backup of csv file
        print("Creating csv backup\nSaved as:{}".format(new_name))
        copyfile("./" + self.csv_file, "./" + new_name)


    def addDir2ipfs(self, full_dir_path=''):
        """ Pass a dir path and asks to add files with default file name"""
        if full_dir_path == '':
            full_dir_path = input("Full Path to dir: ")
        try:
            # gets a list of all files in working dir
            print("\nLooking in:\n{}".format(full_dir_path))
            files2add = subprocess.run(["ls", "{}".format(full_dir_path)], stdout=subprocess.PIPE).stdout.decode('utf-8')
            files2add = files2add.split('\n')
            for file_name in files2add:
                # handles empty file names
                if file_name == '':
                    continue
                try:
                    answer = input("\n{}\nADD [y][n]?\n".format(file_name))
                    if answer.lower() == 'y':
                        # add file to IPFS
                        print("Adding file: {}".format(full_dir_path+file_name))
                        # checks "/" is @ end of string
                        if full_dir_path[-1:] == '/':
                            pass
                        else:
                            full_dir_path = full_dir_path + "/"

                        hashNname = subprocess.run(["ipfs", "add", "{}".format(full_dir_path+file_name)], stdout=subprocess.PIPE).stdout.decode('utf-8')
                        # passes name to be saved to file
                        self.give_name('',hashNname)

                except Exception as e:
                    os.chdir(cwd)
                    print(e)

        except Exception as e:
            print("In addDirr2ipfs", e)

    def exit(self):
        print("You selected to exit")
        return 'exit'

    def main(self):
        """ Intended to be used on a terminal """
        import time
        #os.system('clear')
        
        while 1:
            self.display_hash([''])
            method_dic = {'1':self.addDir2ipfs,
                        '2':self.find_new_hash,
                        '3':self.open_hash,
                        '4':self.save_hash2csv,
                        '5':self.back_up_csv_file,
                        '6':self.rmPinned,
                        '7':self.exit}

            print("""
            [1] Add Files
            [2] Find New IPFS Objects
            [3] Open in Browser
            [4] Save 
            [5] Backup
            [6] remove Hash
            [7] Exit """)

            answer = input("\nSelect a function:\n")
            try:
                if method_dic[answer]() == "exit":
                    return
                time.sleep(2)
                os.system('clear')
            except Exception as e:
                print(e)


if __name__  == "__main__":
    O = IpfsHash()
    O.main()
