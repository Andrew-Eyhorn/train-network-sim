from station import Station
from train_line import Direction, TrainLine, LoopLine
from generate_json import read_json_network

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import math




def generate_graph(stations: dict[Station], train_lines: list[TrainLine]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for station_name in stations.keys():
        size = len(stations[station_name].connections) * 50
        graph.add_node(station_name, size = size)
                
    for i,line in enumerate(train_lines):
        for station in line.stations:
            for connection in stations[station].connections:
                if connection[1] == i:
                    graph.add_edge(station, connection[0], color=line.line_color, key=i)
    return graph


def draw_lines(G: nx.MultiDiGraph, pos, ax):
    offsets = [0.005, 0.01, 0.015, 0.02]
    for i, (u,v, key, data) in enumerate(G.edges(keys=True, data=True)):
        x1,y1 = pos[u]
        x2,y2 = pos[v]
        vx,vy = x2-x1, y2-y1
        vy,vx = vx,-vy
        d = math.sqrt(vx**2 + vy**2)
        offset = offsets[key]
        ox,oy = offset*vx/d, offset*vy/d
        start = (x1 + ox, y1 + oy)
        end = (x2 + ox, y2 + oy)
        ax.add_patch(FancyArrowPatch(start,end,connectionstyle="arc3,rad=0",color = data["color"],linewidth = 1))


mapped_stations: dict[Station] = {}





def map_stations(line_group: list[TrainLine], mapped_stations: dict[Station], direction: Direction):
    #get longest line
    sorted_lines = line_group.sort(reverse = True, key = lambda line: line.length)

    for line in sorted_lines:
        for i,station in line.stations:
            if station not in mapped_stations.keys():
                pass
    #draw it out in desired direciton
    #do the smaller lines
    

def calculate_loop_station_pos(loop: LoopLine, mapped_stations: dict[Station]):
    pass#what angle to say for each city loop station


if __name__ == "__main__":
    data = read_json_network("data/network_data.json")
    stations = data["stations"]
    train_lines = data["linear_lines"]
    
    G = generate_graph(stations, train_lines)
    #display graph
    pos = nx.spring_layout(G)
    fig,ax = plt.subplots(figsize=(18,9))
    node_sizes = nx.get_node_attributes(G, "size")
    nx.draw_networkx_nodes(G,pos,nodelist = node_sizes.keys(), node_size = list(node_sizes.values()))
    nx.draw_networkx_labels(G,pos,ax=ax)
    # nx.draw_networkx_edges(G,pos)
    draw_lines(G,pos,ax)
    plt.show()

    # with open("sample_network.json", "w") as outfile:
    #     outfile.write(json.dumps(nx.readwrite.json_graph.node_link_data(G)))