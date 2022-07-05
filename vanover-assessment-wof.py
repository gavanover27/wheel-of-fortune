from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random
import collections

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""

def readDictionaryFile():
    global dictionary
    f=open(dictionaryloc)
    dictionary.extend((f.read()).upper().splitlines())
    f.close()
    # Read dictionary file in from dictionary file location
    # Store each word in a list

def readTurnTxtFile():
    global turntext
    h=open(turntextloc)
    turntext = (h.read()).upper()
    h.close()
    #read in turn intial turn status "message" from file

        
def readFinalRoundTxtFile():
    global finalroundtext   
    j=open(finalRoundTextLoc)
    finalroundtext = (j.read()).upper()
    j.close()
    #read in turn intial turn status "message" from file

def readRoundStatusTxtFile():
    global roundstatus
    k=open(roundstatusloc)
    roundstatus = (k.read()).upper()
    k.close()
    # read the round status  the Config roundstatusloc file location 

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location 
    g=open(wheeltextloc)
    wheellist.extend((g.read()).upper().splitlines())
    g.close()
    
def getPlayerInfo():
    global players
    # read in player names from command prompt input
    players[0]['name'] = str(input("Enter Player 0's Name: ").upper())
    players[1]['name'] = str(input("Enter Player 1's Name: ").upper())
    players[2]['name'] = str(input("Enter Player 2's Name: ").upper())

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    global roundWord
    global blankWord
    #choose random word from dictionary
    roundWord = str(random.choice(dictionary))
    #make a list of the word with underscores instead of letters.
    blankWord = list('_' for i in roundWord)

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    # Return the starting player number (random)
    initPlayer = random.choice(range(0,3))
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    getWord()

    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    goodGuess = None
    # Get the Player Number
    # Get random value for wheellist
    wheelvalue = random.choice(wheellist)
    # Check for bankruptcy, and take action.
    if wheelvalue == "BANKRUPT":
        players[playerNum]['roundtotal'] = 0
        print("Sorry, you went BANKRUPT!")
        goodGuess = False
    # Check for lose a turn
    elif wheelvalue == "LOSE A TURN":
        print("Sorry, you've lost your turn!")
        goodGuess = False
    # Get amount from wheel if not lose turn or bankruptcy
    else:
        print(f'The wheel landed on ${wheelvalue}!')
        guess = input("What letter would you like to guess?: ").upper()
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
        goodGuess, count = guessletter(guess, playerNum)
        players[playerNum]['roundtotal'] += (count * int(wheelvalue))
        players[playerNum]['gametotal'] += (count * int(wheelvalue))
    # Change player round total if they guess right.     
    return goodGuess


def guessletter(guess, playerNum): 
    global players
    global blankWord
    global vowels
    goodGuess = None
    count = 0
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore
    # Make sure the guess is a consonant
    if guess.isalpha() == False:
        print("Please guess a consonant")
    elif guess.lower() in vowels:
        print("Please guess a consonant.")
    elif guess in list(roundWord):
        goodGuess = True
        count = int(collections.Counter(roundWord)[guess])
        blankWord[list(roundWord).index(guess)] = guess
        print(blankWord)
    else:
        print(f"{guess} is not in the word!")
        goodGuess = False
        count = 0
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    goodGuess = None
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    if players[playerNum]['roundtotal'] >=250:
        players[playerNum]['roundtotal'] -= 250
        players[playerNum]['gametotal'] -= 250
        vowelguess = input("Enter a vowel: ").upper()
        if vowelguess.lower() not in vowels:
            print("Please guess a vowel.")
        elif vowelguess in list(roundWord):
            guessAgain = False
            goodGuess = True
            if vowelguess in list(roundWord):
                blankWord[list(roundWord).index(vowelguess)] = vowelguess
                print(blankWord)
        else:
            print(f"{vowelguess} is not in the word!")
            guessAgain = False
            goodGuess = False
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    else:
        print("Sorry, you can't afford to buy a vowel!")
    
    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    wordGuess = input("Enter a word: ").upper()
    if wordGuess == roundWord:
        blankWord = roundWord
        print(f"Congrats, the word was {roundWord}, you are correct!")
    # Fill in blankList with all letters, instead of underscores if correct 
    if wordGuess != roundWord:
        print("Sorry, that is incorrect.")
    # return False ( to indicate the turn will finish)  
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players
    # take in a player number.
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    print(f"It is player {playerNum}'s turn.")
    stillinTurn = True
    while stillinTurn:
        choice = input("Would you like to (S)pin the wheel, (B)uy vowel, or (G)uess the word: ")
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")     
    # Check to see if the word is solved, and return false if it is,
    if '_' in blankWord:
        return True
    else:
        return False
    # Or otherwise break the while loop of the turn.     

def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    unsolved = True
    print(blankWord)
    while unsolved:
        for i in range(0,3):
            unsolved = wofTurn(i)
            if unsolved == False:
                break

    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    winningPlayer = max(players, key=lambda v: int(players[v]['gametotal']))
    print(f'Player {winningPlayer} is going on to the final round!')
    print(finalroundtext)
    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    getWord()
    print(blankWord)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    finalRoundGivens = {'R','S','T','L','N'}
    for i in finalRoundGivens:
        guessletter(i, winningPlayer)
    if "E" in list(roundWord):
        blankWord[list(roundWord).index('E')] = 'E'
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(blankWord)
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    finalConsonantss = list(input("Enter 3 consonants: ").upper())
    for i in finalConsonantss:
        guessletter(i, winningPlayer)
    finalVowel = input("Enter 1 vowel: ").upper()
    if finalVowel in list(roundWord):
        blankWord[list(roundWord).index(finalVowel)] = finalVowel
    # Print out the current blankWord again
    print(blankWord)
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    finalWordGuess = input("Enter your final word guess: ").upper()
    if finalWordGuess == roundWord:
        blankWord = roundWord
        players[winningPlayer]['gametotal'] += finalprize
        print(f"Congrats, the word was {roundWord}, you are correct! You win ${players[winningPlayer]['gametotal']}!")
    # Fill in blankList with all letters, instead of underscores if correct 
    if finalWordGuess != roundWord:
        print(f"Sorry, that is incorrect. You still win {players[winningPlayer]['gametotal']}")
    # If they do, add finalprize and gametotal and print out that the player won 


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            players[0]['roundtotal'] = 0
            players[1]['roundtotal'] = 0
            players[2]['roundtotal'] = 0
            print(f"We are now starting round {i + 1}")
            wofRound()
            print(roundstatus.format(ROUNDNUM = i+1))
            print(players)
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
