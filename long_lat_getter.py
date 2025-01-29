from station import Station


# This dictionary is used to store the GPS coordinates of each station.
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
        "North Melbourne": (-37.8067303,144.9426907),
        "Craigieburn": 	(-37.6022613,144.9430882),
        "Sunbury": (-37.5791363,144.7279832),
        "Upfield": (-37.6660199,144.9468555),
        "Mernda": (-37.6025113,145.1011002),
        "Hurstbridge": (-37.6382525,145.1937326),
        "South Yarra": (-37.83787435,144.99240370674687),
        "Malvern": (-37.8662837,145.02934699227836),
        "Caulfield": (-37.8768317,145.0421711),
        "Dandenong": (-37.990080199999994,145.20974888689744),
        "Cranbourne": (-38.0996605,145.2802839),
        "East Pakenham": (-38.0843248,145.506738),
        "Frankston": (-38.1438097,145.1253744),
        "Clifton Hill": (-37.78887625,144.99536132966975),
        "Sandringham": 	(-37.9500934,145.0045424),
        "Footscray": (-37.8004606,144.900251), ####
        "Werribee": (-37.9000445,144.6603525),
        "Williamstown": (-37.8561229,144.8974805),
        "Newport": (-37.842752,144.883938), 
        "Coolaroo": (-37.6483429,144.9318723),
        "Roxburgh Park": (-37.6333333,144.9333333),
        "Gowrie": (-37.6094444,144.9466667),
        "Ormond": (-37.9033333,145.0422222),
        "McKinnon": (-37.9044444,145.0422222),
        "Prahran": (-37.8494444,144.9933333),
        "Windsor": (-37.8566667,144.9905556),
        "Sunshine": (-37.7872222,144.8344444),
        "Albion": (-37.7755556,144.8194444),
        "Macaulay": (-37.7944444,144.9366667),
        "Flemington Bridge": (-37.7888889,144.9394444),
        "Kooyong": (-37.8394444,145.035),
        "Tooronga": (-37.8488889,145.0522222),
        "Pascoe Vale": (-37.7266667,144.925),
        "Oak Park": (-37.7188889,144.9277778),
        "Merlynston": (-37.7088889,144.9577778),
        "Fawkner": (-37.7027778,144.9605556),
        "Toorak": (-37.8411111,145.0138889),
        "Armadale": (-37.8561111,145.0194444),
        

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