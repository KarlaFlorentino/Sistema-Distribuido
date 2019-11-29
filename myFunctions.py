#Classe que subtrai valores do primeiro numero informado
class Subtracao:
  def compute(self, valor):
    valores = []
    for i in range (len(valor.split(","))):
		valores.append(valor.split(",")[i])
    resultado = int(valores[0])
    for i in range (1,len(valores)):
		resultado -= int(valores[i])
    return resultado

#Classe que soma os valores informados
class Soma:
  def compute(self, valor):
    valores = []
    for i in range (len(valor.split(","))):
		valores.append(valor.split(",")[i])
    resultado = int(valores[0])
    for i in range (1,len(valores)):
		resultado += int(valores[i])
    return resultado

#Classe que multiplica os valores informados
class Multiplicacao:
  def compute(self, valor):
    valores = []
    for i in range (len(valor.split(","))):
		valores.append(valor.split(",")[i])
    resultado = int(valores[0])
    for i in range (1,len(valores)):
		resultado *= int(valores[i])
    return resultado

