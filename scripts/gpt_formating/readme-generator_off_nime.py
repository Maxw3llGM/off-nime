import bibtexparser as bp
from bibtexparser.model import Block
import pybtex
import os
import pandas as pd
import re

import pybtex.database
import bibtexparser.middlewares as m


bibfile = bp.parse_file("bib_entries.bib")
sorted_blocks = []

def get_year(x):
    try:
        return x['year']
    except:
        return ''
    
all_entries = sorted(bibfile.entries, key=get_year)
sortedbibfile = bp.Library()
sortedbibfile.add(all_entries)
        
# bibfile.entries = sorted(bibfile.entries, key=lambda ref: ref.get)
tag = "dd"
re_str = "<" + tag + ">(.*?)</" + tag + ">"
with open("README.md", "w") as md_file:
    md_file.write(f"# Off-NIME ISIDM Papers\n")
    md_file.write(f"Nime papers, chapters and books published outside of the NIME Conference Proceedings\n")
    all_entries = []
    
    count = 0
    md_file.write("<body>")
    for ref in sortedbibfile.entries:
        ref['title'] = "{" + ref['title'] + "}"
        try:
            bib_string = pybtex.format_from_string(ref.raw, "plain", output_backend = "html").replace("\n"," ")
            md_file.write(re.findall(re_str,bib_string)[0])
        except Exception as inst: 
            md_file.write("Failed Reference \n ")
            ref['error'] = str(inst)
            count += 1
        temp_lib=bp.Library()
        temp_lib.add(ref)
        string_ref = bp.write_string(temp_lib)
        
        md_file.write("\n\n")
        md_file.write("```\n")
        md_file.write(string_ref)
        md_file.write("\n```")
        md_file.write("\n\n")
    bp.write_file("bib_entries.bib",sortedbibfile)
            
    md_file.write("</body>")
    
    
    
    