"""
    This is sample example to start and stop already loaded map
    This sample uses the Spirent Network Emulator ReST Client
"""


import sys
import time

# loading SNE path
sys.path.insert(0, '/Users/pwari/workspace/sne_rest_client')
from SpirentNetworkEmulator import SpirentNetworkEmulator

# initialize SNE credentials
sne_ip = '10.140.96.99'
username = 'pwari'
map_name = 'Basic_impairment'

# initialize sne
print('loading Spirent network emulator ReSt Client ')
sne = SpirentNetworkEmulator(sne_ip, username)

# get the SNE version
sne_version = sne.get('/instrument/software/buildversion')
print('SNE Version : ', sne_version)

# get the list of existing maps
response = sne.get('/maps')
print(response['status']['message'])
map_list = response['maps']
map_id = ''

# filter map_list for user specified map name
for map in map_list:
    if map['mapName'] == map_name:
        map_id = map['mapId']
    else:
        print('map name %s doesnt exist :', map_name)
        raise ValueError('map name %s doesnt exist :', map_name)

# start the map
# Note the map needs to be loaded already
print('starting the map')
response = sne.put('/maps/' + map_id + '/start')
print(response)

# uncomment below line if you need to add sleep time
# time.sleep(5)

# stop the map
print('stopping the map')
response = sne.put('/maps/' + map_id + '/stop')
print(response)

print('Done')