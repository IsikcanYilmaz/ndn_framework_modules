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

import util

PREFIX : str = "/example"
NUM_TRIALS : int = 5

def runMininet(topo):
    net = Mininet(topo = topo, waitConnected = True)

    net.start()

    hosts : array = net.hosts
    print("hosts:", hosts)

    producer : Node = net.getNodeByName('h0_0')
    consumer : Node = net.getNodeByName('h3_3')
    filename : str = "payload.bin"
    recvFilename : str = "received_payload.bin"
    sizeBytes : int = 100 * 1024 
    
    util.nodeTest(producer)
    util.nodeTest(consumer)
    util.createPayload(node=producer, filename=filename, sizeBytes=sizeBytes)
    util.listenForFile(node=consumer, filename=recvFilename)

    print(f'{producer.name} transferring {sizeBytes} Bytes to {consumer.name} at {consumer.IP()}') 
    for i in range(0, NUM_TRIALS):
        t0 = time.time()
        util.sendFile(node=producer, destNode=consumer, filename=filename)
        t1 = time.time()
        print(f'Trial {i}: File transfer in {t1-t0} ms')

    # CLI(net)
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

    hosts = ndn.net.hosts
    print("hosts:", hosts)

    producer : Node = ndn.net.getNodeByName('h0_0')
    consumer : Node = ndn.net.getNodeByName('h3_3')
    filename = "payload.bin"
    recvFilename = "received_payload.bin"
    sizeBytes = 100 * 1024 
    
    util.nodeTest(producer)
    util.nodeTest(consumer)
    util.createPayload(node=producer, filename=filename, sizeBytes=sizeBytes)
    util.listenForFile(node=consumer, filename=recvFilename)

    print(f'{producer.name} transferring {sizeBytes} Bytes to {consumer.name} at {consumer.IP()}') 
    for i in range(0, NUM_TRIALS):
        t0 = time.time()
        util.sendFile(node=producer, destNode=consumer, filename=filename)
        t1 = time.time()
        print(f'Trial {i}: File transfer in {t1-t0} ms')
    
    print(f'{producer.name} starting NDN filetransfer')
    producer.cmd(f'nlsrc advertise {PREFIX}')
    producer.cmd(f'cat {filename} | ndnpoke {PREFIX} &> producer.log &')
    t0 = time.time()
    consumer.cmd(f'ndnpeek -p {PREFIX} &> {recvFilename}')
    t1 = time.time()
    print(f'NDN File transfer in {t1-t0} ms')

    MiniNDNCLI(ndn.net)
    ndn.stop()
    
if __name__ == "__main__":
    setLogLevel('info')
    # topo = createTopologySimpleTree(ndn=True)
    # topo = createTopologyComplex(ndn=True)
    # topo = createTopologyPointToPoint()
    # topo = createNdnCacheTopo(ndn=False)
    # runMininet(topo)
    topo = createNdnCacheTopo(ndn=True)
    runMinindn(topo)

