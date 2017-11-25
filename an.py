import re
import matplotlib.pyplot as plt
import numpy as np
import os

data = open("subjs.csv")
lines = data.readlines()


class Sem:
    def __init__(self, subjects):
        self.subjects = subjects

    def __str__(self):
        message = ""
        for subject in self.subjects:
            message += str(subject) + "\n"


class Branch:
    def __init__(self, title, sems):
        self.title = title
        self.sems = sems

    def __str__(self):
        message = ""
        for sem in self.sems:
            message += "\t\t" + str(sem) + "\n"


class Subject:
    def __init__(self, title, ects, w, c, l, p, s):
        self.title = title
        self.ects = ects
        self.w = float(w)
        self.c = float(c)
        self.l = float(l)
        self.p = float(p)
        self.s = float(s)

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
    line = line.replace("\n", "")
    line = line.replace("(", " ")
    line = line.replace(")", " ")
    line = line.replace("-", " ")
    if line:
        mat = re.match("([A-Za-z -.)(]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+),([0-9]+).*",
                       line)
        var = []
        var.append(mat.group(0))
        var.append(mat.group(1))
        var.append(mat.group(2))
        var.append(mat.group(3))
        var.append(mat.group(4))
        var.append(mat.group(5))
        var.append(mat.group(6))
        var.append(mat.group(7))

        x = Subject(mat.group(1), mat.group(2), mat.group(3), mat.group(4), mat.group(5),
                    mat.group(6), mat.group(7))
        return x


path = f".\\heatmaps\\"
if not os.path.exists(path):
    os.makedirs(path)

subjects = []
for line in lines:
    if "SPEC" in line:
        subjects.append([line])
    else:
        subjects[-1].append(line)

branches = []
for line in lines:
    if "SPEC" in line:
        branches.append(Branch(line, []))
    elif "SEM" in line or "Sem" in line or "Nazwa" in line :
        branches[-1].sems.append(Sem([]))
    elif "Pobierz" in line or "Suma" in line or "Technologie geoinformatyczne i mobilne" in line:
        pass
    else:
        sem = branches[-1].sems[-1]
        a = parse_subject(line)
        if a:
            sem.subjects.append(a)
titles = []
g = []
for branch in branches:
    titles.append(branch.title)
    sub_tab = []
    gathered = [0, 0, 0, 0, 0]
    for sem in branch.sems:
        for subj in sem.subjects:
            sub_tab.append([subj.w,subj.c,subj.l,subj.p,subj.s])
            gathered[0] += subj.w
            gathered[1] += subj.c
            gathered[2] += subj.l
            gathered[3] += subj.p
            gathered[4] += subj.s
    g.append(gathered)
fig, ax = plt.subplots( figsize=(15,10))
fig.subplots_adjust(bottom=0.25, left=0.25)  # make room for labels

heatmap = ax.pcolor(g, cmap="hot")
cbar = plt.colorbar(heatmap)

# Set ticks in center of cells
ax.set_xticks(np.arange(5) + 0.5, minor=False)
ax.set_yticks(np.arange(len(branches)) + 0.5, minor=False)

# Rotate the xlabels. Set both x and y labels to headers[1:]
ax.set_xticklabels(["Wyklad","Cwiczenia","Laboratoria","Projekt","Seminarium"], rotation=90)
ax.set_yticklabels(titles)

title = branch.title.replace("\n","");
plt.savefig(f"{path}img{title}.png")
plt.close()
