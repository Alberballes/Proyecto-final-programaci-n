import time
import random
from colorama import init
import json
init()  # Activa soporte ANSI en Windows automáticamente




# Colores ANSI
RESET = "\033[0m"
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
GRIS = "\033[90m"
BLANCO = "\033[97m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"



#-------------------------------------------------------------
#combat and characters
#----------------------------------------------------------------
enemy_roster = {
    "goblin" : {"hp" : 40, "ataque": 8, "defensa" : 4, "affinity" : {"weakness" : "fire", "resistance": "ice"}},
    "skeleton" : {"hp" : 45, "ataque": 9, "defensa" : 6, "affinity" : {"weakness" : "dark", "resistance": "fire"}},
    "cultist" : {"hp" : 50, "ataque": 10, "defensa" : 5, "affinity" : {"weakness" : "light", "resistance": "dark"}},
    "plant" : {"hp" : 55, "ataque": 8, "defensa" : 7, "affinity" : {"weakness" : "ice", "resistance": "wind"}},
    "cerberus" : {"hp" : 400, "ataque": 15, "defensa" : 12, "affinity" : {"weakness" : "none", "resistance": "none"}}

}

default_char = {
    "mage" : {"hp" : 120, "ataque" : 12, "defensa" : 6 , "mp" : 100, "skill list": {"fireball" : {"affinity" : "fire", "mult" : 1.6, "cost" : 12 },"ice storm" : {"affinity" : "ice", "mult" : 1.6, "cost" : 12 }}} ,
    "dancer" : {"hp" : 150, "ataque" : 10, "defensa" : 10, "mp" : 80, "skill list": {"healing dance" : {"affinity" : "healing", "mult" : 1.2 , "cost" : 10}, "windblast" : {"affinity" : "wind", "mult" : 1.5 , "cost" : 12}}},
    "assasin" : {"hp" : 130, "ataque" : 16, "defensa" : 8, "mp" : 60, "skill list": {"hack away" : {"affinity" : "phys", "mult" : 1.8 , "cost" : 8}, "dark blade" : {"affinity" : "dark", "mult" : 1.8 , "cost" : 15}}},
    "knight" : {"hp" : 180, "ataque" : 13, "defensa" : 14, "mp" : 70, "skill list" : {"holy sword" : {"affinity" : "light", "mult" : 1.7, "cost" : 15}, "Spear thrust" : {"affinity" : "phys" , "mult" : 1.8, "cost" : 8}}}
}



class Char:
    def __init__(self, nombre, tipo, hp, mp, ataque, defensa):
        self.nombre = nombre
        self.tipo = tipo
        self.hp = default_char[tipo]["hp"]
        self.ataque = default_char[tipo]["ataque"]
        self.defensa = default_char[tipo]["defensa"]
        self.mp = default_char[tipo]["mp"]
        self.nivel = 1
        self.exp = 0

    def __str__(self):
        return f"{self.nombre}   con   {self.hp} hp --- {self.mp} mp --- {self.ataque} ataque --- {self.defensa} defsensa"
    
    def __sub__(self, otro):
        
        turno = 1
        if turno % 2 !=0:
            battle_menu = input("what do you want to do?   1--- normal attack    2--- skill ")
            
            if battle_menu == "1": #ataque normal
                dmg = int(round(max(0, self.ataque - otro.defensa // 2),0))
                
            elif battle_menu == "2":
                print("-----SKILLS-----")
                n = -1
                for i in default_char[tipo]['skill list']:
                    aff = default_char[tipo]['skill list'][i]['affinity']
                    n = n+1
                    print(f"{n}) {i} - Affinity: {aff} - Mp cost: {default_char[tipo]['skill list'][i]['cost']}")
                    
                skill_select = int(input("What skill do you want to use?   "))
                skill = default_char[tipo]['skill list']
                claves = list(skill.keys())  
                time.sleep(0.5)
                if enemy_roster[enem.bicho]['affinity']['weakness'] == default_char[tipo]['skill list'][claves[skill_select]]['affinity']: #Mira a ver si el enemigo es débil al ataque

                    dmg = int(round(max(0,self.ataque * default_char[tipo]['skill list'][claves[skill_select]]['mult'] - otro.defensa // 2) * 2, 0))

                    self.mp -= default_char[tipo]['skill list'][claves[skill_select]]['cost'] #Resta el coste de la skill al Mp del jugador
                
                elif enemy_roster[enem.bicho]['affinity']['resistance'] == default_char[tipo]['skill list'][claves[skill_select]]['affinity']: #Mira a ver si el enemigo resiste ataque
                    dmg = int(round(max(0,self.ataque * default_char[tipo]['skill list'][claves[skill_select]]['mult'] - otro.defensa // 2) * 0.5, 0))

                elif default_char[tipo]['skill list'][claves[skill_select]]['affinity'] == "healing": #Caso de tener una skill que cura en vez de hacer daño
                    dmg = 0
                    heal = random.randint(100,150)
                    self.hp += heal
                    self.mp -= default_char[tipo]['skill list'][claves[skill_select]]['cost']

                else:
                    dmg = int(round(max(0,self.ataque * default_char[tipo]['skill list'][claves[skill_select]]['mult'] - otro.defensa // 2),0))
                    self.mp -= default_char[tipo]['skill list'][claves[skill_select]]['cost']
            turno +=1
            
        
        otro.hp -= dmg
        if dmg > 0:
            print(f" {self.nombre} ataca a {otro.nombre} causando {dmg} de daño!")
        else:
            print(f"{self.nombre} se cura {heal} hp!") #En caso de curación
        turno +=1
        time.sleep(0.8)
        if otro.hp <= 0:
            otro.hp = 0
            print(f" {otro.nombre} ha sido derrotado!")
        return otro
    
    def __add__(self, exp_ganada):
        
        self.exp += exp_ganada
        print(f" {self.nombre} gana {exp_ganada} puntos de experiencia!")
        if self.exp >= 100:
            self.subir_nivel()
        return self
    
    def subir_nivel(self):
        self.nivel += 1
        self.exp = 0
        self.ataque = int(self.ataque * 1.1)
        self.defensa = int(self.defensa * 1.1)
        self.hp = int(self.hp * 1.1)
        self.mp = int(self.mp * 1.1)
        print(f" {self.nombre} ha subido al nivel {self.nivel}!")
        time.sleep(0.7)
    
    def guardar(self):
        return {"nombre" : self.nombre, "tipo" : self.tipo, "hp" : self.hp, "mp": self.mp, "ataque" : self.ataque, "defensa" : self.defensa, "nivel" : self.nivel, "exp" : self.exp}

class Enemy:
    def __init__(self, nombre, bicho, hp, ataque, defensa, affinity):
        self.nombre = nombre
        self.bicho = bicho
        self.hp = hp
        self.ataque = ataque
        self.defensa = defensa
        self.affinity = affinity

    def __str__(self):
        return f"{self.nombre}, {self.bicho}, {self.hp} hp , {self.ataque} ataque, {self.defensa} defensa, {self.affinity}"
    
    def __sub__(self, otro):  #Turno del enemigo
        en_act = int(random.randint(1,3)) #Acción que toma el enemigo
        if en_act == 1 or en_act == 2:
            print(f"{self.nombre} te ataca!")
            edmg = int(round(max(0,self.ataque - otro.defensa // 2),0))
        elif en_act == 3:
            eskill = random.randint(1,3)
            if eskill == 1:
                edmg = int(round(max(0, self.ataque *1.4 - otro.defensa),0))
                print(f"{self.nombre} se lanza contra ti!")

            elif eskill == 2:
                edmg = int(round(max(0,self.ataque - otro.defensa //1.5),0))
                print(f"{self.nombre} te lanza una piedra!")
            
            elif eskill == 3:
                edmg = int(round(max(0, self.ataque * 2.5),0))
                print(f"{self.nombre} te lanza un hechizo!")
        time.sleep(0.8)
        otro.hp -= edmg
        print(f"{otro.nombre} ha recibido {edmg} daño!")
        time.sleep(0.5)

def enemy_gen(): #genera el enemigo contra el que luchas de una lista de enemigos posibles
    roll = random.randint(1,4)
    if roll == 1:
        bicho = "goblin"
        ename_list = ["Goblino", "Gerber"]
        ename = random.choice(ename_list)
    elif roll == 2:
        bicho = "skeleton"
        ename_list = ["sans", "papyrus"]
        ename = random.choice(ename_list)
    elif roll == 3: 
        bicho = "cultist"
        ename_list = ["Brad", "Gabriel"]
        ename = random.choice(ename_list)
    elif roll == 4:
        bicho = "plant"
        ename_list = ["piranha plant", "Carnivorous plant"]
        ename = random.choice(ename_list)

    return Enemy(ename, bicho, enemy_roster[bicho]["hp"], enemy_roster[bicho]["ataque"],enemy_roster[bicho]["defensa"], enemy_roster[bicho]['affinity'])

def Boss(): #Genera el jefe final
    ename = "Cerberus"
    bicho ="cerberus"
    return Enemy(ename, bicho, enemy_roster[bicho]["hp"], enemy_roster[bicho]["ataque"],enemy_roster[bicho]["defensa"], enemy_roster[bicho]['affinity'])

#--------------------------------------
#json
#--------------------------------------

archivo = "Proyecto final programacion/FINAL/saves.json"
def guardar_datos(archivo, player): #Guarda los datos del jugador
    data = {
        "player": {
            "nombre": player.nombre,
            "tipo" : player.tipo,
            "hp" : player.hp,
            "mp" : player.mp,
            "ataque" : player.ataque,
            "defensa" : player.defensa,
            "lvl" : player.nivel,
            "exp" : player.exp
        }
    }

    with open(archivo, "w") as f:
        json.dump(data,f)
    print(f"Partida guardada! en {archivo}")

def cargar_datos(archivo):
    with open(archivo, "r") as f:
        data = json.load(f)
    player = Char(
    data["player"]["nombre"], 
    data["player"]["tipo"], 
    data["player"]["hp"], 
    data["player"]["mp"], 
    data["player"]["ataque"], 
    data["player"]["defensa"]
    )

    print("partida cargada")
    return player

a = input("cargar partida?  (s/n)     ") #En caso de querer crear un personaje nuevo, pulsa n, si quieres usar uno ya guardado, s

if a == "s":
    cargar_datos(archivo)
    with open(archivo, "r") as f:
        data = json.load(f)
    player = Char(
        data["player"]["nombre"], 
        data["player"]["tipo"], 
        data["player"]["hp"], 
        data["player"]["mp"], 
        data["player"]["ataque"], 
        data["player"]["defensa"]
        )
    tipo = player.tipo
else: #En caso de nuevo personaje, play intro

    print("Te despiertas en una mazmorra oscura, lo único que puedes sentir es el olor del fuego y sangre")
    time.sleep(0.8)
    print("No recuerdas cómo llegaste aquí, pero si recuerdas...")
    time.sleep(0.8)

    tipo = int(input("Tu profesión \n1) Mago \n2) Bailarín \n3) Asesino \n4) Caballero    "))
    time.sleep(0.8)
    nombre = input("También recuerdas que tu nombre es...    ")
    time.sleep(0.8)
    if tipo == 1:
        tipo = "mage"
        player = Char(nombre, tipo, default_char[tipo]["hp"],default_char[tipo]["mp"],default_char[tipo]["ataque"],default_char[tipo]["defensa"])
    elif tipo == 2:
        tipo = "dancer"
        player = Char(nombre, tipo, default_char[tipo]["hp"],default_char[tipo]["mp"],default_char[tipo]["ataque"],default_char[tipo]["defensa"])
    elif tipo == 3:
        tipo = "assasin"
        player = Char(nombre, tipo, default_char[tipo]["hp"],default_char[tipo]["mp"],default_char[tipo]["ataque"],default_char[tipo]["defensa"])
    else:
        tipo = "knight"
        player = Char(nombre, tipo, default_char[tipo]["hp"],default_char[tipo]["mp"],default_char[tipo]["ataque"],default_char[tipo]["defensa"])


#----------------------------------------------------
#dungeon
#----------------------------------------------------

def encontrar_posiciones(lab):
    pos_p = None
    monstruos = []

    filas = len(lab)
    columnas = len(lab[0])

    for i in range(filas):
        for j in range(columnas):
            if lab[i][j] == "P":
                pos_p = (i, j)
            elif lab[i][j] == "M":
                monstruos.append((i, j))

    return pos_p, monstruos




def imprimir_laberinto(lab):
    for fila in lab:
        linea = ""
        for elemento in fila:
            if elemento == 1:
                linea += GRIS + "1 " + RESET
            elif elemento == "P":
                linea += VERDE + "P " + RESET
            elif elemento == "M":
                linea += ROJO + "M " + RESET
            elif elemento == "B":
                linea += ROJO + "B " + RESET
            elif elemento == "C":
                linea += MAGENTA + "C " + RESET
            elif elemento == 4:
                linea += AMARILLO + "4 " + RESET
            elif elemento == 5:
                linea += AZUL + "5 " + RESET
            else:
                linea += BLANCO + str(elemento) + " " + RESET
        print(linea)
    print()

laby = 1
if laby == 1:
    lab = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,"C","M",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,"C",1,0,0,0,0,0,0,0,0,1,0,0,0,0,"M",0,0,0,1],
        [1,"M",0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1],
        [1,0,0,0,0,1,0,"M",0,0,0,0,0,0,"M",0,0,0,0,0,1],
        [1,5,0,0,"M",0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1,"M",1,0,0,0,1,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
        [1,0,0,"M",0,0,0,0,"M",0,0,0,"M",0,0,0,0,0,0,0,1],
        [1,0,0,0,1,0,0,0,1,0,0,4,1,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,"M",0,0,1],
        [1,0,0,0,"M",0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
        [1,0,0,0,1,1,0,0,0,"M",0,0,0,0,0,"M",0,0,0,0,1],
        [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,1,1,"M",0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1],
        [1,1,1,0,0,0,0,0,0,1,"P",1,0,0,1,0,0,"M","C",1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    level = 1



(pos_i, pos_j), monstruos = encontrar_posiciones(lab)

turno = 0  

movs = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1)
}
    

#-------------------------------------------------
#juego
#-------------------------------------------------



jugando = True
battle = False
numb_of_mp = 2
numb_of_potions = 2

print("Estás rodeado de monstruos    (M)   , pero intuyes que hay una manera de salir...")
print("Hay escaleras hacia arriba  (4)")
print("Escaleras hacia abajo  (5)")
print("Y cofres con cosas!    (C)")
time.sleep(2)
imprimir_laberinto(lab)

while jugando:
    
    mov = input("Mover (w/a/s/d) o 'q' para salir, i para inventario, g para guardar: ")

    if mov == "q":
        print("Fin del juego.")
        jugando = False

    elif mov == "g":
        guardar_datos(archivo,player)
        

    elif mov == "i":
        inventario = True
        while inventario:
            inv_menu = int(input("1-- items  2-- status "))

            if inv_menu == 1:
                print("-----ITEMS-----")
                print(f"1-- Potion x{numb_of_potions}\n2-- MP vial x{numb_of_mp}")
                time.sleep(0.4)
                choir = int(input("What choose?  "))

                if choir == 1:
                    numb_of_potions -=1
                    player.hp += 100
                    print("Te tomas una poición... Recuperas 100 hp!")
                    #restores X hp
                elif choir == 2:
                    numb_of_mp -= 1
                    player.mp += 100
                    print("Te tomas un mp vial... Recuperas 100 mp!")
                    #restores Y mp
                else:
                    pass
                time.sleep(0.8)
            
            else:
                print(str(player))
                
                time.sleep(0.8)

            inventario = False
        time.sleep(0.5)
        imprimir_laberinto(lab)
        
    else:
        
        try:
            di, dj = movs[mov]
            movimiento_valido = True
        except KeyError:
            movimiento_valido = False

        if movimiento_valido:
            ni = pos_i + di
            nj = pos_j + dj
            casilla = lab[ni][nj]

            # 1) Chocar contra pared       revise this ig
            if casilla == 1:
                
                print("Has chocado contra una pared.")
                


            elif casilla == 4: #stairs up
                laby += 1
                lab[pos_i][pos_j] = 0
                temp = ni,nj
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj
                
                
                if laby == 2:
                    level = 2
                    lab = [
                                        
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,1,1,1,1,1,1,"M",0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,"C",1,1,1,1,0,1,1,1,1,1,0,1,0,1],
                    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,"M",1,0,1],
                    [1,4,1,0,0,0,"M",0,0,0,0,0,1,1,1,1,1,0,1,0,1],
                    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
                    [1,1,0,0,0,1,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1],
                    [1,0,0,0,1,1,1,0,0,0,1,"M",0,0,1,0,1,0,1,0,1],
                    [1,0,0,"M",0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,"C",1],
                    [1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,1,1,1,1],
                    [1,0,0,0,0,0,0,"M",0,0,0,0,1,0,1,0,0,0,0,0,1],
                    [1,0,0,0,1,0,0,0,1,0,5,0,1,0,1,0,0,0,1,0,1],
                    [1,0,0,1,1,1,0,0,0,1,1,1,0,0,1,0,"M",1,1,0,1],
                    [1,0,0,0,1,0,"M",0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,1],
                    [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,0,1,0,0,0,"M",0,0,1,1,1,1,0,0,0,1],
                    [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1],
                    [1,0,"C",1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,"C",1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

                ]
                    

                elif laby == 1:
                    level = 1 #to know where on earth you are
                    lab = [
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,"C","M",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,"C",1,0,0,0,0,0,0,0,0,1,0,0,0,0,"M",0,0,0,1],
                    [1,"M",0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1],
                    [1,0,0,0,0,1,0,"M",0,0,0,0,0,0,"M",0,0,0,0,0,1],
                    [1,5,0,0,"M",0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
                    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1,"M",1,0,0,0,1,1,1,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                    [1,0,0,"M",0,0,0,0,"M",0,0,0,"M",0,0,0,0,0,0,0,1],
                    [1,0,0,0,1,0,0,0,1,0,0,4,1,0,0,0,0,0,0,0,1],
                    [1,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1],
                    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,"M",0,0,1],
                    [1,0,0,0,"M",0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
                    [1,0,0,0,1,1,0,0,0,"M",0,0,0,0,0,"M",0,0,0,0,1],
                    [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                    [1,0,1,1,"M",0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1],
                    [1,1,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,"M","C",1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]
                    
                elif laby == 3:
                    level = 3
                    lab = [
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,1,"C",1,0,0,1,"C",1,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"B",0,1],
                    [1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1],
                    [1,0,0,1,"C",1,0,0,1,"C",1,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]

                    
                lab[pos_i][pos_j] = 0    #this is needed cuz if not it doesn't initally show the player character when exiting/entering a room
                temp = ni,nj
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj
                
                    

            elif casilla == 5:      #stairs down
                laby -= 1
                lab[pos_i][pos_j] = 0
                temp = ni,nj
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj

                if laby == 1:
                    level = 1 #to know where you are
                    lab = [
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,"C","M",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,"C",1,0,0,0,0,0,0,0,0,1,0,0,0,0,"M",0,0,0,1],
                    [1,"M",0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1],
                    [1,0,0,0,0,1,0,"M",0,0,0,0,0,0,"M",0,0,0,0,0,1],
                    [1,5,0,0,"M",0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
                    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1,"M",1,0,0,0,1,1,1,0,0,1],
                    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                    [1,0,0,"M",0,0,0,0,"M",0,0,0,"M",0,0,0,0,0,0,0,1],
                    [1,0,0,0,1,0,0,0,1,0,0,4,1,0,0,0,0,0,0,0,1],
                    [1,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1],
                    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,"M",0,0,1],
                    [1,0,0,0,"M",0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
                    [1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1],
                    [1,0,0,0,1,1,0,0,0,"M",0,0,0,0,0,"M",0,0,0,0,1],
                    [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                    [1,0,1,1,"M",0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1],
                    [1,1,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,"M","C",1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                ]
                    
                elif laby == 0:
                    level = 0
                    lab = [
                        [1,1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,0,1],
                        [1,0,0,1,1,1,0,0,1],
                        [1,0,"M",0,"C",0,1,0,1],
                        [1,0,1,0,"C",0,"M",0,1],
                        [1,0,0,1,1,1,0,0,1],
                        [1,0,4,0,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1,1],
                    ]

                elif laby == 2:
                    level = 2
                    lab = [
                                        
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,1,1,1,1,1,1,"M",0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,"C",1,1,1,1,0,1,1,1,1,1,0,1,0,1],
                        [1,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,"M",1,0,1],
                        [1,4,1,0,0,0,"M",0,0,0,0,0,1,1,1,1,1,0,1,0,1],
                        [1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
                        [1,1,0,0,0,1,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1],
                        [1,0,0,0,1,1,1,0,0,0,1,"M",0,0,1,0,1,0,1,0,1],
                        [1,0,0,"M",0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,"C",1],
                        [1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,1,1,1,1],
                        [1,0,0,0,0,0,0,"M",0,0,0,0,1,0,1,0,0,0,0,0,1],
                        [1,0,0,0,1,0,0,0,1,0,5,0,1,0,1,0,0,0,1,0,1],
                        [1,0,0,1,1,1,0,0,0,1,1,1,0,0,1,0,"M",1,1,0,1],
                        [1,0,0,0,1,0,"M",0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,1],
                        [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,1,1,0,0,1,0,0,0,"M",0,0,1,1,1,1,0,0,0,1],
                        [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1],
                        [1,0,"C",1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,"C",1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

                    ]

                lab[pos_i][pos_j] = 0  #this is needed cuz if not it doesn't initally show the player character when exiting/entering a room
                temp = ni,nj
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj
                    
            elif casilla == "M": #initiates battle vs enemy
                battle = True
                enem = enemy_gen()
                print(f"Te topaste con {enem.nombre}!")
                time.sleep(0.8)
                #makes it so after landing on enemy tile it turns into zero
                lab[pos_i][pos_j] = 0
                temp = ni,nj
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj

                while battle:  #here you put all the battle mechanics
                    
                    turno = 1
                    print(f"{player.nombre}   con   {player.hp} hp --- {player.mp} mp    VS     {enem.nombre}  --- {enem.hp} Hp")
                    choice = input("Que quieres? 1-- atacar   2-- inventario   3--- analizar  ")

                    if choice == "1":
                        player - enem

                    elif choice == "2":
                        print(f"-----ITEMS-----\n 1) Potion x{numb_of_potions} \n2) Mp vial x{numb_of_mp}")
                        inv = input("What do you want to use?   ")
                        if inv == "1":
                            player.hp += 100
                            numb_of_potions -=1
                            print("Te tomas una poción, te curas 100 hp!")
                        
                        elif inv == "2":
                            player.mp += 100
                            numb_of_mp -=1
                            print("Consumes un Mp vial, recuperas 100 mp!")
                        time.sleep(0.8)

                        

                    elif choice == "3":
                        print(f"Te paras un segundo a analizar a {enem.nombre}!")
                        time.sleep(1)
                        for analisis in enemy_roster[enem.bicho]['affinity']:
                            print(analisis,":", enemy_roster[enem.bicho]['affinity'][analisis])
                        time.sleep(0.8)

                    else:
                        print("You tripped and the enemy took advantage!")
                        time.sleep(0.8)

                    if enem.hp >0:
                        enem - player

                    if enem.hp <=0:
                        exp = random.randint(50,70)
                        player + exp
                        print(f"You win! You earned {exp} EXP!")
                        battle = False
                    turno +=1
                casilla = 0
                    
            
            elif casilla == "C":
                item_roll = random.randint(1,3)

                if item_roll == 1:
                    numb_of_mp +=1
                    print("You got an mp bottle!")
                elif item_roll == 2:
                    numb_of_potions +=1
                    print("You got a potion!")
                else:
                    numb_of_mp +=1
                    numb_of_potions +=1
                    print("lucky! got a potion and mp vial!")
                time.sleep(0.8)
                
                lab[pos_i][pos_j] = 0 #la casilla deja de ser especial y se convierte en casilla normal
                temp = ni,nj
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj
                
            elif casilla == "B":
                boss_battle = True
                enem = Boss()  
                print(f"{player.nombre}, he estado esperando tu llegada")
                time.sleep(0.8)
                print("Bienvenido a la salida de Tártarus, la torre del infierno")
                time.sleep(0.8)
                print("Siento que tenga que ser así, pero no puedo dejar que nadie salga de aquí")
                time.sleep(0.8)
                print("En garde!")
                time.sleep(0.8)
                print("Comienza la batalla contra Cerberus!")
                time.sleep(0.8)
                #makes it so after landing on enemy tile it turns into zero
                lab[pos_i][pos_j] = 0
                temp = ni,nj
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj

                while boss_battle:  
                    
                    turno = 1
                    print(f"{player.nombre}   con   {player.hp} hp --- {player.mp} mp    VS     {enem.nombre}  --- {enem.hp} Hp")
                    choice = input("Que quieres? 1-- atacar   2-- inventario   3--- analizar  ")

                    if choice == "1":
                        player - enem

                    elif choice == "2":
                        print(f"-----ITEMS-----\n 1) Potion x{numb_of_potions} \n2) Mp vial x{numb_of_mp}")
                        inv = input("What do you want to use?   ")
                        if inv == "1":
                            player.hp += 100
                            numb_of_potions -=1
                            print("Te tomas una poción, te curas 100 hp!")
                        
                        elif inv == "2":
                            player.mp += 100
                            numb_of_mp -=1
                            print("Consumes un Mp vial, recuperas 100 mp!")
                        
                        else:
                            print("Te olvidaste que querías usar y te atacan!")
                        time.sleep(0.8)

                        

                    elif choice == "3":
                        print(f"Te paras un segundo a analizar a {enem.nombre}!")
                        time.sleep(1)
                        for analisis in enemy_roster[enem.bicho]['affinity']:
                            print(analisis, enemy_roster[enem.bicho]['affinity'][analisis])
                        time.sleep(0.8)

                    else:
                        print("You tripped and the enemy took advantage!")
                        time.sleep(0.8)

                    if enem.hp >0:
                        enem - player

                    if enem.hp <=0:
                        exp = random.randint(500,700)
                        player + exp
                        print(f"You win! You earned {exp} EXP!")
                        boss_battle = False
                        cerberus_dead = True
                        print("me derrotaste, supongo que mereces salir de esta torre infernal")
                        jugando = False
                        time.sleep(1.5)
                    turno +=1
                casilla = 0  



                
            
            # 4) Casilla normal
            else:
                lab[pos_i][pos_j] = 0
                lab[ni][nj] = "P"
                pos_i, pos_j = ni, nj
                #imprimir_laberinto(lab)

            time.sleep(0.1)
            

            if battle == False or boss_battle == False:
                print(f"Level {level}")
                imprimir_laberinto(lab)

            elif cerberus_dead:
                print("Has conseguido escapar de tartarus!")
            
            
                
            

        else:
            print("Movimiento no válido.")