#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

CLIENT_ADDRESS = '127.0.0.1'  
CLIENT_PORT = 5000
MID_ADDRESS = '127.0.0.1'  
MID_PORT = 5001

#Conecta e envia a função desejada para o middleware
def processar():       
	soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	destino = (MID_ADDRESS,MID_PORT)
	conectou = False
	i=0
	while conectou != True and i != 3:
		try:	
			soquete.connect(destino)
			soquete.send("Subtracao:10,5,2")
			#soquete.send("Soma:10,5,2")
			#soquete.send("Multiplicacao:10,5,2")
			obterResultado(soquete)
			conectou = True
		except:
			pass
		i+=1
	if conectou == False:
		print("Erro: Não foi possível conectar com o middleware.")
		soquete.close()

#Obtem resultado do middleware
def obterResultado(soquete):
	resultado = soquete.recv(1024)
	if resultado == "Tentar":
		tentar = raw_input("Tentar novamente?(s/n): ")
		if tentar == 's' or tentar =='S':
			soquete.send(tentar)
			obterResultado(soquete)
		else:
			soquete.close()
	elif resultado == "Erro":
		print("Erro: a operação não pode ser realizada!")
		soquete.close()
	else:
		print(resultado)
		soquete.close()

if __name__ == "__main__":
	processar()
