from State import State

class Avoid(State):
    def __init__(self, id):
        super().__init__(id)
        self.target_direction = None

    def Start(self):
        print("[Avoid] Incio")
        self.target_direction = None

    def Update(self, perception, orientation):
        print("[Avoid] Update:")
        self.target_direction = orientation
        # Índices de los elementos de percepción relevantes
        UP, DOWN, RIGHT, LEFT = 0, 1, 2, 3
        



        # Detectar si hay un obstáculo irrompible justo en frente
        obstaculo_frente = perception[self.target_direction - 1] == 1 and perception[self.target_direction + 3] <= 1

        if obstaculo_frente:
            print("Irrompible encontrado")
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

        print(f"Acción elegida en Avoid: {action}")
        return action, False  # `True` indica que sigue en el mismo estado

    def Transit(self, perception, orientation):
        print("[Avoid] Transit:")
       
        return "GoToCommandCenter"
        

    def End(self):
        print("Fin del estado de esquivar")
