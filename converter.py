import networkx as nx
import csv

net = nx.MultiDiGraph()

with open('data\\edgesNoKey.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        if row[6] != "Forbidden":
            net.add_edge(int(row[2]), int(row[3]), float(row[4]), wkt=row[11], type=row[6])
        if row[7] != "Forbidden":
            net.add_edge(int(row[3]), int(row[2]), float(row[4]), wkt=row[11], type=row[7])
# print([i for i in net.neighbors(49724252)])