with open("医生.txt", "r", encoding="utf-8") as f:
    data = f.read()


for i in data.split("、"):
    for j in i.split():
        for k in j.split("，"):
            print(k)
