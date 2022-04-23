# SI507Project
SI507 Final Project Steam Friends Network
The Steam API keys can be obtained from steam link: https://steamcommunity.com/dev

The API keys can be used to fetch user public information, achievenmtns, apps news, and etc steam services.
Two frequently weblink for steam cashing are: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_.28v0001.29
and https://partner.steamgames.com/doc/api

Every steam user account has a corresponding user id. Using both API key and user id to fetch desired data.
Be awared that each steam API keys have a limit of 100,000 calls per day. No permission after exceeding the limit that day.
Only needs two simple packages, beautiful soup and requests, are needed to run my code. 
