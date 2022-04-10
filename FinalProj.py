#########################################
##### Name:Fangcheng Tan            #####
##### Uniqname: fctan               #####
#########################################

import requests
from bs4 import BeautifulSoup
import json
import re

API = "C61898C31C380EF70DC822DBE3AA1FAF"

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

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
    
userId = input ("Please input your steam id (17-digits, Default would be my Id): ")
if len(userId) != 17:
    myId = 76561198112190070
else:
    myId = userId

# Get game name from game app id
game_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
Gresp = requests.get(game_URL)
Gfile = Gresp.text
Gsamples = json.loads(Gfile)


# Cashing from Steam API information page
Base_URL = "https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_.28v0001.29"
response = requests.get(Base_URL)
soup = BeautifulSoup(response.text, 'html.parser')
#print(soup.prettify()) 
body = soup.find('div', class_='mw-parser-output')
main = body.find_all('a', class_="external free")
# Find friends
site = main[5].contents[0]
newsite=re.sub(r"/\?.+", "",site)
parameter = {'key':API,'steamid':myId,'relationship':'friend'}
resp = requests.get(newsite, parameter)
file = resp.text
if re.search("Error",file):
    print("Wrong id")
else:
    samples = json.loads(file)
    if samples == {}:
        print("This user does not proivde public information ")
    else:
        g = Graph()
        g.addVertex(myId)
        List = []
        count = 0
        count1 = count
        print("Friends' ids are: ")
        for i in samples['friendslist']["friends"]:
            count+=1
            if count <= 200:
                print(count, i['steamid'])
                List.append(i['steamid'])
                g.addVertex(i['steamid'])
            else:
                None
        print("You have", count, "friends (get no more than 200)")
        for i in range(0,count):
            g.addEdge(myId,List[i],i+1)

        #Find Games
        gameLink = main[8].contents[0]
        gameLink1 = re.sub(r"/\?.+", "",gameLink)
        gameParameter = {'key':API,'steamid':myId,'format':'json'}
        gameResp = requests.get(gameLink1, gameParameter)
        gameFile = gameResp.text
        gameSamples = json.loads(gameFile)
        gameCount = gameSamples['response']['game_count']
        gameList = []
        for i in range(0, gameCount):
            gameList.append(gameSamples['response']['games'][i]['appid'])
        gameDict = None
        gameDict = dict.fromkeys(gameList, 1)
        for i in range(0, count):
            gameParameter1 = {'key':API,'steamid':List[i],'format':'json'}
            #print(gameParameter1)

            gameResp1 = requests.get(gameLink1, gameParameter1)
            gameFile1 = gameResp1.text
            gameSamples1 = json.loads(gameFile1)
            if gameSamples1['response'] != {}:
                gameCount1 = gameSamples1['response']['game_count']
                gameList1 = []
                for i in range(0, gameCount1):
                    thisGame = gameSamples1['response']['games'][i]['appid']
                    if thisGame in gameDict:
                        #print(thisGame, "is already here")
                        gameDict[thisGame] = gameDict[thisGame] + 1
                    else:
                        gameDict[thisGame] = 1
        gameDict = dict(sorted(gameDict.items(),key=lambda item: item[1],reverse=True))
        ownedMost = dict(list(gameDict.items())[0:20])
        for j in list(ownedMost):
            for i in range(0,len(Gsamples['applist']['apps'])):
                if re.search(r'\b'+ str(j) + r'\b', str(Gsamples['applist']['apps'][i]["appid"])):
                    gameName = (Gsamples['applist']['apps'][i]["name"])
                    ownedMost[gameName] = ownedMost.pop(j)
        print("Most popular games are")
        place = 0
        for k, v in ownedMost.items():
            place+=1
            print(place, k)
            print("  Owned by", v ,"players")