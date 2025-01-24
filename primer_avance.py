# De los dados
# Los dados son dados usuales que están numerados del 1 al 6 (inclusive) y se lanzan
# dos dados una vez por cada turno.

import random

class Dados:
    def __init__(self):

        # Los valores de los dados se inicializan como None hasta que se lancen
        self.dado1 = None
        self.dado2 = None

    def lanzar(self):
        # Lanza dos dados, cada uno con valores aleatorios entre 1 y 6.
        self.dado1 = random.randint(1, 6)
        self.dado2 = random.randint(1, 6)
        return self.dado1, self.dado2

    def mostrar_resultado(self):
        # Muestra el resultado del lanzamiento de los dos dados.
        if self.dado1 is None or self.dado2 is None:
            print("Los dados aún no se han lanzado.")
        else:
            print(f"Resultado del lanzamiento: Dado 1 = {self.dado1}, Dado 2 = {self.dado2}")

# De cómo salen las fichas 
# 1) Las fichas salen a su respectiva salida que está exactamente a 5 casillas del seguro inmediatamente anterior,
# en la imagen de referencia de la anterior sección se encuentra marcada como “Salida 1”. 
# 2) Cada ficha sale con un cinco en los dados, ya sea repartido entre los dos dados o con el dígito completo en
# uno de los dos dados. 
# 3) Solo se permiten dos fichas máximo por cada casilla. En caso de que ya haya dos fichas en la salida del 
# respectivo equipo, las fichas solo podrán hacer movimientos. No obstante, las fichas también pueden moverse y 
# desocupar el espacio para que salga otra ficha. Ejemplo: Supongamos que tenemos 2 fichas en la salida 1, y
# tenemos en los dados 4 y 5, podemos mover 4 con una de las fichas y usar el otro 5 para sacar otra ficha. 

class Fichas:
    def __init__(self, num_equipos=4):
        # Cada equipo tiene una lista para su salida y fichas
        self.equipos = {f"Equipo {i+1}": {"fichas": [0, 0, 0, 0], "salida": 5} for i in range(num_equipos)}
        self.casillas = {i: [] for i in range(1, 69)}  # Casillas numeradas del 1 al 68

    def puede_sacar_ficha(self, equipo, dado1, dado2):
        # Verifica si un equipo puede sacar una ficha basado en los dados.
        salida = self.equipos[equipo]["salida"]
        if len(self.casillas[salida]) < 2 and (dado1 == 5 or dado2 == 5 or dado1 + dado2 == 5):
            return True
        return False

    def sacar_ficha(self, equipo, dado1, dado2):
        
        # Saca una ficha a la salida si es posible.
        salida = self.equipos[equipo]["salida"]

        if self.puede_sacar_ficha(equipo, dado1, dado2):
            # Encuentra una ficha en la cárcel (posición 0)
            for i in range(len(self.equipos[equipo]["fichas"])):
                if self.equipos[equipo]["fichas"][i] == 0:
                    # Coloca la ficha en la salida
                    self.equipos[equipo]["fichas"][i] = salida
                    self.casillas[salida].append(equipo)
                    print(f"{equipo} ha sacado una ficha a la casilla {salida}.")
                    return True
        print(f"{equipo} no puede sacar una ficha.")
        return False

    def mover_ficha(self, equipo, ficha_idx, movimientos):
        # Mueve una ficha un número determinado de casillas si es posible.
        ficha_pos = self.equipos[equipo]["fichas"][ficha_idx]
        if ficha_pos == 0:
            print(f"La ficha {ficha_idx + 1} de {equipo} está en la cárcel y no puede moverse.")
            return False

        nueva_pos = ficha_pos + movimientos

        # Verifica si hay un bloqueo o si la casilla de destino tiene más de dos fichas
        if len(self.casillas.get(nueva_pos, [])) < 2:
            # Actualiza la posición de la ficha
            self.equipos[equipo]["fichas"][ficha_idx] = nueva_pos
            self.casillas[ficha_pos].remove(equipo)
            self.casillas[nueva_pos].append(equipo)
            print(f"{equipo} ha movido su ficha {ficha_idx + 1} a la casilla {nueva_pos}.")
            return True
        else:
            print(f"No se puede mover la ficha a la casilla {nueva_pos} porque hay un bloqueo o está llena.")
            return False

if __name__ == "__main__":
    # Crear instancias
    dados = Dados()
    ficha = Fichas()

    # Simular un turno para el Equipo 1
    equipo = "Equipo 1"
    dado1, dado2 = dados.lanzar()
    dados.mostrar_resultado()

    # Intentar sacar una ficha
    if ficha.sacar_ficha(equipo, dado1, dado2):
        # Si hay movimientos restantes, intentar mover una ficha
        if dado1 != 5:
            ficha.mover_ficha(equipo, 0, dado1)  # Mueve la primera ficha con el dado1
        if dado2 != 5:
            ficha.mover_ficha(equipo, 0, dado2)  # Mueve la primera ficha con el dado2
