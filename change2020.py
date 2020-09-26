"""

@author: Kwame Ampadu-Boateng

"""
import requests
import random
import time


# This class is used in order to make a request using my Bearer Token
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


# This method return the json object of the last 3200 tweets of a user
def getJson(user, count=3200):
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='
    url += user
    url += '&count=' + str(count)
    response = requests.get(url, auth=BearerAuth(
        'AAAAAAAAAAAAAAAAAAAAAKyyHwEAAAAABAnig801%2FLZrGQ2Ta5hT9Sog4pg%3DJpWSr'
        + '583RYptt4TMttnz2I8IFb23EPrnqptRDNwIstIsIC2ktx'))
    return response.json()


# This methods checks each tweet in the json object to make sure that it does 
# not contain a link or an @, if it does not then the tweet is added into an 
# array of acceptable  tweets
def filterJson(json):
    realResponse = []
    for i in range(len(json)):
        if "@" not in json[i]['text'] and "https" not in json[i]['text']:
            realResponse.append(json[i]['text'])
    return realResponse


# This method gets a random tweet from the array of acceptable tweets
def getTweet(tweetList):
    index = random.randrange(len(tweetList))
    tweet = tweetList[index]
    # We pop because we do not want to give to tweet back to the user
    tweetList.pop(index)
    return tweet


if __name__ == "__main__":
    character1 = 'elonmusk'
    character2 = 'kanyewest'
    print("You will be playing a guessing game. You will get a random tweet " +
          "from 2 people and you have to choose which one the tweets " +
          f"belongs to. The people for this game are {character1} and " +
          f"{character2}.")
    print()
    
    char1List = getJson('elonmusk')
    char2List = getJson('kanyewest')
    
    char1List = filterJson(char1List)
    char2List = filterJson(char2List)
    correct, total = 0, 0
    
    print()
    print("Get ready to play!!!")
    print()
    time.sleep(5)
    
    # Continue with the game until one of the arrays is empty
    while len(char1List) > 0 and len(char2List) > 0:
        # choose from one of the characters to display the tweet
        chooseChar = random.randrange(1, 3) 
        if chooseChar == 1:
            displayTweet = getTweet(char1List)
        else:
            displayTweet = getTweet(char2List)
        print(displayTweet)
        
        userChoice = input(
            f"Whose tweet is this? The choices are {character1} or {character2}.\t")
        if ((userChoice.lower() == character1.lower() and chooseChar == 1)
                or (userChoice.lower() == character2.lower() and chooseChar == 2)):
            print("\nCorrect!!!")
            correct += 1
            total += 1
        else:
            print("Sorry incorrect. \t :(")
            total += 1
            
        doQuit = input("If you want to quit now type Q or Quit\t")
        print()
        print("="*30)
        print()
        if doQuit.lower() == "q" or doQuit.lower() == "quit":
            break
        
    print("Thank you for playing!!!")
    print(
        f"Your stats for this round were {(correct/total) * 100:.4}% correct")
