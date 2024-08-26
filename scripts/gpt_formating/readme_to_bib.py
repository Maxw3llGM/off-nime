import bibtexparser as bp
import pybtex
import os
import pandas as pd
import re

def extract_md_blocks(text):
    pattern = r"```(?:\w+\s+)?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [block.strip() for block in matches]


with open("README.md", "r") as md_file:
    results = extract_md_blocks(''.join(md_file.readlines()))
    bib_refs = bp.parse_string(''.join([x.replace("\n\t","") for x in results]))
    bp.write_file("bib_entries_with_errors.bib", bib_refs)


    