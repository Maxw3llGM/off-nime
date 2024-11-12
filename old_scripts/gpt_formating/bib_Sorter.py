import bibtexparser as bp
import pybtex
import os
import pandas as pd
import re

# TODO Generate the readme for ISIDIM
# TODO Fix errors and create an error scaper and file refactorer.
tag = "dd"
re_str = r"^\d{4}$"
re_str_ref = "<" + tag + ">(.*?)</" + tag + ">"
def create_New_Folder(folder_name, location = "ISIDM/bib_files/"):
    location = location+folder_name
    os.mkdir(location)

def create_SubfilesByYear(bib_entries):
    if not os.path.isdir("ISIDM/bib_files/"+"other"):
        create_New_Folder("other")

    try:
        for x in bib_entries.entries:
            try:
                if not os.path.isdir("ISIDM/bib_files/"+x['year']) and bool(re.fullmatch(re_str,x["year"])):
                    create_New_Folder(x['year'])
                # print(x['year'])
            except Exception as inst:
                print(inst)
    except Exception as inst:
        print(inst)
        exit

def sort_bib_files(bib_entries,location = "ISIDM/bib_files/"):
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
            
def yearsorter(e):
    return str(e)

def bib_string_formater(bib_string):
    bib_string = bib_string.replace("\n"," ")
    bib_string = re.findall(re_str_ref,bib_string)[0]
    return bib_string

def generate_readme(directory):
    with open("ISIDM/README.md","w") as md_file:
        md_file.write(f"# Off-NIME ISIDM Papers\n") 
        bib_folders = [folder for folder in os.listdir(directory)]
        bib_folders.sort()
        for folder in bib_folders:
            md_file.write(f"## " + folder + "\n")

            bib_files = [bib_ref for bib_ref in os.listdir(directory+"/"+folder)]
            for bib_file in bib_files:
                try:
                    bib_ref = bp.parse_file(directory+"/"+folder+"/"+bib_file)
                    bib_string = pybtex.format_from_string(bib_ref.entries[0].raw,"plain", output_backend = "html")
                    md_file.write(">" + bib_string_formater(bib_string))
                    md_file.write("\n\n")
                    md_file.write(f"[<kbd><br>BibTex<br></kbd>](bib_files/{folder}/{bib_file})\n\n") 
                    
                except Exception as inst:
                    md_file.write(f"> Error: {inst} ")
                    md_file.write("\n\n")
                    md_file.write(f"[<kbd><br>BibTex<br></kbd>](bib_files/{folder}/{bib_file})\n\n") 
                    md_file.write("\n\n")

                
                
def main():
    # bib_entries = bp.parse_file("ISIDM/bib_entries.bib")
    # create_SubfilesByYear(bib_entries)
    # sort_bib_files(bib_entries)
    generate_readme("ISIDM/bib_files")
if __name__ == "__main__":
    main()