import hashlib
import os
import sys
from collections import defaultdict


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def rm_dup(path):
    """relies on the md5 function above to remove duplicate files"""
    if not os.path.isdir(path):  # make sure the given directory exists
        print('specified directory does not exist!')
        return

    md5_dict = defaultdict(list)
    for root, dirs, files in os.walk(path):  # the os.walk function allows checking subdirectories too...
        for filename in files:
            filepath = os.path.join(root, filename)
            file_md5 = md5(filepath)
            md5_dict[file_md5].append(filepath)
    for key in md5_dict:
        file_list = md5_dict[key]
        if len(file_list)>1:
            print(file_list)

if __name__ == '__main__':
    rm_dup(sys.argv[1])
