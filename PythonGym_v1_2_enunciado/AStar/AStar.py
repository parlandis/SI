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
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        path = []
        self.open = []
        self.precessed = set()
        print("Ha llegado hasta A*, generando plan")
        print(BCProblem.Initial(self.problem))
        self.open.append(self.problem.Initial())
        print("Nodo inicial: ", self.problem.Initial())
        print("Nodo meta: ", self.problem.goal)
        
        while len(self.open) > 0:
            #sacamos el nodo con menor coste de la frontera de exploración
            node = min(self.open, key=lambda node: BCNode.F(node))

            #si es la meta, reconstruimos el path y salimos
            if self.problem.IsASolution(node):
                findGoal = True
                path = self.ReconstructPath(node)
                return path[::-1]
            
            self.open.remove(node)
            self.precessed.add(node)

            print("Estamos en el nodo : ", node)
            neigh = BCProblem.GetSucessors(self.problem, node)
            
            print("vecinos: ", len(neigh), neigh)
            for act in neigh:
                
                if self.precessed.__contains__(act):
                    continue
                
                tentative_g = BCNode.G(node) + BCProblem.GetGCost(node, act)
                
                if not self.GetSucesorInOpen(act):
                    self.open.append(act)
                elif tentative_g >= BCNode.G(act):
                    continue
                
                print("tentative: ", tentative_g)
                self._ConfigureNode(act, node, tentative_g)

                
        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*
        return findGoal

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        
        node.SetParent(parent)
        node.SetG(newG)
        BCNode.SetH(node, BCProblem.Heuristic(self.problem, node))
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

        return path



