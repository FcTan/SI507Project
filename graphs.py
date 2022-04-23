#########################################
##### Name:Fangcheng Tan            #####
##### Uniqname: fctan               #####
#########################################

class Vertex:
    def __init__(self,key,name = None, gameCount = 0, ownedGame = [], recentgame = {}):
        self.id = key
        self.name = name #get from user status
        self.count = gameCount #get from find games
        self.games = ownedGame #get from find games
        self.recentplayed = recentgame #get from user status
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def setName(self,personName):
        self.name = personName
    
    def setCount(self, count):
        self.count = count

    def setOwnedGame(self, ownedGame):
        self.games = ownedGame

    def setRecentGame(self,recent):
        self.recentplayed = recent

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])
           
    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]
    
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        if key in self.vertList:
          return None
        else:
            
          self.numVertices = self.numVertices + 1
          newVertex = Vertex(key)
          self.vertList[key] = newVertex
          return newVertex
        
    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())