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
  
        if self.target_direction is None:
            self.target_direction = self.targetDir(perception)
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
            return move + 1, perception[AgentConsts.CAN_FIRE] == 1 



        action, shot = self.Combate(perception)
        print(f"[Attack] Acción: {action}, Disparo: {shot}")
        return action, shot

    def Transit(self, perception, map):
        self.target_direction = self.targetDir(perception)
        if perception[self.target_direction] != AgentConsts.PLAYER and \
           perception[self.target_direction] != AgentConsts.COMMAND_CENTER:
            print("[Attack] Objetivo No en direccion Orientando)")
        

        jug = any(perception[i] == AgentConsts.PLAYER for i in range(4))
        if not jug:
            print("[Attack] Jugador no detectado. Volviendo a ExecutePlan")
            return "ExecutePlan"
        
        if perception[AgentConsts.HEALTH] < 2:
            print("[Attack] Salud baja. Volviendo a ExecutePlan")
            return "ExecutePlan"

        
        if perception[self.target_direction] == AgentConsts.UNBREAKABLE:
            print("[Attack] Obstáculo irrompible detectado")
            return "ExecutePlan"
            
        return self.id

    def targetDir(self, perception):
        
        dx = perception[AgentConsts.PLAYER_X] - perception[AgentConsts.AGENT_X]
        dy = perception[AgentConsts.PLAYER_Y] - perception[AgentConsts.AGENT_Y]
        
        if abs(dx) > abs(dy):
            return AgentConsts.NEIGHBORHOOD_RIGHT if dx > 0 else AgentConsts.NEIGHBORHOOD_LEFT
        else:
            return AgentConsts.NEIGHBORHOOD_DOWN if dy > 0 else AgentConsts.NEIGHBORHOOD_UP

    def Combate(self, perception):
       
        if perception[self.target_direction] == AgentConsts.PLAYER:
            if perception[AgentConsts.CAN_FIRE] == 1:
                print("[Attack] ¡Disparando al objetivo!")
                return AgentConsts.NO_MOVE, True           #Si disparamos no nos movemos
            else:
                print("[Attack] Esperando recarga...")     #si recargamos debemos movernos?
                return AgentConsts.NO_MOVE, False
        else:
            
            if perception[self.target_direction + 4] > 1.0:  # Usar distancia de percepción
                print(f"[Attack] Avanzando hacia objetivo")
                return self.target_direction, False
            else:
                print("[Attack] Obstáculo cercano, replanificando")
                return AgentConsts.NO_MOVE, False

    def End(self):
        print("[Attack] Finalizando modo ataque")