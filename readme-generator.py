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

with open("README.md", "w") as md_file:
    md_file.write(f"# Off-NIME NIME Papers\n")
    md_file.write(f"Nime papers, chapters and books published outside of the NIME Conference Proceedings\n")

    for directory in directories:
        if directory == "./CMJ":
            md_file.write(f"\n## Computer Music Journal (CMJ)\n\n")
            ref_parser_one(directory,md_file)

        elif directory == "./ICMC":
            md_file.write(f"\n## International Computer Music Conference (ICMC)\n\n")
            ref_parser_one(directory,md_file)

        if directory == "./ISIDM":
            md_file.write(f"\n## Interactive Systems and Instrument Design in Music (ISIDM)\n\n")
            ref_parser_two(directory,md_file)
        