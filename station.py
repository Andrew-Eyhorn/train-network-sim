from __future__ import annotations

class Station:
    def __init__(self, name: str, connections: list[str] = None):
        self.name = name
        self.connections = connections
    
    def add_connection(self, station_name: str):
        """
        Adds a connection if not already in the station's connections list
        """
        if self.connections is None:
            self.connections = [station_name]
        else:
            if station_name not in self.connections:
                self.connections.append(station_name)

    def __str__(self):
        return f"{self.name} station, connects to: {self.connections}"