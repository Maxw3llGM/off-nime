import bibtexparser as bp
import os
import pybtex
import re

def bib_string_formater(bib_string):
    tag = "dd"
    re_str_ref = "<" + tag + ">(.*?)</" + tag + ">"

    bib_string = bib_string.replace("\n"," ")
    bib_string = re.findall(re_str_ref,bib_string)[0]
    return bib_string

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

def sorter(ref):
    # if (ref.get('author', '')): 
    #     value = ref.get('author', '').value 
    # elif (ref.get('editor', '')):
    #     value = ref.get('editor', '').value
    value = ref.key[0].upper()
    return value

def bib_sorter(bib_Lib):
    print(bib_Lib)
    all_entries = bib_Lib.entries

    all_entries.sort(key=lambda x: int(x.get('year', '').value))
    temp_entry_list = []
    entry_list = []
    last_entry = all_entries[0]
    for ref in all_entries:
        if last_entry.get('year', '').value != ref.get('year', '').value:
            print(last_entry.get('year', '').value)
            temp_entry_list.sort(key=sorter)
            arb = []
            for x in temp_entry_list:
                arb.append(x.key[0])
            print(arb)
            entry_list = entry_list + temp_entry_list
            temp_entry_list = []
        temp_entry_list.append(ref)
        last_entry = ref
        
    return entry_list

def md_generator(entry, repo, md_file):
    entry.pop('repo')
    if entry.get('URL', ''):
        entry['url'] = entry.pop('URL').value
    year = entry.get('year', '').value
    key = entry.key
    try:
        temp_lib = bp.Library()
        temp_lib.add(entry)
        temp_bib_string = bp.write_string(temp_lib)
        bib_string = pybtex.format_from_string(temp_bib_string,"plain", output_backend = "html")
        md_file.write(bib_string_formater(bib_string))
        md_file.write("\n")
    except Exception as inst:
        print(inst)
        md_file.write("Error : " + str(inst))
        md_file.write("\n")

    if entry.get('url', ''):
        url = entry.get('url', '').value
        md_file.write(f"[<kbd><br>Download PDF<br></kbd>]({url}) <nbsp>") #I hardcoded all the journal articles to be identified with CMJ Folder. Fix this later
    md_file.write(f"[<kbd><br>BibTex<br></kbd>]({repo}/bib_files/{year}/{key}.bib)\n\n")
    
def ref_fetcher(md_file):
    bib_Lib = bp.Library()
    other_bib_Lib = bp.Library()
    bib_Lib = file_fetcher(bib_Lib, "ISIDM")
    bib_Lib = file_fetcher(bib_Lib[0], "CMJ")
    bib_Lib = file_fetcher(bib_Lib[0], "ICMC")
    all_entries = bib_sorter(bib_Lib[0])
    last_entry = all_entries[0]
    md_file.write(f"## {last_entry.get('year', '').value}\n\n")
    for entry in all_entries:
        if last_entry.get('year', '').value != entry.get('year', '').value:
            md_file.write(f"## {entry.get('year', '').value}\n\n")
        md_generator(entry, entry.get('repo', '').value, md_file)
        last_entry = entry

def main():
    with open("README.md", "w") as md_file:
        md_file.write(f"# Off-NIME Papers\n")
        md_file.write(f"NIME-related papers, chapters, thesis and books published in other venues\n")
        ref_fetcher(md_file)


if __name__ =='__main__':
    main()