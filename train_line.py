from station import Station

class TrainLine:
    line_colors = ["Red", "navy", "Blue","Green"]
    line_number = 0

    def __init__(self, name: str, color_id: int):
        self.stations = []
        self.name = name
        self.line_color = self.line_colors[color_id]
        self.line_id = self.line_number
        TrainLine.line_number += 1
    
    def add_station(self, station: Station):
        self.stations.append(station)
    
    def __str__(self):
        return self.name + " line, stations:" + str(self.stations)
    
    def __repr__(self):
        return self.__str__()