from __future__ import annotations

class Station:
    def __init__(self, name: str, connections: list[str] = None):
        self.name = name
        self.connections: list[tuple[str,int]] = connections #list of (name, line_id), so connections to stations and via which line
    
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

    def __str__(self):
        return f"{self.name} station, connects to: {self.connections}"
    
    def __repr__(self):
        return self.__str__()