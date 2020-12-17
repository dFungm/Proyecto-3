import random
from Flor import Flor
from Abeja import Abeja
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
        porRemplazar = []
        nuevasFlores = []
        for flor in self.flores:
            temp = flor.seleccionFlor(flor)
            if len(temp) == 2:
                porRemplazar.append(temp)
            elif len(temp) == 3:
                nuevasFlores.append(temp)
            else:
                print("Hay un error en los cruces de flores")
        return nuevasFlores,porRemplazar

    def creaAbeja(self,color,dira,dirb):
        abeja = Abeja()
        abeja.__init__(color,dira,dirb)
        self.abejas.append(abeja)

    def eliminaAbeja(self,color,dira,dirb):
        for abeja in self.abejas:
            if abeja.color == color and abeja.direccionA == dira and abeja.direccionB == dirb:
                self.abejas.remove(abeja)
                return 

    def creaFlor(self,pos,polen):
        flor = Flor()
        flor.__init__(flor,pos,polen)
        self.flores.append(flor)


    def eliminaFlor(self,pos):
        for flor in self.flores:
            if flor.pos == pos:
                self.flores.remove(flor)
                return

    def mutacion(self, abeja):
        tira = abeja.getADN()
        ran = random.randint(1, len(tira))
        if tira[ran] == 0:
            return tira[:ran - 1] + '1' + tira[ran:]
        else:
            return tira[:ran - 1] + '0' + tira[ran:]

    # def generacion(self):

