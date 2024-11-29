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


data = {"loop_lines": [], "linear_lines": []}
stations = {}



if __name__ == "__main__":
    #read existing json

    try:
        with open("data/temp.json") as f:
            data = json.load(f)
            read_data = {}
            read_data["loop_lines"] = [TrainLine.model_validate(line) for line in data["loop_lines"]]
            read_data["linear_lines"] = [TrainLine.model_validate(line) for line in data["linear_lines"]]
            data = read_data
    except:
        pass

   
    # #read new txt
    # new_line = read_train_line("data/lilydale_line_stations.txt", stations, "Lilydale", "lightblue", Direction.EAST)
    # new_line = read_train_line("data/alamein_line_stations.txt", stations, "Alamein", "lightpurple", Direction.EAST)
    # new_line = read_train_line("data/belgrave_line_stations.txt", stations, "Belgrave", "blue", Direction.EAST)
    # new_line = read_train_line("data/glen_waverly_line_stations.txt", stations, "Glen Waverly", "purple", Direction.EAST)


    #TODO - need to fix line_id not all being 0
    data["linear_lines"].append(new_line)
    #custom changes
    station: Station = stations["Flinders Street"]
    station.add_connection("Richmond", new_line.line_id)
    #save json
    with open("data/temp.json", 'w', encoding='utf-8') as f:
        json_data = {"loop_lines": [], "linear_lines": []}
        json_data["loop_lines"] = [line.model_dump() for line in data["loop_lines"]]
        json_data["linear_lines"] = [line.model_dump() for line in data["linear_lines"]]
        json.dump(json_data, f, indent=4)



#TODO - make data json serialisable, then work on drawing loop, then drwaing sations