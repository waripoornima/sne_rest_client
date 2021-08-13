"""
    This is sample example to load the existing MAP and run the traffic
    Use's the SpirentNetworkEmulation ReST Client
"""

import sys
import time
from py_sne_rest_client.SpirentNetworkEmulator import SpirentNetworkEmulator

# initialize SNE credentials
sne_ip = '10.140.96.99'
username = 'pwari'
map_name = 'Basic_impairment'

# load SNE ReST Client
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

if not map_id:
   print('map name doesnt exist ',map_name)
   raise ValueError('map name doesnt exist ',map_name)

# load the map
print('loading the map')
response = sne.post('/maps/' + map_id + '/load')
print(response)

# start the map
print('starting the map')
response = sne.put('/maps/' + map_id + '/start')
print(response)

# wait for 5 sec
print('wait for 5 sec')
time.sleep(5)

# /api/maps/{mapId}/impairments/{impId}/packetdrop
# get the drop count settings
# get the packect drop Imp Id
print('getting the packdrop imp id')
map_dict = sne.get('/api/maps/'+map_id+'/impairments')
impairment_id = ''
for imp in map_dict['impairments']:
    if imp['name'] == 'Drop Packets':
        impairment_id = imp['impId']

response = sne.get('/maps/'+map_id+'/impairments/'+impairment_id+'/packetdrop')
print(response['packetDrop']['packetDropSettings'])

# get the stats
response = sne.get('/maps/'+map_id+'/stats')
print('Stats :')
print(response)
print('')

# stop the map
print('stopping the map')
response = sne.put('/maps/' + map_id + '/stop')
print(response)

# unload the map
print('unloading the map')
response = sne.put('/maps/' + map_id + '/unload')
print(response)

print('Done !')