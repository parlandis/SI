from State import State

class Shot(State):
    def __init__(self, id):
        super().__init__(id)
        self.target_direction = None
        
    #Metodo que se llama al iniciar el estado
    def Start(self):
        print("[Shot] Inicio - Modo destrucción de obstáculos")
        self.target_direction = None

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception, orientation):
        print("State update")
        if self.target_direction is None:
            self.target_direction = orientation
            print(f"[Shot] Orientación objetivo: {self.target_direction}")

        # Disparar solo si puede (CAN_FIRE = 14)
        return (0, True) if perception[14] == 1 else (self.target_direction, False)
    
    #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self,perception, orientation):
        print("State Transit")
        print("Objeto enfrente: ", perception[self.target_direction - 1], perception[self.target_direction + 3] )
        if perception[self.target_direction - 1] == 0:
            
            print("[Shot] Obstáculo destruido. Volviendo a GoToCommandCenter")
            return "GoToCommandCenter"

        if perception[self.target_direction - 1] == 1:
            print("State Transit Avoid")
           
        
        print("State Transit Shot")
       
        return "Shot"

    
    #Metodo que se llama al finalizar el estado
    def End(self):
        print("fin del shot")