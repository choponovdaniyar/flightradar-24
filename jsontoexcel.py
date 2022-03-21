import pandas 
import json

def to_excel_result(fn):
    with open(f"json/result.json", "r", encoding="utf-8")  as f:
        jf = json.load(f)
    s = max([len(jf[x]) for x in jf])
    for x in jf:
        for _ in range(s - len(jf[x])):
            jf[x] += [None] 
    s = [len(jf[x]) for x in jf]

    df = pandas.DataFrame(jf)   
    df.to_excel(f'result/result.xlsx') 

def to_excel_final():
    with open(f"json/final.json", "r", encoding="utf-8")  as f:
        jf = json.load(f)
    c1 = list()
    c2 = list()
    for x in jf:
        c1.append(x)
        c2.append(jf[x])
    jf = {"air": c1, "cnt": c2}
    df = pandas.DataFrame(jf)   
    df.to_excel(f'result/final.xlsx') 

to_excel_final()