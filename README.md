# SI507Project
SI507 Final Project Steam Friends Network
The Steam API keys can be obtained from steam link: https://steamcommunity.com/dev

The API keys can be used to fetch user public information, achievenmtns, apps news, and etc steam services.
Two frequently weblink for steam cashing are: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_.28v0001.29
and https://partner.steamgames.com/doc/api

Every steam user account has a corresponding user id. Using both API key and user id to fetch desired data.
Be aware that each steam API keys have a limit of 100,000 calls per day. No permission after exceeding the limit that day.
Only needs two simple packages, beautiful soup and requests, are needed to run my code. 

The first layer of the graph network contains the friends on the friend list of a user’s account. The second layer would be the friends of the users’ friends. As more layers added, the number of users would be increased in power function. Each vertex represents a class object which contains user’s friend’s id, their status, and owned games stats, so it is possible to count all the games and rate the most popular games and top players in this graph network. 

•FinalProj.py contains loading, constructing and outputing the graph data structure.

•graphs.py contains the class variable for vertex and graph.

•construct.py provide the code for loading JSON file and construct graph data structure.

•readJSON.py dumps the graph data structure to graph.json.
