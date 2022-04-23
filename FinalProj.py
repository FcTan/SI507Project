#########################################
##### Name:Fangcheng Tan            #####
##### Uniqname: fctan               #####
#########################################

import requests
from bs4 import BeautifulSoup
import json
import re
from graphs import Vertex,Graph
import os
#Input your steam API from https://steamcommunity.com/dev/apikey
API = ""

def pickCommonWords(Descript,uniques,gamename):
    a = re.sub(r'href="https?:\/\/\S*', '', Descript)
    word = re.split("[^a-zA-Z]+", a)

    for i in word:
        if i not in uniques:
            uniques.append(i)
    counts = []
    commonWords = ['the','about','which','has','of','is','are','and','in','s','that', 'it','you','have','be','Steam','I',"new",'It','or','SteamDB','can','ve','after',
                  'to','a','for','on','section','at','with','very','type','only','game', 'games','an','week','more','will','players','your','their','Read','apos',
                  'This','as','class','not','but','All','Area','A','The','up','from','th','There','sheet','explanation','t','its','em','we','was','who','one','year',
                  'On','there','this','development','rd','above','Descriptions','by','some','Otherwise','been','nbsp', 'd','We','they', 're','x','all','into','rel',
                  'a','b','c','d','e','f','g','x','y','z','our','where','when','https','png','jpg','via','www','like','If','if','As','as','STEAM','m','com','blank','An',
                  'while','no','so','what','hello','hey','update','now','steamcommunity','images','IMAGE','HELLO','Hey','http','Hello','files','file','Ver','out',
                  'also','Fixed','fixed','bug','bugs','BUG','Update','update','href','Updated','us','time','Bug','here','two','just','release','could','released','issue',
                  'issues','next','being','CLAN','fixes','having','patch','clans','Added','added','his','get','Mode','mode','would','net','her']
    if isinstance(gamename,int):
        b = gamename
    else:
        b = re.split("[^a-zA-Z]+", gamename)
        for i in b:
            commonWords.append(i)

    for i in uniques:
        count = 0              # Initialize the count to zero.
        for j in word:     # Iterate over the words.
            if j == i and j not in commonWords:   
                count += 1         
        counts.append((count, i))
    counts.sort()
    counts.reverse()
    words = []
    for i in range(min(20, len(counts))):
        count,word = counts[i]
        words.append(word)
    return words

def findFriends(main,myId):
    # Find friends
    site = main[5].contents[0]
    newsite = re.sub(r"/\?.+", "",site)
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
            g.addVertex(str(myId))
            List = []
            obj = {}
            count = 0
            #print("Friends' ids are: ")
            for i in samples['friendslist']["friends"]:
                count += 1
                if count <= 30:
                    #print(count, i['steamid'])
                    List.append(i['steamid'])
                    g.addVertex(i['steamid'])
                count = len(List)
            print("You have", count, "friends (get no more than 30)...")
            for i in range(0,len(List)):
                g.addEdge(str(myId),List[i],i+1)
            countnew = count
            for i in List:
                fparameter = {'key':API,'steamid':i,'relationship':'friend'}
                fresp = requests.get(newsite, fparameter)
                ffile = fresp.text
                fsamples = json.loads(ffile)
                if fsamples == {}:
                    print(i,"This user does not proivde public information ")
                else:
                    #print("now i is ",i)
                    fcount = 0

                    obj['l'+str(i)] = []
                    for j in fsamples['friendslist']["friends"]:
                        fcount += 1
                        if fcount <= 10:
                            obj['l'+str(i)].append(j['steamid'])
                            g.addVertex(j['steamid'])
                        fcount = len(obj['l'+str(i)])
                    for j in range(0, fcount):
                        countnew += 1        
                        g.addEdge(i, obj['l'+str(i)][j], countnew)
            print("your friends have", len(g.vertList)-1-count, "friends in total (get no more than 10 friends per your friends)...")
    return g, List, obj

def findGames(main, g, List, obj):
#Find Games
    List2 = List.copy()
    for key, value in obj.items():
        for i in value:
            if i not in List2:
                List2.append(i)
    totalList = List2.copy()
    gameLink = main[8].contents[0]
    gameLink1 = re.sub(r"/\?.+", "",gameLink)
    gameDict = {}
    ownedDict = {}
    for i in range(0, len(totalList)):
        gameParameter1 = {'key':API,'steamid':totalList[i],'format':'json'}
        gameResp1 = requests.get(gameLink1, gameParameter1)
        gameFile1 = gameResp1.text
        gameSamples1 = json.loads(gameFile1)
        if gameSamples1['response'] != {}:
            gameCount1 = gameSamples1['response']['game_count']
            g.getVertex(totalList[i]).setCount(gameCount1)
            ownedDict[totalList[i]] = gameCount1
            ownedList = []
            for j in range(0, gameCount1):
                thisGame = gameSamples1['response']['games'][j]['appid']
                ownedList.append(thisGame)
                if thisGame in gameDict:
                    gameDict[thisGame] = gameDict[thisGame] + 1
                else:
                    gameDict[thisGame] = 1
            g.getVertex(totalList[i]).setOwnedGame(ownedList)
    gameDict = dict(sorted(gameDict.items(), key = lambda item: item[1], reverse = True))
    return gameDict, ownedDict, g

def lookUp(user, g, myId):
    lookUser = user
    friendcount = 0
    if lookUser == str(myId):
        print(myId, "is yourself")
    else:
        for v in g:
            for w in v.getConnections():
                if  w.getId() == lookUser:
                    friendcount += 1
                    if v.getId() != str(myId):
                        for x in g:
                            for z in x.getConnections():
                                if z.getId() == v.getId():
                                    if x.getId() == str(myId):
                                        print(lookUser, "is the friend of", v.getId(), "who is the friend of", str(myId),"(you)")
                                    else:
                                        print(lookUser, "is the friend of", v.getId(), "who is the friend of", x.getId())
                    else:
                        print(lookUser, "is the friend of", str(myId),"(you)")
        if friendcount == 0:
            print(lookUser, "is not your friend or your friend's friend")
    
def findStatus(findUser, g, main,Gsamples):
    if g.getVertex(findUser) == None:
        print("This user is not in your friends list")
    else:
        if g.getVertex(findUser).name == None:
            #findUser = '76561198112190070'
            playerLink = main[3].contents[0]
            playerLink1 = re.sub(r"/\?.+", "",playerLink)
            playerparameter = {'key':API,'steamids':findUser,'format':'json'}
            playerResp = requests.get(playerLink1, playerparameter)
            playerFile = playerResp.text
            playerSamples = json.loads(playerFile)
            username = playerSamples['response']['players'][0]['personaname']
            g.getVertex(findUser).setName(username)
            print ("The username is", username)
        else:
            print("The username is", g.getVertex(findUser).name)

        print(findUser, "owns", g.getVertex(findUser).count, "games")
        print(findUser,"'s gamelist(display 30 games for maximum): ")
        ownedGame = g.getVertex(findUser).games.copy()
        searchcount = 0
        stop = False
        for j in ownedGame:
            if stop == False:
                for i in range(0,len(Gsamples['applist']['apps'])):
                    if re.search(r'\b'+ str(j) + r'\b', str(Gsamples['applist']['apps'][i]["appid"])):
                        searchcount +=1
                        gameName = (Gsamples['applist']['apps'][i]["name"])
                        print(gameName)
                        if searchcount >= 30:
                            stop = True
                            print("...etc")
                        elif searchcount == 0:
                            print("this user does not own any games")
        print("The user recent played in two weeks:")
        if g.getVertex(findUser).recentplayed == {}:
            recentLink = main[9].contents[0]
            recentLink1 = re.sub(r"/\?.+", "", recentLink)
            recentparameter = {'key':API,'steamid':findUser,'format':'json'}
            recentResp = requests.get(recentLink1, recentparameter)
            recentFile = recentResp.text
            recentSamples = json.loads(recentFile)
            recentDict = {}
            if recentSamples['response'] == {}:
                print("this user does not play any games in recent two weeks")
            else:
                for i in range(0, recentSamples['response']['total_count']):
                    recentTime = recentSamples['response']['games'][i]['playtime_2weeks']
                    recentDict[recentSamples['response']['games'][i]['appid']] = recentTime
                for j, k in recentDict.items():
                    for i in range(0,len(Gsamples['applist']['apps'])):
                        if re.search(r'\b'+ str(j) + r'\b', str(Gsamples['applist']['apps'][i]["appid"])):
                            gameName = (Gsamples['applist']['apps'][i]["name"])
                            print(gameName, ", recently played", k, "mins")
                g.getVertex(findUser).setRecentGame(recentDict)
        else:
            for j,k in g.getVertex(findUser).recentplayed.items():
                for i in range(0,len(Gsamples['applist']['apps'])):
                    if re.search(r'\b'+ str(j) + r'\b', str(Gsamples['applist']['apps'][i]["appid"])):
                        gameName = (Gsamples['applist']['apps'][i]["name"])
                        print(gameName, ", recently played", k, "mins")

def findPopular(main, gameDict, Gsamples):
    ownedMost = dict(list(gameDict.items())[0:10])
    for j in list(ownedMost):
        find = False
        for i in range(0,len(Gsamples['applist']['apps'])):
            
            if re.search(r'\b'+ str(j) + r'\b', str(Gsamples['applist']['apps'][i]["appid"])) and find == False :
                find = True
                gameName = Gsamples['applist']['apps'][i]["name"]
                ownedMost[gameName] = ownedMost.pop(j)
    ownedMost = dict(sorted(ownedMost.items(), key = lambda item: item[1], reverse = True))
    mostCommonList = []
    for i in range(0,10):
        #print(i)
        news = main[1].contents[0]
        news1 = re.sub(r"/\?.+", "",news)
        newsparameter = {'appid':list(gameDict.keys())[i],'count':1000,'maxlength':300}
        newsresp = requests.get(news1, newsparameter)
        newsfile = newsresp.text
        newssamples = json.loads(newsfile)
        newsText = []
        gameDescript = list(ownedMost.keys())[i]
        newcounts = newssamples['appnews']['count']
        if newcounts >= 200:
            newcounts = 200
        for j in range(0, newcounts):
            newsText.append(newssamples['appnews']['newsitems'][j]['contents'])

        Descript = ''.join(map(str,newsText))
        uniques = []
        mostCommon = pickCommonWords(Descript, uniques, gameDescript)
        mostCommonList.append(mostCommon)
    print("Most popular games are")
    place = 0
    for k, v in ownedMost.items():
        place+=1
        print(place, k)
        print("  Owned by", v ,"players")
        print("  Game key words: ", end= '') 
        print(*mostCommonList[place-1], sep = ', ')
        
def yes(prompt):
    correct = ["yes",'y','sure','yup','correct','right','true','yep','yeah']
    incorrect = ['no','nope','false']
    if prompt in correct:
        return True
    elif prompt in incorrect:
        return False
    else:
        return None

#def main():

print("Welcome to the Friends network of Steam Application!")
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


load = input("Would you like to use data from a JSON file? ")
if yes(load):
    
    fileName = input('Please input filename:')
    with open(fileName,'r') as jsonFile:
        data = json.load(jsonFile)
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
    print("your input id is: ", myId)
    print("finish loading file!")
else:
    userId = input ("Please input your steam id (17-digits, Default would be my Id): ")
    if len(userId) != 17:
        myId = 76561198112190070
    else:
        myId = userId
    print("your input id is: ", myId)
    print("collecting data from steam...")
    g, List, obj= findFriends(main, myId)
    gameDict, ownedDict, g = findGames(main, g, List, obj)
    print("finish collecting!")
        
        
askAgain = True
while(askAgain):
    print("Please select an option:")
    print("1. Look up for one specific user id and relation")
    print("2. Display the ten users who own the most games")
    print("3. Show the most popular games in your friends")
    print("4. Search the friends network of another user ID")
    print("5. Exit the program")
    choice = input("your choice(1-5): ")    
    if int(choice) == 1:
        findUser = input("The steam id you want to search: ")
        lookUp(findUser, g, myId)
        findStatus(findUser, g, main, Gsamples)
    elif int(choice) == 2:
        print("The top ten users who owned the most games are:")
        ownedDict1 = dict(sorted(ownedDict.items(),key=lambda item: item[1],reverse=True))
        userOwned = dict(list(ownedDict1.items())[0:10])
        place = 0
        for k, v in userOwned.items():
            place += 1
            print(place, " user id:", k, "  Owned", v, "games")
    elif int(choice) == 3:
        print("collecting game data...")
        findPopular(main, gameDict, Gsamples)
    elif int(choice) == 4:
        userId = input ("Please input your steam id (17-digits, Default would be my Id): ")
        if len(userId) != 17:
              myId = 76561198112190070
        else:
            myId = userId
        g, List, obj= findFriends(main, myId)
        gameDict, ownedDict, g = findGames(main, g, List, obj)
    elif int(choice) == 5:
        askAgain = False
    else:
        print("I do not recognize your input")
saveFile = input("Would you like to save record to file? ")
if yes(saveFile):
    classDict = {}
    connectList = []
    for v in g:
        classDict[v.id] = {}
        classDict[v.id]['name'] = v.name
        classDict[v.id]['gamecount'] = v.count
        classDict[v.id]['ownedGame'] = v.games
        classDict[v.id]['recentGame'] = v.recentplayed
        classDict[v.id]['connections'] = {}
        for w in v.getConnections():       
            connectList.append((w.getId(), v.getWeight(w)))
        classDict[v.id]['connections'] = connectList
        connectList = []
    with open('graph.json', 'w') as json_file:
        json.dump(classDict, json_file,indent = 4)
    print('Record save as "graph.json"')
print("Thank you for using the program!")
