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
        self.tipoRecorrido = ['Lejos del panal, por anchura', 'Cerca del panal, por anchura',
                              'Lejos del panal, por profundidad', 'Cerca del panal, por profundidad',
                              'Aleatorio']
        self.ventana = ventana
        self.ventanamain = ventanamain
        #-------------------------
        self.cantidadFlores = 20
        self.cantidadAbejas = 8
        self.threadTime = 1
        #-------------------------
        self.flores = []
        self.abejas = []
        self.parada = 0
        self.grafoFlores = None
        self.floresGeneraciones = []
        self.abejasGeneraciones = []
        self.numFlores = 0
        self.numAbejas = 0
        self.countGeneracion = 1

    # Generaciones (Threads)
    def generaciones(self,gens,lb1,lb2):
        qp = QPainter(self.ventana.pixmap())
        while self.parada < gens:
            if self.countGeneracion == 1:
                hilo = threading.Thread(name='Generacion %s' % self.parada,
                                        target=self.generacionInicial,
                                        args=(self.threadTime, qp,))
                hilo.start()
                self.countGeneracion += 1
                self.parada += 1
                time.sleep(self.threadTime)
            else:
                hilo = threading.Thread(name='Generacion %s' % self.parada,
                                        target=self.generacion,
                                        args=(self.threadTime, qp,))
                hilo.start()
                self.countGeneracion += 1
                self.parada += 1
                time.sleep(self.threadTime)
            dis = 0
            flor = 0
            for abeja in self.abejas:
                dis += abeja.distanciaTotal
                flor += abeja.floresEncontradas
            print("Distancia total: ", dis)
            print("Flores totales: ", flor)
            lb1.setText(str(flor))
            lb2.setText(str(dis))
        self.TextFile()

    def generacionInicial(self, segundos, qp):
        print("Generación ", self.countGeneracion)
        for i in range(self.cantidadFlores):
            ranX = random.randint(0,99)
            ranY = random.randint(0, 99)
            color = random.randint(0, 7)
            flor = Flor([ranX, ranY],self.colorFlor[color])
            self.flores.append(flor)

            self.drawNewFlower(qp, flor) # Pinta la flor en la ventana
            # hilo = threading.Thread(target=self.drawNewFlower, args=(qp, flor,))
            # hilo.start()

        self.grafoBusqueda()

        for i in range(self.cantidadAbejas):
            self.numAbejas += 1
            color = random.randint(0, 7)
            direccion = random.randint(0, 7)
            angulo = random.randint(10, 50)
            diametro = random.randint(10, 50)
            recorrido = random.randint(0, 15)
            abeja = Abeja(self.numAbejas, self.colorFlor[color], direccion, angulo,
                          diametro, recorrido, [], self.countGeneracion)
            self.abejas.append(abeja)

        self.threadAbejas()

    def generacion(self, segundos, qp):
        print("Generación ", self.countGeneracion)

        self.floresGeneraciones.append(self.flores)
        self.abejasGeneraciones.append(self.abejas)

        # Nuevas flores
        auxFlores = []
        for flor in self.flores:
            pos, polen = flor.seleccionFlor()
            newflor = Flor(pos, polen)
            auxFlores.append(newflor)

            self.drawNewFlower(qp, newflor) # Pinta la flor en la ventana
            # hilo = threading.Thread(target=self.drawNewFlower, args=(qp, newflor,))
            # hilo.start()

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

        self.threadAbejas()

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
        ran = random.randint(0,50)
        if ran < 10:
            adn = self.mutacion(adn)

        ang = int(adn[27:33], 2)
        if ang > 50:
            ang = 40

        dir = int(adn[33:39], 2)
        if dir > 50:
            dir = 40

        tipo = int(adn[39:43], 2)

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
                if x is not y:
                # if (x is not y) and self.flores.index(x) < self.flores.index(y):
                    dis = self.distanciaPuntos(x.pos, y.pos)
                    g.agregarArista(self.flores.index(x), self.flores.index(y), dis)

        for v in g:
            for w in v.obtenerConexiones():
                print("( %s , %s )" % (v.obtenerId(), w.obtenerId()) ,v.obtenerDistancia(w))

        for i in range(len(self.flores)):
            print(i, self.flores[i].pos)

        self.grafoFlores = g

    def busquedaAnchura(self, g, abeja):
        fIndex, campo = self.florMasCercana(abeja)

        if fIndex == -1:
            return

        visitados = []
        cola = [fIndex]  # Vertice de inicio

        while cola:
            actual = cola.pop(0)

            # Si el vertice actual no ha sido visitado o no esta en el radio
            if actual not in visitados and (self.flores[actual].pos in campo):
                visitados.append(actual)
                abeja.floresEncontradas += 1

            v = g.obtenerVertice(actual)

            for vertice in v.conectadoA:
                if vertice.obtenerId() not in cola and vertice.obtenerId() not in visitados and \
                    (self.flores[actual].pos in campo):
                    cola.append(vertice.obtenerId())

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
            else:
                self.depositarPolen(self.flores[visitados.index(v)], abeja.polenCarry)
                abeja.polenCarry.append(self.flores[visitados.index(v)])

        if len(visitados) > 0:
            abeja.distanciaTotal += self.distanciaPuntos(abeja.pos, self.flores[fIndex].pos)

        # print("-> Abeja ", abeja.id,
        #       "\n   ADN: ", abeja.getADN(), " -> ",len(abeja.getADN()),
        #       "\n   Distancia recorrida: ", abeja.distanciaTotal,
        #       "\n   Flores visitadas: ", len(abeja.polenCarry), " -> ", visitados,
        #       "\n   Angulo: ", abeja.angulo,
        #       "\n   Diametro: ", abeja.diametro)
        return

    def busquedaProfundidad(self, g, abeja):
        fIndex, campo = self.florMasCercana(abeja)

        if fIndex == -1:
            return

        cola = [fIndex]
        visitados = self.busquedaProfundidadAux(cola, [], campo, g, abeja)

        for v in visitados:
            if visitados.index(v) < len(visitados) - 1:
                inicio = g.obtenerVertice(v)
                final = g.obtenerVertice(visitados[visitados.index(v) + 1])
                if final in inicio.conectadoA:
                    print("-> Distacia recorrida por la abeja -> ", inicio.obtenerDistancia(final),
                          " ( %s , %s )" % (inicio.obtenerId(), final.obtenerId()))

                    abeja.distanciaTotal += inicio.obtenerDistancia(final)
                    self.depositarPolen(self.flores[visitados.index(v)], abeja.polenCarry)
                    abeja.polenCarry.append(self.flores[visitados.index(v)])
            else:
                self.depositarPolen(self.flores[visitados.index(v)], abeja.polenCarry)
                abeja.polenCarry.append(self.flores[visitados.index(v)])

        if len(visitados) > 0:
            abeja.distanciaTotal += self.distanciaPuntos(abeja.pos, self.flores[fIndex].pos)

    def busquedaProfundidadAux(self, cola, visitados, campo, g, abeja):

        if len(cola) > 0:
            actual = cola.pop(0)

            if actual not in visitados and (self.flores[actual].pos in campo):
                visitados.append(actual)
                abeja.floresEncontradas += 1

            v = g.obtenerVertice(actual)
            print('cola', visitados)
            for vertice in v.conectadoA:
                if vertice.obtenerId() not in cola and vertice.obtenerId() not in visitados and \
                        (self.flores[actual].pos in campo):
                    cola.append(vertice.obtenerId())
                    return self.busquedaProfundidadAux(cola, visitados, campo, g, abeja)
        else:
            return visitados

    def busquedaRandom(self, abeja):
        pos, campo = self.getCampo(abeja)
        li = list(range(len(self.flores)))

        for i in range(len(self.flores)):
            ran = random.randint(0, len(li)-1)
            if self.flores[li[ran]].pos in campo:
                dis = self.distanciaPuntos(abeja.pos, self.flores[li[ran]].pos)
                abeja.distanciaTotal += dis
                abeja.floresEncontradas += 1
                self.depositarPolen(self.flores[li[ran]], abeja.polenCarry)
                abeja.polenCarry.append(self.flores[li[ran]])
                abeja.pos = self.flores[li[ran]].pos
            li.remove(li[ran])
        return


    # Crea los threads de las abejas
    def threadAbejas(self):
        for abeja in self.abejas:
            hilo = None
            if 0 <= abeja.tipoRecorrido <= 5: # Por anchura
                hilo = threading.Thread(name='Abeja %s' % abeja.id,
                                        target=self.busquedaAnchura,
                                        args=(self.grafoFlores, abeja,))
            elif 6 <= abeja.tipoRecorrido <= 11: # Por profundidad
                hilo = threading.Thread(name='Abeja %s' % abeja.id,
                                        target=self.busquedaAnchura,
                                        args=(self.grafoFlores, abeja,))
            else: # Random
                hilo = threading.Thread(name='Abeja %s' % abeja.id,
                                        target=self.busquedaRandom,
                                        args=(abeja,))
            hilo.start()
            time.sleep(self.threadTime//len(self.abejas))

    # Distancia entre puntos
    def distanciaPuntos(self, p1, p2):
        distancia = math.sqrt(abs(((p2[0] - p1[0]) * (p2[0] - p1[0])) + ((p2[1] - p1[1]) * (p2[1] - p1[1]))))
        return distancia

    # Busca la flor mas cerca a la abeja
    def florMasCercana(self, abeja):
        florIndex = -1
        dis = 150

        pos, campo = self.getCampo(abeja)

        for flor in self.flores:
            distancia = self.distanciaPuntos(pos, flor.pos)
            if distancia < dis and flor.pos in campo:
                dis = distancia
                florIndex = self.flores.index(flor)
        return florIndex, campo

    # Obtiene el radio y la posicion inicial de la abeja
    def getCampo(self, abeja):
        campo = abeja.Radio(abeja.pos[0], abeja.pos[1])
        pos = abeja.pos
        if (0 <= abeja.tipoRecorrido <= 2) or (6 <= abeja.tipoRecorrido <= 8):
            ran = random.randint(0,1)
            pos = sorted(campo, key=lambda x: x[ran], reverse=True)[0]
            campo = abeja.Radio(pos[0], pos[1])
            # print(abeja.angulo, abeja.diametro)
        return pos,campo

    # Agrega el polen de la abeja a la flor
    def depositarPolen(self, flor, polenFlores):
        for f in polenFlores:
            flor.deposito(f.polen)

    # Pinta el pixel de la flor
    def drawNewFlower(self, qp, flor):
        print('DRAW')
        pen = QPen(QColor(flor.polen[0], flor.polen[1], flor.polen[2]),3)
        qp.setPen(pen)
        point = qp.drawPoint(flor.pos[0], flor.pos[1])
        self.ventanamain.update()

    # Archivo de texto
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
                    text += '\t\t' + 'Padres: ' + str(abeja.padres) + '\n'
                text += '\t\t' + 'Puntaje: ' + str(abeja.puntaje) + '\n' + \
                '\t\t' + 'Angulo: ' + str(abeja.angulo) + ', Radio: ' + str(abeja.diametro) + '\n'

                if 0 <= abeja.tipoRecorrido <= 2:
                    text += '\t\t' + 'Tipo de recorrido: ' + self.tipoRecorrido[0] + '\n\n'
                elif 3 <= abeja.tipoRecorrido <= 5:
                    text += '\t\t' + 'Tipo de recorrido: ' + self.tipoRecorrido[1] + '\n\n'
                elif 6 <= abeja.tipoRecorrido <= 8:
                    text += '\t\t' + 'Tipo de recorrido: ' + self.tipoRecorrido[2] + '\n\n'
                elif 9 <= abeja.tipoRecorrido <= 11:
                    text += '\t\t' + 'Tipo de recorrido: ' + self.tipoRecorrido[3] + '\n\n'
                else:
                    text += '\t\t' + 'Tipo de recorrido: ' + self.tipoRecorrido[4] + '\n\n'

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

