import os
import bibtexparser as bp
from pathlib import Path
import pickle
def file_fetcher(bib_Lib, directory):
    other_bib_Lib = bp.Library()
    directory = directory+"/bib_files"
    bib_folders = [folder for folder in os.listdir(directory)]
    bib_folders.sort()
    for folder in bib_folders:
        bib_files = [bib_ref for bib_ref in os.listdir(directory+"/"+folder)]
        print(bib_files)
        for bib_file in bib_files:
            try:
                bib_ref = bp.parse_file(directory+"/"+folder+"/"+bib_file)
                bib_ref.entries[0]['repo'] = directory
                if folder == "other":
                    other_bib_Lib.add(bib_ref.entries[0])
                else:
                    bib_Lib.add(bib_ref.entries[0])
            except Exception as inst:
                print(inst)
            print(type(bib_Lib))
    print(len(bib_Lib.entries))
    return bib_Lib, other_bib_Lib

def references_fetcher(directory):
    other_bib_Lib = bp.Library()
    bib_Lib = bp.Library()
    directory = directory+"/bib_files"
    bib_folders = [folder for folder in os.listdir(directory)]
    bib_folders.sort()
    for folder in bib_folders:
        bib_files = [bib_ref for bib_ref in os.listdir(directory+"/"+folder)]
        for bib_file in bib_files:
            try:
                bib_ref = bp.parse_file(directory+"/"+folder+"/"+bib_file)
                # bib_ref['title'] = "{" + bib_ref['title'] + "}"
                if folder == "other":
                    other_bib_Lib.add(bib_ref.entries[0])
                else:
                    bib_Lib.add(bib_ref.entries[0])
            except Exception as inst:
                print(inst)
    return bib_Lib, other_bib_Lib

def pkl_fetcher(location):
    if location == "q":
        raise Exception("quiting the function")
    elif not path_checker(location):
        print("Does not exits try again")
        new_location = input("Input a new location")
        pkl_file = pkl_fetcher(new_location)
    else:
        f = open(location, 'rb')
        pkl_file = pickle.load(f)
        f.close()
    return pkl_file

def pkl_storer(location, bib_data):
    f = open(location, 'wb')
    pickle.dump(bib_data, f)
    return 0

def path_checker(location):
    return Path(str(location)).is_file()