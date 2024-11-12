from functions_helper import *

def main():
    directories = ["CMJ","ICMC","ISIDM"]
    bib_references = []
    for d in directories:
        print(f"./{d}/{d}.pkl")
        bib_references.append(pkl_fetcher(f"./{d}/{d}.pkl"))
    
    list0 = sorted(bib_references[0][0].entries, key=(lambda x: x.key[0]))
    list1 = sorted(bib_references[1][0].entries, key=(lambda x: x.key[0]))
    list2 = sorted(bib_references[2][0].entries, key=(lambda x: x.key[0]))

    for (ref1, ref2) in zip(list2, list1 + ['']*(len(bib_references[2][0].entries)-len(bib_references[1][0].entries))):
        if ref2 == '':
            empty = '-'
        else:
            empty = ref2.key
        print(f"{ref1.key} : {empty}")
    return 0

if __name__ =='__main__':
    main()
