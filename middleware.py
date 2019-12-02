#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
from datetime import datetime

MID_ADDRESS = '127.0.0.1' 
MID_PORT = 5001
SERVERNAME_ADDRESS = ['0.0.0.0','127.0.0.1']
SERVERNAME_PORT = 5002
SERVER_ADDRESS = []

global solicitacao
solicitacao = ""
global resultado
resultado = 0
global cache
cache = {}

#Conecta com o serverName e obtem os hosts dos server
def conectarServerName(funcao):
	global cache
	conectou = False
	soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for j in range(len(SERVERNAME_ADDRESS)):	
		i=0
		while conectou != True and i != 3:
			try:	
						
				destino = (SERVERNAME_ADDRESS[j],SERVERNAME_PORT)
				soquete.settimeout(0.1)
				soquete.sendto(funcao,destino)		
				resposta,destino = soquete.recvfrom(1024)
				soquete.close()

				horaAtual = datetime.now().strftime("%H:%M")
				SERVER_ADDRESS.append(horaAtual)

				for i in range (len(resposta.split(";"))):
					SERVER_ADDRESS.append(resposta.split(";")[i])

				cache.update({funcao:SERVER_ADDRESS})
				conectou = True
			except:
				pass
			i+=1

	if conectou == False:
		return False	
	else:
		return True

#Conecta com o server e obtem o resultado
def conectarServerReflection(funcao,conexao):
	global solicitacao
	global resultado
	global cache
	conectou = False
	i = 1
	j = 0
	while conectou != True and i != (len(SERVER_ADDRESS) - 1):
		while conectou != True and j != 3:
			try:
				soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				destino = (cache[funcao][i], 5003)
				soquete.settimeout(0.1)
				soquete.connect(destino)
				conectou = True			
				soquete.send(solicitacao)

				
				try:
					resultado = soquete.recv(1024)
					soquete.close()
					notificarCliente(resultado,conexao)
					return True
				except socket.timeout as e:
					return "Tentar"		
			except:
				pass
			j+=1
		j = 0
		i += 1	

	if conectou == False:
		return False
		
def requisicaoLookUP(funcao,conexao):
	global cache
	if funcao in cache:
		auxHoraCache = int(cache[funcao][0].split(":")[0]) * 60 + int(cache[funcao][0].split(":")[1])
		auxHoraAtual = int(datetime.now().strftime("%H:%M").split(":")[0]) * 60 + int(datetime.now().strftime("%H:%M").split(":")[1])

		if (auxHoraAtual - auxHoraCache) > 3:
			del(cache[funcao])
			if not conectarServerName(funcao):
				try:
					conexao.send("Erro")
				except:
					pass
				conexao.close()
			else:
				auxSR = conectarServerReflection(funcao,conexao)
				if auxSR == "Tentar":
					try:
						conexao.send("Tentar")
						tentar = conexao.recv(1024)
						if tentar == 'S' or tentar=='s':
							auxSR = conectarServerReflection(funcao,conexao)
							if auxSR == "Tentar" or auxSR == False:
								try:
									conexao.send("Erro")
								except:
									pass
								conexao.close()
						else:
							conexao.close()
					except:
						pass
				if not auxSR:
					try:
						conexao.send("Erro")
					except:
						pass
					conexao.close()
		else:
			auxSR = conectarServerReflection(funcao,conexao)
			if auxSR == "Tentar":
				try:
					conexao.send("Tentar")
					tentar = conexao.recv(1024)
					if tentar == 'S' or tentar=='s':
						auxSR = conectarServerReflection(funcao,conexao)
						if auxSR == "Tentar" or auxSR == False:
							try:
								conexao.send("Erro")
							except:
								pass
							conexao.close()
					else:
						conexao.close()
				except:
					pass
			if not auxSR:
				try:
					conexao.send("Erro")
				except:
					pass
				conexao.close()
	
	else:
		auxSN = conectarServerName(funcao)
		if not auxSN:
			try:
				conexao.send("Erro")
			except:
				pass
			conexao.close()
		else:
			auxSR = conectarServerReflection(funcao,conexao)
			if auxSR == "Tentar":
				try:
					conexao.send("Tentar")
					tentar = conexao.recv(1024)
					if tentar == 'S' or tentar=='s':
						auxSR = conectarServerReflection(funcao,conexao)
						if auxSR == "Tentar" or auxSR == False:
							try:
								conexao.send("Erro")
							except:
								pass
							conexao.close()
					else:
						conexao.close()
				except:
					pass
			if not auxSR:
				try:
					conexao.send("Erro")
				except:
					pass
				conexao.close()


def receber(conexao,cliente):
	global solicitacao
	solicitacao = conexao.recv(1024)
	funcao = solicitacao.split(":")[0]
	requisicaoLookUP(funcao,conexao)

#Notifica o cliente sobre o resultado
def notificarCliente(resultado,conexao):
	try:
		conexao.send(resultado)
	except:
		pass
	conexao.close()

soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (MID_ADDRESS,MID_PORT )
soquete.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soquete.bind(origem)
soquete.listen(0)

while True:
	tc = threading.Thread(target=receber, args=soquete.accept())
	tc.start()
