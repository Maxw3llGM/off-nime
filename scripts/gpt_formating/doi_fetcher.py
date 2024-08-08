import requests
def BibtexFromDoi(doi):
    url =  "http://dx.doi.org/" + doi
    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)
    return r.text

print(BibtexFromDoi("10.5281/zenodo.1176782"))