f = open("matrizP.txt", "r")
C = []
for linha in f:
    listaDeInteiros = []
    valores = linha.split(',')
    for i in valores:
        listaDeInteiros.append(int(i))
    C.append(listaDeInteiros)

print(C)

f.close()