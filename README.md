# train-network-sim

Set of scripts to generate a train network map as an undirected multigraph, in order to easily generate and display a network map for either an existing or created train network. 

For a real-world city train network, it uses certain stations as "anchor points", and uses their real-world coordinates as the basis on which to determine the position of the other train stations. 
An anchor point station is one that is either a station on a loop, the terminus of the line (that is, if it has at least one incoming line that doesn't continue past it) or if it is a split station, where a following or previous station has fewer line connections than the split station does.

![image](https://github.com/user-attachments/assets/bd5834c7-8e54-49fa-b8f9-ae8d504c9793) 

*In this example for Melbourne, both Dandenong and Cranbourne would be anchor points.*


Real station coordinates are obtained using long_lat_getter.py which uses the Nominatim python API - https://nominatim.org/release-docs/develop/api/Overview/, and are stored in a json file. For a custom network, these coordinates would have to be provided for the network to be able to be mapped.

To generate the graph, the script requires a json files that stores the information of train line and station. This is generated using generate_json.py, which reads a set of train line txts.

The main script reads the json, and with a specified a centre station, which will be located at 0,0 and must be an anchor point as its real coordinates are used to scale the locations of other stations, the script then maps out the other stations by spacing them out along line vectors which are drawn between pairs of anchor's for each train line. 

This graph data is then finally saved to json. Currently, the output graph is displayed using: https://github.com/Andrew-Eyhorn/train-network-sim-ui, and an example for Melbourne's train network can currently be seen at https://andrew-eyhorn.github.io/train-network-sim-ui/




