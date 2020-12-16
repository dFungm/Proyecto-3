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
