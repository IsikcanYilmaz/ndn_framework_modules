#!/usr/bin/env python3 

import sys, os
from mininet.node import Node

NC_PORT = 12345

def createPayload(sizeBytes: int = 4096, 
                  filename: str = "payload.bin"
                  ) -> None:
    os.system(f'dd if=/dev/urandom of={filename} count={sizeBytes} bs=1')

def listenForFile(node: Node = None,
                  filename: str = "received_payload.bin",
                  port: int = 12345
                  ):
    # nc -l -p 12345 > received_payload.img
    # -l : listen, -p : port
    cmd = f'nc -l -p -q {port} > {filename}'

    # If this is being called thru mininet
    if node is not None:
        node.sendCmd(cmd)
    else:
        os.system(cmd)

def sendFile(node: Node = None,
             destNode: Node = None,
             destIp: str = None,
             filename: str = "payload.bin",
             port: int = 12345):
    # nc localhost 12345 < payload.img

    dest = destNode.IP() if destNode is not None else destIp
    if dest is None:
        print("Need either a destionation mininet node object or a destination IP")
    cmd = f'nc {dest} {port} < {filename}'

    # If this is being called thru mininet
    if node is not None:
        node.sendCmd(cmd)
    else:
        os.system(cmd)

