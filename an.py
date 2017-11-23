import re

data = open("subjs.csv")
lines = data.readlines()

class Subject:
    def __init__(self, ects, w, c,l,p,s):
        self.ects = ects
        self.w = w
        self.c = c
        self.l = l
        self.p = p
        self.s = s

def parse_subject(line):
    if "SEM" in line or "Sem" in line or "SPEC" in line:
        return None
    mat = re.match("([A-Za-z ]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+).*", line)
    var = []
    var.append(mat.group(0))
    var.append(mat.group(1))
    var.append(mat.group(2))
    var.append(mat.group(3))
    var.append(mat.group(4))
    var.append(mat.group(5))
    var.append(mat.group(6))
    var.append(mat.group(7))

    x = Subject(mat.group(2),mat.group(3),mat.group(4),mat.group(5),mat.group(6),mat.group(7))

    return x

subjects = []
for line in lines:
    if "SPEC" in line:
        subjects.append([line])
    else:
        subjects[-1].append(line)

for subject in subjects:
    for line in subject:
        subject = parse_subject(line)
        pass

pass