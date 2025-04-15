from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem

#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.



       
        self.open = [self.problem.Initial()]
        self.processed = set()

        while self.open:
            current = min(self.open, key=lambda n: n.F())
            self.open.remove(current)
            self.processed.add(current)

            if self.problem.IsASolution(current):
                return self.ReconstructPath(current)

            for successor in self.problem.GetSucessors(current):
                if successor in self.processed:
                    continue

                tentative_g = current.G() + self.problem.GetGCost(successor)
                in_open = self.GetSucesorInOpen(successor)

                if not in_open or tentative_g < successor.G():
                    successor.SetParent(current)
                    successor.SetG(tentative_g)
                    successor.SetH(self.problem.Heuristic(successor))
                    if not in_open:
                        self.open.append(successor)
        return []

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        
        node.SetParent(parent)
        node.SetG(newG)
        node.setH(self.problem.Heuristic(node)) #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found


    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
        
        while goal != None:
            path.append( goal)
            goal = BCNode.GetParent(goal)

        return path[::-1]



