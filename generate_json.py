from train_line import TrainLine, Direction, LoopLine
from station import Station

import json

import matplotlib as mpl
import os




def read_train_line(filepath: str, stations: dict[Station], color: str) -> TrainLine:
    """
    Read a txt file containing station names in order
    """
    #read txt, and get station names, and connect them
    station_name_list = []
    with open(filepath, newline ='') as stations_file:
        line_data = stations_file.readlines()
        name = line_data[0].strip()
        direction = Direction[line_data[1].upper().strip()]
        for row in line_data[2:]:
            station_name_list.append(row.strip())

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
    
    #add loop connection:
    loop_entry = None
    loop_exit = None
    for i,station in enumerate(train_line.stations):
        station_name = station["station"]
        if loop_entry is None and stations[station_name].is_loop_station:
            loop_entry = i
        if loop_exit is None and not stations[station_name].is_loop_station:
            loop_exit = i
            break
    if loop_exit > loop_entry + 2:
        stations[train_line.stations[loop_entry]["station"]].add_connection(train_line.stations[loop_exit]["station"], train_line.line_id)
        stations[train_line.stations[loop_exit]["station"]].add_connection(train_line.stations[loop_entry]["station"], train_line.line_id)


    return train_line




def read_loop_line(filepath: str, centre: tuple[int,int], data: dict):
    """
    Makes stations that are in the loop marked as "loop stations"
    """
    stations_list = []
    with open(filepath, newline ='') as stations_file:
        for line in stations_file.readlines():
            stations_list.append(line.strip())
    new_loop = LoopLine(centre_pos = centre, stations = stations_list)
    for i in range(len(stations_list) - 1):
        if stations_list[i] not in data["stations"].keys():
            data["stations"][stations_list[i]] = Station(name  = stations_list[i])
        data["stations"][stations_list[i]].is_loop_station = True

    data["loop_lines"][new_loop.loop_id] = new_loop




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
            # read_data["loop_lines"] = [LoopLine.model_validate(line) for line in data["loop_lines"]]
            # read_data["linear_lines"] = [TrainLine.model_validate(line) for line in data["linear_lines"]]
            read_data["loop_lines"] = {line_id : LoopLine.model_validate(line) for line_id,line in data["loop_lines"].items()}
            read_data["linear_lines"] = {line_id : TrainLine.model_validate(line) for line_id,line in data["linear_lines"].items()}
            return read_data
    

def add_line(data: dict, line_stations_file: str, color: str):
    stations = data["stations"]
    new_line = read_train_line(line_stations_file, stations, color)

    
    data["linear_lines"][new_line.line_id] = new_line
    
    data["line_count"] += 1




def find_pass_stations(data: dict, target_line: TrainLine):
    """
    Finds if the target line has stations it passes through without stopping by checking the order of stations in other lines.
    If such stations are found, they are insterted into the target's station list with "stop" as False
    
    Lines must have more than 2 stations for this to work
    """
    lines = data["linear_lines"]
    for line_id in lines.keys():
        comparison_line = lines[line_id]
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





data = {"stations": {}, "line_count": 0, "loop_lines": {}, "linear_lines": {}}

if __name__ == "__main__":
    #read existing json
    filepath = "data/temp.json"
    try:
        data = read_json_network(filepath)
    except:
        pass
    
    stations = data["stations"]

    
    read_loop_line("data/loop_lines/city_loop.txt", (0,0), data)

    #init
    line_data_path = "data/linear_lines"
    lines_to_read = len(os.listdir(line_data_path))

    #prepare colors
    gradient = [x * 1/lines_to_read for x in range(lines_to_read)]
    cmap = mpl.colormaps["nipy_spectral"]
    colors = [mpl.colors.to_hex(cmap(i)) for i in gradient]
    i = 0
    for file_name in os.listdir(line_data_path):
        #get filepath
        line = os.path.join(line_data_path, file_name)
        add_line(data, line, color = str(colors[i]))
        #get to next color
        i += 1



    

    for line in data["linear_lines"].keys():
        find_pass_stations(data, data["linear_lines"][line])

    #save json
    with open(filepath, 'w', encoding='utf-8') as f:
        json_data = {"stations": [], "line_count": data["line_count"], "loop_lines": {}, "linear_lines": {}}
        json_data["stations"]= [stations[station].model_dump() for station in stations.keys()]
        json_data["loop_lines"] = {line_id : line.model_dump() for line_id,line in data["loop_lines"].items()}
        json_data["linear_lines"] = {line_id : line.model_dump() for line_id,line in data["linear_lines"].items()}
        json.dump(json_data, f, indent=4)






"""TODO - Change station conenctions to be "line id" : [connections] pairs - #DONE
#     - Change line station list to be pairs of ["station name": str, "stops" : boolean] for wehather it stops or not - #DONE
#     - When reading lines, now do 2nd passthrough of all lines, to try and detect non-stopping stations, and insert them at correct ps with "false" DONE
      - Fix text on map #mostly done, but loop needs condition
      - Have line return to direction #Done
#     - Rework data to store lines with an id as key isntead of 0,1,2 blah 
"""





"""
name
direction
station
break
 - check wehn exiting loop. connect to entry of loop #problem - werribee line/wilismation


"""