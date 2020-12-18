import random
class Flor:
    def __init__(self,pos,polen):
        self.pos = pos
        self.polen = polen #Polen tiene el rgb
        self.polenmezcla = []
        self.seleccionada = True

    def recolecta(self):
        return self.polen

    def deposito(self,Polen):
        self.polenmezcla.append(Polen)
        return []

    def resetpolen(self):
        self.polenmezcla = []

    #Retorna una nueva flor a base del polen depositado por las abejas
    def seleccionFlor(self):
        self.seleccionada = True
        if self.polenmezcla == []:
            self.seleccionada = False
            return self.pos
        cantidad = len(self.polenmezcla)
        proba = random.randint(1,40)
        if cantidad > proba:
            self.seleccionada = False
            return self.pos
        else:
            ran = random.randint(0, len(self.polenmezcla)-1)
            polenselect = self.polenmezcla[ran]
            mezcla = [self.polen,polenselect]
            R=mezcla[random.randint(0,1)][0]
            G=mezcla[random.randint(0,1)][1]
            B=mezcla[random.randint(0,1)][2]
            nuevaFlor = [R,G,B]
            return nuevaFlor
