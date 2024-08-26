import requests
import re
from bs4 import BeautifulSoup
import bibtexparser as bp

def bib_formater_proceedings(authors,year,title,conference,doi):
    return f"""@inproceedings{{{authors.split(" ")[0]}{year},
    title        = {title},
	authors      = {authors},
	booktitle    = {conference},
	year         = {year}
    doi          = {doi}
    }}"""

pattern = r'<li>\s*(.*?)\s*\.\s*(\d{4})\.\s*<a href="(.*?)">\s*(.*?)\s*</a>\s*<em>(.*?)</em>\.\s*DOI:\s*<a href="(.*?)">(.*?)</a>\s*</li>'
def ref_format(re_pattr,content):
    pattern = re.compile(re_pattr,re.DOTALL)
    match = pattern.search(str(content))
    ref_items = []
    if match:
        authors = match.group(1)
        year = match.group(2)
        title = match.group(4)
        conference = match.group(5)
        doi_link = match.group(6)
        doi = match.group(7)
        return bib_formater_proceedings(authors,year,title,conference,doi)


url = "https://www.nime.org/archives/"
response = requests.get(url)
html_page = response.text
soup = BeautifulSoup(html_page, 'html.parser')
bib_strings = []
for refs in soup.find_all("li"):
    bib_strings.append(ref_format(pattern,refs))

