#!/usr/bin/env python3

from subprocess import PIPE

from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI

import minindn
import time 

from minindn.minindn import Minindn
from minindn.apps.app_manager import AppManager
from minindn.util import MiniNDNCLI, getPopen
from minindn.apps.nlsr import Nlsr
from minindn.apps.nfd import Nfd
from minindn.helpers.nfdc import Nfdc
from minindn.helpers.ip_routing_helper import IPRoutingHelper

from mytopologies.basic import *
from mytopologies.ndn_cache_topo import *

PREFIX = "/example"
   
def runMininet(topo):
    net = Mininet(topo = topo, waitConnected = True)

    net.start()
    CLI(net)
    net.stop()

def runMinindn(topo):
    Minindn.cleanUp()
    Minindn.verifyDependencies()
    ndn = Minindn(topo=topo)
    ndn.start()

    info('Starting nfd and nlsr on nodes')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)
    nlsrs = AppManager(ndn, ndn.net.hosts, Nlsr)
    sleepSecs = 5
    info(f'Sleeping for {sleepSecs} secs')
    time.sleep(sleepSecs)
    IPRoutingHelper.calcAllRoutes(ndn.net)

    MiniNDNCLI(ndn.net)
    ndn.stop()
    
if __name__ == "__main__":
    setLogLevel('info')
    # topo = createTopologySimpleTree(ndn=True)
    # topo = createTopologyComplex(ndn=True)
    topo = createTopologyPointToPoint()
    # topo = createNdnCacheTopo(ndn=False)
    runMininet(topo)
    # runMinindn(topo)

