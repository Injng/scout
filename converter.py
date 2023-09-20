import math

import networkx as nx
import csv
import numpy as np

def convertToGraph(filepath):
    net = nx.MultiDiGraph()
    with open(filepath, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if row[6] != "Forbidden":
                net.add_edge(int(row[2]), int(row[3]), float(row[4]), wkt=row[11], type=row[6])
            if row[7] != "Forbidden":
                net.add_edge(int(row[3]), int(row[2]), float(row[4]), wkt=row[11], type=row[7])
    return net

net = convertToGraph("data\\edgesNoKey.csv")


A = np.array([[0.2, 0.1, 0],
             [0.8, 0.9, 0.1],
              [0, 0, 0.9]])
def major_eigenvalue(A):
# print(np.linalg.eigvals(A))
    a = np.linalg.eig(A)
    eigenvalue = list(a.eigenvalues)
    eigenvector = list(a.eigenvectors)

    Index = 0
    nume = len(a)
    for i in range(nume):
        if ((eigenvalue[i] -1)* (eigenvalue[i] -1)<1):
            Index = i

    majorvector = []
    leng = len(eigenvalue)
    for i in range(leng):
        majorvector.append(eigenvector[i][Index])
    return majorvector

def diff_in_potential(Current, ideal):
    diff = []
    leng = len(ideal)
    for i in range(leng):
        diff.append(ideal - Current)
    return diff



