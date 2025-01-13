from __future__ import annotations

import math


class LineVector:

    def __init__(self, x1, y1, x2, y2, vector_x, vector_y):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.vector_x = vector_x
        self.vector_y = vector_y
        self.stations = []


    def add_station(self, station_name: str):
        self.stations.append(station_name)
    
    def slope(self):
        return (self.y2 - self.y1) / (self.x2 - self.x1)

    def parallel(self, other: LineVector):
        return math.isclose(self.slope(),other.slope())

    def intersect(self, other: LineVector):
        if self.parallel(other):
            return None
        x = (self.slope() * self.x1 - other.slope() * other.x1 + other.y1 - self.y1) / (self.slope() - other.slope())
        y = self.slope() * (x - self.x1) + self.y1
        
        #If the interstion occurs at the start point of the vectors, return None
        if (math.isclose(x,self.x1) and math.isclose(y,self.y1)) or (math.isclose(x,self.x2) and math.isclose(y,self.y2)):
            return None


        # Check if the intersection point is within the bounds of both line segments
        if (min(self.x1, self.x2) <= x <= max(self.x1, self.x2) and
            min(self.y1, self.y2) <= y <= max(self.y1, self.y2) and
            min(other.x1, other.x2) <= x <= max(other.x1, other.x2) and
            min(other.y1, other.y2) <= y <= max(other.y1, other.y2)):
            return (x, y)
        else:
            return None
        
    
    def __eq__(self, other: LineVector):
        for i in range(len(self.stations)):
            try:
                if self.stations[i] != other.stations[i]:
                    return False
            except IndexError:
                return False
            
        return True
    
    def __str__(self):
        if self.stations == []:
            return f"Line vector from ({self.x1},{self.y1}) to ({self.x2},{self.y2}) with vector ({self.vector_x},{self.vector_y})"
        else:
            return f"Line vector from {self.stations[0]} to {self.stations[-1]} with vector ({self.vector_x},{self.vector_y})"
        

#TODO - add intersection thats splits into 2 new vectors method