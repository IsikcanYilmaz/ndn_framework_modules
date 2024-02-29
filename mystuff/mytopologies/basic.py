#!/usr/bin/env python3
from mininet.topo import Topo

# Point to point topology
def createTopologyPointToPoint(numHosts=4):
    topo = Topo()
    hosts = []
    for i in range(0, numHosts):
        hosts.append(topo.addHost(f'h{i}'))

    for i in range(0, numHosts-1):
        topo.addLink(hosts[i], hosts[i+1])
    
    return topo

# Simple tree. One switch connecting hosts
def createTopologySimpleTree(numHosts=5, ndn=False):
    topo = Topo()
    hosts = []
    sw = topo.addSwitch('s0') if not ndn else topo.addHost('s0')
    for i in range(0, numHosts):
        hosts.append(topo.addHost(f'h{i}'))
        topo.addLink(sw, hosts[-1])
    return topo

# Line topology
def createTopologyLine(numNodes=5, ndn=False):
    topo = Topo()

    # Hosts, switches, and links
    hosts = []
    switches = []
    for i in range(0, numNodes):
        hosts.append(topo.addHost(f'h{i}', ip=f'10.0.0.{i}'))

    for i in range(0, numNodes):
        switches.append(topo.addSwitch(f's{i}') if not ndn else topo.addHost(f's{i}'))
        topo.addLink(hosts[i], switches[i])

    for i in range(0, numNodes-1):
        topo.addLink(switches[i], switches[i+1])

    return topo

# $leafSwitches leaf switches 2 internal switches
# Every leaf switch has 3 hosts connected
def createTopologyComplex(numLeafSwitches=4, numHostsPerSwitch=3, ndn=False):
    if (numLeafSwitches % 2 != 0):
        print("Num leaf switches need to be an even number. Incrementing by 1!")
        numLeafSwitches += 1

    topo = Topo()

    hosts = []
    leafSwitches = []
    for i in range(0, numLeafSwitches):
        leafSwitches.append(topo.addSwitch(f'sl{i}') if not ndn else topo.addHost(f'sl{i}'))
        for j in range(0, numHostsPerSwitch):
            hosts.append(topo.addHost(f'h{i}_{j}'))
            topo.addLink(leafSwitches[-1], hosts[-1])

    internalSwitch0 = topo.addSwitch('si0') if not ndn else topo.addHost('si0') # North switch
    internalSwitch1 = topo.addSwitch('si1') if not ndn else topo.addHost('si1') # South switch

    # Connect switches and hosts
    for i in range(0, int(len(leafSwitches)/2)):
        topo.addLink(leafSwitches[i], internalSwitch0)

    for i in range(int(len(leafSwitches)/2), len(leafSwitches)):
        topo.addLink(leafSwitches[i], internalSwitch1)

    # Connect N/S switches
    topo.addLink(internalSwitch0, internalSwitch1)
    
    return topo
 
