from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class RandomMovement(State):

    def __init__(self, id):
        super().__init__(id)

    def Start(self, agent):
        super().Start(agent)
        self.action = random.randint(1,4)
        self.updateTime = 0

    def Update(self, perception, map, agent):
        
        return self.action, False

    def Transit(self,perception, map):
        
        return "ExecutePlan"
        return self.id
    