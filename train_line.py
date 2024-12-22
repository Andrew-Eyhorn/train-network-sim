from station import Station
import math
from enum import Enum

from pydantic import BaseModel, Field
from typing import ClassVar

class Direction(float, Enum):
    EAST = 0
    SOUTH_EAST = math.pi * -1/4
    SOUTH = math.pi * -1/2
    SOUTH_WEST = math.pi * -3/4
    WEST = math.pi
    NORTH_WEST = math.pi * 3/4
    NORTH = math.pi * 1/2
    NORTH_EAST = math.pi * 1/4


class TrainLine(BaseModel):
    _line_number: ClassVar[int] = 0
    name: str
    line_color: str
    
    line_id: str = Field(init = False, default= 0)
    length: int = Field(init = False, default= 0)
    direction: Direction
    stations: list[dict] = Field(default_factory=list) #List of {"station name": str, "stop" : boolean}




    def __init__(self, **data):
        super().__init__(**data)
        if 'line_id' not in data or data['line_id'] is None:
            self.line_id = str(self._line_number) + "_" + self.name
            TrainLine._line_number += 1
    
    def add_station(self, station: Station, stop: bool = True):
        self.stations.append({"station": station.name, "stop": stop})
        self.length += 1

    def insert_station(self, position: int, station: Station, stop: bool = True):
        self.stations.insert(position,{"station": station.name, "stop": stop})
        self.length += 1
    
    def __str__(self):
        return self.name + " line, stations:" + str(self.stations)
    
    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.length

    def __getitem__(self, i: int):
        return self.stations[i]

class LoopLine(BaseModel):
    _loop_number: ClassVar[int] = 0
    centre_pos: tuple[int,int]
    stations: list[str]
    loop_id: int = Field(init = False, default= 0)
    def __init__(self, **data):
        super().__init__(**data)
        if 'line_id' not in data or data['line_id'] is None:
            self.loop_id = self._loop_number
            LoopLine._loop_number += 1



if __name__ == "__main__":
    # new_line = train_line = TrainLine(name = "Belgrave", line_color = "blue", direction = Direction.EAST)
    # print(new_line.model_dump_json(indent = 4))
    test = Direction["NORTH_EAST"]
    print(test)