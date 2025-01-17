from __future__ import annotations
from station import Station
from long_lat_getter import set_station_coords
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


    def add_station(self, station: Station):
        self.stations.append(station)
    
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
        if (self.stations[-1] is other.stations[0] or self.stations[0] is other.stations[-1]):
            return None

        # Check if the intersection point is within the bounds of both line segments
        if (min(self.x1, self.x2) <= x <= max(self.x1, self.x2) and
            min(self.y1, self.y2) <= y <= max(self.y1, self.y2) and
            min(other.x1, other.x2) <= x <= max(other.x1, other.x2) and
            min(other.y1, other.y2) <= y <= max(other.y1, other.y2)):
            return (x, y)
        else:
            return None
        
    
    def split(self, intersection: tuple[float,float], offset: tuple[float, float]) -> tuple[LineVector,LineVector]:
        """
        Splits the line vector into two new line vectors using the two stations nearest the intersection point
        """
        closest_station_index = None
        closest_distance = float("inf")
        second_closest_station_index = None
        for i,station in enumerate(self.stations):
            distance = math.sqrt(
                (station.map_x - intersection[0]) ** 2
                + (station.map_y - intersection[1]) ** 2
            )
            if distance < closest_distance:
                closest_station_index = i
                closest_distance = distance
                if i == len(self.stations) - 1:
                    second_closest_station_index = i-1
                else:
                    second_closest_station_index = i+1
        set_station_coords(self.stations[closest_station_index], offset)
        set_station_coords(self.stations[second_closest_station_index], offset)
        # Create the new line vectors
        if closest_station_index < second_closest_station_index:
            left_station = self.stations[closest_station_index]
            right_station = self.stations[second_closest_station_index]
        else:
            left_station = self.stations[second_closest_station_index]
            right_station = self.stations[closest_station_index]
        left_split = LineVector(
            self.x1, self.y1, left_station.map_x, left_station.map_y,
            (left_station.map_x - self.x1) / self.stations.index(left_station), (left_station.map_y - self.y1) / self.stations.index(left_station)
        )
        for station in self.stations[:self.stations.index(left_station)+1]:
            left_split.add_station(station)

        right_split = LineVector(
            right_station.map_x, right_station.map_y, self.x2, self.y2,
            (self.x2 - right_station.map_x) / (len(self.stations) - self.stations.index(right_station)), (self.y2 - right_station.map_y) / (len(self.stations) - self.stations.index(right_station))
        )
        for station in self.stations[self.stations.index(right_station):]:
            right_split.add_station(station)
        
        return left_split, right_split
        


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
            return f"Line vector from {self.stations[0].name} to {self.stations[-1].name} with vector ({self.vector_x},{self.vector_y})"
        

#TODO - add intersection thats splits into 2 new vectors method