with open("data/airs.txt", "r", encoding="utf-8") as f:
    airs = f.read().split("\n")

def is_valid(name,el):
    if "United States" in name:
        return 0
    for x in airs:
        if el in x:
            return 0
    return 1
