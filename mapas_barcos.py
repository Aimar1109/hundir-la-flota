# HUNDIR LA FLOTA

import os
import random
import time

class Mapa():
    def __init__(self, name):
        self.name = name
        self.mar = 0
        self.mapa = [[self.mar]*10 for _ in range(10)]
        self.barcos = []
        self.disparos = []
        self.tipos_barco = {"Portaaviones": 5,
                       "Acorazado": 4, 
                       "Crucero": 3, 
                       "Destructor": 2,
                       "Submarino": 1}

    def actualizar_mapa(self, fila, columna, valor):
        self.mapa[fila][columna] = valor
    
    def colocar_barcos(self):
        for barco in self.barcos:
            for posicion in barco.posiciones:
                self.actualizar_mapa(posicion[0], posicion[1], barco.tamaño)

    def crear_barco(self, name, tamaño, fila, columna, orientacion, direccion):
        nuevo_barco = Barco(name, tamaño, [fila, columna], orientacion, direccion)
        self.barcos.append(nuevo_barco)

    def colocar_flota(self):
        for barco, tamaño in self.tipos_barco.items():
            if barco == "Destructor" or barco == "Submarino":
                cantidad = 2
            else:
                cantidad = 1
            for i in range(cantidad):
                while True:
                    self.display_un_mapa()
                    print(f"\nColocar {barco} {i+1} de tamaño {tamaño}:")
                    fila = int(input("Ingrese la fila inicial: "))
                    columna = int(input("Ingrese la columna inicial: "))
                    if tamaño == 1:
                        orientacion = None
                        direccion = None
                    else:
                        orientacion = input("Ingrese la orientación (vertical)/(horizontal): ")
                        if orientacion == 'vertical':
                            orientacion = True
                            direccion = input("Ingrese la orientación Vertical: (ar)/(ab): ")
                        else:
                            orientacion = False
                            direccion = input("Ingrese la orientación Horizontal (d)/(i): ")
                    nuevo_barco = Barco(barco, tamaño, [fila, columna], orientacion, direccion)
                    nuevo_barco.crear_barco()
                    if self.validar_barco(nuevo_barco):
                        break
                    else:
                        os.system('cls')
                        print('\n       NO ES POSIBLE PONER EL BARCO AHI')
                        time.sleep(3)
                self.barcos.append(nuevo_barco)
                self.colocar_barcos()
    
    def display_un_mapa(self):
        os.system('cls')
        print(f"\t       {self.name.upper()}")
        for i in range(11):
            if i == 0:
                for x in range(10):
                    if x == 0:
                        print(f'   {x}', end="")
                    elif x == 9:
                        print(f'  {x}')
                    else:
                        print(f'  {x}', end="")
            else:
                print(f'{i-1} ' + str(self.mapa[i-1]))

    def display_juego(self, bot):
        os.system('cls')
        print(f"\t       {self.name.upper()}\t\t\t\t    BOT")
        for i in range(11):
            if i == 0:
                for x in range(10):
                    if x == 0:
                        print(f'   {x}', end="")
                    else:
                        print(f'  {x}', end="")
                print('   |  ', end='')
                for x in range(10):
                    if x == 0:
                        print(f'   {x}', end="")
                    elif x == 9:
                        print(f'  {x}')
                    else:
                        print(f'  {x}', end="")
            else:
                print(f"{i-1} {self.mapa[i-1]}  | {i-1}  {bot.mapa[i-1]}")


    
    def validar_barco(self, n_barco):
        for pos in n_barco.posiciones:
            if pos[0] < 0 or pos[1] < 0 or pos[0] > 9 or pos[1] > 9:
                return False
            for barco in self.barcos:
                if pos in barco.posiciones or pos in barco.alrededor:
                    return False
        return True
    
    def disparo(self, contrario, y, x):
        col = False
        self.disparos.append([y, x])
        for barco in contrario.barcos:
            if [y, x] in barco.posiciones:
                col = True
                contrario.actualizar_mapa(y, x, '-')
                barco.posiciones.remove([y, x])
                if len(barco.posiciones) != 0:
                    return True, 1
                else:
                    contrario.barcos.remove(barco)
                    return True, 2
        if not col:
            contrario.actualizar_mapa(y, x, 'X')
            return False, 0
            


class MapaBot(Mapa):
    def __init__(self):
        self.name = 'Bot'
        self.mar = 0
        self.mapa = [[self.mar]*10 for _ in range(10)]
        self.barcos = []
        self.disparos = []

    def colocar_flota_aleatoria(self):
        tipos_barco = {"Portaaviones": 5,
                       "Acorazado": 4,
                       "Crucero": 3,
                       "Destructor": 2,
                       "Submarino": 1}

        for barco, tamaño in tipos_barco.items():
            if barco == "Destructor" or barco == "Submarino":
                cantidad = 2
            else:
                cantidad = 1
            for i in range(cantidad):
                orientacion = random.choice(['vertical', 'horizontal'])
                if orientacion == 'vertical':
                    orientacion = True
                    direccion = random.choice(['ar', 'ab'])
                else:
                    orientacion = False
                    direccion = random.choice(['d', 'i'])
                while True:
                    fila = random.randint(0, 9)
                    columna = random.randint(0, 9)
                    nuevo_barco = Barco(barco, tamaño, [fila, columna], orientacion, direccion)
                    nuevo_barco.crear_barco()
                    nuevo_barco.guadar_alrededor()
                    if self.validar_barco(nuevo_barco):
                        break
                self.barcos.append(nuevo_barco)
    

class Barco():
    def __init__(self, nombre, tamaño, p_posicion, vertical, direccion):
        self.nombre = nombre
        self.tamaño = tamaño
        self.p_posicion = p_posicion
        self.vertical = vertical
        self.direccion = direccion
        self.posiciones = []
        self.alrededor = []

    def crear_barco(self):
        if self.tamaño > 1:
            for i in range(self.tamaño):
                if self.vertical:
                    if self.direccion == 'ab':
                        self.posiciones.append([self.p_posicion[0]+i, self.p_posicion[1]])
                    else:
                        self.posiciones.append([self.p_posicion[0]-i, self.p_posicion[1]])
                else:
                    if self.direccion == 'd':
                        self.posiciones.append([self.p_posicion[0], self.p_posicion[1]+i])
                    else:
                        self.posiciones.append([self.p_posicion[0], self.p_posicion[1]-i])
        else:
            self.posiciones.append([self.p_posicion[0], self.p_posicion[1]])
    
    def guadar_alrededor(self):
        p = []
        for pos in self.posiciones:
            p.append(pos)
        if self.vertical:
            if self.direccion == 'ar':
                p.reverse()

            if (p[0][0] - 1) > -1:
                self.alrededor.append([p[0][0] - 1, p[0][1]])
                p.insert(0, [p[0][0] - 1, p[0][1]])
            if (p[-1][0] + 1)  <= 9:
                self.alrededor.append([p[-1][0] + 1, p[0][1]])
                p.append([p[-1][0] + 1, p[0][1]])

            a = []
            b = []
            for pos in p:
                if pos[1]+1 < 10:
                    a.append([pos[0], pos[1]+1])
                if pos[1]-1 > -1:
                    b.append([pos[0], pos[1]-1])
            self.alrededor = self.alrededor + a + b

        else:
            if self.direccion == 'i':
                p.reverse()

            if p[0][1] + 1 < 10:
                self.alrededor.append([p[0][0], p[0][1]-1])
                p.insert(0, [p[0][0], p[0][1]-1])
            if p[-1][1] - 1 > -1:
                self.alrededor.append([p[0][0], p[-1][1]+1])
                p.append([p[0][0], p[-1][1]+1])

            a = []
            b = []
            for pos in p:
                if pos[1]+1 < 10:
                    a.append([pos[0]+1, pos[1]])
                if pos[1]-1 >= 0:
                    b.append([pos[0]-1, pos[1]])
            self.alrededor = self.alrededor + a + b