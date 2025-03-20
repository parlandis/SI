from State import State

class StateMachine(State):
    # Enumeración de las orientaciones 1 up , 2 down, 3 left, 4 right
    enum_orientation = [ 1, 2,3, 4]

    def __init__(self, id, states, initial, orientation):
        super().__init__(id)
        self.states = states
        self.curentState = initial
        self.orientation = orientation
    
    #Metodo que se llama al iniciar la máquina de estado
    def Start(self):
        print(f"[StateMachine] Iniciando máquina de estados. Estado inicial: {self.curentState}")
        self.states[self.curentState].Start()

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception):
        actions = self.states[self.curentState].Update(perception, self.orientation)
        newState=self.states[self.curentState].Transit(perception, self.orientation)
        
        if newState != self.curentState:
            print(f"[StateMachine] Transición: {self.curentState} -> {newState}")
            self.states[self.curentState].End()
            self.curentState=newState
            self.states[self.curentState].Start()
        return actions
    

    #Metodo que se llama al finalizar la máquina de estado
    #def End(self, win):
        #super().End(win)