import re

data = open("subjs.csv")
lines = data.readlines()

class Sem:
    def __init__(self, courses):
        self.courses = courses
class Branch:
    def __init__(self, sems):
        self.sems = sems

class Subject:
    def __init__(self, title, ects, w, c,l,p,s):
        self.title = title
        self.ects = ects
        self.w = w
        self.c = c
        self.l = l
        self.p = p
        self.s = s
        
    def __str__(self):
        return f"{self.title}; ECTS {self.ects}; W {self.w}; C {self.c}; L {self.l}; P {self.p}; S {self.s};"

def parse_subject(line):
    if "SEM" in line or "Sem" in line or "SPEC" in line:
        return None
    if "Nazwa" in line:
        return None
    if "Pobierz" in line:
        return None
    if "Suma" in line:
        return None
    if "Technologie geoinformatyczne i mobilne" in line:
        return None
    line = line.replace("\n","")
    line = line.replace("("," ")
    line = line.replace(")"," ")
    line = line.replace("-"," ")
    if line:
        
        mat = re.match("([A-Za-z -.)(]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+).*", line)
        var = []
        var.append(mat.group(0))
        var.append(mat.group(1))
        var.append(mat.group(2))
        var.append(mat.group(3))
        var.append(mat.group(4))
        var.append(mat.group(5))
        var.append(mat.group(6))
        var.append(mat.group(7))

        x = Subject(mat.group(1), mat.group(2),mat.group(3),mat.group(4),mat.group(5),mat.group(6),mat.group(7))
        return x.title

subjects = []
for line in lines:
    if "SPEC" in line:
        subjects.append([line])
    else:
        subjects[-1].append(line)

courses = []
for line in lines:
    if "SPEC" in line:
        courses.append( Branch([]) )
    elif "SEM" in line or "Sem" in line:
        courses[-1].sems.append(Sem([]))
    else:
        sem = courses[-1]
        a =  parse_subject(line)
        if a:
            sem.sems.append(a)

#print(courses)
for branch in courses:
    #print(branch)
    for sem in branch.sems:
        print(sem)
        #for course in sem.courses:
            #print(course)
