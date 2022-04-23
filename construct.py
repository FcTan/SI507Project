#########################################
##### Name:Fangcheng Tan            #####
##### Uniqname: fctan               #####
#########################################

from readJSON import data
from graphs import Vertex,Graph

g = Graph()
for i in data:
    g.addVertex(i)
for v in g:
    v.setName(data[v.id]['name'])
    v.setCount(data[v.id]['gamecount'])
    v.setOwnedGame(data[v.id]['ownedGame'])
    v.setRecentGame(data[v.id]['recentGame'])
    for i in data[v.id]['connections']:
        g.addEdge(v.id, i[0], i[1])
myId = list(g.vertList.keys())[0]
ownedDict = {}
for v in g:
    if v.count != 0:
        ownedDict[v.id] = v.count
gameDict = {}
for v in g:
    for i in v.games:
        if i in gameDict:
            gameDict[i] = gameDict[i] + 1
        else:
            gameDict[i] = 1
gameDict = dict(sorted(gameDict.items(), key = lambda item: item[1], reverse = True))
print("your input id is:", myId)
print("finish loading file!")