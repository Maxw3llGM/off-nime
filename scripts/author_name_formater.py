import re
import os
import bibtexparser as bp



def file_formater(bib_Lib, directory, function, year=1987):
    other_bib_Lib = bp.Library()
    directory = directory+"/bib_files"
    bib_folders = [folder for folder in os.listdir(directory) if int(folder) >= year]
    
    bib_folders.sort()
    for folder in bib_folders:
        bib_files = [bib_ref for bib_ref in os.listdir(directory+"/"+folder)]
        # print(bib_files)
        for bib_file in bib_files:
            try:
                bib_ref = bp.parse_file(directory+"/"+folder+"/"+bib_file)
                bib_ref.entries[0]["author"] = function(bib_ref.entries[0]["author"])
                bp.write_file(directory+"/"+folder+"/"+bib_file, bib_ref)
                if folder == "other":
                    other_bib_Lib.add(bib_ref.entries[0])
                else:
                    bib_Lib.add(bib_ref.entries[0])
            except Exception as inst:
                print(inst)
            # print(type(bib_Lib))
    print(len(bib_Lib.entries))
    return bib_Lib, other_bib_Lib


def rearrange_names(name: str):
    global verbose
    pattern = r'\band\b'

    list_name = re.split(pattern, name)
    name_elements = [var.split() for var in list_name]
    formated_names = []
    for names in name_elements:
        if len(names) > 3:
            print(f"error: {name}")
        first_names = []
        for name_parts in names[0:-1]:
            if '-' in name_parts and '.' not in name_parts:
                parts = name_parts.split('-')
                first_names.append(f"{parts[0][0]}.-{parts[1][0]}.")
            else : first_names.append(f"{name_parts[0]}.")
        reversed(first_names)
        first_name = ' '.join(first_names)
        last_name = names[-1]
        formated_names.append(f"{last_name}, {first_name}")
    
    formated_names = ' and '.join(formated_names)

    if(verbose):
        print(f"{name_elements} --> {formated_names}")
    
    return formated_names

verbose = 0
bib_Lib = bp.Library()
bib_Lib = file_formater(bib_Lib, "ICMC", rearrange_names)
for entrie in bib_Lib[0].entries:
    # rearranged = rearrange_names(entrie["author"])
    print(f"entrie: {entrie.key} | {entrie["author"]}")
# Process each name
