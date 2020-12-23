class Abeja:
    def __init__(self, id, color, direccion, angulo, diametro, tipoRecorrido, padres, generacion):
        self.dir = ['Norte', 'Noreste', 'Este', 'Sureste', 'Sur', 'Suroeste', 'Oeste', 'Noroeste']
        self.id = id
        self.color = color
        self.direccion = direccion #Posicion del String
        self.angulo = angulo
        self.diametro = diametro
        self.tipoRecorrido = tipoRecorrido
        self.padres = padres
        self.generacion = generacion
        self.direccionFavorita = self.selectDir()

        self.pos = [50,50]
        self.floresEncontradas = 0
        self.distanciaTotal = 0
        self.polenCarry = []
        self.puntaje = 100

    # Color = 8
    # Direccion = 3
    # Angulo =
    # Direccion =
    # Tipo =
    def getADN(self): # Color, direccion, angulo, diametro, tipo de recorrido
        tira = ''
        for i in self.color:
            color = str(bin(i)[2:])
            tira += '0' * (8 - len(color)) + color

        dir = str(bin(self.direccion)[2:])
        tira += '0' * (3 - len(dir)) + dir

        ang = str(bin(self.angulo)[2:])
        tira += '0' * (6 - len(ang)) + ang

        dm = str(bin(self.diametro)[2:])
        tira += '0' * (6 - len(dm)) + dm

        tipo = str(bin(self.tipoRecorrido)[2:])
        tira += '0' * (4 - len(tipo)) + tipo

        return tira


    # Dado una direccion ejemplo Norte Este retorna las cordenadas hacia donde se debe mover,
    # como ejemplo en este caso [1,1] ya que se mueve para arriba en Y y para el
    # lado derecho en X, SOLO SE EJECTUA CUANDO SE CREA UNA ABEJA, luego de eso no se
    # deberia de llamar, para eliminar strains en performance
    def selectDir(self):
        if self.dir[self.direccion] == 'Norte':
            return [0,1]
        elif self.dir[self.direccion] == 'Noreste':
            return [1,1]
        elif self.dir[self.direccion] == 'Este':
            return [1,0]
        elif self.dir[self.direccion] == 'Sureste':
            return [1,-1]
        elif self.dir[self.direccion] == 'Sur':
            return [0,-1]
        elif self.dir[self.direccion] == 'Suroeste':
            return [-1,-1]
        elif self.dir[self.direccion] == 'Oeste':
            return [-1, 0]
        elif self.dir[self.direccion] == 'Noroeste':
            return [-1,1]

    def Radio(self,puntoOrigenX,puntoOrigenY):
        Adv = self.angulo
        Dm = self.diametro
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
        PuntosPerdidos = self.distanciaTotal // 2
        self.puntaje -= PuntosPerdidos
        PuntosPorFlor = self.floresEncontradas * 2
        self.puntaje += PuntosPorFlor
        return self.puntaje