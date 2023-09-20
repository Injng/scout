import networkx as nx
import csv
import numpy as np
import math

def convert_to_graph(filepath):
    net = nx.MultiDiGraph()
    with open(filepath, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if row[6] != "Forbidden":
                net.add_edge(int(row[2]), int(row[3]), w=float(row[4]), wkt=row[11], type=row[6], dir=1)
            if row[7] != "Forbidden":
                net.add_edge(int(row[3]), int(row[2]), w=float(row[4]), wkt=row[11], type=row[7], dir=-1)
    return net

# takes a list of ubers and a dictionary of stations with the node id being the key and the value being the number of ubers needed
def get_shortestpaths(ubers, stations, net):
	distances = {}
	paths = []
	for uber in ubers:
		uber_distances = {}
		for station in stations.keys():
			uber_distances[station] = nx.dijkstra_path_length(net, uber, station, weight="w")
		distances[uber] = uber_distances
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

def dist(x1, y1, x2, y2):
	return math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)

def get_latlon(node, net):
	try:
		edge = list(net.out_edges(node))[0]
		edge += (0,)
		con = net.edges[edge]
		wkt = con["wkt"]
		spl = wkt.split(" ")
		if con["dir"] == 1:
			return [float(spl[0][11:]), float(spl[1][:len(spl[1])-1])]
		if con["dir"] == -1:
			return [float(spl[len(spl)-2]), float(spl[len(spl)-1][:len(spl[len(spl)-1])-1])]
	except:
		edge = list(net.in_edges(node))[0]
		edge += (0,)
		con = net.edges[edge]
		wkt = con["wkt"]
		spl = wkt.split(" ")
		if con["dir"] == 1:
			return [float(spl[0][11:]), float(spl[1][:len(spl[1])-1])]
		if con["dir"] == -1:
			return [float(spl[len(spl)-2]), float(spl[len(spl)-1][:len(spl[len(spl)-1])-1])]

def get_node(lat, lon, net):
	lowest_dist = -1
	right = -1
	for node in net.nodes:
		latlon = get_latlon(node, net)
		d = dist(lat, lon, latlon[0], latlon[1])
		if lowest_dist == -1 or d < lowest_dist:
			lowest_dist = d
			right = node
	return right

net = convert_to_graph("data\\edgesNoKey.csv")
# print(net.nodes)
# print(nx.dijkstra_path_length(net, 10127575312, 10092398257, weight="w"))
# print(getShortestPaths([10127575312,10127575312,10127575312,4788602122, 4643843108, 49751367, 10092398257, 10979910220], {10070536261: 3, 10127575312:3}, net))
# print([i for i in net.neighbors(49724252)])
# print(get_latlon(6799231643, net))
print(get_node(-77.1, 38.9, net))
print(get_latlon(get_node(-77.1,38.9, net), net))


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
