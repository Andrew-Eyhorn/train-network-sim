from station import Station

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import math

stations: dict[Station] = {}

def read_train_line(filepath: str, stations: dict[Station]):
    """
    Read a txt file containing station names in order
    """
    #read txt, and get station names, and connect them
    station_name_list = []
    with open(filepath, newline ='') as stations_file:
        for line in stations_file.readlines():
            station_name_list.append(line.strip())

    for i, station_name in enumerate(station_name_list):
        if station_name in stations.keys():
            new_station = stations[station_name]
        else:
            new_station = Station(station_name)
        if i != len(station_name_list) - 1:
            new_station.add_connection(station_name_list[i+1])
        if i != 0:
            new_station.add_connection(station_name_list[i-1])
        stations[station_name] = new_station

def generate_graph(stations: dict[Station]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for station_name in stations.keys():
        graph.add_node(station_name)
    for station_name in stations.keys():
        for connection in stations[station_name].connections:
            graph.add_edge(station_name, connection)
    return graph


def draw_lines(G, pos, ax):
    offset = 0.02
    for u,v in G.edges(keys=False):
        x1,y1 = pos[u]
        x2,y2 = pos[v]
        vx,vy = x2-x1, y2-y1
        vy,vx = vx,-vy
        d = math.sqrt(vx**2 + vy**2)
        ox,oy = offset*vx, offset*vy
        start = (x1 + ox, y1 + oy)
        end = (x2 + ox, y2 + oy)
        ax.add_patch(FancyArrowPatch(start,end,connectionstyle="arc3,rad=0",color = "blue",linewidth = 0.5))


if __name__ == "__main__":
    read_train_line("data/belgrave_line_stations.txt", stations)
    read_train_line("data/lilydale_line_stations.txt", stations)
    
    G = generate_graph(stations)
    print(G.edges(keys = False))
    #display graph
    pos = nx.spring_layout(G)
    fig,ax = plt.subplots(figsize=(18,9))
    nx.draw_networkx_nodes(G,pos,node_size = 100)
    nx.draw_networkx_labels(G,pos,ax=ax)
    # nx.draw_networkx_edges(G,pos)
    draw_lines(G,pos,ax)
    plt.show()