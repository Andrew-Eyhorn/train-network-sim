from __future__ import annotations
import random
from pydantic import BaseModel, Field
from typing import Optional


class Station(BaseModel):
    name: str
    connections: list[tuple[str,int]] = Field(default_factory=list) #list of (name, line_id), so connections to stations and via which line
    map_x: Optional[int] = random.randint(1,100)
    map_y: Optional[int] = random.randint(1,100)
    map_angle: Optional[float] = 0
    is_loop_station: Optional[bool] = False

    def __init__(self, **data):
        super().__init__(**data)
    
    def add_connection(self, station_name: str, line_id: int):
        """
        Adds a connection if not already in the station's connections list
        """
        connection = (station_name, line_id)
        if self.connections is None:
            self.connections = [connection]
        else:
            if connection not in self.connections:
                self.connections.append(connection)


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
    def __str__(self):
        return f"{self.name} station. Location: ({self.map_x, self.map_y}). Angle: {self.map_angle}"
    
    def __repr__(self):
        return self.__str__()
    
