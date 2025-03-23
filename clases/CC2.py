from State import State


class CC2(State):

    def __init__(self, id):
        super().__init__(id)
        self.target_direction = None
        self.last_axis = None
        self.movs_consecutivos = 0


    def Start(self):
        print("[GoToCommandCenter] Inicio")
        self.target_direction = None
        self.last_axis = None
        self.movs_consecutivos = 0

        

    def Update(self, perception, orientation):
        print("[GoToCommandCenter] Update")


        if self.target_direction and perception[self.target_direction - 1] == 0:
            self.target_direction = None
        
        if(self.target_direction == None):
            self.target_direction = self.dirCC(perception)
            print(f"[GoToCommandCenter] Dirección recalculada: {self.target_direction}")
            
        if perception[self.target_direction - 1] == 3:
            print(f"[GoToCommandCenter] CC encontrada a tiro: { perception[self.target_direction - 1] }")
            return self.target_direction, True
        else:
                print("CC no a tiro , seguimos buscando")
                peligro = self.manejo_peligros(perception)
                if peligro:
                    return peligro
                
                print("Sin peligro: buscando obst")
                obstaculos = self.manejo_obstaculos(perception)
                if obstaculos:
                    return obstaculos


        return self.target_direction, False


    def Transit(self, perception, orientation):
        #action = self.dirCC(perception)
        print("[GoToCommandCenter] Transit")
        
        if self.jugadorCerca(perception):
            print("[CC2] ¡Jugador detectado! Transición a Combate")
            return "Combate"
       
        self.movs_consecutivos += 1

        if self.movs_consecutivos >= 3:
           print("[CC2] Sin progreso. Recalculando...")
           self.target_direction = self.dirCC(perception)
           self.movs_consecutivos = 0
    
        if self.irrompible_en_dir(perception):
            print("[CC2] Obstáculo irrompible. Forzando recálculo...")
            self.target_direction = self.dirCC(perception)
            return self.id  # Permanece en CC2 pero con nueva dirección

        return self.id


    #Metodo que se llama al finalizar el estado
    def End(self):
        print("Fin de GotoCommandCenter")

    def _is_brick_blocking(self, perception):
        return (
            self.target_direction is not None and
            perception[self.target_direction - 1] == 2 and
            perception[self.target_direction + 3] < 1.5
        )

    def irrompible_en_dir(self, perception):
         return (
            self.target_direction is not None and
            perception[self.target_direction - 1] == 1 and
            perception[self.target_direction + 3] < 1
        )

    #Si una bala viene hacia nosotros
    def bala(self, perception):
        for i in range(4):
            if perception[i] == 5 :
                return True
        return False
    
    def _bala_en_direccion_actual(self, perception):
        return perception[self.target_direction - 1] == 5

    #sabemos qeu hay bala
    def dirBala(self, percepcion):
        for i in range(4):
            if percepcion[i] == 5:
                return i
       
    #Si nos hay un jugador a la vista
    def jugador(self,  perception):
        for i in range(4):
            if perception[i] == 4:
                return True
        return False
    
    def dirJugador(self, perception):
        for i in range(4):
            if perception[i] == 4:
                return i  # Devuelve 0-3 (UP, DOWN, RIGHT, LEFT)
        return None

    def manejo_obstaculos(self, perception):
        if self.target_direction is None:
            print("[CC2]: Sin dir ")
            self.target_direction = self.dirCC(perception)
        
        UP, DOWN, RIGHT, LEFT = 0, 1, 2, 3
        tipo_obstaculo = perception[self.target_direction - 1]
        distancia = perception[self.target_direction + 3]
        
        if tipo_obstaculo == 2 and distancia < 1.5:  # BRICK
            print("[CC2] ¡Ladrillo detectado! Disparando...")
            return self.target_direction, True
        elif tipo_obstaculo == 1 and distancia < 1:  # METAL
            print("[CC2] ¡Obstáculo irrompible! Recalculando ruta...")

            if self.last_axis == "X":
                #Si nos moviamos en eje x priorizamos eje y 
                if perception[DOWN] != 1: 
                    print("Esquivando irrompible por abajo")
                    action = 2
                    return 2, True
                elif perception[UP] != 1: 
                    print("Esquivando irrompible por arriba")
                    action = 1
                    return 1, True
                elif perception[LEFT] != 1: 
                    print("Esquivando irrompible por la izquierda")
                    action = 2
                elif perception[RIGHT] != 0: 
                    print("Esquivando irrompible por la derecha")
                    action = 1
                else:
                    action = 0  # Si está completamente atrapado, detenerse
            else: 
                # Prioridad: Intentar moverse lateralmente
                if perception[LEFT] != 1:  # Si a la izquierda está libre
                    print("Esquivando irrompible por la izquierda")
                    action = 4
                elif perception[RIGHT] != 1:  # Si a la derecha está libre
                    print("Esquivando irrompible por la derecha")
                    action = 3
                elif perception[DOWN] != 1:  # Si no hay espacio lateral, intenta retroceder
                    print("Esquivando irrompible por abajo")
                    action = 2
                elif perception[UP] != 0:  # Si no hay espacio lateral, intenta retroceder
                    print("Esquivando irrompible por arriba")
                    action = 1
                else:
                    action = 0  # Si está completamente atrapado, detenerse
        else:
            action = self.target_direction  # Si no hay obstáculos en frente, avanzar
   
        return action, False

       

 #Nos dice en que direccion se encuentra el Command Center primero recortanto la distancia en x y luego en y
    def dirCC(self, perception):
        dx = perception[10] - perception[12]  # CC_X - AGENT_X
        dy = perception[11] - perception[13]  # CC_Y - AGENT_Y

        
        #print(f"[GoToCommandCenter] dx es: { dx }")
        #print(f"[GoToCommandCenter] dy es: { dy }")
        # Lógica mejorada para evitar oscilaciones
        if abs(dx) < 1.0 and self.last_axis == "X":  # Umbral de alineación
            self.last_axis = "Y"
            return 2 if dy < 0 else 1
        elif abs(dy) < 1.0 and self.last_axis == "Y":
            self.last_axis = "X"
            return 3 if dx > 0 else 4

        # Lógica original si no está alineado
        if abs(dx) < abs(dy):
            self.last_axis = "Y"
            return 2 if dy < 0 else 1
        else:
            self.last_axis = "X"
            return 3 if dx > 0 else 4
                
    
    def jugadorCerca(self, perception):
        dir_jugador = self.dirJugador(perception)
        return dir_jugador is not None and perception[dir_jugador + 4] < 2
            
            
        
    def manejo_peligros(self, perception):
            dir_bala = self.dirBala(perception)
            dir_jugador = self.dirJugador(perception)
            
            # Prioridad: Balas
            if dir_bala is not None:
                distancia_bala = perception[dir_bala + 4]
                if distancia_bala < 4:
                    if dir_bala == (self.target_direction - 1):  # Bala en dirección actual
                        print("[CC2] ¡Bala frontal! Disparando...")
                        return 0, True
                    else:
                        print("[CC2] ¡Bala cercana! Evadiendo...")
                        self.target_direction = self.dirCC(perception)
                        return self.target_direction, False
                else:
                     print("[CC2] Bala lejos! Reorientando...")
            
            # Jugador
            if dir_jugador is not None:
                distancia_jugador = perception[dir_jugador + 4]
                if distancia_jugador < 5:
                    if dir_jugador == (self.target_direction - 1):  # Jugador en dirección actual
                        print("[CC2] ¡Jugador a tiro! Disparando...")
                        return 0, True
                    else:
                        print("[CC2] ¡Jugador cerca! Reorientando...")
                        self.target_direction = dir_jugador + 1
                        return self.target_direction, False
                else:
                     print("[CC2] ¡Jugador lejano! Reorientando...")
            return None
