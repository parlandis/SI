from State import State


class GoToCommandCenter(State):

    def __init__(self, id):
        super().__init__(id)
        self.target_direction = None
        self.last_axis = None


    def Start(self):
        print("Iniciando GotoCC:")
        self.target_direction = None
        self.last_axis = None

        

    def Update(self, perception, orientation):
        
        if self.target_direction is None:
            self.target_direction = self.dirCC(perception)
            print(f"[GoToCommandCenter] Dirección recalculada: {self.target_direction}")

        return self.target_direction, False



    def Transit(self, perception, orientation):
        #action = self.dirCC(perception)
        print("Transit de CC")

        if perception[self.target_direction - 1] == 3:
            return "Shot"

        # 1. Lógica para balas (prioridad máxima)
        if self.bala(perception):
            print(f"[GoToCommandCenter] bala encontrada: { perception[self.target_direction - 1] }")

            if self._bala_en_direccion_actual(perception):
                return "Shot"  # Disparar si la bala viene hacia nosotros
            else :
                dirB = self.dirBala(perception)
                if perception[dirB + 3] > 4:
                    return "Avoid"
                else : 
                    return "Change"  # Esquivar cambiando de dirección
        # 2. Lógica para jugador (segunda prioridad)
        if self.jugador(perception):
            print("jugador encontrado")
            jugador_dir = self.dirJugador(perception)
            if jugador_dir == (self.target_direction - 1):  # Jugador en dirección actual
                return "Shot"
            else:
                return "Change"  # Reorientarse hacia el jugador

        if self.irrompible_en_dir(perception):
            print(f"[GoToCommandCenter] irrompible encontrado a distancia: { perception[self.target_direction + 3] }")
            return "Avoid"

        if self._is_brick_blocking(perception):
            print(f"[GoToCommandCenter] ladrillo encontrado a distancia: { perception[self.target_direction + 3] }")
            return "Shot" 


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


 #Nos dice en que direccion se encuentra el Command Center primero recortanto la distancia en x y luego en y
    def dirCC(self, perception):
        dx = perception[10] - perception[12]  # CC_X - AGENT_X
        dy = perception[11] - perception[13]  # CC_Y - AGENT_Y


        print(f"[GoToCommandCenter] dx es: { dx }")
        print(f"[GoToCommandCenter] dy es: { dy }")
        # Lógica mejorada para evitar oscilaciones
        if abs(dx) < abs(dy):
            self.last_axis = "Y"
            return 2 if dy < 0 else 1
            
        else:
            self.last_axis = "X"
            return 3 if dx > 0 else 4
            
        
            return 0  # No movimiento
            
        
