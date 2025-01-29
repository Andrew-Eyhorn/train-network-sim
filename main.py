from station import Station
from train_line import Direction, TrainLine, LoopLine
from generate_json import read_json_network
from line_vector import LineVector
from long_lat_getter import set_station_coords, longlat_dict

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import math
import json


def generate_graph(
    stations: dict[Station], train_lines: list[TrainLine]
) -> nx.MultiGraph:

    graph = nx.MultiGraph()
    for station_name in stations.keys():
        station: Station = stations[station_name]
        size = len(station.connections) * 50
        graph.add_node(
            station_name,
            size=size,
            pos=(station.map_x, station.map_y),
            map_angle=station.map_angle,
        )

    def get_edge_offset(id: int):
        if id % 2 == 0:
            return id / 2
        else:
            return -1 * (id + 1) / 2

    # For each station, we map its connections to 0,1, .... and add 1 if its even
    for station in stations.values():
        connected_lines: list = station.connections.keys()
        sorted_connections = list(connected_lines)
        sorted_connections.sort()
        is_even = len(sorted_connections) % 2 == 0

        normalised_id: dict = {}
        for i in range(len(sorted_connections)):
            normalised_id[sorted_connections[i]] = i + is_even

        for line_id in connected_lines:
            for connected_station in station.connections[line_id]:
                graph.add_edge(
                    station.name,
                    connected_station,
                    color=train_lines[line_id].line_color,
                    key=line_id,
                    offset=get_edge_offset(normalised_id[line_id]),
                )
    return graph


def draw_lines(G: nx.MultiDiGraph, pos, ax):
    offsets = [0.05 * x for x in range(1, 21)]
    for i, (u, v, key, data) in enumerate(G.edges(keys=True, data=True)):
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        if (x1, y1) != (x2, y2):
            vx, vy = x2 - x1, y2 - y1
            vy, vx = vx, -vy
            d = math.sqrt(vx**2 + vy**2)
            offset = offsets[key]
            ox, oy = offset * vx / d, offset * vy / d
            start = (x1 + ox, y1 + oy)
            end = (x2 + ox, y2 + oy)
            ax.add_patch(
                FancyArrowPatch(
                    start,
                    end,
                    connectionstyle="arc3,rad=0",
                    color=data["color"],
                    linewidth=1,
                )
            )


def get_offset_angle(station_number: int) -> float:
    """
    Gives how much we should offset off the current line based on nubmer of stations passed(more stations, smaller offset)
    station_number must be >= 0
    """
    max_angle = math.pi / 2
    station_number = min(station_number, 20)
    reducer = station_number // 5 + 1
    return max_angle / reducer


def get_vector(angle: float) -> tuple[float, float]:
    """
    Does a tangent of the angle, but accounts for invalid values
    """
    if math.isclose(angle, Direction.EAST):
        return (1, 0)
    elif math.isclose(angle, Direction.NORTH):
        return (0, 1)
    elif math.isclose(angle, Direction.WEST):
        return (-1, 0)
    elif math.isclose(angle, Direction.SOUTH):
        return (0, -1)
    else:
        return (math.cos(angle), math.sin(angle))


def map_stations(
    line_group: dict[str, TrainLine],
    stations: dict[Station],
    mapped_stations: dict[Station],
    spacing: int,
):
    # get longest line
    line_group = list(line_group.values())
    sorted_lines = sorted(line_group, reverse=True, key=lambda line: line.length)
    # draw it out in desired direciton
    line: TrainLine
    for line in sorted_lines:
        direction = None
        vector = None
        new_stations_placed = 0
        for i in range(len(line.stations)):
            station: Station = stations[line.stations[i]["station"]]
            if station.name not in mapped_stations.keys():
                if i == 0:  # if this is the first station to be mapped
                    direction = line.direction
                    vector = get_vector(direction)
                    x, y = 0, 0
                    station.map_angle = direction
                    station.update_map_coords((x, y))
                    mapped_stations[station.name] = station
                else:
                    prev_station: Station = stations[line.stations[i - 1]["station"]]
                    if direction is None:
                        prev_angle = prev_station.map_angle
                        if prev_station.is_loop_station or not math.isclose(
                            line.direction, prev_angle
                        ):
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
                        spacing_changed = spacing * 3
                    if new_stations_placed == 6:
                        if not math.isclose(line.direction, direction):
                            direction = line.direction
                            spacing_changed = spacing * 2
                        vector = get_vector(direction)
                    p_x, p_y = prev_station.map_x, prev_station.map_y
                    x = p_x + spacing_changed * vector[0]
                    y = p_y + spacing_changed * vector[1]
                    station.update_map_coords((x, y))
                    station.map_angle = direction
                    mapped_stations[station.name] = station
                    new_stations_placed += 1


def calculate_loop_station_pos(
    loop: LoopLine,
    stations: dict[Station],
    mapped_stations: dict[Station],
    distance: int,
):
    n = len(loop.stations) - 1
    angle = 2 * math.pi / n
    r = distance * math.sin(angle / 2) / math.sin(angle)
    for i in range(n):
        station: Station = stations[loop.stations[i]]
        t = i * angle + math.pi / 5
        x = r * math.cos(t) + loop.centre_pos[0]
        y = r * math.sin(t) + loop.centre_pos[1]
        station.update_map_coords((x, y))
        station.map_angle = -t
        station.is_loop_station = True
        mapped_stations[station.name] = station






def map_line_vector_stations(line_vector: LineVector) -> None:
    """
    Maps the stations along the line vector that aren't the end points
    """
    current_coord = [line_vector.stations[0].map_x, line_vector.stations[0].map_y]
    for i in range(1, len(line_vector.stations) - 1):
        station: Station = line_vector.stations[i]
        current_coord[0] += line_vector.vector_x
        current_coord[1] += line_vector.vector_y
        station.update_map_coords(current_coord)


def is_anchor_point(station: Station, stations: dict[str, Station]) -> bool:
    if station.is_loop_station:
        return True
    for line, connections in station.connections.items():
        if len(station.connections[line]) == 1:
            return True
        for connection in connections:
            if len(station.connections) > len(stations[connection].connections):
                return True
    return False


def update_anchor_points_coordinates(stations: dict[str, Station], offset: tuple[float, float]) -> None:
    for station in stations.values():
        if is_anchor_point(station, stations):
            set_station_coords(station, offset)
            
def scale_coordinates(target_coords: tuple[float, float]) -> tuple[float, float]:
    """
    Scales the target coordinates based on distance from the centre, the closer the target coords are the to the centre, the more they are scaled
    """
    x, y = target_coords
    # boundaries = [25, 50, 100, 200, 300]
    # multipliers = [2, 1, 0.5, 0.25, 0.1]
    boundaries = [50, 100, 150]
    multipliers = [2, 1, 0.5]
    x_out, y_out = dynamic_scale_alt(boundaries, multipliers, abs(x)), dynamic_scale_alt(boundaries, multipliers, abs(y))
    if x >= 0 and y >= 0:
        return x_out, y_out
    elif x < 0 and y >= 0:
        return -1 * x_out, y_out
    elif x < 0 and y < 0:
        return -1 * x_out, -1 * y_out
    elif x >= 0 and y < 0:
        return x_out, -1 * y_out
            

        
def dynamic_scale_alt(boundaries: list[float], multipliers: list[float], x: float) -> float:
    """
    Given a list of boundaries and boarder multipliers, scales the coordinate value based where it falls on the map
    """
    assert len(boundaries) == len(multipliers)
    assert x >= 0
    if x > boundaries[-1]:
        print(x)
    i = 0
    output = 0
    if x < boundaries[0]:
        return x * multipliers[0]
    while i < len(boundaries) and x > boundaries[i]:
        output += boundaries[i] * multipliers[i]
        i += 1
    try:
        if i >= len(boundaries):
            i-=1
        diff = x - boundaries[i-1]
        return diff * multipliers[i] + output
    except IndexError:
        # print information for debugging and raise error
        print("Error in dynamic scale")
        print("Boundaries: " + str(boundaries))
        print("Multipliers: " + str(multipliers))
        print("X: " + str(x))
        print("I: " + str(i))
        print("Output: " + str(output))
        print("Diff: " + str(diff))
        raise IndexError("Error in dynamic scale")
if __name__ == "__main__":
    
    # Temp test of lon lat
    train_line_path = "data/melbourne_data"
    data = read_json_network(train_line_path + "/network_data.json")
    stations = data["stations"]
    train_lines = data["linear_lines"]
    loops = data["loop_lines"]
    mapped_stations: dict[Station] = {}

    calculate_loop_station_pos(loops["0"], stations, mapped_stations, 100)

    


    line_vectors: list[LineVector] = []



    


    centre = "Flinders Street"
    stations[centre].update_map_coords((0, 0))
    stations[centre].update_real_coords(longlat_dict[centre][0], longlat_dict[centre][1])
    offset = (stations[centre].longitude, stations[centre].latitude)
    update_anchor_points_coordinates(stations, offset)

    for line_name in train_lines.keys():
        line = train_lines[line_name]

        new_stations_placed = 0

        section_start = None
        section_end = None



        for i in range(len(line.stations)):
            station: Station = stations[line.stations[i]["station"]]

            if station.longitude is not None:
                if station.map_x is None:
                    station.update_map_coords(
                        (
                            (station.longitude - offset[0]) * 1111,
                            (station.latitude - offset[1]) * 1111,
                        )
                    )
                    mapped_stations[station.name] = station

                if section_start is None:
                    section_start = i
                else:
                    section_end = i
                
            if section_end is not None:
                if section_end - section_start < 1:
                    section_start = section_end
                    section_end = None
                    break

                start_coord = [
                    stations[line.stations[section_start]["station"]].map_x,
                    stations[line.stations[section_start]["station"]].map_y,
                ]
                end_coord = [
                    stations[line.stations[section_end]["station"]].map_x,
                    stations[line.stations[section_end]["station"]].map_y,
                ]
                vector = [
                    (end_coord[0] - start_coord[0]) / (section_end - section_start),
                    (end_coord[1] - start_coord[1]) / (section_end - section_start),
                ]

                current_line_vector = LineVector(
                    start_coord[0],
                    start_coord[1],
                    end_coord[0],
                    end_coord[1],
                    vector[0],
                    vector[1],
                )

                current_coord = start_coord
                current_line_vector.add_station(stations[line.stations[section_start]["station"]])
                for j in range(section_start + 1, section_end):
                    current_coord[0] += current_line_vector.vector_x
                    current_coord[1] += current_line_vector.vector_y
                    station: Station = stations[line.stations[j]["station"]]
                    current_line_vector.add_station(station)
                    if station.name not in mapped_stations.keys():
                        station.update_map_coords(current_coord)
                current_line_vector.add_station(stations[line.stations[section_end]["station"]])

                if current_line_vector not in line_vectors:
                    line_vectors.append(current_line_vector)

                section_start = section_end
                section_end = None



    #Check for vector crossovers and adjust stations positions
    intersection_found = True
    while intersection_found:
        intersection_found = False
        for i in range(len(line_vectors)):
            for j in range(i + 1, len(line_vectors)):
                intersection = line_vectors[i].intersect(line_vectors[j])
                if intersection is not None and len(line_vectors[i].stations) > 2 and len(line_vectors[j].stations) > 2:
                    intersection_found = True
                    new_vectors = []
                    # Do it for one line
                    left_split, right_split = line_vectors[i].split(intersection, offset)
                    new_vectors.extend([left_split, right_split])

                    map_line_vector_stations(left_split)
                    map_line_vector_stations(right_split)

                    #recalculate station positions for this vector, need to somehow get the line's vector correct before knowing the station's position

                    
                    # Do it for the other line
                    left_split, right_split = line_vectors[j].split(intersection, offset)
                    new_vectors.extend([left_split, right_split])

                    map_line_vector_stations(left_split)
                    map_line_vector_stations(right_split)


                    line_vectors.remove(line_vectors[i])
                    line_vectors.remove(line_vectors[j - 1])
                    line_vectors.extend(new_vectors)



    #scale the stations
    for station in stations.values():
        try:
            station.update_map_coords(scale_coordinates((station.map_x, station.map_y)))
            station.update_angle(math.atan2(station.map_y, station.map_x))
        except TypeError:
            print(station.name)
            print(station.map_x)
            print(station.map_y)
            print(scale_coordinates((station.map_x, station.map_y)))


    # for line_vector in line_vectors:
    #     print(line_vector)
    G = generate_graph(stations, train_lines)

    # save to json
    with open("C:\code\web-ui\src\data\sample_network.json", "w") as outfile:
        outfile.write(json.dumps(nx.readwrite.json_graph.node_link_data(G)))


"""
#TODO:
for returning joints, need to redirect when (stations left till rejoin) * (distance) is < the distance between current station and that station
#maybe mid-line direction change?

#define centre location to convert longlat to cooord
#Use real location for splits, map between these points
#maybe lookup location in api if possible (could maybe scrape if not)

#at some point change data storage from txt to something better

#mininmum test: lilydale line mapping


#have maunally picked of decent colors and exytended version, have option to set color
#compared various big city maps to se how they do things (styling, colors, thickness?)
"""
