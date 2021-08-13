"""
    This is sample script to unload the map
"""

from py_sne_rest_client import SpirentNetworkEmulator

sne_ip = '10.140.96.99'
uname = 'pwari'
map_name = 'Basic_impairment'

# load the sne
sne = SpirentNetworkEmulator.SpirentNetworkEmulator(sne_ip, username=uname)

# SNE version
sne_version = sne.get('/instrument/software/buildversion')
print('Loaded SNE version ', sne_version)

# get the map dictionary
map_dict = sne.get('/maps')
# filter user specified map
map_list = map_dict['maps']
map_id = ''

for map in map_list:
    if map['mapName'] == map_name:
        map_id = map['mapId']

if not map_id:
    print('Map name doesnt exist ', map_name)
    raise ValueError('Map name doesnt exist ', map_name)

response = sne.put('/maps/'+map_id+'/unload')
print('Status ', response)

print('Done !')


