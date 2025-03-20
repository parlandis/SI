from State import State

class Change(State):
    def __init__(self, id):
        super().__init__(id)
        self.target_orientation = None


    #Metodo que se llama al iniciar el estado
    def Start(self):
        print("Iniciando cambio de orientacion hacia :")
        self.target_orientation = None

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception):
        direcciones = []  # Inicializar fuera del bloque if

        if self.target_orientation is None:
            for i in range(4):
                if perception[i] == 1:  # Ignorar direcciones bloqueadas
                    continue

                # Prioridades según el tipo de objeto detectado
                if perception[i] == 4:   # Jugador
                    direcciones.append((10, i))
                elif perception[i] == 3: # Command Center
                    direcciones.append((9, i))
                elif perception[i] == 2: # Ladrillo
                    direcciones.append((8, i))
                elif perception[i] == 0: # Vacío
                    direcciones.append((7, i))

            # Ordenar por prioridad (mayor primero)
            if direcciones:
                direcciones.sort(reverse=True)
                self.target_orientation = direcciones[0][1]
            else:
                # Si todas están bloqueadas, elegir una dirección circular
                current_dir = int(perception[12] % 4)  # perception[12] = AGENT_X
                self.target_orientation = (current_dir + 1) % 4 + 1

        # Retornar la acción y si disparar
        should_fire = perception[self.target_orientation - 1] == 2
        return self.target_orientation, should_fire
    
    #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
def Transit(self, perception, orientation):
    if orientation == self.target_orientation:
        # Corregir índice: perception[0-3] corresponde a direcciones 1-4
        obstaculo = perception[orientation - 1]  # Índice ajustado

        if obstaculo == 1:  # UNBREAKABLE (pared indestructible)
            self.id = "GoToCommandCenter"  # No se puede avanzar, volver al estado principal
        elif obstaculo in [2, 5]:  # BRICK (ladrillo)
            self.id = "Shot"  # Disparar para destruirlo
        elif obstaculo in [3, 4]:  # COMMAND_CENTER o PLAYER
            self.id = "Shot"  # Disparar al objetivo
        else:  # Vacío (0) u otro
            self.id = "GoToCommandCenter"  # Continuar movimiento
    else:
        # Seguir intentando alcanzar la orientación objetivo
        self.id = "Change"

    return self.id

  
         
            
    
    #Metodo que se llama al finalizar el estado
    def End(self):
        print("Fin del cambio de orientacion")