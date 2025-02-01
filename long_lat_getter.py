#Gets the long and lat of each station in the list and adds it to the dictionary, saving it to the file between each request
#uses the nominatim openstreetmap api to get the long and lat of each station
#https://nominatim.org/

import aiohttp
import asyncio
import time
import json

from generate_json import read_json_network
async def fetch_station_data(station_name: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': station_name,
        'format': 'json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            await asyncio.sleep(2)  # Pause for 2 seconds
            return data

    # Simulate fetching data without making a request
    # await asyncio.sleep(2)  # Pause for 2 seconds
    # return [{'lat': 0.0, 'lon': 0.0}]  # Dummy data

async def main(stations: list[str], city: str, longlat_dict: dict[str, tuple[float, float]], filepath: str):
    """
    Fetches the long and lat of each station in the list and adds it to the dictionary, saving it to the file between each request
    """
    start_time = time.time()
    for station_name in stations:
        elapsed_time = time.time() - start_time
        print(f"\nTime elapsed: {elapsed_time:.2f} seconds")
        print("Fetching data for", station_name)
        data = await fetch_station_data(station_name + " Station, " + city)
        print("Received data for", station_name)
        longlat_dict[station_name] = (float(data[0]['lat']), float(data[0]['lon']))
        print("Added data for", station_name, ": ", longlat_dict[station_name])
        with open(filepath, 'w') as f:
            json.dump(longlat_dict, f)
    print(f"Finished fetching data for all stations, total time elapsed: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    city = "Melbourne"
    train_line_path = "data/" + city.lower() + "_data"
    data = read_json_network(train_line_path + "/network_data.json")
    stations = data["stations"]
    station_names = [stations[station].name for station in stations.keys()]
    print(station_names)
    longlat_dict = {}
    filepath = train_line_path + "/longlat_dict.json"
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(station_names, city, longlat_dict, filepath))
