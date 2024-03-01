#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.link import TCLink

"""
Topology to test basic NDN caching features. Special hosts will act as switches. 
Small Island LANs connected to eachother in a line like fashion. O-O-O-O-...
inter bw and delay denote the bw and delay between switches
intra bw and delay denote the bw and delay between hosts and their respective switches
"""
def createNdnCacheTopo(numIslands=4, \
                       numHostsPerIsland=4, \
                       interIslandBw=1, \
                       intraIslandBw=10, \
                       interIslandDelay="500ms", \
                       intraIslandDelay="10ms", \
                       ndn=True):
    topo = Topo()
    switches = []
    hosts = []

    # Form the islands
    for i in range(0, numIslands):
        switches.append(topo.addHost(f's{i}') if ndn else topo.addSwitch(f's{i}'))
        for j in range(0, numHostsPerIsland):
            hosts.append(topo.addHost(f'h{i}_{j}'))
            topo.addLink(hosts[-1], switches[-1], cls=TCLink, bw=intraIslandBw, delay=intraIslandDelay)

    # Link the islands
    for i in range(0, numIslands-1):
        topo.addLink(switches[i], switches[i+1], cls=TCLink, bw=interIslandBw, delay=interIslandDelay)

    return topo
