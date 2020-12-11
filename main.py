import random

class Abeja:
    def __init__(self, color, direccion):
        self.color = color
        self.direccion = direccion
        self.floresEncontradas = 0
        self.distanciaTotal = 0

    def getADN(self):
        tira = ''
        for i in self.color:
            color = str(bin(i)[2:])
            tira += '0' * (8 - len(color)) + color
        return tira


class Poblacion:
    def __init__(self):
        self.cantidadFlores = 5
        self.cantidadAbejas = 5
        self.flores = []
        self.abejas = []

        #a = Abeja([10,255,0],'Norte')
        #b = Abeja([8, 65, 45], 'Norte')

    # def seleccion(self):

    def cruce(self, a1, a2):
        tira1 = a1.getADN()
        tira2 = a2.getADN()
        ran = random.randint(0,len(tira1))

        return tira1[:ran]+tira2[ran:], tira2[:ran]+tira1[ran:]


    def mutacion(self, abeja):
        tira = abeja.getADN()
        ran = random.randint(1, len(tira))
        if tira[ran] == 0:
            return tira[:ran - 1] + '1' + tira[ran:]
        else:
            return tira[:ran - 1] + '0' + tira[ran:]

    # def generacion(self):


if __name__ == '__main__':
    Poblacion()
