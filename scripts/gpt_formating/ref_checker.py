import requests
import pickle
import time
import os
import pandas as pd
from typing import TypedDict

data : pd.DataFrame = pd.read_pickle("ISIDM/sorted_references.pkl")
d = "d'homme."
fix = data['references'][0].split(d)
fix[0] = fix[0]+d
print(fix)

data['references'][0] = fix[0]
data.loc[-1] = [fix[1], "N/A", "N/A"]
data.index +=1
data = data.sort_index()
print(data)

data.to_pickle("ISIDM/sorted_references.pkl")

