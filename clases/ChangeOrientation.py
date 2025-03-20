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
    def Update(self, perception, orientation):

        
        dir_peligro  = self.peligro(perception)
        print(f"{dir_peligro}")
        if dir_peligro == None:
            return 0, False
        else:
            return dir_peligro, False
    
    #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self, perception, orientation):
        print("[Change] Transit:")

        """ if orientation == self.target_orientation:
            # Corregir índice: perception[0-3] corresponde a direcciones 1-4
            obstaculo = perception[orientation - 1]  # Índice ajustado

            if obstaculo == 1:  # UNBREAKABLE (pared indestructible)
                self.id = "Avoid"  # No se puede avanzar, volver al estado principal
            elif obstaculo in [2, 5,3, 4 ]:  # BRICK (ladrillo) o bala
                self.id = "Shot"  # Disparar para destruirlo
        
            # Seguir intentando alcanzar la orientación objetivo
            self.id = "GoToCommandCenter"""

        return "Shot"

  
    def peligro(self, perception):
        for i in range(4):
            if perception[i] in [5, 6]:
                return i 

            
    
    #Metodo que se llama al finalizar el estado
    def End(self):
        print("Fin del cambio de orientacion")