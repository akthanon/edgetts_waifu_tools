import time
import random
import os
import pygame

# Inicializa Pygame
pygame.init()

# Configura la pantalla
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Aventura en Niria')

# Define los nombres de las zonas
directorios = ["camino_inicio", "camino_norte", "camino_sur", "camino_este", "camino_oeste",
         "camino_lago", "camino_desierto", "camino_piramide", "camino_vista", "camino_santuario", "camino_normal"]

# Define la ruta principal de las imágenes
ruta_principal = 'imagenes'

def cargar_imagen(zona, indice):
    """
    Carga y devuelve una imagen basada en la zona y el índice.
    """
    ruta_imagen = os.path.join(ruta_principal, zona, f'{indice}.jfif')
    if os.path.exists(ruta_imagen):
        return pygame.image.load(ruta_imagen)
    else:
        print(f"Imagen no encontrada: {ruta_imagen}")
        return None

def mostrar_texto_pygame(texto, posicion, tamano=30, color=(255, 255, 255)):
    """
    Muestra texto en la pantalla de Pygame.
    """
    fuente = pygame.font.Font(None, tamano)
    superficie_texto = fuente.render(texto, True, color)
    screen.blit(superficie_texto, posicion)
    pygame.display.flip()
    print(texto)

def funcion_imagenes(zona, indice, texto=""):
    """
    Muestra la imagen seleccionada en la pantalla y opcionalmente texto debajo.
    """
    imagen = cargar_imagen(zona, indice)
    if imagen:
        screen.fill((0, 0, 0))  # Limpia la pantalla
        ancho_pantalla, alto_pantalla = screen.get_size()
        margen_inferior = 50  # Espacio reservado para el texto
        alto_imagen_max = alto_pantalla - margen_inferior

        # Calcula el nuevo tamaño de la imagen
        imagen = pygame.transform.scale(imagen, (ancho_pantalla, alto_imagen_max))
        
        screen.blit(imagen, (0, 0))  # Dibuja la imagen en la esquina superior izquierda
        
        if texto:
            mostrar_texto_pygame(texto, (10, alto_imagen_max + 10))  # Muestra el texto debajo de la imagen
        
        pygame.display.flip()  # Actualiza la pantalla
    else:
        print(f"No se pudo cargar la imagen para {zona} con índice {indice}")

class Enemigo:
    def __init__(self, nombre, vida, ataques, velocidad):
        self.nombre = nombre
        self.vida = vida
        self.ataques = ataques
        self.velocidad = velocidad

    def atacar(self):
        ataque = random.choice(self.ataques)
        return f"{self.nombre} usa {ataque} para atacar."

    def recibir_danio(self, danio):
        self.vida -= danio
        if self.vida <= 0:
            return f"{self.nombre} ha sido derrotado."
        else:
            return f"{self.nombre} ha recibido {danio} de daño y tiene {self.vida} puntos de vida restantes."

    def escapar(self):
        chance = random.random()
        if chance < self.velocidad:
            return f"{self.nombre} ha escapado con éxito."
        else:
            return f"{self.nombre} no pudo escapar y sigue en la batalla."

    def usar_item(self, item):
        return f"{self.nombre} usa el item {item}."

# Enemigos
enemigo_orco = Enemigo("Orco", 100, ["Golpe fuerte", "Gruñido aterrador", "Ataque feroz"], 0.3)


def funcion_combate(enemigo):
    print("\nInicia un combate con: "+enemigo.nombre)
    time.sleep(refresh)
    print("Ganaste el combate.")
    time.sleep(refresh)

def dexto(texto,timp):
    for i in range(len(texto)):
        print(str(texto[i]),end="")
        time.sleep(timp)
    print("")
    
def iniciar_aventura():
    global x
    global y
    global terminar
    global mostrar_zona
    global zonas
    global coordenadas
    os.system('cls')
    funcion_imagenes(zona="camino_inicio", indice=0, texto=">¡Bienvenido a la Aventura titulada: 20 Natural, Aventuras en Niria!")
    time.sleep(refresh*2)
    funcion_imagenes(zona="camino_inicio", indice=1, texto=">Estás en un bosque misterioso de Kanta. No tienes idea de cómo llegaste aquí.")
    time.sleep(refresh*2)
    funcion_imagenes(zona="camino_inicio", indice=2, texto=">Frente a ti, ves cuatro caminos. ¿Cuál eliges?")
    time.sleep(refresh*2)
    os.system('cls')
    while terminar==False:
        #mostrar_mapa()
        funcion_imagenes(zona="camino_inicio", indice=3, texto=">Opciones: Norte, Sur, Este, Oeste, Explorar, Información")
        eleccion = random.choice(["1", "2", "3", "4", "5", "6","51","52"])
        
        time.sleep(refresh)
        print("")
        if eleccion == "1":
            print("Elegiste ir al Norte.")
        elif eleccion == "2":
            print("Elegiste ir al Sur.")
        elif eleccion == "3":
            print("Elegiste ir al Este.")
        elif eleccion == "4":
            print("Elegiste ir al Oeste.")
        elif eleccion == "5" or eleccion=="51" or eleccion=="52":
            print("Elegiste Explorar.")
        elif eleccion == "6":
            print("Elegiste obtener Información.")
        time.sleep(refresh)
        os.system('cls')
        xtemp=x
        ytemp=y
        
        if eleccion == "1":
            y=y-1
        elif eleccion == "2":
            y=y+1
        elif eleccion == "3":
            x=x+1
        elif eleccion == "4":
            x=x-1
        elif eleccion=="5" or eleccion=="51" or eleccion=="52":
            mostrar_zona=True
        elif eleccion=="6":
            mostrar_inventario()


        avanzado=False
        indis=0
        for funcion in zonas:
            cordis=coordenadas[indis]
            cx=cordis[0]
            cy=cordis[1]
            if x==cx and y==cy:
                funcion()
                avanzado=True
            indis=indis+1
        if avanzado==False:
            print("No hay camino en esa dirección. Elige Otro camino.")
            x=xtemp
            y=ytemp
        mostrar_zona=False    
    print("HAZ MUERTO!!! O__o")
    time.sleep(5)
    os.system('cls')

def mostrar_mapa():
    global coordenadas
    global x
    global y
    print("\n****Mapa****\n")
    max_x = max(coordenada[0] for coordenada in coordenadas)
    max_y = max(coordenada[1] for coordenada in coordenadas)
    min_x = min(coordenada[0] for coordenada in coordenadas)
    min_y = min(coordenada[1] for coordenada in coordenadas)

    # Crea una cuadrícula de asteriscos
    grid = [[' * ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Marca las coordenadas con 'X' en la cuadrícula
    con=0
    actual_indice=coordenadas.index([x,y])
    for ux, uy in coordenadas:
        if con==actual_indice:
            grid[uy][ux] = ' O '
        else:
            grid[uy][ux] = ' X '
        con=con+1

    # Imprime la cuadrícula en pantalla
    for fila in grid:
        print(''.join(fila))
    #time.sleep(refresh)
    
    
def mostrar_inventario():

    print("\n****Inventario****\n")
    if len(inventario) == 0:
        print("*inventario vacio.")
    else:
        for item in inventario:
            print(f"- {item}")
    print("\ntienes "+str(dinero)+"$ murciemonedas")
    print("\n****Descripción****")
    time.sleep(refresh)
    

def camino_norte():
    global dinero
    global terminar
    if mostrar_zona==False:
        print("\nVisualisas un sendero.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("Caminas por un sendero estrecho y encuentras un cofre escondido.")
        time.sleep(refresh*2)
        print("¿Qué haces?")
        time.sleep(refresh*2)
        while True:
            print("\nOpciones:")
            print("1. Abrir el cofre.")
            print("2. Ignorar el cofre y seguir adelante.")
            eleccion = random.choice(["1", "2"])
            
            if eleccion == "1":
                releccion=random.choice(["1", "2", "3", "4"])
                if releccion == "1":              
                    print("\nDentro del cofre encuentras una gema preciosa con un valor de 500 murciemonedas. ¡Has tenido suerte!")
                    inventario.append("Gema")
                    dinero=dinero+500
                if releccion == "2":              
                    print("\nDentro del cofre encuentras una chanwich. ¡al menos no te moriras de hambre!")
                    inventario.append("Chanwich")
                if releccion == "3":              
                    print("\nEra un cofre trampa. ¡Te comió!")
                    inventario.append("Cabeza")
                    terminar=True
                if releccion == "4":              
                    print("\nDentro del cofre encuentras 1000 murciemonedas. ¡eres murciemillonario!")
                    inventario.append("Bolsa con dinero")
                    dinero=dinero+1000
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nDecides seguir adelante sin abrir el cofre.")
                time.sleep(refresh*2)
                break
        if terminar==False:
            print("Sigues avanzando y te encuentras con un leñador que te ofrece comida y refugio para la noche. Aceptas su amable oferta y descansas.")
            time.sleep(refresh*2)
            print("A la mañana siguiente, el leñador te da un mapa que te muestra el camino de regreso a casa.")
            time.sleep(refresh*2)
            print("¡Has completado la primera parte de la aventura!")
            mostrar_inventario()
            time.sleep(refresh*2)

def camino_sur():
    global llave_oeste
    if mostrar_zona==False:
        print("\nVes un gran rio a lo lejos.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("Sigues el camino y llegas al río.")
        time.sleep(refresh*2)
        print("¿Qué haces?")
        time.sleep(refresh*2)
        
        while True:
            print("\nOpciones:")
            print("1. Intentar cruzar el río a nado.")
            print("2. Buscar un puente cercano.")
            eleccion = random.choice(["1", "2"])
            
            if eleccion == "1":
                print("\nIntentas cruzar el río a nado, pero la corriente es demasiado fuerte y te arrastra. Game over.")
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nEncuentras un puente cercano y cruzas el río con seguridad.")
                time.sleep(refresh*2)
                break

        print("Del otro lado del río, encuentras una cueva misteriosa. ¿Deseas explorarla?")
        time.sleep(refresh*2)
        
        while True:
            print("\nOpciones:")
            print("1. Entrar en la cueva.")
            print("2. Continuar por el camino.")
            eleccion = random.choice(["1", "2"])
            
            if eleccion == "1":
                print("\nDentro de la cueva, encuentras tesoros antiguos y una llave secreta, además decides quedarte un tiempo explorándola.")
                time.sleep(refresh*2)
                print("Cuando finalmente sales de la cueva, te das cuenta de que ha pasado mucho tiempo.")
                time.sleep(refresh*2)
                print("Decides continuar tu aventura con tesoros en tu mochila.")
                inventario.append("Tesoro antiguo")
                inventario.append("Llave Oeste")
                llave_oeste=True
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nDecides continuar por el camino y no entras en la cueva.")
                time.sleep(refresh*2)
                break

        print("Sigues caminando por el bosque y encuentras una bifurcación. Uno de los caminos parece llevar a un pueblo. ¿Qué haces?")
        time.sleep(refresh*2)

        while True:
            print("\nOpciones:")
            print("1. Tomar el camino hacia el pueblo.")
            print("2. Tomar el otro camino.")
            eleccion = random.choice(["1", "2"])
            
            if eleccion == "1":
                print("\nTe diriges hacia el pueblo en busca de ayuda y refugio.")
                time.sleep(refresh*2)
                print("La gente del pueblo te da la bienvenida y te ofrece un lugar donde quedarte. Continuarás tu aventura mañana.")
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nOptas por tomar el otro camino, curioso por lo que te deparará.")
                time.sleep(refresh*2)
                break
        

def camino_este():
    if mostrar_zona==False:
        print("\nLlegaste a un camino empinado y a lo lejos visualizas una colina.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("Caminas por ese camino y llegas a la colina.")
        time.sleep(refresh*2)
        print("Desde la cima de la colina, ves un pueblo en la distancia.")
        time.sleep(refresh*2)
        print("¿Qué haces?")
        time.sleep(refresh*2)
        
        while True:
            print("\nOpciones:")
            print("1. Descender la colina y dirigirte al pueblo.")
            print("2. Explorar la colina en busca de tesoros ocultos.")
            eleccion = random.choice(["1", "2"])
            
            if eleccion == "1":
                print("\nDeslizas por la colina y te diriges al pueblo en busca de ayuda.")
                time.sleep(refresh*2)
                print("La gente del pueblo te da la bienvenida y te ofrece refugio. Continuarás tu aventura mañana.")
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nDecides explorar la colina, pero no encuentras tesoros. Finalmente, te diriges al pueblo.")
                time.sleep(refresh*2)
                print("La gente del pueblo te da la bienvenida y te ofrece refugio. Continuarás tu aventura mañana.")
                time.sleep(refresh*2)
                break
    
def camino_oeste():
    global llave_oeste
    if mostrar_zona==False:
        print("\nObservas una cabaña en la zona...")
        time.sleep(refresh)
    if mostrar_zona==True:
        print("Te acercas a la cabaña donde observas una pueta secreta.")
        time.sleep(refresh)
        while True:
            print("\nOpciones:")
            print("1. Intentar abrir la puerta.")
            print("2. Tocar la puerta.")
            eleccion = random.choice(["1", "2"])
                
            if eleccion == "1":
                print("\nIntentas abrir la puerta.")
                time.sleep(refresh*2)
                if llave_oeste==True:
                    print("Abres la puerta con la llave que tienes en tu inventario y observas que no hay nadie.")
                elif llave_oeste==False:
                    print("Intentas abrir la puerta pero notas que está cerrada con llave.")
                    time.sleep(refresh*2)
                    print("No pasa nada.")
                time.sleep(refresh*2)    
                break
            elif eleccion == "2":
                print("\nDecides tocar la puerta.")
                time.sleep(refresh*2)
                print("No pasa nada.")
                time.sleep(refresh*2)
                break

def camino_inicio():
    if mostrar_zona==False:
        print("\nTe encuentras en el punto de inicio.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        v_gerundio=gerundio[random.randint(0,len(gerundio))-1]
        animal=animales[random.randint(0,len(animales))-1]
        print("Estás "+v_gerundio+" "+animal)
        time.sleep(refresh*2)


def camino_lago():
    if mostrar_zona==False:
        print("\nEstás caminando a lo largo de un serpenteante camino.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("Observas la longitud del camino, parece interminable.")
        time.sleep(refresh*2)
        print("\n¿Qué decides hacer?")
        time.sleep(refresh*2)
        while True:
            print("\nOpciones:")
            print("1. Continuar caminando.")
            print("2. Descansar un momento.")
            print("3. Intentar encontrar un atajo.")
            eleccion = random.choice(["1", "2", "3"])
            if eleccion == "1":
                print("\nDecides seguir caminando.")
                break
            elif eleccion == "2":
                print("\nTe detienes a descansar un momento.")
                time.sleep(refresh*2)
                print("Te sientes mejor y continúas.")
                time.sleep(refresh*2)
                break
            elif eleccion == "3":
                print("\nBuscas un atajo, pero no encuentras ninguno.")
                time.sleep(refresh*2)
                print("Decides seguir por el camino principal.")
                time.sleep(refresh*2)
                break


def camino_desierto():
    if mostrar_zona==False:
        print("\nTe adentras en un vasto desierto.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("El calor del desierto te abruma.")
        time.sleep(refresh*2)
        print("\n¿Qué decides hacer?")
        time.sleep(refresh*2)
        while True:
            print("\nOpciones:")
            print("1. Continuar caminando.")
            print("2. Buscar sombra y descansar.")
            print("3. Intentar orientarte usando el sol.")
            eleccion = random.choice(["1", "2", "3"])
            if eleccion == "1":
                print("\nDecides seguir caminando bajo el sol ardiente.")
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nBuscas una pequeña sombra y descansas por un momento.")
                time.sleep(refresh*2)
                print("Recuperas algo de energía y continúas tu viaje.")
                time.sleep(refresh*2)
                break
            elif eleccion == "3":
                print("\nIntentas orientarte usando la posición del sol.")
                time.sleep(refresh*2)
                print("Con cuidado, decides seguir en una dirección determinada.")
                time.sleep(refresh*2)
                break

def camino_piramide():
    if mostrar_zona==False:
        print("\nTe encuentras frente a una impresionante pirámide.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("Observas la majestuosidad de la pirámide.")
        time.sleep(refresh*2)
        print("\n¿Qué decides hacer?")
        time.sleep(refresh*2)
        while True:
            print("\nOpciones:")
            print("1. Entrar en la pirámide.")
            print("2. Explorar los alrededores.")
            print("3. Tomar fotos y seguir adelante.")
            eleccion = random.choice(["1", "2", "3"])
            if eleccion == "1":
                print("\nDecides entrar en la pirámide y explorar su interior.")
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nExploras los alrededores de la pirámide en busca de tesoros.")
                time.sleep(refresh*2)
                print("Encuentras algunos artefactos interesantes cerca de la entrada.")
                break
            elif eleccion == "3":
                print("\nTomas algunas fotos de la pirámide y continúas tu viaje.")
                time.sleep(refresh*2)
                print("No quieres perder demasiado tiempo aquí.")
                time.sleep(refresh*2)
                break

def camino_vista():
    if mostrar_zona==False:
        print("\nHaz encontrado un camino con una hermosa vista.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("La vista es muy hermosa.")
        time.sleep(refresh*2)
        print("\n¿Qué decides hacer?")
        time.sleep(refresh*2)
        while True:
            print("\nOpciones:")
            print("1. Detenerte y disfrutar de la vista por un rato.")
            print("2. Sacar tu cámara y tomar algunas fotos.")
            print("3. Continuar tu camino sin detenerte.")
            eleccion = random.choice(["1", "2", "3"])
            if eleccion == "1":
                print("\nTe sientas en un lugar tranquilo y tomas un merecido descanso.")
                time.sleep(refresh*2)
                print("Quieres aprovechar este momento para relajarte y apreciar la belleza del paisaje.")
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nSacas tu cámara y tomas algunas fotos del paisaje.")
                time.sleep(refresh*2)
                print("Quieres conservar estos recuerdos para siempre.")
                time.sleep(refresh*2)
                break
            elif eleccion == "3":
                print("\nDecides continuar tu camino, dejando atrás esta vista impresionante.")
                time.sleep(refresh*2)
                print("Aunque te gustaría quedarte más tiempo, tienes una aventura que continuar.")
                time.sleep(refresh*2)
                break

def camino_santuario():
    if mostrar_zona==False:
        print("\nA lo lejos, ves un antiguo santuario.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("Te acercas al santuario, sintiendo una extraña paz en el aire.")
        time.sleep(refresh*2)
        print("\n¿Qué decides hacer?")
        time.sleep(refresh*2)
        while True:
            print("\nOpciones:")
            print("1. Entrar en el santuario y explorarlo.")
            print("2. Observar el santuario desde lejos.")
            print("3. Continuar tu camino sin entrar.")
            eleccion = random.choice(["1", "2", "3"])
            if eleccion == "1":
                print("\nDecides entrar en el santuario y explorar su interior.")
                time.sleep(refresh*2)
                break
            elif eleccion == "2":
                print("\nPrefieres observar el santuario desde lejos, sin entrar.")
                time.sleep(refresh*2)
                print("No te sientes completamente cómodo con la idea de entrar ahora mismo.")
                time.sleep(refresh*2)
                break
            elif eleccion == "3":
                print("\nDecides continuar tu camino sin entrar en el santuario.")
                time.sleep(refresh*2)
                print("Aunque te intriga, tienes otros lugares que explorar antes.")
                time.sleep(refresh*2)
                break


def camino_normal():
    if mostrar_zona==False:
        print("\nUn camino normal.")
        time.sleep(refresh*2)
    if mostrar_zona==True:
        print("No hay nada interesante :C.")
        time.sleep(refresh*2)
        funcion_combate(enemigo_orco)


if __name__ == "__main__":
    refresh=1
    while True:

        gerundio= [
        "corrompiendo", "oliendo",
        "moviendo","amordazando","amarrando","mordizqueando",
        "atrayendo", "sacando",
        "aclarando", "venciendo",
        "despertando","extenuando",
        "haciendo","enriqueciendo","pintando",
        "jalando","jalando","besando","observar",
        "filmando","acariciando","llevando a nadar",
        "cocinando", "contrayendo", "perseguiendo", "mordiendo",
        "estacionando", "rompiendo", "partiendo",
        "pintando", "arrancando", "arrojando al foso","yendo a buscar"
        "escuchando","arrastrando","empollando",
        "limpiando", "moviendo", "sintiendo", "dando de comer", "dando apoyo a", "atormentando",
        "combatiendo", "extrangulando","yendo a vender",
        "teniendo", "repartiendo", "asesinando",
        "batiendo", "hechando a la cazuela", "partiendo","venciendo",
        "escogiendo", "recibiendo","acariciando",
        "donando", "excluyendo", "matando","yendo a jalar el cuello a",
        "conteniendo", "hirviendo", "escarbando", "viendo aplaudir",
        "paseando", "comprimiendo", "pelando","sacudiendo", 
        "obedeciendo","sacando a pasear"
        ]

        presente=[]
        pasado=[]
        animales = [
        "el camello", "el lobo", "el topo",
        "la liebre", "la pantera", "la gallina",
        "la tarántula",
        "la oveja", "el cerdo", "la iguana",
        "el búfalo", "el gusano", "el mapache",
        "el alce", "el escorpión", "el elefante",
        "el tlacuache", "el venado", "el oso",
        "la araña", "el rinoceronte", "la mula",
        "el orangután", "la rata", "la chita",
        "el avestruz", "el leopardo", "el gorila",
        "la serpiente", "el ganso", "el ratón",
        "el cocodrilo", "el tigre", "la anaconda",
        "el gallo", "la cucaracha", "el caballo",
        "el pingüino", "la cabra", "el jaguar",
        "la vaca", "la víbora", "el castor",
        "la rana", "el canguro", "el hámster",
        "el conejo", "el asno", "la lagartija",
        "el becerro", "el alacrán", "el mandril",
        "el armadillo", "el caimán", "el oso",
        "el camaleón", "la tortuga",
        "el koala", "la ardilla", "la hormiga",
        "el burro", "la jirafa", "el león",
        "el mono", "el chango", "el toro"
        ]

        # Inventario del jugador
        inventario = []
        zonas = [camino_inicio, camino_norte, camino_sur, camino_este, camino_oeste, camino_lago, camino_desierto, camino_piramide, camino_vista, camino_santuario]
        
        tx=random.randint(100,200)
        ty=random.randint(100,200)
        coordenadas=[[tx,ty]]

        normales=[camino_normal]*random.randint(0,len(zonas))

        
        for camino in normales:
            zonas.append(camino)

        
        random.shuffle(zonas)

        inicio_indice=zonas.index(camino_inicio)

        for i in range(len(zonas)-1):
            colocado=False
            newcor=[]
            while colocado==False:
                
                dire=random.randint(0,1)
                if len(coordenadas)>0:
                    ranindice=random.randint(0,len(coordenadas)-1)
                else:
                    ranindice=0
                rancor=coordenadas[ranindice]
                tx=rancor[0]
                ty=rancor[1]
                
                if dire==0:
                    ex=random.randint(-1,1)
                    tx=tx+ex
                elif dire==1:
                    ey=random.randint(-1,1)
                    ty=ty+ey
                newcor=[tx,ty]
                if not(newcor in coordenadas):
                    colocado=True
                    
            coordenadas.append(newcor)

            
        min_x = min(coordenada[0] for coordenada in coordenadas)
        min_y = min(coordenada[1] for coordenada in coordenadas)

        coordenadas_a_restar=[min_x,min_y]
            
        coordenadas = [[nx - coordenadas_a_restar[0], ny - coordenadas_a_restar[1]] for nx, ny in coordenadas]
        
        inicio_cords=coordenadas[inicio_indice]
        x=inicio_cords[0]
        y=inicio_cords[1]
        terminar=False
        dinero=0
        mostrar_zona=False
        #OBJETOS
        llave_oeste=False
        iniciar_aventura()
pygame.quit()

