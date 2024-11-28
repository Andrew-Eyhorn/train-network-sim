from train_line import TrainLine, Direction
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

    train_line = TrainLine(name, color, direction)
    for i, station_name in enumerate(station_name_list):
        if station_name in stations.keys():
            new_station = stations[station_name]
        else:
            new_station = Station(station_name)
            stations[station_name] = new_station
        if i != len(station_name_list) - 1:
            new_station.add_connection(station_name_list[i+1], train_line.line_id)
        if i != 0:
            new_station.add_connection(station_name_list[i-1], train_line.line_id)
        train_line.add_station(new_station)
    return train_line


data = {"loop_lines": [], "linear_lines": []}
stations = {}



if __name__ == "__main__":
    #read existing json

    try:
        with open("data/network_data.json") as f:
            d = json.load(f)
            data["loop_lines"],data["linear_lines"] = d["loop_lines"], d["linear_lines"]
    except:
        pass
    #read new txt
    new_line = read_train_line("data/belgrave_line_stations.txt", stations, "Belgrave", "blue", Direction.EAST)
    data["linear_lines"].append(new_line)
    #custom changes
    station: Station = stations["Flinders Street"]
    station.add_connection("Richmond", new_line.line_id)
    #save json
    with open("data/temp.json", 'w', encoding='utf-8') as f:
        json.dump(data["linear_lines"][0].__dict__,f)
    