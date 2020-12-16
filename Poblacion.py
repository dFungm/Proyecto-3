import random
class Poblacion:
    def __init__(self):
        self.cantidadFlores = 5
        self.cantidadAbejas = 5
        self.flores = []
        self.abejas = []

        #a = Abeja([10,255,0],"Sur", "Oeste")
        #b = Abeja([8, 65, 45], "Norte", "Este")

    # def seleccion(self):

    def cruceAbeja(self, a1, a2):
        tira1 = a1.getADN()
        tira2 = a2.getADN()
        ran = random.randint(0,len(tira1))

        return tira1[:ran]+tira2[ran:], tira2[:ran]+tira1[ran:]

    def cruceFlor(self):
        pass

    def mutacion(self, abeja):
        tira = abeja.getADN()
        ran = random.randint(1, len(tira))
        if tira[ran] == 0:
            return tira[:ran - 1] + '1' + tira[ran:]
        else:
            return tira[:ran - 1] + '0' + tira[ran:]

    # def generacion(self):

