import networkx as nx
import csv
import numpy as np
import math
import random
import requests
import os
from stations import codes, namesfinal

stationsfinal = [49762207, 5445789476, 3011762637, 5294170126, 8455344314, 9748716629, 10109933697, 3669211313, 2146602922, 2146602922, 49283688, 49283688, 49283688, 2146602922, 2146602922, 49762191, 2791130921, 3000430332, 9083099465, 4401779099, 9068828613, 9082995718, 2591082909, 49752478, 49752478, 49752478, 9481540451, 49762207, 1381307999, 8626399984, 9123357154, 63349926, 575531863, 645731563, 643359029, 703037116, 703037116, 8901206658, 2057037354, 644150792, 644150792, 316162894, 5610652552, 6179193967, 49796861, 10087854710, 49792125, 9592649173, 1443170224, 49841238, 646246183, 1474688577, 4108851327, 4108851327, 4108851327, 3012784294, 5446812471, 8411953540, 2921245044, 1937256103, 9068828613, 50795293, 50795293, 50795293, 50795293, 49762191, 3012535014, 49796861, 3006162400, 8459177912, 4788602128, 5445925412, 49750033, 50483631, 50791672, 3660934424, 49769407, 649841051, 50490877, 50490877, 50490877, 316162894, 316162894, 63346822, 292915466, 292915466, 292915466, 63359657, 63359657, 63359657, 63359657, 6801446389, 6801446389, 6801446389, 6801446389, 49252020, 49252020, 49252020, 49252020, 49252020, 49252020, 49252020]
# Get API key from environment variable API_KEY, requires a .env file in the same directory
API_KEY = os.getenv("API_KEY")

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

def get_names():
    out = {}
    for code in codes:
        out[code] = get_name(code)
    return out

def get_trains():
    out = {}
    for i in codes:
        # print(i)
        out[i] = len(get_train(i))
    return out

def get_stats(day, AM_PM):
    stats = {}
    # trains = get_trains()
    trains = {}
    for code in codes:
        trains[code] = 5

    need = need_for_each_station(day, AM_PM)
    for i in trains.keys():
        # print(i)
        singleneed = 0
        name = namesfinal[i]
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
def get_shortestpaths(ubers, stations):
    totaldist = 0
    distances = {}
    paths = []
    # write_ubers(ubers)
    for i in ubers.keys():
        print(i)
        uber = ubers[i]
        uber_distances = {}
        for station in stations.keys():
            try:
                uber_distances[station] = nx.dijkstra_path_length(net, uber, station, weight="w")
            except:
                uber_distances[station] = -1
        distances[uber] = uber_distances
    for uber_id in ubers.keys():
        uber = ubers[uber_id]
        d = [distances[uber][i] for i in distances[uber].keys()]
        d.sort()
        l = True
        for i in range(len(d)):
            if l and d[i] > -1:
                for key in distances[uber].keys():
                    if distances[uber][key] == d[i]:
                        if stations[key] > 0:
                            paths.append([uber, key, get_latlon(uber), get_latlon(key), uber_id])
                            totaldist += d[i]
                            stations[key] -= 1
                            l = False
                        break
    return [paths, totaldist]

def get_shortestpathstime(ubers, day, AM_PM, div):
    stats = get_stats(day, AM_PM)
    stations = {}
    for i in stats.keys():
        stations[stationsfinal[codes.index(i)]] = stats[i] // div
    return get_shortestpaths(ubers, stations)

def update(day, AM_PM, div):
    ubers = {}
    with open("data/ubers.csv", newline='\n') as file:
        reader = list(csv.reader(file))
        print(reader)
        for row in reader:
            if row != ["uber_id","lat","lon"]:
                ubers[row[0]] = get_node(float(row[1]), float(row[2]))
    print(ubers)
    return get_shortestpathstime(ubers, day, AM_PM, div)

def update_one(lat, lon, day, AM_PM, div):
    uber_id = append_uber(lat, lon)
    print(uber_id)
    paths = update(day, AM_PM, div)[0]
    # print(paths)
    for path in paths:
        if str(path[4]) == str(uber_id):
            return path

def write_ubers(ubers):
    with open('data/ubers.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["uber_id","lat","lon"])
        for i in range(len(ubers)):
            latlon = get_latlon(ubers[i])
            writer.writerow([i, latlon[0], latlon[1]])

def append_uber(lat, lon):
    with open('data/ubers.csv', newline='\n') as file:
        reader = list(csv.reader(file))
        i = len(reader) - 1
    with open('data/ubers.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([i, lat, lon])
    return i

def dist(x1, y1, x2, y2):
    return math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)

def get_latlon(node):
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

def get_node(lat, lon):
    lowest_dist = -1
    right = -1
    for node in net.nodes:
        latlon = get_latlon(node)
        d = dist(lat, lon, latlon[0], latlon[1])
        if lowest_dist == -1 or d < lowest_dist:
            lowest_dist = d
            right = node
    return right

def get_stations(latlons):
    stations = []
    for i in latlons:
        stations.append(get_node(i[1], i[0]))
    return stations

def get_random_ubers(num):
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

def get_station_name(lat, lon):
    node_id = get_node(float(lat), float(lon))
    station_idx = stationsfinal.index(node_id)
    station_code = codes[station_idx]
    return namesfinal[station_code] 

global net
net = convert_to_graph("data/edgesNoKey.csv")
