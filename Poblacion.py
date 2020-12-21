import random
import math
import threading, time

from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QBrush
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Flor import Flor
from Abeja import Abeja
from Grafo import Grafo

class Poblacion:

    def __init__(self,ventana,ventanamain):

        # Gris - Rojo - Amarillo - Verde - Azul - Morado - Blanco - Aqua
        self.colorFlor = [(128, 128, 128), (255, 0, 0), (255, 255, 0), (0, 128, 0),
                     (0, 0, 255), (128, 0, 128), (255, 255, 255), (0, 255, 255)]
        self.direccion = ['Norte', 'Noreste', 'Este', 'Sureste', 'Sur', 'Suroeste', 'Oeste', 'Noroeste']
        self.ventana = ventana
        self.ventanamain = ventanamain
        self.cantidadFlores = 10
        self.cantidadAbejas = 8
        self.flores = []
        self.abejas = []
        self.countGeneracion = 1
        self.threadTime = 1
        self.parada = 0
        self.grafoFlores = None
        self.floresGeneraciones = []
        self.abejasGeneraciones = []
        self.numFlores = 0
        self.numAbejas = 0

    # Generaciones (Threads)
    def generaciones(self,gens,lb1,lb2):
        while self.parada < gens:
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
            dis = 0
            flor = 0
            for abeja in self.abejas:
                dis = dis + abeja.distanciaTotal
                flor = flor + abeja.floresEncontradas
            print("Distancia total: ", dis)
            print("Flores totales: ", flor)
            lb1.setText(str(flor))
            lb2.setText(str(dis))
            self.ventanamain.update()
        self.TextFile()


    def generacionInicial(self, segundos):
        qp = QPainter(self.ventana.pixmap())
        print("PRIMERA GENERACION")
        for i in range(self.cantidadFlores):
            ranX = random.randint(0,99)
            ranY = random.randint(0, 99)
            color = random.randint(0, 7)
            flor = Flor([ranX, ranY],self.colorFlor[color])
            pen = QPen(QColor(self.colorFlor[color][0],self.colorFlor[color][1],self.colorFlor[color][2]))
            qp.setPen(pen)
            qp.drawPoint(ranX,ranY)
            self.ventanamain.update()
            self.flores.append(flor)
        self.ventanamain.update()
        self.grafoBusqueda()

        for i in range(self.cantidadAbejas):
            self.numAbejas += 1
            color = random.randint(0, 7)
            direccion = random.randint(0, 7)
            angulo = random.randint(10, 50)
            diametro = random.randint(10, 50)
            recorrido = random.randint(0, 4)
            abeja = Abeja(self.numAbejas, self.colorFlor[color], direccion, angulo,
                          diametro, recorrido, [], self.countGeneracion)
            self.abejas.append(abeja)

        for abeja in self.abejas:
            time.sleep(self.threadTime//len(self.abejas))
            hilo = threading.Thread(name='Abeja %s' % abeja.id,
                                    target=self.busquedaAnchura,
                                    args=(self.grafoFlores, abeja,))
            hilo.start()

    def generacion(self, segundos):
        qp = QPainter(self.ventana.pixmap())
        print("Generación ", self.countGeneracion)

        self.floresGeneraciones.append(self.flores)
        self.abejasGeneraciones.append(self.abejas)

        # Nuevas flores
        auxFlores = []
        for flor in self.flores:
            pos, polen = flor.seleccionFlor()
            newflor = Flor(pos, polen)
            pen = QPen(QColor(polen[0], polen[1], polen[2]))
            qp.setPen(pen)
            qp.drawPoint(pos[0], pos[1])
            self.ventanamain.update()
            auxFlores.append(newflor)

        # Nuevas Abejas
        for abeja in self.abejas:
            abeja.SeleccionAbeja()

        # Abejas ordenadas por puntuacion
        sortedAbejas = sorted(self.abejas, key=lambda x: x.puntaje, reverse=True)

        # Algoritmo Genetico
        auxAbejas = []
        for i in range(0, len(self.abejas)-1, 2):
            a1, a2 = self.cruceAbeja(self.abejas[i], self.abejas[i+1])
            auxAbejas.append(a1)
            auxAbejas.append(a2)

        self.flores = auxFlores
        self.abejas = auxAbejas

        for abeja in self.abejas:
            time.sleep(self.threadTime//len(self.abejas))
            hilo = threading.Thread(name='Abeja %s' % abeja.id,
                                    target=self.busquedaAnchura,
                                    args=(self.grafoFlores, abeja,))
            hilo.start()

    # Algoritmo Genético
    def cruceAbeja(self, a1, a2):
        ADN1 = a1.getADN()
        ADN2 = a2.getADN()
        ran = random.randint(0, len(ADN1) - 1)

        AUX1 = ADN1[:ran] + ADN2[ran:]
        AUX2 = ADN2[:ran] + ADN1[ran:]

        abeja1 = self.creaAbeja(AUX1, [a1.id, a2.id])
        abeja2 = self.creaAbeja(AUX2, [a1.id, a2.id])
        return abeja1, abeja2

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
        return nuevasFlores, porRemplazar

    def mutacion(self, adn):
        # tira = abeja.getADN()
        ran = random.randint(1, len(adn))
        if adn[ran] == 0:
            return adn[:ran - 1] + '1' + adn[ran:]
        else:
            return adn[:ran - 1] + '0' + adn[ran:]

    # Abejas | Flores
    def creaAbeja(self, adn, padres):
        # R - G - B - Direccion - Angulo - Diametro - Tipo de recorrido

        # MUTACION


        ang = int(adn[27:33], 2)
        if ang > 50:
            ang = 50

        dir = int(adn[33:39], 2)
        if dir > 50:
            dir = 50

        tipo = int(adn[39:42], 2)
        if tipo > 5:
            tipo = 3

        self.numAbejas += 1
        abeja = Abeja(self.numAbejas, [int(adn[0:8], 2), int(adn[8:16], 2), int(adn[16:24], 2)],
                       int(adn[24:27], 2), ang, dir, tipo, padres, self.countGeneracion)
        return abeja

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
        qp = QPainter(self.ventana.pixmap())
        fIndex = self.florMasCercana(abeja.pos)
        campo = abeja.Radio(50,50) # (Origen), angulo, diametro

        visitados = []
        cola = [fIndex]  # Vertice de inicio

        while cola:
            pen = QPen(QColor(abeja.color[0], abeja.color[1], abeja.color[2]))
            qp.setPen(pen)
            qp.drawPoint(abeja.pos[0], abeja.pos[1])
            self.ventanamain.update()
            actual = cola.pop(0)

            # Si el vertice actual no ha sido visitado o no esta en el radio
            if actual not in visitados and (self.flores[actual].pos in campo):
                visitados.append(actual)
                abeja.floresEncontradas += 1

            for v in g:
                if (v.obtenerId() not in visitados) and (self.flores[actual].pos in campo):
                    cola.append(v.obtenerId())

        for v in visitados:
            if visitados.index(v) < len(visitados)-1:
                inicio = g.obtenerVertice(v)
                final = g.obtenerVertice(visitados[visitados.index(v)+1])
                if final in inicio.conectadoA:
                    print("-> Distacia recorrida por la abeja -> ", inicio.obtenerDistancia(final),
                          " ( %s , %s )" % (inicio.obtenerId(), final.obtenerId()))

                    abeja.distanciaTotal += inicio.obtenerDistancia(final)
                    self.depositarPolen(self.flores[visitados.index(v)], abeja.polenCarry)
                    abeja.polenCarry.append(self.flores[visitados.index(v)])

                elif inicio in final.conectadoA:
                    print("-> Distacia recorrida por la abeja -> ", final.obtenerDistancia(inicio),
                          " ( %s , %s )" % (inicio.obtenerId(), final.obtenerId()))

                    abeja.distanciaTotal += final.obtenerDistancia(inicio)
                    self.depositarPolen(self.flores[visitados.index(v)], abeja.polenCarry)
                    abeja.polenCarry.append(self.flores[visitados.index(v)])
            else:
                print(visitados.index(v)-1, len(self.flores))
                self.depositarPolen(self.flores[visitados.index(v)], abeja.polenCarry)
                abeja.polenCarry.append(self.flores[visitados.index(v)])

        if len(visitados) > 1:
            abeja.distanciaTotal += self.distanciaPuntos(abeja.pos, self.flores[fIndex].pos)

        print("-> Abeja ", abeja.id,
              "\n   ADN: ", abeja.getADN(), " -> ",len(abeja.getADN()),
              "\n   Distancia recorrida: ", abeja.distanciaTotal,
              "\n   Flores visitadas: ", len(abeja.polenCarry), " -> ", visitados,
              "\n   Angulo: ", abeja.angulo,
              "\n   Diametro: ", abeja.diametro)

        return

    def busquedaProfundidad(self):
        return

    def distanciaPuntos(self, p1, p2):
        distancia = math.sqrt(abs(((p2[0] - p1[0]) * (p2[0] - p1[0])) + ((p2[1] - p1[1]) * (p2[1] - p1[1]))))
        return distancia

    def posInversa(self, index):
        pos = self.flores[index].pos
        return (pos[1], pos[0])

    def depositarPolen(self, flor, polenFlores):
        for f in polenFlores:
            flor.deposito(f.polen)

    def TextFile(self):
        text = ''
        for i in range(len(self.abejasGeneraciones)):
            text += 'Generacion ' + str(i+1) + '\n\n'
            for abeja in self.abejasGeneraciones[i]:
                text += '\t' + 'Abeja ' + str(abeja.id) + '\n' + \
                        '\t\t' + 'Color Favorito: (' + str(abeja.color[0]) + ', ' + \
                        str(abeja.color[1]) + ', ' + str(abeja.color[2]) + ')\n' + \
                        '\t\t' + 'Direccion Favorita: ' + self.direccion[abeja.direccion] + '\n' + \
                        '\t\t' + 'Distancia Recorrida: ' + str(abeja.distanciaTotal) + '\n' + \
                        '\t\t' + 'Flores Encontradas: ' + str(abeja.floresEncontradas) + '\n'
                if abeja.padres is not []:
                    print(str(abeja.padres))
                    text += '\t\t' + 'Padres: ' + str(abeja.padres) + '\n'
                text += '\t\t' + 'Puntaje: ' + str(abeja.puntaje) + '\n' + \
                '\t\t' + 'Angulo: ' + str(abeja.angulo) + ', Radio: ' + str(abeja.diametro) + '\n\n'



        f = open('Generaciones.txt', 'a')
        f.write(text)
        f.close()




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


