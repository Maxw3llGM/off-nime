from functions_helper import *

def main():
    directories = ["CMJ","ICMC","ISIDM"]
    bib_references = []
    for d in directories:
        print("./"+d+"/"+d+".pkl")
        bib_list = references_fetcher("./"+d)
        pkl_storer("./"+d+"/"+d+".pkl", bib_list)
    return 0


if __name__ =='__main__':
    main()

