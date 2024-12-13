from functions_helper import *
import shutil
from datetime import date
import os

def main():
    directories = ["CMJ","ICMC","ISIDM"]
    bib_references = []
    for d in directories:
        goal = ("./"+d+"/"+d+".pkl")
        if(os.path.isfile(goal)):
            # first backups the files
            shutil.copy(goal, f"./backups/{d}_{date.today()}.pkl")
            # fetches
            bib_list = references_fetcher("./"+d)
            #stores them
            pkl_storer(goal, bib_list)
    return 0


if __name__ =='__main__':
    main()

