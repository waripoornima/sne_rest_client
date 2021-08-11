# sne_rest_client

SpirentNetworkEmulator is python ReST client for SPirent Network Emulator ReST API that contains handy functions. 

This ReST client supports python2+ and python3+

## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SpirentNetworkEmulator like below. 
Rerun this command to check for and install  updates .

```bash

pip install py_sne_rest_client # python2
python3 -m pip install py_sne_rest_client # python3

```

## Usage
Features:
Command Syntax/Example :

            sne_object = SpirentNetworkEmulator(sne_ip,sne_username)

            1: Get the Build version
                end_point = '/instrument/software/buildversion'
                sne_object.get(end_point)

            2: Get the maps
                end_point = '/maps'
                sne_object.get(end_point)

            3: Load map.json file
                end_point = '/maps/json?shareWithAll=true'
                sne_object.post(end_point,file=file_name)

            4: Load the map into SNE, ready to be started
                end_point = '/maps/<mapid>/load'
                sne_object.post(end_point)

            5: Star the map
                end_point = '/maps/<mapId>/start'
                sne_object.put(end_point)

            6: Updates the current settings of a packet drop impairment
                end_point = '/maps/<MapID>/impairments/<ImpID>/packetdrop'
                true,false = 'true','false' # SNE is case sensitive
                drop_payload = {
                      "packetDropMode": "standardDropMode",
                      "enabled": true,
                      "timeConstraints": {
                        "enableTimeConstraints": false,
                        "startDelay": 1000,
                        "duration": 5000
                      },
                      "packetDropSettings": {
                        "standardDropMode": {
                          "packetDropCount": drop_count,
                          "perPacketCount": 100,
                          "dropMethod": "dropEvenly"
                        }
                      }
                    }
                sne_object.put(end_point, payload=drop_payload)

            7: Deletes a loaded capture replay file
                end_point = '/files/capturereplay/<pcapFile>'
                sne_object.delete(end_point)
                
#### Demo of some of the features:
```python
/examples/load_existing_map.py:
This is sample test to load the existing map, start traffic, check the drop packet setting , collect the stats , stop traffic and unload the map.

Note update following variables in script for your environment:
# currently SNE supports no password login
sne_ip = '10.140.96.99'
username = 'pwari'
map_name = 'Basic_impairment'

```

## Contact
feel free to contact for any issue while using the restclient
poornima.wari@spirent.com
support@spirent.com

## License
[MIT]
