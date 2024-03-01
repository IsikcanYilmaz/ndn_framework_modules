#!/usr/bin/env python3 

import sys, os, shlex
import subprocess
import time

from mininet.node import Node

NC_PORT = 12345

def nodeTest(node: Node):
    node.cmd(f'echo Node {node.name} at {node.IP()}')

def createPayload(node: Node = None, 
                  sizeBytes: int = 4096, 
                  filename: str = "payload.bin"
                  ) -> None:
    cmd = f'dd if=/dev/urandom of={filename} count={sizeBytes} bs=1'
    if node is not None:
        node.cmd(cmd)
    else:
        os.system(cmd)

def listenForFile(node: Node = None,
                  filename: str = "received_payload.bin",
                  port: int = 12345
                  ):
    # nc -l -p 12345 > received_payload.bin
    # -l : listen, -p : port
    cmd = f'nc -l -p {port} > {filename} &'
    # print(">", cmd)

    # If this is being called thru mininet
    if node is not None:
        node.cmd(cmd)
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

    # nc -w0 10.0.0.2 12345 < payload.bin
    # -w0 exit after EOF
    cmd = f'nc -w0 {dest} {port} < {filename}'

    # If this is being called thru mininet
    if node is not None:
        node.cmd(cmd)
    else:
        os.system(cmd)
        # print(output.stdout)

def test():
    pass
