from station import Station
from train_line import Direction, TrainLine, LoopLine
from generate_json import read_json_network

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import math
import json



def generate_graph(stations: dict[Station], train_lines: list[TrainLine]) -> nx.MultiGraph:
    
    graph = nx.MultiGraph()
    for station_name in stations.keys():
        station: Station = stations[station_name]
        size = len(station.connections) * 50
        graph.add_node(station_name, size = size, pos = (station.map_x, station.map_y), map_angle = station.map_angle)
                
    def get_edge_offset(id: int):
        if id % 2 == 0:
            return id / 2
        else:
            return -1 * (id + 1) / 2
        
    #For each station, we map its connections to 0,1, .... and add 1 if its even
    for station in stations.values():
        connected_lines: list = station.connections.keys()
        sorted_connections = list(connected_lines)
        sorted_connections.sort()
        is_even = (len(sorted_connections) % 2 == 0)

        normalised_id: dict = {}
        for i in range(len(sorted_connections)):
            normalised_id[sorted_connections[i]] = i + is_even

        for line_id in connected_lines:
            for connected_station in station.connections[line_id]:
                graph.add_edge(station.name, connected_station, color=train_lines[line_id].line_color, key=line_id, offset = get_edge_offset(normalised_id[line_id]))
    return graph


def draw_lines(G: nx.MultiDiGraph, pos, ax):
    offsets = [0.05 * x for x in range(1, 21)]
    for i, (u,v, key, data) in enumerate(G.edges(keys=True, data=True)):
        x1,y1 = pos[u]
        x2,y2 = pos[v]
        if (x1,y1) != (x2,y2):
            vx,vy = x2-x1, y2-y1
            vy,vx = vx,-vy
            d = math.sqrt(vx**2 + vy**2)
            offset = offsets[key]
            ox,oy = offset*vx/d, offset*vy/d
            start = (x1 + ox, y1 + oy)
            end = (x2 + ox, y2 + oy)
            ax.add_patch(FancyArrowPatch(start,end,connectionstyle="arc3,rad=0",color = data["color"],linewidth = 1))







def get_offset_angle(station_number: int) -> float:
    """
    Gives how much we should offset off the current line based on nubmer of stations passed(more stations, smaller offset)
    station_number must be >= 0
    """
    # max_angle = math.pi/4
    max_angle = math.pi/2
    station_number = min(station_number, 20)
    reducer = station_number // 5 + 1
    return max_angle / reducer

def get_vector(angle: float) -> tuple[float,float]:
    """
    Does a tangent of the angle, but accounts for invalid values
    """
    if math.isclose(angle, Direction.EAST):
        return (1,0)
    elif math.isclose(angle, Direction.NORTH):
        return (0,1)
    elif math.isclose(angle, Direction.WEST):
        return (-1,0)
    elif math.isclose(angle, Direction.SOUTH):
        return (0,-1)
    else:
        return (math.cos(angle), math.sin(angle))


def map_stations(line_group: list[TrainLine], stations: dict[Station], mapped_stations: dict[Station], spacing: int):
    #get longest line
    sorted_lines = sorted(line_group, reverse = True, key = lambda line: line.length)
    #draw it out in desired direciton
    line: TrainLine
    for line in sorted_lines:
        direction = None
        vector = None
        new_stations_placed = 0
        for i in range(len(line.stations)):
            station: Station = stations[line.stations[i]["station"]]
            if station.name not in mapped_stations.keys():
                if i == 0: #if this is the first station to be mapped
                    direction = get_offset_angle(line.direction)
                    vector = get_vector(direction)
                    x,y = 0,0
                    station.map_angle = direction
                    station.update_map_coords((x,y))
                    mapped_stations[station.name] = station
                else:
                    prev_station: Station = stations[line.stations[i-1]["station"]]
                    if direction is None:
                        prev_angle = prev_station.map_angle
                        if prev_station.is_loop_station or not math.isclose(line.direction, prev_angle):
                            direction = line.direction
                            vector = get_vector(direction)
                        else:
                            offset_angle = get_offset_angle(i)
                            if line.direction - prev_angle > 0:
                                offset_angle *= -1
                            direction = prev_angle - offset_angle
                            vector = get_vector(direction)
                    spacing_changed = spacing
                    if new_stations_placed == 0:
                        spacing_changed = spacing * 2.5
                    p_x, p_y = prev_station.map_x, prev_station.map_y
                    x = p_x + spacing_changed * vector[0]
                    y = p_y + spacing_changed * vector[1]
                    station.update_map_coords((x,y))
                    station.map_angle = direction
                    mapped_stations[station.name] = station
                    new_stations_placed += 1
    

def calculate_loop_station_pos(loop: LoopLine, stations: dict[Station], mapped_stations: dict[Station], distance: int):
    n = len(loop.stations) - 1
    angle = 2 * math.pi / n
    r = distance * math.sin(angle/2) / math.sin(angle) 
    for i in range(n):
        station: Station = stations[loop.stations[i]]
        t = i * angle
        x = r * math.cos(t) + loop.centre_pos[0]
        y = r * math.sin(t) + loop.centre_pos[1]
        station.update_map_coords((x,y))
        station.map_angle = angle
        station.is_loop_station = True
        mapped_stations[station.name] = station


if __name__ == "__main__":
    data = read_json_network("data/temp.json")
    # data = read_json_network("data/temp.json")
    stations = data["stations"]
    train_lines = data["linear_lines"]
    loops = data["loop_lines"]
    mapped_stations: dict[Station] = {}

    calculate_loop_station_pos(loops[0], stations, mapped_stations,  100)
    map_stations(train_lines, stations, mapped_stations, 30)
    G = generate_graph(stations, train_lines)

    #save to json
    with open("C:\code\web-ui\src\data\sample_network.json", "w") as outfile:
        outfile.write(json.dumps(nx.readwrite.json_graph.node_link_data(G)))