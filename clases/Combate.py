from State import State

class Combate(State):
    def __init__(self, id):
        super().__init__(id)
        self.target_direction = None
        
    #Metodo que se llama al iniciar el estado
    def Start(self):
        print("[Combate] Inicio")
        self.target_direction = None

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza


    #Disparamos solo si podemos 
    def Update(self, perception, orientation):
        print("[Combate] Update -")
        if self.target_direction is None:
            self.target_direction = self.Buscar(perception)
            print(f"[Combate] Orientación objetivo: {self.target_direction - 1}")
        
        if perception[self.target_direction - 1] == 4:
            print("[Combate] Jugador a tiro")
            if perception[14] == 1:
                print("[Combate] Disparando")
                return (self.target_direction, True)
            else:
                print("[Combate] No puede disparar")
                return (self.target_direction, False)   
        else:
                print("[Combate] Jugador no a tiro")
                return self.target_direction, True
        
        
        

    #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self,perception, orientation):
        print("[Combate] Transición")        
        print("Objeto enfrente: ", perception[self.target_direction - 1], perception[self.target_direction + 3] )
        if perception[self.target_direction - 1] == 0:
            
            print("[Combate] Obstáculo destruido. Volviendo a GoToCommandCenter")
            return "GoToCommandCenter"

        if perception[self.target_direction -1] == 1:
            print["[Combate]: Irrompible"]
            self.target_direction = self.Buscar(perception)
            return "Combate"
        
        return "Combate"

    def Buscar(self, perception):
        dx = perception[8] - perception[12]
        dy = perception[9] - perception[13]

        if abs(dx) < abs(dy):
            if dy > 0:
                return 1
            else:
                return 2
        else:
            if dx > 0:
                return 3
            else:
                return 4
        
    
    def manejo_obstaculos(self, perception):
        if self.target_direction is None:
            print("[Combate]: Sin dir ")
            self.target_direction = self.dirCC(perception)
        
        UP, DOWN, RIGHT, LEFT = 0, 1, 2, 3
        tipo_obstaculo = perception[self.target_direction - 1]
        distancia = perception[self.target_direction + 3]
        
        if tipo_obstaculo == 2 and distancia < 1.5:  # BRICK
            print("[Combate] ¡Ladrillo detectado! Disparando...")
            return 0, True
        elif tipo_obstaculo == 1 and distancia < 1:  # METAL
            print("[Combate] ¡Obstáculo irrompible! Recalculando ruta...")

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


    
    #Metodo que se llama al finalizar el estado
    def End(self):
        print("[Combate] fin del combate")