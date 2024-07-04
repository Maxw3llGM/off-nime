import bibtexparser as bp
import pybtex
import os
import pandas as pd
import re

bibfile = bp.parse_file("bib_entries.bib")

tag = "dd"
re_str = "<" + tag + ">(.*?)</" + tag + ">"
with open("README.md", "w") as md_file:
    md_file.write(f"# Off-NIME ISIDM Papers\n")
    md_file.write(f"Nime papers, chapters and books published outside of the NIME Conference Proceedings\n")
    
    count = 0
    md_file.write("<body>")
    for ref in bibfile.entries:
        try:
            bib_string = pybtex.format_from_string(ref.raw, "plain", output_backend = "html").replace("\n"," ")
            md_file.write(re.findall(re_str,bib_string)[0])
            temp_lib=bp.Library()
            temp_lib.add(ref)
            string_ref = bp.write_string(temp_lib)
            
            md_file.write("\n\n")
            md_file.write("```\n")
            md_file.write(string_ref)
            md_file.write("\n```")
            md_file.write("\n\n")
        except Exception as inst: 
            # md_file.write("Failed Reference \n ")
            ref['error'] = str(inst)
            # temp_lib=bp.Library()
            # temp_lib.add(ref)
            # string_ref = bp.write_string(temp_lib)
            
            # md_file.write("\n\n")
            # md_file.write("```\n")
            # md_file.write(string_ref)
            # md_file.write("\n```")
            # md_file.write("\n\n")
        
    
    for ref in bibfile.entries:
        try:
            bib_string = pybtex.format_from_string(ref.raw, "plain", output_backend = "html").replace("\n"," ")
            # md_file.write(re.findall(re_str,bib_string)[0])
        except Exception as inst: 
            md_file.write("Failed Reference \n ")
            # ref['error'] = str(inst)
            temp_lib=bp.Library()
            temp_lib.add(ref)
            string_ref = bp.write_string(temp_lib)
            
            md_file.write("\n\n")
            md_file.write("```\n")
            md_file.write(string_ref)
            md_file.write("\n```")
            md_file.write("\n\n")
            
    md_file.write("</body>")


    