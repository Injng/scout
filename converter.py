import networkx as nx
import csv
import numpy as np
import math
import random
import requests

stationsfinal = [49762207, 5445789476, 3011762637, 5294170126, 8455344314, 9748716629, 10109933697, 3669211313, 2146602922, 2146602922, 49283688, 49283688, 49283688, 2146602922, 2146602922, 49762191, 2791130921, 3000430332, 9083099465, 4401779099, 9068828613, 9082995718, 2591082909, 49752478, 49752478, 49752478, 9481540451, 49762207, 1381307999, 8626399984, 9123357154, 63349926, 575531863, 645731563, 643359029, 703037116, 703037116, 8901206658, 2057037354, 644150792, 644150792, 316162894, 5610652552, 6179193967, 49796861, 10087854710, 49792125, 9592649173, 1443170224, 49841238, 646246183, 1474688577, 4108851327, 4108851327, 4108851327, 3012784294, 5446812471, 8411953540, 2921245044, 1937256103, 9068828613, 50795293, 50795293, 50795293, 50795293, 49762191, 3012535014, 49796861, 3006162400, 8459177912, 4788602128, 5445925412, 49750033, 50483631, 50791672, 3660934424, 49769407, 649841051, 50490877, 50490877, 50490877, 316162894, 316162894, 63346822, 292915466, 292915466, 292915466, 63359657, 63359657, 63359657, 63359657, 6801446389, 6801446389, 6801446389, 6801446389, 49252020, 49252020, 49252020, 49252020, 49252020, 49252020, 49252020]
# Get API key from environment variable API_KEY, requires a .env file in the same directory
# API_KEY = os.getenv("API_KEY")
API_KEY = "73d4a5d2f6fa4acb9a905bb0b14e073c"
codes = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B35', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 'D13', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'G01', 'G02', 'G03', 'G04', 'G05', 'J02', 'J03', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'N01', 'N02', 'N03', 'N04', 'N06', 'N07', 'N08', 'N09', 'N10', 'N11', 'N12']

def get_train(id):
    next_train = requests.get(f"https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{id}", headers={"api_key" : API_KEY})

    if next_train.status_code == 200:
        pass
    else:
        raise ValueError("The URL is invalid")

    next_train = next_train.json()
    train_times = []

    for train in next_train["Trains"]:
        time = train["Min"]
        # if data is passed as '', interpret as no data and skip
        if time == '' or time == 'ARR' or time == 'BRD' or time == '---':
            continue
        train_times.append(int(time))

    return train_times

def get_name(id):
    station_name = requests.get(f"https://api.wmata.com/Rail.svc/json/jStationInfo?StationCode={id}", headers={"api_key" : API_KEY})

    if station_name.status_code == 200:
        pass
    else:
        raise ValueError("The URL is invalid")

    station_name = station_name.json()
    return station_name["Name"]

def get_trains():
	out = {}
	for i in codes:
		print(i)
		out[i] = len(get_train(i))
	return out

def get_stats(day, AM_PM):
	stats = {}
	trains = get_trains()
	need = need_for_each_station(day, AM_PM)
	for i in trains.keys():
		print(i)
		singleneed = 0
		name = get_name(i)
		for j in need:
			if j[0] == name:
				singleneed = j[1]
		stats[i] = singleneed * trains[i] // 60
	return stats

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
	totaldist = 0
	distances = {}
	paths = []
	for i in range(len(ubers)):
		print(i)
		uber = ubers[i]
		uber_distances = {}
		for station in stations.keys():
			try:
				uber_distances[station] = nx.dijkstra_path_length(net, uber, station, weight="w")
			except:
				uber_distances[station] = -1
		distances[uber] = uber_distances
	for uber in ubers:
		d = [distances[uber][i] for i in distances[uber].keys()]
		d.sort()
		l = True
		for i in range(len(d)):
			if l and d[i] > -1:
				for key in distances[uber].keys():
					if distances[uber][key] == d[i]:
						if stations[key] > 0:
							paths.append([uber, key])
							totaldist += d[i]
							stations[key] -= 1
							l = False
						break
	return [paths, totaldist]

def get_shortestpathstime(ubers, day, AM_PM, div, net):
	stats = get_stats(day, AM_PM)
	stations = {}
	for i in stats.keys():
		stations[stationsfinal[codes.index(i)]] = stats[i] // div
	return get_shortestpaths(ubers, stations, net)

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

def get_stations(latlons, net):
	stations = []
	for i in latlons:
		stations.append(get_node(i[1], i[0], net))
	return stations

def get_random_ubers(num, net):
	return random.sample(list(net.nodes), num)

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

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        list = []
        for row in csv_reader:
            list.append(row)
            # print(row)
        return list
# Example usage:
def need_for_each_station(day, AM_PM):#the day is a string monday, tuesday ... time is PM Peak, AM Peak, Evening, Midday
    file_path = 'data/' + day + '_exits.csv'  # Replace with the path to your CSV file
    list = read_csv_file(file_path)
    ret =[]
    for i in list:
        r = []
        if (i[6] == AM_PM):
            r .append(i[5])
            need = int(i[-1])# -int(i[-2])
            r.append(need)
        if (len(r) != 0):
            ret.append(r)
    return ret



# print(get_train("A01"))
# print(need_for_each_station('monday','PM Peak (3pm-7pm)'))
# print(get_stats('monday','PM Peak (3pm-7pm)'))

net = convert_to_graph("data\\edgesNoKey.csv")
print(get_shortestpathstime(get_random_ubers(120, net), 'monday', 'PM Peak (3pm-7pm)', net))

# print(net.nodes)
# print(nx.dijkstra_path_length(net, 10127575312, 10092398257, weight="w"))
# print(getShortestPaths([10127575312,10127575312,10127575312,4788602122, 4643843108, 49751367, 10092398257, 10979910220], {10070536261: 3, 10127575312:3}, net))
# print([i for i in net.neighbors(49724252)])
# print(get_latlon(6799231643, net))
# print(get_node(-77.1, 38.9, net))
# print(get_latlon(get_node(-77.1,38.9, net), net))
# print(get_stations([[38.898303, -77.028099], [38.903192, -77.039766], [38.909499, -77.04362], [38.924999, -77.052648], [38.934703, -77.058226], [38.94362, -77.063511], [38.947808, -77.079615], [38.960744, -77.085969], [38.984282, -77.094431], [38.999947, -77.097253], [39.029158, -77.10415], [39.048043, -77.113131], [39.062359, -77.121113], [39.084215, -77.146424], [39.119819, -77.164921], [38.89834, -77.021851], [38.896084, -77.016643], [38.897723, -77.006745], [38.920741, -76.995984], [38.933234, -76.994544], [38.951777, -77.002174], [38.975532, -77.017834], [38.993841, -77.031321], [39.015413, -77.042953], [39.038558, -77.051098], [39.061713, -77.05341], [38.907407, -77.002961], [38.898303, -77.028099], [38.901316, -77.033652], [38.901311, -77.03981], [38.900599, -77.050273], [38.896595, -77.07146], [38.884574, -77.063108], [38.869349, -77.054013], [38.863045, -77.059507], [38.85779, -77.050589], [38.852985, -77.043805], [38.83108, -77.04644], [38.814009, -77.053763], [38.806474, -77.061115], [38.800313, -77.071173], [38.793841, -77.075301], [38.893757, -77.028218], [38.888022, -77.028232], [38.884775, -77.021964], [38.884958, -77.01586], [38.884968, -77.005137], [38.884124, -76.995334], [38.880841, -76.985721], [38.88594, -76.977485], [38.898284, -76.948042], [38.907734, -76.936177], [38.91652, -76.915427], [38.934411, -76.890988], [38.947674, -76.872144], [38.905604, -77.022256], [38.912919, -77.022194], [38.916489, -77.028938], [38.928672, -77.032775], [38.936077, -77.024728], [38.951777, -77.002174], [38.954931, -76.969881], [38.965276, -76.956182], [38.978523, -76.928432], [39.011036, -76.911362], [38.89834, -77.021851], [38.893893, -77.021902], [38.884775, -77.021964], [38.876221, -77.017491], [38.876588, -77.005086], [38.862072, -76.995648], [38.845334, -76.98817], [38.840974, -76.97536], [38.851187, -76.956565], [38.843891, -76.932022], [38.826995, -76.912134], [38.890488, -76.938291], [38.889757, -76.913382], [38.886713, -76.893592], [38.8913, -76.8682], [38.9008, -76.8449], [38.799193, -77.129407], [38.766129, -77.168797], [38.891499, -77.08391], [38.886373, -77.096963], [38.88331, -77.104267], [38.882071, -77.111845], [38.885841, -77.157177], [38.90067, -77.189394], [38.883015, -77.228939], [38.877693, -77.271562], [38.924478, -77.210167], [38.920056, -77.223314], [38.919749, -77.235192], [38.929273, -77.241988], [38.947753, -77.340179], [38.952768, -77.360185], [38.952821, -77.385178], [38.960758, -77.415295], [38.955784, -77.448148], [38.99204, -77.460685], [39.005283, -77.491537]], net))

"""stats = {}
for i in stationsfinal:
	stats[i]=1
print(get_shortestpaths(get_random_ubers(120, net), stats, net))"""