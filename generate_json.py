from train_line import TrainLine, Direction, LoopLine
from station import Station

import json

def read_train_line(filepath: str, stations: dict[Station], name: str, color: str, direction: Direction) -> TrainLine:
    """
    Read a txt file containing station names in order
    """
    #read txt, and get station names, and connect them
    station_name_list = []
    with open(filepath, newline ='') as stations_file:
        for line in stations_file.readlines():
            station_name_list.append(line.strip())

    train_line = TrainLine(name = name, line_color = color, direction = direction)
    for i, station_name in enumerate(station_name_list):
        if station_name in stations.keys():
            new_station = stations[station_name]
        else:
            new_station = Station(name = station_name)
            stations[station_name] = new_station
        if i != len(station_name_list) - 1:
            new_station.add_connection(station_name_list[i+1], train_line.line_id)
        if i != 0:
            new_station.add_connection(station_name_list[i-1], train_line.line_id)
        train_line.add_station(new_station)
    return train_line


def get_all_stations(train_lines: list[TrainLine], stations: dict[Station]):
    for line in train_lines:
        for station in line.stations:
            if station.name not in stations.keys():
                stations[station.name] = station

def read_loop_line(filepath: str, centre: tuple[int,int], data: dict):
    stations_list = []
    with open(filepath, newline ='') as stations_file:
        for line in stations_file.readlines():
            stations_list.append(line.strip())
    new_loop = LoopLine(centre_pos = centre, stations = stations_list)
    for i in range(len(stations_list) - 1):
        data["stations"][stations_list[i]].is_loop_station = True

    data["loop_lines"].append(new_loop)
data = {"stations": {}, "line_count": 0, "loop_lines": [], "linear_lines": []}
# data = {"line_count": 0, "loop_lines": [], "linear_lines": []}


def read_json_network(filepath: str) -> dict:
    """
    Reads a network json file, returns a dict of the following format:
    data = {"stations": dict[Station], "line_count": 0, "loop_lines": list[TrainLine], "linear_lines": list[TrainLine]}
    """
    with open(filepath) as f:
            data = json.load(f)
            read_data = {"stations": {}, "line_count": 0, "loop_lines": [], "linear_lines": []}
            for station in data["stations"]:
                # station["is_loop_station"] = False
                station: Station = Station.model_validate(station)
                read_data["stations"][station.name] = station
            read_data["line_count"] = data["line_count"]
            TrainLine._line_number = read_data["line_count"]
            read_data["loop_lines"] = [LoopLine.model_validate(line) for line in data["loop_lines"]]
            read_data["linear_lines"] = [TrainLine.model_validate(line) for line in data["linear_lines"]]
            return read_data
if __name__ == "__main__":
    #read existing json
    filepath = "data/temp.json"
    try:
        data = read_json_network(filepath)
    except:
        pass
    
    stations = data["stations"]
    # #read new txt
    # new_line = read_train_line("data/lilydale_line_stations.txt", stations, "Lilydale", "lightblue", Direction.EAST)
    # new_line = read_train_line("data/belgrave_line_stations.txt", stations, "Belgrave", "cyan", Direction.EAST)
    # new_line = read_train_line("data/alamein_line_stations.txt", stations, "Alamein", "blue", Direction.EAST)
    # new_line = read_train_line("data/glen_waverly_line_stations.txt", stations, "Glen Waverly", "darkblue", Direction.EAST)
    # new_line = read_train_line("data/pakenham_line_stations.txt", stations, "Pakenham", "purple", Direction.SOUTH_EAST)
    # new_line = read_train_line("data/cranbourne_line_stations.txt", stations, "Cranbourne", "lightpurple", Direction.SOUTH_EAST)
    # new_line = read_train_line("data/frankston_line_stations.txt", stations, "Frankston", "darkpink", Direction.SOUTH)
    # new_line = read_train_line("data/sandringham_line_stations.txt", stations, "Sandringham", "pink", Direction.SOUTH)
    # new_line = read_train_line("data/williamstown_line_stations.txt", stations, "Williamstown", "green", Direction.SOUTH_WEST)
    # new_line = read_train_line("data/werribee_line_stations.txt", stations, "Werribee", "lightgreen", Direction.SOUTH_WEST)
    # new_line = read_train_line("data/sunbury_line_stations.txt", stations, "Sunbury", "darkyellow", Direction.NORTH_WEST)
    # new_line = read_train_line("data/craigieburn_line_stations.txt", stations, "Craigieburn", "orange", Direction.NORTH)
    # new_line = read_train_line("data/upfield_line_stations.txt", stations, "Upflied", "darkorange", Direction.NORTH)
    # new_line = read_train_line("data/hurstbridge_line_stations.txt", stations, "Hurstbridge", "darkred", Direction.NORTH_EAST)
    # new_line = read_train_line("data/mernda_line_stations.txt", stations, "Mernda", "red", Direction.NORTH_EAST)



    new_line = read_train_line("data/mernda_line_stations.txt", stations, "Mernda", "red", Direction.NORTH_EAST)
    
    data["linear_lines"].append(new_line)
    
    data["line_count"] += 1
    #custom changes
    # station1: Station = stations["North Melbourne"]
    # station2: Station = stations["Southern Cross"]
    station1: Station = stations["Flinders Street"]
    station2: Station = stations["Jolimont"]
    station1.add_connection(station2.name, new_line.line_id)
    station2.add_connection(station1.name, new_line.line_id)
    # read_loop_line("data/city_loop.txt", (0,0), data)
    #save json
    with open(filepath, 'w', encoding='utf-8') as f:
        json_data = {"stations": [], "line_count": data["line_count"], "loop_lines": [], "linear_lines": []}
        json_data["stations"]= [stations[station].model_dump() for station in stations.keys()]
        json_data["loop_lines"] = [line.model_dump() for line in data["loop_lines"]]
        json_data["linear_lines"] = [line.model_dump() for line in data["linear_lines"]]
        json.dump(json_data, f, indent=4)






#TODO - Change station conenctions to be "line id" : [connections] pairs
#     - Change line station list to be pairs of ["station name": str, "stops" : boolean] for wehather it stops or not
#     - When reading lines, now do 2nd passthrough of all lines, to try and detect non-stopping stations, and insert them at correct ps with "false"