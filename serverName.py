#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import threading

SERVERNAME_ADDRESS = '127.0.0.1' 
SERVERNAME_PORT = 5002

portas = []
portas = [("Subtracao",'10.90.37.4'),("Subtracao",'127.0.0.1')]

soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
origem = (SERVERNAME_ADDRESS, SERVERNAME_PORT)
soquete.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soquete.bind(origem)

#Notifica o middleware sobre os hosts dos server
while True:
	resp = ""
	mensagem, middleware = soquete.recvfrom(1024)
	for i in portas:
		if i[0] == mensagem:
			resp += str(i[1]) + ";"
	try:
		soquete.sendto(resp, middleware)
	except:
		pass
soquete.close()
