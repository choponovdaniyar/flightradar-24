import pandas 
import json

with open("res.json", "r", encoding="utf-8")  as f:
    jf = json.load(f)
s = max([len(jf[x]) for x in jf])
for x in jf:
    for _ in range(s - len(jf[x])):
        jf[x] += [None] 
s = [len(jf[x]) for x in jf]
df = pandas.DataFrame(jf)   
df.to_excel('./result.xlsx') 