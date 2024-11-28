from __future__ import annotations
import random



class Station:
    def __init__(self, name: str, connections: list[str] = None):
        self.name = name
        self.connections: list[tuple[str,int]] = connections #list of (name, line_id), so connections to stations and via which line
        self.map_x = random.randint(1,100)
        self.map_y = random.randint(1,100)
        self.map_angle = 0
    
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
        return f"{self.name} station, connects to: {self.connections}"
    
    def __repr__(self):
        return self.__str__()
    
