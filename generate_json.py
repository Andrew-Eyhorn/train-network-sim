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
    """
    Only works when the stations already exist in data
    """
    stations_list = []
    with open(filepath, newline ='') as stations_file:
        for line in stations_file.readlines():
            stations_list.append(line.strip())
    new_loop = LoopLine(centre_pos = centre, stations = stations_list)
    for i in range(len(stations_list) - 1):
        data["stations"][stations_list[i]].is_loop_station = True

    data["loop_lines"].append(new_loop)




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
    

def add_line(data: dict, line_stations_file: str, name: str, color: str, direction: Direction, extra_connection: tuple[str,str] | None):
    stations = data["stations"]
    new_line = read_train_line(line_stations_file, stations, name, color, direction)

    
    data["linear_lines"].append(new_line)
    
    data["line_count"] += 1
    if extra_connection is not None:
        #custom changes
        station1: Station = stations[extra_connection[0]]
        station2: Station = stations[extra_connection[1]]
        station1.add_connection(station2.name, new_line.line_id)
        station2.add_connection(station1.name, new_line.line_id)




def find_pass_stations(data: dict, target_line: TrainLine):
    """
    Finds if the target line has stations it passes through without stopping by checking the order of stations in other lines.
    If such stations are found, they are insterted into the target's station list with "stop" as False
    
    Lines must have more than 2 stations for this to work
    """
    lines = data["linear_lines"]
    for comparison_line in lines:
        if comparison_line.line_id == target_line.line_id:
            continue

        #for every conseutive pair in target, check if they exist in consecutive order in comparison line
        for i in range(len(target_line) - 1):
            
            if not target_line[i]["stop"] or stations[target_line[i]["station"]].is_loop_station:
                continue
            start = target_line.stations[i]["station"]
            end = target_line.stations[i + 1]["station"]

            start_pos = None
            end_pos = None
            for j in range(len(comparison_line)):
                if comparison_line[j]["station"] == start:
                    start_pos = j
                if comparison_line[j]["station"] == end:
                    end_pos = j
            if start_pos is None or end_pos is None:
                continue
            
            if start_pos + 1 < end_pos:
                extra_stations: list[str] = []
            
                for j in range(start_pos + 1, end_pos):
                    extra_stations.append(comparison_line.stations[j]["station"])
                pos = i + 1
                for station in extra_stations:
                    target_line.insert_station(pos, data["stations"][station], False)
                    pos += 1





data = {"stations": {}, "line_count": 0, "loop_lines": [], "linear_lines": []}

if __name__ == "__main__":
    #read existing json
    filepath = "data/temp.json"
    try:
        data = read_json_network(filepath)
    except:
        pass
    
    stations = data["stations"]

    add_line(data,"data/lilydale_line_stations.txt", "Lilydale", "lightblue", Direction.EAST, ("Flinders Street", "Richmond"))
    add_line(data,"data/belgrave_line_stations.txt", "Belgrave", "cyan", Direction.EAST,("Flinders Street", "Richmond"))
    add_line(data,"data/alamein_line_stations.txt", "Alamein", "blue", Direction.EAST,("Flinders Street", "Richmond"))
    add_line(data,"data/glen_waverly_line_stations.txt", "Glen Waverly", "darkblue", Direction.EAST,("Flinders Street", "Richmond"))
    add_line(data,"data/pakenham_line_stations.txt", "Pakenham", "purple", Direction.SOUTH_EAST,("Flinders Street", "Richmond"))
    add_line(data,"data/cranbourne_line_stations.txt", "Cranbourne", "#a569bd", Direction.SOUTH_EAST,("Flinders Street", "Richmond"))
    add_line(data,"data/frankston_line_stations.txt", "Frankston", "magenta", Direction.SOUTH,("Flinders Street", "Richmond"))
    add_line(data,"data/sandringham_line_stations.txt", "Sandringham", "pink", Direction.SOUTH,("Flinders Street", "Richmond"))
    add_line(data,"data/williamstown_line_stations.txt", "Williamstown", "green", Direction.SOUTH,None)
    add_line(data,"data/werribee_line_stations.txt", "Werribee", "lightgreen", Direction.SOUTH_WEST,None)
    add_line(data,"data/sunbury_line_stations.txt", "Sunbury", "yellow", Direction.WEST,("Southern Cross", "North Melbourne"))
    add_line(data,"data/craigieburn_line_stations.txt", "Craigieburn", "orange", Direction.NORTH,("Southern Cross", "North Melbourne"))
    add_line(data,"data/upfield_line_stations.txt", "Upfield", "darkorange", Direction.NORTH,("Southern Cross", "North Melbourne"))
    add_line(data,"data/hurstbridge_line_stations.txt", "Hurstbridge", "darkred", Direction.NORTH_EAST,("Flinders Street", "Jolimont"))
    add_line(data,"data/mernda_line_stations.txt", "Mernda", "red", Direction.NORTH_EAST,("Flinders Street", "Jolimont"))




    
    read_loop_line("data/city_loop.txt", (0,0), data)

    for line in data["linear_lines"]:
        find_pass_stations(data, line)

    #save json
    with open(filepath, 'w', encoding='utf-8') as f:
        json_data = {"stations": [], "line_count": data["line_count"], "loop_lines": [], "linear_lines": []}
        json_data["stations"]= [stations[station].model_dump() for station in stations.keys()]
        json_data["loop_lines"] = [line.model_dump() for line in data["loop_lines"]]
        json_data["linear_lines"] = [line.model_dump() for line in data["linear_lines"]]
        json.dump(json_data, f, indent=4)






"""TODO - Change station conenctions to be "line id" : [connections] pairs - #DONE
#     - Change line station list to be pairs of ["station name": str, "stops" : boolean] for wehather it stops or not - #DONE
#     - When reading lines, now do 2nd passthrough of all lines, to try and detect non-stopping stations, and insert them at correct ps with "false" DONE
      - Fix text on map
      - Have line return to direction
#     - Rework data to store lines with an id as key isntead of 0,1,2 blah
"""