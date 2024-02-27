#!/usr/bin/env python3

from subprocess import PIPE

from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI

import minindn

from minindn.minindn import Minindn
from minindn.apps.app_manager import AppManager
from minindn.util import MiniNDNCLI, getPopen
from minindn.apps.nfd import Nfd
from minindn.helpers.nfdc import Nfdc

PREFIX = "/example"

def createTopology():
    topo = Topo()

    # # hosts
    # a = topo.addHost('a')
    # b = topo.addHost('b')
    # c = topo.addHost('c')
    #
    # # add links
    # topo.addLink(a, b, delay='10ms', bw=10)
    # topo.addLink(b, c, delay='10ms', bw=10)
    
    # Hosts, switches, and links
    hosts = []
    switches = []
    for i in range(0, 5):
        hosts.append(topo.addHost(f'h{i}', ip=f'10.0.0.{i}'))

    for i in range(0, 5):
        switches.append(topo.addSwitch(f's{i}'))
        topo.addLink(hosts[i], switches[i])

    for i in range(0, 4):
        topo.addLink(switches[i], switches[i+1])

    return topo

def createRoutes():
    pass

def runMininet():
    topo = createTopology() 
    net = Mininet(topo = topo, waitConnected = True)
    net.start()
    CLI(net)
    net.stop()
    
if __name__ == "__main__":
    runMininet()





