from BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from States.ExecutePlan import ExecutePlan
from GoalMonitor import GoalMonitor
from AStar.AStar import AStar
from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem
from States.AgentConsts import AgentConsts
from States.Attack import Attack
from States.RandomMovement import RandomMovement

#implementación de un agente básico basado en objetivos.
#disponemos de la clase GoalMonitor que nos monitorea y replanifica cad cierto tiempo
#o cuando se establezca una serie de condiciones.
class GoalOrientedAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "ExecutePlan" : ExecutePlan("ExecutePlan"),
        "Attack" : Attack("Attack"),
        "RandomMovement" : RandomMovement("RandomMovement")
        }
        
        self.stateMachine = StateMachine("GoalOrientedBehavior",dictionary,"ExecutePlan")
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")
        self.stateMachine.Start(self)
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception, map):

        

        if not self.agentInit:
            self.InitAgent(perception,map)
            self.agentInit = True
 
        #le damos update a la máquina de estados.
       

        #Actualizamos el plan refrescando la posición del player (meta 2)
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player,2)



        if self.goalMonitor.NeedReplaning(perception,map,self):
            print("Replanificando")
            self.problem.InitMap(map) ## refrescamos el mapa
            initialNode = self._CreateInitialNode(perception) ## creamos el nodo inicial    
            self.problem.SetInitial(initialNode) ## establecemos el nodo inicial al problemas
            self.plan = self._CreatePlan(perception, map) ## creamos un nuevo plan
            if not self.plan:
                print("No hay plan, me quedo quieto")
                self.goalMonitor.ForceToRecalculate()
            


        action, shot = self.stateMachine.Update(perception, map, self)

        return action, shot
    
    #método interno que encapsula la creació nde un plan
    def _CreatePlan(self,perception,map):
        #currentGoal = self.problem.GetGoal()
        if self.goalMonitor != None:
            #TODO creamos un plan, pasos:
            #-con gualMonito, seleccionamos la meta actual (Que será la mas propicia => definir la estrategia a seguir).
            #-le damos el modo inicial _CreateInitialNode
            #-establecer la meta actual al problema para que A* sepa cual es.
            #-Calcular el plan usando A*

            
            currentGoal = self.goalMonitor.SelectGoal(perception,map,self)   ## seleccionamos la meta actual
            self.problem.SetGoal(currentGoal)   ## establecemos la meta actual al problema
            print("Meta actual: ", currentGoal.value)
            initialNode = self._CreateInitialNode(perception) ## creamos el nodo inicial
            self.problem.SetInitial(initialNode) ## establecemos el nodo inicial al problema

            
            return self.aStar.GetPlan()
                       
        return []
    
        
        
    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y,ySize):
        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X],perception[perceptionID_Y],ySize)
        newNode = BCNode(None,BCProblem.GetCost(value),value,xMap,yMap)
        return newNode

    def _CreatePlayerGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.PLAYER,AgentConsts.PLAYER_X,AgentConsts.PLAYER_Y,15)

    
    def _CreateLifeGoal(self, perception):
        if perception[AgentConsts.LIFE_X] == -1:
            return None

        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.LIFE,AgentConsts.LIFE_X,AgentConsts.LIFE_Y,15)
    
    def _CreateInitialNode(self, perception):
        node = GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.NOTHING,AgentConsts.AGENT_X,AgentConsts.AGENT_Y,15)
        node.SetG(0)
        return node
    
    def _CreateDefaultGoal(self, perception):
        return GoalOrientedAgent.CreateNodeByPerception(perception,AgentConsts.COMMAND_CENTER,AgentConsts.COMMAND_CENTER_X,AgentConsts.COMMAND_CENTER_Y,15)
    
    #no podemos iniciarlo en el start porque no conocemos el mapa ni las posiciones de los objetos
    def InitAgent(self,perception,map):
        #creamos el problema
        #TODO inicializamos:
        # - creamos el problema con BCProblem
        # - inicializamos el mapa problem.InitMap
        # - inicializamos A*
        # - creamos un plan inicial
        goal1CommanCenter = self._CreateDefaultGoal(perception)
        goal2Life = self._CreateLifeGoal(perception)
        goal3Player = self._CreatePlayerGoal(perception)
        inicial = self._CreateInitialNode(perception)
        self.problem = BCProblem(inicial, goal1CommanCenter, 15, 15 )
        self.problem.InitMap(map)
        self.goalMonitor = GoalMonitor(self.problem,[goal1CommanCenter,goal2Life, goal3Player])
        self.aStar = AStar(self.problem)
        self.plan = self._CreatePlan(perception, map)


        
        print("Agente creado :)")

    #muestra un plan por consola
    @staticmethod
    def ShowPlan(plan):
        for n in plan:
            print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")

    def GetPlan(self):
        return self.plan
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()