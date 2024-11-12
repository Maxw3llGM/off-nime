import os
import bibtexparser as bp
import re

tag = "dd"
re_str = r"^\d{4}$"
re_str_ref = "<" + tag + ">(.*?)</" + tag + ">"

def CMJ_fetcher(bib_Lib, directory = "ICMC"):
    all_entries = []

    # create a list of bib files in the directory
    bib_files = [f for f in os.listdir(directory) if f.endswith('.bib')]
    # iterate over all bib files and extract the data
    
    for bib_file in bib_files:
        bib_list = bp.parse_file(os.path.join(directory, bib_file))
        
        for entries in bib_list.entries:
            entries['title'] = "{" + entries['title'] + "}"
            all_entries.append(entries)
    all_entries.sort(key=lambda x: int(x.get('year', '').value))
    for ref in all_entries:
        bib_Lib.add(ref)
    print(len(all_entries))
    return bib_Lib

def create_New_Folder(folder_name, location = "ICMC/bib_files/"):
    location = location+folder_name
    os.mkdir(location)

def create_SubfilesByYear(bib_entries):
    try:
        for x in bib_entries.entries:
            try:
                if not os.path.isdir("ICMC/bib_files/"+x['year']) and bool(re.fullmatch(re_str,x["year"])):
                    create_New_Folder(x['year'])
                # print(x['year'])
            except Exception as inst:
                print(inst)
    except Exception as inst:
        print(inst)
        exit

def sort_bib_files(bib_entries,location = "ICMC/bib_files/"):
    for ref in bib_entries.entries:
        temp_lib = bp.Library()
        temp_lib.add(ref)
        try:
            path_name = location+ref['year']+"/"+ref.key+".bib"
            if not os.path.isfile(path_name):
                bp.write_file(path_name,temp_lib)
        except Exception as inst:
            path_name = location+"other/"+ref.key+".bib"
            bp.write_file(path_name,temp_lib)
  

def main():
    bib_Lib = bp.Library()
    bib_Lib = CMJ_fetcher(bib_Lib)
    os.mkdir('./ICMC/bib_files')
    create_SubfilesByYear(bib_Lib)
    sort_bib_files(bib_Lib)
    return 0


if __name__ =='__main__':
    main()