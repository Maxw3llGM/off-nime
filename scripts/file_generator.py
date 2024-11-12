import bibtexparser as bp
import os
import pybtex
import re
from pathlib import Path
from functions_helper import *


def bib_string_formater(bib_string):
    tag = "dd"
    re_str_ref = "<" + tag + ">(.*?)</" + tag + ">"

    bib_string = bib_string.replace("\n"," ")
    bib_string = re.findall(re_str_ref,bib_string)[0]
    return bib_string



def sorter(ref):
    # if (ref.get('author', '')): 
    #     value = ref.get('author', '').value 
    # elif (ref.get('editor', '')):
    #     value = ref.get('editor', '').value
    value = ref.key[0].upper()
    return value

def bib_sorter(bib_Lib):
    all_entries = bib_Lib

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
        bib_string = pybtex.format_from_string(entry.raw,"plain", output_backend = "html")
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

def sub_md_generator(entry, repo, md_file):
    entry.pop('repo')
    if entry.get('URL', ''):
        entry['url'] = entry.pop('URL').value
    year = entry.get('year', '').value
    key = entry.key
    try:
        bib_string = pybtex.format_from_string(entry.raw,"plain", output_backend = "html")
        md_file.write(bib_string_formater(bib_string))
        md_file.write("\n")
    except Exception as inst:
        print(inst)
        md_file.write("Error : " + str(inst))
        md_file.write("\n")

    if entry.get('url', ''):
        url = entry.get('url', '').value
        md_file.write(f"[<kbd><br>Download PDF<br></kbd>]({url}) <nbsp>") #I hardcoded all the journal articles to be identified with CMJ Folder. Fix this later
    md_file.write(f"[<kbd><br>BibTex<br></kbd>](bib_files/{year}/{key}.bib)\n\n")
        
def ref_fetcher(directories):
    
    bib_references = []
    for d in directories:
        print(f"./{d}/{d}.pkl")
        bib_references.append(pkl_fetcher(f"./{d}/{d}.pkl"))

    for idx, conferences in enumerate(bib_references):
        for refs in conferences[0].entries:
            refs['repo'] = directories[idx]
            print(refs)
    bib_list = []
    bib_list.extend(bib_references[0][0].entries)
    bib_list.extend(bib_references[1][0].entries)
    bib_list.extend(bib_references[2][0].entries)
    bib_list = bib_sorter(bib_list)

    return bib_list, bib_references
    

def main():
    directories = ["CMJ","ICMC","ISIDM"]
    bib_refs, bib_sections = ref_fetcher(directories)
    with open("README.md", "w") as md_file:
        md_file.write(f"# Off-NIME NIME Papers\n")
        md_file.write(f"NIME-related papers, chapters, thesis and books published in other venues\n\n")
        
        last_entry = bib_refs[0]
        md_file.write(f"## {last_entry.get('year', '').value}\n\n")
        for entry in bib_refs:
            if last_entry.get('year', '').value != entry.get('year', '').value:
                md_file.write(f"## {entry.get('year', '').value}\n\n")
            md_generator(entry, entry.get('repo', '').value, md_file)
            last_entry = entry

    for idx, directorie in enumerate(directories):
        with open(f"{directorie}/README.md", "w") as md_file:
            md_file.write(f"# {directorie} Papers\n")
            md_file.write(f"papers, chapters, thesis and books published in {directorie}\n\n")
            
            last_entry = bib_sections[idx][0].entries[0]
            md_file.write(f"## {last_entry.get('year', '').value}\n\n")
            for entry in bib_sections[idx][0].entries:
                if last_entry.get('year', '').value != entry.get('year', '').value:
                    md_file.write(f"## {entry.get('year', '').value}\n\n")
                sub_md_generator(entry, directorie, md_file)
                last_entry = entry
        bp.write_file(f"{directorie}/{directorie}_bibtex.bib", bib_sections[idx][0])
if __name__ =='__main__':
    main()