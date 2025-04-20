import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False
        self.dir = 0

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):
        if self.recalculate:
            print("Recalculando")
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        if perception[AgentConsts.TIME] - self.lastTime > 2:
            print("Recalculando por tiempo")
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        if perception[AgentConsts.HEALTH] < 2:
            print("Recalculando por vida")
            return True
        
        if any(perception[i] == AgentConsts.PLAYER for i in range(4)): 
            print("Recalculando por player")
            return True

        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):

        #TODO definir la estrategia del cambio de meta
        if self.player(perception):
            print("Meta: Player")
            return self.goals[self.GOAL_PLAYER]
            
        if(perception[AgentConsts.LIFE_X] != -1 and perception[AgentConsts.LIFE_Y] != -1 and perception[AgentConsts.HEALTH] < 2):
            print("Meta: Vida")
            return self.goals[self.GOAL_LIFE]
        
        print("Meta: CommandCenter")
        return self.goals[self.GOAL_COMMAND_CENTRER]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal


    def CC_atiro(self, perception): 
        if perception[AgentConsts.COMMAND_CENTER] == self.dir:
            print("CC a tiro")

    def player(self, perception):
        for i in range (4 ):
            if perception[i] == perception[AgentConsts.PLAYER]:
                return i

        return None   