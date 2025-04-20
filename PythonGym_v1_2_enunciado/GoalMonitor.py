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
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True
        

        current_time = perception[AgentConsts.TIME]
        time_elapsed = current_time - self.lastTime

        if time_elapsed > 3:
            self.lastTime = current_time
            return True

        if perception[AgentConsts.TIME] - self.lastTime > 5: #si pasa mucho recalculamos 
            return True
        
        goal = agent.problem.GetGoal().value


        if goal == AgentConsts.LIFE and perception[AgentConsts.LIFE_X] == -1:
            return True

        if perception[AgentConsts.HEALTH] < 3:
            if perception[AgentConsts.LIFE_X] != -1 and perception[AgentConsts.LIFE_Y] != -1:
                
                return True
        
        if any(perception[i] == AgentConsts.PLAYER for i in range(4)): 
            return True
        


        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.
        return False
    


    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        health = perception[AgentConsts.HEALTH]
        player_near = any(perception[i] == AgentConsts.PLAYER for i in range(4))
        hay_health = perception[AgentConsts.LIFE_X] != -1 and perception[AgentConsts.LIFE_Y] != -1

        if not hay_health:
            self.goals[self.GOAL_LIFE] = None

        if health < 2 and self.goals[self.GOAL_LIFE] is not None:
            return self.goals[self.GOAL_LIFE]
        elif player_near:
            return self.goals[self.GOAL_PLAYER]
        else:
            return self.goals[self.GOAL_COMMAND_CENTRER]

    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal


  