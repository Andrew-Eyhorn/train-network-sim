from station import Station



longlat_dict = {
        "Burwood": (-37.851671,145.0805767),
        "Hartwell": (-37.848978,145.083073),
        "Darling": (-37.8689928,145.0629478),
        'Glen Iris': (-37.8596103,145.0586893),
        "Lilydale": (-37.7571582, 145.34586560554067),
        "Ringwood": (-37.8152752, 145.22962),
        "Camberwell": (-37.82658505, 145.0586576878648),
        "Burnley": (-37.82762235, 145.0080911963464),
        "Richmond": (-37.823932049999996, 144.98957127791425),
        "Flinders Street": (-37.818185650000004, 144.9664771839778),
        "Belgrave": (-37.9096952,145.3548577),
        "Alamein": (-37.8683603,145.0797334),
        "Glen Waverley": (-37.8793882,145.1627795),
        "Parliament": (-37.8127127,144.9734669),
        "Melbourne Central": (-37.81000385,144.96256902021068),
        "Flagstaff": (-37.8118581,144.95602868156527),
        "Southern Cross": (-37.8191925,144.9533975),
    }


def set_station_coords(closest_station: Station, offset: tuple[float,float]) -> None:
    """
    Sets the stations map coordinates based on the station's real coordinates and the offset.
    """
    if closest_station.longitude is None:
        try:
            location = longlat_dict[closest_station.name]
        except KeyError:
            raise Exception("Error updating station coords - no current GPS coords for station " + closest_station.name)
        closest_station.update_real_coords(location[0], location[1])
    closest_station.update_map_coords(
                    (
                        (closest_station.longitude - offset[0]) * 1111,
                        (closest_station.latitude - offset[1]) * 1111,
                    ))