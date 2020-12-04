
def writeline(line):
    with open('data.csv','a+',encoding="utf-8") as f:
        f.write(line+'\n')
