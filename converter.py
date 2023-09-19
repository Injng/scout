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
# print([i for i in net.neighbors(49724252)])

# Define a matrix
# A = np.array([[1, 2, 3],
#               [4, 5, 6],
#               [7, 8, 9]])

A = np.array([[0.2, 0.1],
             [0.8, 0.9]])

B = np.array([[1,0],
              [0,1]])


C = np.subtract(A,B)
print(C)
D = [-C[0][1], C[0][0]];
print(D)
# Perform SVD
U, S, V = np.linalg.svd(A)

# U, S, and V are the factorized matrices
print("U:")
print(U)

print("\nS:")
print(S)

print("\nV:")
print(V)
