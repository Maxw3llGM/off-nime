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

def ISIDM_fetcher(bib_Lib, directory="./ISIDM"):
    other_bib_Lib = bp.Library()
    directory = directory+"/bib_files"
    bib_folders = [folder for folder in os.listdir(directory)]
    bib_folders.sort()
    for folder in bib_folders:
        print(folder)
        bib_files = [bib_ref for bib_ref in os.listdir(directory+"/"+folder)]
        for bib_file in bib_files:
            try:
                bib_ref = bp.parse_file(directory+"/"+folder+"/"+bib_file)
                bib_ref.entries[0]['repo'] = "ISIDM"
                # bib_ref.entries[0]['repo'] = "ISIDM"
                if folder == "other":
                    other_bib_Lib.add(bib_ref.entries[0])
                else:
                    bib_Lib.add(bib_ref.entries[0])
            except:
                print("oops")
            # print(bib_ref.entries[0]['repo'])
        

    return bib_Lib, other_bib_Lib

def CMJ_fetcher(bib_Lib, directory = "./CMJ"):
    all_entries = []

    # create a list of bib files in the directory
    bib_files = [f for f in os.listdir(directory) if f.endswith('.bib')]
    # iterate over all bib files and extract the data
    
    for bib_file in bib_files:
        bib_list = bp.parse_file(os.path.join(directory, bib_file))
        
        for entries in bib_list.entries:
            entries['repo'] = "CMJ"
            all_entries.append(entries)
    all_entries.sort(key=lambda x: int(x.get('year', '').value))
    for ref in all_entries:
        bib_Lib.add(ref)
    # print(len(all_entries))
    return bib_Lib

def ICMC_fetcher(bib_Lib, directory = "./ICMC"):
    all_entries = []

    # create a list of bib files in the directory
    bib_files = [f for f in os.listdir(directory) if f.endswith('.bib')]
    # iterate over all bib files and extract the data
    
    for bib_file in bib_files:
        bib_list = bp.parse_file(os.path.join(directory, bib_file))
            
        for entries in bib_list.entries:
            entries['repo'] = "ICMC"
            all_entries.append(entries)
    all_entries.sort(key=lambda x: int(x.get('year', '').value))
    for ref in all_entries:
        bib_Lib.add(ref)
    # print(len(all_entries))
    return bib_Lib

def sorter(ref):
    if (ref.get('author', '')): 
        value = ref.get('author', '').value 
    elif (ref.get('editor', '')):
        value = ref.get('editor', '').value
    return value

def bib_sorter(bib_Lib):
    all_entries = bib_Lib.entries

    all_entries.sort(key=lambda x: int(x.get('year', '').value))
    temp_entry_list = []
    entry_list = []
    last_entry = all_entries[0]
    for ref in all_entries:
        if last_entry.get('year', '').value != ref.get('year', '').value:
            temp_entry_list.sort(key=sorter)
            entry_list = entry_list + temp_entry_list
            temp_entry_list = []
        temp_entry_list.append(ref)
        last_entry = ref

    return all_entries


    # for ref in entry_list:
    #     if (ref.get('author', '')): 
    #         print(f"{ref.get('year', '').value}: {ref.get('author', '').value} - {ref.get('title', '').value}") 
    #     elif (ref.get('editor', '')):
    #         print(f"{ref.get('year', '').value}: {ref.get('editor', '').value} - {ref.get('title', '').value}")

def md_generator(entry, repo, md_file):
    if repo == "ISIDM":
        year = entry.get('year', '').value
        key = entry.key
        try:
            bib_string = pybtex.format_from_string(entry.raw,"plain", output_backend = "html")
            md_file.write(">" + bib_string_formater(bib_string))
            md_file.write("\n\n")
            md_file.write(f"[<kbd><br>BibTex<br></kbd>](ISIDM/bib_files/{year}/{key}.bib)\n\n") 
            
        except Exception as inst:
            md_file.write(f"> Error: {inst} ")
            md_file.write("\n\n")
            md_file.write(f"[<kbd><br>BibTex<br></kbd>](ISIDM/bib_files/{year}/{key}.bib)\n\n") 
            md_file.write("\n\n")
    else:
        title = entry.get('title', '').value
        author = entry.get('author', '').value
        year = entry.get('year', '').value
        try:
            url = entry.get('url', '').value
        except:
            url = entry.get('URL', '').value   
        entry_type = entry.entry_type
        if repo == "CMJ":
            number = entry.get('number', '').value
            journal = entry.get('journal', '').value
            volume = entry.get('volume', '').value
            md_file.write(f"> {author}. {year}. {title}. *{journal} v.{volume} n.{number}*.\n\n")
            md_file.write(f"[<kbd><br>Download PDF<br></kbd>]({url}) <nbsp> [<kbd><br>BibTex<br></kbd>](CMJ/{year}.bib)\n\n") #I hardcoded all the journal articles to be identified with CMJ Folder. Fix this later

        if repo == "ICMC":
            booktitle = entry.get('booktitle', '').value
            md_file.write(f"> {author}. {year}. {title}. *{booktitle}*.\n\n")
            md_file.write(f"[<kbd><br>Download PDF<br></kbd>]({url}) <nbsp> [<kbd><br>BibTex<br></kbd>](ICMC/{year}.bib)\n\n") #I hardcoded all the conference proceedings papers to be identified with ICMC Folder. Fix this later
        
    


def ref_fetcher(md_file):
    bib_Lib = bp.Library()
    other_bib_Lib = bp.Library()
    bib_Lib, other_bib_Lib = ISIDM_fetcher(bib_Lib)
    # print(other_bib_Lib.entries)
    bib_Lib = CMJ_fetcher(bib_Lib)
    bib_Lib = ICMC_fetcher(bib_Lib)
    all_entries = bib_sorter(bib_Lib)

    for entry in all_entries:
        md_generator(entry, entry.get('repo', '').value, md_file)

        


def ref_parser_one(directory, md_file):
    # create a list to store entries from all bib files
        all_entries = []    
    
        # create a list of bib files in the directory
        bib_files = [f for f in os.listdir(directory) if f.endswith('.bib')]
    
        # iterate over all bib files and extract the data
        for bib_file in bib_files:
            bib_database = bp.parse_file(os.path.join(directory, bib_file))
            all_entries = bib_database.entries
            md_file.write(f"### " + bib_file.split(".")[0] + "\n")
            md_file.write("---" + "\n")

            for entry in all_entries:
                title = entry.get('title', '').value
                author = entry.get('author', '').value
                year = entry.get('year', '').value
                try:
                    url = entry.get('url', '').value
                except:
                    url = entry.get('URL', '').value
                entry_type = entry.entry_type
                if entry_type == 'article':
                    number = entry.get('number', '').value
                    journal = entry.get('journal', '').value
                    volume = entry.get('volume', '').value
                    md_file.write(f"> {author}. {year}. {title}. *{journal} v.{volume} n.{number}*.\n\n")
                    md_file.write(f"[<kbd><br>Download PDF<br></kbd>]({url}) <nbsp> [<kbd><br>BibTex<br></kbd>](CMJ/{year}.bib)\n\n") #I hardcoded all the journal articles to be identified with CMJ Folder. Fix this later
        
                if entry_type == 'inproceedings':
                    booktitle = entry.get('booktitle', '').value
                    md_file.write(f"> {author}. {year}. {title}. *{booktitle}*.\n\n")
                    md_file.write(f"[<kbd><br>Download PDF<br></kbd>]({url}) <nbsp> [<kbd><br>BibTex<br></kbd>](ICMC/{year}.bib)\n\n") #I hardcoded all the conference proceedings papers to be identified with ICMC Folder. Fix this later

def ref_parser_two(directory, md_file):
    directory = directory+"/bib_files"
    bib_folders = [folder for folder in os.listdir(directory)]
    bib_folders.sort()
    for folder in bib_folders:
        md_file.write(f"### {folder} \n --- \n")
        
        bib_files = [bib_ref for bib_ref in os.listdir(directory+"/"+folder)]
        for bib_file in bib_files:
            try:
                bib_ref = bp.parse_file(directory+"/"+folder+"/"+bib_file)
                bib_string = pybtex.format_from_string(bib_ref.entries[0].raw,"plain", output_backend = "html")
                md_file.write(">" + bib_string_formater(bib_string))
                md_file.write("\n\n")
                md_file.write(f"[<kbd><br>BibTex<br></kbd>]({directory}/{folder}/{bib_file})\n\n") 
                
            except Exception as inst:
                md_file.write(f"> Error: {inst} ")
                md_file.write("\n\n")
                md_file.write(f"[<kbd><br>BibTex<br></kbd>]({directory}/{folder}/{bib_file})\n\n") 
                md_file.write("\n\n")


# create a list of subdirectories containing bib files
directories = ["./CMJ", "./ICMC", "./ISIDM"]

with open("README2.md", "w") as md_file:
    md_file.write(f"# Off-NIME NIME Papers\n")
    md_file.write(f"Nime papers, chapters and books published outside of the NIME Conference Proceedings\n")
    
    ref_fetcher(md_file)

        