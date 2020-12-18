import random
import math
import threading, time
from Flor import Flor
from Abeja import Abeja
from Grafo import Grafo

class Poblacion:

    def __init__(self):

        # Gris - Rojo - Amarillo - Verde - Azul - Morado - Blanco - Aqua
        self.colorFlor = [(128, 128, 128), (255, 0, 0), (255, 255, 0), (0, 128, 0),
                     (0, 0, 255), (128, 0, 128), (255, 255, 255), (0, 255, 255)]
        self.direccion = ['Norte', 'Noreste', 'Este', 'Sureste', 'Sur', 'Suroeste', 'Oeste', 'Noroeste']

        self.cantidadFlores = 10
        self.cantidadAbejas = 5
        self.flores = []
        self.abejas = []
        self.countGeneracion = 1
        self.threadTime = 0.5
        # self.threadsGeneraciones = []
        self.parada = 0
        self.grafoFlores = None
        self.floresGeneraciones = []
        self.abejasGeneraciones = []
        self.numFlores = 0
        self.numAbejas = 0

    # Generaciones (Threads)
    def generaciones(self):
        while self.parada < 5:
            if self.countGeneracion == 1:
                hilo = threading.Thread(name='Generacion %s' % self.parada,
                                        target=self.generacionInicial,
                                        args=(self.threadTime,))
                hilo.start()
                self.countGeneracion += 1
                self.parada += 1
                time.sleep(self.threadTime)
            else:
                hilo = threading.Thread(name='Generacion %s' % self.parada,
                                        target=self.generacion,
                                        args=(self.threadTime,))
                hilo.start()
                self.countGeneracion += 1
                self.parada += 1
                time.sleep(self.threadTime)

    def generacionInicial(self, segundos):
        print("PRIMERA GENERACION")
        for i in range(self.cantidadFlores):
            ranX = random.randint(0,99)
            ranY = random.randint(0, 99)
            color = random.randint(0, 7)
            flor = Flor([ranX, ranY],self.colorFlor[color])
            self.flores.append(flor)

        self.grafoBusqueda()

        for i in range(self.cantidadAbejas):
            self.numAbejas += 1
            color = random.randint(0, 7)
            direccion = random.randint(0, 7)
            abeja = Abeja(self.numAbejas, self.colorFlor[color],self.direccion[direccion])
            self.abejas.append(abeja)

        for abeja in self.abejas:
            hilo = threading.Thread(name='Abeja %s' % 1,
                                    target=self.busquedaAnchura,
                                    args=(self.grafoFlores, abeja,))
            hilo.start()

    def generacion(self, segundos):
        self.floresGeneraciones.append(self.flores)
        self.abejasGeneraciones.append(self.abejas)
        self.abejas = []
        self.flores = []
        print("Generación ", self.countGeneracion)

        '''
        .......
        '''

    # Abejas | Flores
    def creaAbeja(self, id, color, dir):
        abeja = Abeja()
        abeja.__init__(id, color,dir)
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


    # Algoritmo Genético
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

    def mutacion(self, abeja):
        tira = abeja.getADN()
        ran = random.randint(1, len(tira))
        if tira[ran] == 0:
            return tira[:ran - 1] + '1' + tira[ran:]
        else:
            return tira[:ran - 1] + '0' + tira[ran:]


    # Recorridos
    def grafoBusqueda(self):
        g = Grafo()
        for i in range(len(self.flores)):
            g.agregarVertice(i)

        for x in self.flores:
            for y in self.flores:
                if (x is not y) and self.flores.index(x) < self.flores.index(y):
                    dis = self.distanciaPuntos(x.pos, y.pos)
                    g.agregarArista(self.flores.index(x), self.flores.index(y), dis)

        for v in g:
            for w in v.obtenerConexiones():
                print("( %s , %s )" % (v.obtenerId(), w.obtenerId()) ,v.obtenerDistancia(w))

        for i in range(len(self.flores)):
            print(i, self.flores[i].pos)

        self.grafoFlores = g

    def florMasCercana(self, pos):
        florIndex = 0
        dis = 150
        for flor in self.flores:
            distancia = self.distanciaPuntos(pos, flor.pos)
            if distancia < dis:
                dis = distancia
                florIndex = self.flores.index(flor)
        return florIndex

    def busquedaAnchura(self, g, abeja):
        fIndex = self.florMasCercana(abeja.pos)
        campo = abeja.Radio(50,50, 100, 100) # (Origen), grados de error, diametro

        visitados = []
        cola = [fIndex]  # Vertice de inicio

        abeja.distanciaTotal += self.distanciaPuntos(abeja.pos, self.flores[fIndex].pos)

        while cola:
            actual = cola.pop(0)

            # Si el vertice actual no ha sido visitado o no esta en el radio
            if actual not in visitados and (self.flores[actual].pos in campo):
                visitados.append(actual)

            for v in g:
                if (v.obtenerId() not in visitados) and (self.flores[actual].pos in campo):
                    cola.append(v.obtenerId())

        # for flor in self.flores:
        #     if flor.pos in campo:
        #         print('flor', flor.pos)

        for v in visitados:
            if visitados.index(v) < len(visitados)-1:
                inicio = g.obtenerVertice(v)
                final = g.obtenerVertice(visitados[visitados.index(v)+1])
                if final in inicio.conectadoA:
                    print("-> Distacia recorrida por la abeja -> ", inicio.obtenerDistancia(final),
                          " ( %s , %s )" % (inicio.obtenerId(), final.obtenerId()))
                    abeja.distanciaTotal += inicio.obtenerDistancia(final)
                elif inicio in final.conectadoA:
                    print("-> Distacia recorrida por la abeja -> ", final.obtenerDistancia(inicio),
                          " ( %s , %s )" % (inicio.obtenerId(), final.obtenerId()))
                    abeja.distanciaTotal += final.obtenerDistancia(inicio)

        print("Abeja ", abeja.id, "-> Distancia recorrida: ", abeja.distanciaTotal)
        return

    def busquedaProfundidad(self):
        return

    def distanciaPuntos(self, p1, p2):
        distancia = math.sqrt(abs(((p2[0] - p1[0]) * (p2[0] - p1[0])) + ((p2[1] - p1[1]) * (p2[1] - p1[1]))))
        return distancia

    def posInversa(self, index):
        pos = self.flores[index].pos
        return (pos[1], pos[0])

p = Poblacion()
p.generaciones()

# def contar(self, segundos):
#     contador = 0
#     inicial = time.time()
#     limite = inicial + segundos
#     nombre = threading.current_thread().getName()
#     while inicial <= limite:
#         contador += 1
#         inicial = time.time()
#         print(nombre, contador)
#         time.sleep(1)


