from station import Station
import math
from enum import Enum

from pydantic import BaseModel, Field

class Direction(float, Enum):
    EAST = 0
    SOUTH_EAST = math.pi * -1/4
    SOUTH = math.pi * -1/2
    SOUTH_WEST = math.pi * 3/4
    WEST = math.pi
    NORTH_WEST = math.pi * 3/4
    NORTH = math.pi * 1/2
    NORTH_EAST = math.pi * 1/4


class TrainLine(BaseModel):
    _line_number: int = 0
    name: str
    line_color: str
    line_id: int = Field(init = False, default= 0)
    length: int = Field(init = False, default= 0)
    direction: Direction
    stations: list[str] = Field(default_factory=list)




    def __init__(self, **data):
        super().__init__(**data)
        if 'line_id' not in data or data['line_id'] is None:
            self.line_id = self._line_number
            self._line_number += 1
    
    def add_station(self, station: Station):
        self.stations.append(station.name)
        self.length += 1
    
    def __str__(self):
        return self.name + " line, stations:" + str(self.stations)
    
    def __repr__(self):
        return self.__str__()
    


class LoopLine(BaseModel):
    centre_pos: tuple[int,int]
    stations: list[str]








if __name__ == "__main__":
    new_line = train_line = TrainLine(name = "Belgrave", line_color = "blue", direction = Direction.EAST)
    print(new_line.model_dump_json(indent = 4))