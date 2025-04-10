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
            self.lastTime = perception[AgentConsts.TIME]

            return True
        
        if perception[AgentConsts.TIME] - self.lastTime > 5: #si pasa mucho recalculamos 
            return True
        
        if perception[AgentConsts.HEALTH] < 2:
            return True
        
        if any(perception[i] == AgentConsts.PLAYER for i in range(4)): 
            return True

        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):

            #TODO definir la estrategia del cambio de meta
            if self.CC_atiro(perception):
                return self.goals[self.GOAL_COMMAND_CENTRER]
            else:
                if self.player(perception):
                    return self.goals[self.GOAL_LIFE]
            
                if(perception[AgentConsts.HEALTH] < 2 ):
                    return self.goals[self.GOAL_PLAYER]
        
            
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