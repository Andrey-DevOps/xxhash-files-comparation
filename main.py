import pathlib
import re
from ubelt import hash_file
import yaml
with open("config.yaml", "r") as f:
    config = yaml.load(f)

#source_path="/Users/andreyyurevich/PycharmProjects/pythonProject/source"
#destination_path="/Users/andreyyurevich/PycharmProjects/pythonProject/dest"
source_path="./"
destination_path="./"

def list_objects(dir_path):
    files = []
    dirs = []
    for object in pathlib.Path(dir_path).rglob("*"):
        if object.is_dir():
            dir = re.sub("^{0}".format(dir_path),"",str(object)).strip("/")
            dirs.append(str(dir))
        elif object.is_file():
            file = re.sub("^{0}".format(dir_path),"",str(object)).strip("/")
            files.append((str(file)))
    return files, dirs

def is_all_subdirs_exists(source_dirs, destination_dirs):
    match=0
    missed_dirs = []
    for source_dir in source_dirs:
        if source_dir in destination_dirs:
            match+=1
        else:
            missed_dirs.append(source_dir)
            print("Directory ./{0} does not exist on destination.".format(source_dir))

    if len(missed_dirs) > 0:
        return False, missed_dirs
    else:
        return True, missed_dirs

def is_all_files_exists(source_files, destination_files):
    match=0
    missed_files = []
    for source_file in source_files:
        if source_file in destination_files:
            match+=1
        else:
            missed_files.append(source_file)
            print("File ./{0} does not exist on destination.".format(source_file))
    if len(missed_files) > 0:
        return False, missed_files
    else:
        return True, missed_files


def compare_check_sums(source_files: list):
    missmatch_hashes=[]
    match_hashes=[]
    for source_file in (source_files):
        if source_file in missed_dirs:
            continue
        source_hash = hash_file("{0}/{1}".format(source_path,source_file),hasher='xx64')
        destination_hash = hash_file("{0}/{1}".format(destination_path,source_file),hasher='xx64')
        if source_hash != destination_hash:
            missmatch_hashes.append([source_file, source_hash, destination_hash])
            print("File {0} has {1} sum, but it must be {2}".format(source_file, destination_hash, source_hash))
        elif source_hash == destination_hash:
            match_hashes.append([source_file, source_hash, destination_hash])
            print("File {0} has correct sum: {1}".format(source_file, destination_hash))
    return missmatch_hashes,match_hashes

source_objects_list = (list_objects(source_path))
destination_objects_list = (list_objects(destination_path))

subdirs_exists = (is_all_subdirs_exists(source_objects_list[1],destination_objects_list[1]))
all_dirs_exists, missed_dirs = (is_all_files_exists(source_objects_list[0],destination_objects_list[0]))
missmatch_hashes, match_hashes=compare_check_sums(source_objects_list[0])
total_dest_files_scanned=(len(match_hashes)+len(missmatch_hashes)*2)

if __name__ == "__main__":
    print("Total destination files checked: ", total_dest_files_scanned)

    if len(missmatch_hashes) == 0:
        print("No corrupted files")
    else:
        print("-----------")
        for i in missmatch_hashes:
            print(i[0], " corrupted")
        print("-----------")
    if len(missed_dirs) == 0:
        print("All directories exists")
    else:
        print("-----------")
        print("Directories missed on destination: ")
        for i in missed_dirs:
            print(i)
        print("-----------")
