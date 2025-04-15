from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Attack(State):
    def __init__(self, id):
        super().__init__(id)
        self.nextNode = 0
        self.lastMove = 0
        self.transition = ""
        self.target_direction = None
        self.orientation = -1

    def Start(self, agent):
        print("[Attack] Iniciando modo ataque")
        self.target_direction = None
        self.orientation = agent.directionToLook
        self.transition = ""
        self.XPos = -1
        self.YPos = -1
        self.noMovements = 0


    def Update(self, perception, map, agent):
        # Lógica de búsqueda de objetivo
        if self.target_direction is None:
            self.target_direction = self._CalculateTargetDirection(perception)
            print(f"[Attack] Orientación objetivo: {self.target_direction}")

        bala_dir = None
        for i in range(4):
            if perception[i] == AgentConsts.SHELL and perception[i+4] <= 1.5:
                bala_dir = i
                break
        if bala_dir is not None:
            direction_map = {
            0: AgentConsts.MOVE_UP,    # Bala arriba
            1: AgentConsts.MOVE_DOWN,  # Bala abajo
            2: AgentConsts.MOVE_RIGHT, # Bala derecha
            3: AgentConsts.MOVE_LEFT   # Bala izquierda
            }
            move = direction_map[bala_dir]
            agent.directionToLook = move - 1 

            print(f"[Attack]¡Bala detectada en dirección {move}! Disparando...")
            return move, perception[AgentConsts.CAN_FIRE] == 1 


        # Manejo de obstáculos y disparo
        action, shot = self._HandleCombat(perception)
        print(f"[Attack] Acción: {action}, Disparo: {shot}")
        return action + 1, shot  # Ajustar a índices de acciones

    def Transit(self, perception, map):
        # Verificar si el objetivo sigue presente
        if perception[self.target_direction] != AgentConsts.PLAYER and \
           perception[self.target_direction] != AgentConsts.COMMAND_CENTER:
            print("[Attack] Objetivo perdido. Volviendo a ExecutePlan")
            return "ExecutePlan"
        
        if perception[AgentConsts.HEALTH] < 2:
            print("[Attack] Salud baja. Volviendo a ExecutePlan")
            return "ExecutePlan"

        
        # Verificar obstáculos irrompibles
        if perception[self.target_direction] == AgentConsts.UNBREAKABLE:
            print("[Attack] Obstáculo irrompible detectado")
            return "ExecutePlan"
            
        return self.id

    def _CalculateTargetDirection(self, perception):
        # Calcular dirección basada en posición del jugador
        dx = perception[AgentConsts.PLAYER_X] - perception[AgentConsts.AGENT_X]
        dy = perception[AgentConsts.PLAYER_Y] - perception[AgentConsts.AGENT_Y]
        
        if abs(dx) > abs(dy):
            return AgentConsts.NEIGHBORHOOD_RIGHT if dx > 0 else AgentConsts.NEIGHBORHOOD_LEFT
        else:
            return AgentConsts.NEIGHBORHOOD_DOWN if dy > 0 else AgentConsts.NEIGHBORHOOD_UP

    def _HandleCombat(self, perception):
        # Lógica de disparo y movimiento
        if perception[self.target_direction] == AgentConsts.PLAYER:
            if perception[AgentConsts.CAN_FIRE] == 1:
                print("[Attack] ¡Disparando al objetivo!")
                return AgentConsts.NO_MOVE, True
            else:
                print("[Attack] Esperando recarga...")
                return AgentConsts.NO_MOVE, False
        else:
            # Moverse hacia el objetivo si hay camino libre
            if perception[self.target_direction + 4] > 1.0:  # Usar distancia de percepción
                print(f"[Attack] Avanzando hacia objetivo")
                return self.target_direction, False
            else:
                print("[Attack] Obstáculo cercano, replanificando")
                return AgentConsts.NO_MOVE, False

    def End(self):
        print("[Attack] Finalizando modo ataque")