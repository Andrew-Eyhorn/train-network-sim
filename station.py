from __future__ import annotations
import random
from pydantic import BaseModel, Field
from typing import Optional


class Station(BaseModel):
    name: str
    connections: dict[str,list[str]] = Field(default_factory=dict) #dict of  "line id" : [connections list] pairs, all connections of same line under one id
    map_x: Optional[int|None] = None
    map_y: Optional[int|None] = None
    latitude: Optional[float|None] = None
    longitude: Optional[float|None] = None
    map_angle: Optional[float] = 0
    is_loop_station: Optional[bool] = False

    def __init__(self, **data):
        super().__init__(**data)
    
    def add_connection(self, station_name: str, line_id: int):
        """
        Adds a connection if not already in the station's connections list
        """
        if line_id not in self.connections.keys():
            self.connections[line_id] = [station_name]
        else:
            if station_name not in self.connections[line_id]:
                self.connections[line_id].append(station_name)


    def update_map_coords(self, coords: tuple[float,float]):
        """
        Takes in an (x,y) pair and sets it to map_x and map_y
        """
        self.map_x = coords[0]
        self.map_y = coords[1]
    
    def update_angle(self, angle: float):
        """
        Update the stations's relative angle to the graph centre for its line to the origin
        """
        self.map_angle = angle
    
    def update_real_coords(self, latitude: float, longitude: float):
        """
        Update the lat and long of the station
        """
        self.latitude = latitude
        self.longitude = longitude
    def __str__(self):
        return f"{self.name} station. Location: ({self.map_x, self.map_y}). Angle: {self.map_angle}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.name == other.name
