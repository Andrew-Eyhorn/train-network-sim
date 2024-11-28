from station import Station
import math
from enum import Enum

class Direction(Enum):
    EAST = 0
    SOUTH_EAST = math.pi / 4
    SOUTH = math.pi / 2
    SOUTH_WEST = math.pi * 3/4
    WEST = math.pi
    NORTH_WEST = math.pi * -3/4
    NORTH = math.pi*-1/2
    NORTH_EAST = math.pi * -1/4


class TrainLine:
    line_number = 0
    
    def __init__(self, name: str, color: str, direction: Direction):
        self.stations = []
        self.name = name
        self.line_color = color
        self.line_id = self.line_number
        TrainLine.line_number += 1
        self.length = 0
        self.direction = direction
    
    def add_station(self, station: Station):
        self.stations.append(station)
        self.length += 1
    
    def __str__(self):
        return self.name + " line, stations:" + str(self.stations)
    
    def __repr__(self):
        return self.__str__()
    


class LoopLine(TrainLine):

    def __init__(self, name, color_id, direction):
        super().__init__(name, color_id, direction)
    