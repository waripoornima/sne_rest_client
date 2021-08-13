"""
    This is sample script to reserve and release the ports
"""

from py_sne_rest_client import SpirentNetworkEmulator

# sne login details
sne_ip = '10.140.96.99'
uname = 'pwari'

# initialize sne
print('loading sne')
sne = SpirentNetworkEmulator.SpirentNetworkEmulator(sne_ip,username=uname)

# ports to be reserved
ports = [0,1] # Note SNE will reserve ports 1,2 as the ports are indexed 0-n
print('reserve ports',ports)
response = sne.put('/physical/ports/reserve', payload=ports)
print(response)

# release the ports
print('releasing ports',ports)
response = sne.put('/physical/ports/release',payload=ports)
print(response)

print('Done !')