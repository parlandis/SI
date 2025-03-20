from BaseAgent import BaseAgent
from StateMachine import StateMachine
from GoToCommandCenter import GoToCommandCenter
from Shot import Shot
from Avoid import Avoid
from ChangeOrientation import Change

class ReactiveAgent(BaseAgent):

    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "GoToCommandCenter" : GoToCommandCenter("GoToCommandCenter"),
        "Shot" : Shot("Shot"),
        "Avoid" : Avoid("Avoid"),
        "Change" : Change("Change")
        }
        orientation = 2    #orientacion inicial hacia abajo
        self.stateMachine = StateMachine("ReactiveBehavior",dictionary,"GoToCommandCenter", orientation)

    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("[ReactiveAgent] Iniciando agente")
        self.stateMachine.Start()

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception):
        action, shot = self.stateMachine.Update(perception)
        return action, shot
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        super().End(win)
        self.stateMachine.End()