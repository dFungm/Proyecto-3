class Abeja:
    def __init__(self, color, direccionA, direccionB):
        self.color = color
        self.direccionA = direccionA
        self.direccionB = direccionB
        self.direccionFavorita = self.selectDir(self)
        self.floresEncontradas = 0
        self.distanciaTotal = 0
        self.polenCarry = []
        self.puntaje = 100

    def getADN(self):
        tira = ''
        for i in self.color:
            color = str(bin(i)[2:])
            tira += '0' * (8 - len(color)) + color
        return tira
    #Dado una direccion ejemplo Norte Este retorna las cordenadas hacia donde se debe mover, como ejemplo en este caso [1,1] ya que se mueve para arriba en Y y para el
    #lado derecho en X, SOLO SE EJECTUA CUANDO SE CREA UNA ABEJA, luego de eso no se deberia de llamar, para eliminar strains en performance
    def selectDir(self):
        if self.direccionA == "Norte":
            if self.direccionB == "Este":
                return [1,1]
            elif self.direccionB == "Oeste":
                return [-1,1]
            elif self.direccionB == "Norte":
                return [0,1]
            else:
                print("Error la direccion no puede ser Norte Sur haciendo default a solo norte")
                return [0, 1]
        elif self.direccionA == "Sur":
            if self.direccionB == "Este":
                return [1,-1]
            elif self.direccionB == "Oeste":
                return [-1,-1]
            elif self.direccionB == "Sur":
                return [0,-1]
            else:
                print("Error la direccion no puede ser Sur Norte haciendo default a solo sur")
                return [0, -1]
        elif self.direccionA == "Este":
            if self.direccionB == "Norte":
                return [1,1]
            elif self.direccionB == "Sur":
                return [1,-1]
            elif self.direccionB == "Este":
                return [1,0]
            else:
                print("Error la direccion no puede ser Este Oeste haciendo default a solo este")
                return [1, 0]
        else:
            if self.direccionB == "Norte":
                return [-1, 1]
            elif self.direccionB == "Sur":
                return [-1, -1]
            elif self.direccionB == "Oeste":
                return [-1, 0]
            else:
                print("Error la direccion no puede ser Oeste Este haciendo default a solo oeste")
                return [-1, 0]

    def Radio(self,puntoOrigenX,puntoOrigenY,Adv,Dm):
        busquedaValida = []
        while(Dm != 0):
            busquedaValida.append([puntoOrigenX,puntoOrigenY])
            tempX = puntoOrigenX
            tempX2 = puntoOrigenX
            if Dm == 0:
                break
            for i in range(0,Adv):
                tempX += 1
                tempX2 -= 1
                busquedaValida.append([tempX,puntoOrigenY])
                busquedaValida.append([tempX2,puntoOrigenY])
            puntoOrigenX += self.direccionFavorita[0]
            puntoOrigenY += self.direccionFavorita[1]
            Dm -= 1
        return busquedaValida
    #direccionFavorita ya tiene la direccion hacia donde se debe mover, es lo que se le suma es decir si direccion favorita tiene [1,-1] suma X+1 y Y+-1 para el movimiento
    #esto deberia de hacer el movimiento bien
    def busquedaAbeja(self,AdV,Dm,RecorridoI,RecorridoO):
        puntoOrigenX = 1
        PuntoOrigenY = 1#Esto hay que cambiarlo luego son las coordenadas de donde empieza a buscar la abeja
        coordenadasValidas = self.Radio(self,puntoOrigenX,PuntoOrigenY,AdV,Dm) #Esta funcion saca en buena teoria todas las posiciones validas donde se puede mover la abeja
        #Entonces si compara una coordenada con coordenadas validas la vara le deberia decir si la abeja esta en un lugar donde esta permitida, pienso que es util para
        #la busqueda, para que no se salga ni del radio ni mas del angulo de desviacion tampoco, al momento de moverse

    def SeleccionAbeja(self):
        PuntosPerdidos = self.recorrido // 2
        self.puntaje -= PuntosPerdidos
        PuntosPorFlor = self.floresEncontradas * 2
        self.puntaje += PuntosPorFlor
        return self.puntaje