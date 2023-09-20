import networkx as nx
import csv
import numpy as np

def convertToGraph(filepath):
    net = nx.MultiDiGraph()
    with open(filepath, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if row[6] != "Forbidden":
                net.add_edge(int(row[2]), int(row[3]), w=float(row[4]), wkt=row[11], type=row[6])
            if row[7] != "Forbidden":
                net.add_edge(int(row[3]), int(row[2]), w=float(row[4]), wkt=row[11], type=row[7])
    return net

# takes a list of ubers and a dictionary of stations with the node id being the key and the value being the number of ubers needed
def getShortestPaths(ubers, stations, net):
	distances = {}
	paths = []
	for uber in ubers:
		uberDistances = {}
		for station in stations.keys():
			uberDistances[station] = nx.dijkstra_path_length(net, uber, station, weight="w")
		distances[uber] = uberDistances
	for uber in ubers:
		d = [distances[uber][i] for i in distances[uber].keys()]
		d.sort()
		l = True
		for i in range(len(d)):
			if l:
				for key in distances[uber].keys():
					if distances[uber][key] == d[i]:
						if stations[key] > 0:
							paths.append([uber, key])
							stations[key] -= 1
							l = False
						break
	return paths

def getNode(lat, long):
	return 0

net = convertToGraph("data\\edgesNoKey.csv")
# print(net.nodes)
print(nx.dijkstra_path_length(net, 10127575312, 10092398257, weight="w"))
print(getShortestPaths([10127575312,10127575312,10127575312,4788602122, 4643843108, 49751367, 10092398257, 10979910220], {10070536261: 3, 10127575312:3}, net))
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
