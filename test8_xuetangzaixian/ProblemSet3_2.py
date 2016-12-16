'''
def isWordGuessed(secretWord,lettersGuessed):
    index=0
    secretWord = set(secretWord)
    lettersGuessed = set(lettersGuessed)
    for i in lettersGuessed:
        if i in secretWord:
            index += 1
    if index == len(secretWord):
        return True
    else:
        return False
    
def getGuessedWord(secretWord, lettersGuessed):
    SetlettersGuessed = set(lettersGuessed)
    dlist = ['_']* len(secretWord)
    
    for i in SetlettersGuessed:
        if i in secretWord:
            for char in xrange(len(secretWord)):
                if i == secretWord[char]:
                    dlist[char] = i
    ans = ''
    for i in xrange(len(dlist)):
        if dlist[i] == '_':
            dlist[i] = '_ '
    for i in dlist:
        ans += i
    return ans
'''
def getAvailableLetters(lettersGuessed):
    import string
    dlist = []
    for i in string.ascii_lowercase:
        dlist.append(i)
    SetlettersGuessed = set(lettersGuessed)
    for i in SetlettersGuessed:
        if i in dlist:
            dlist.remove(i)
    l = ''
    for i in dlist:
        l += i
    return l

def compare(newchar,secretWord,ans):
    if newchar in secretWord:
        for char in xrange(len(secretWord)):
            if newchar == secretWord[char]:
                ans[char] = newchar
        print'Good guess:',formatAns(ans)
        return ans
    else :
        print'Oops! That letter is not in my word:',formatAns(ans)
        return ans
    
        
def formatAns(dlist):
    for i in xrange(len(dlist)):
        if dlist[i] == '_':
            dlist[i] = '_ '
    ans = ''
    for i in dlist:
        ans += i
    return ans


from ps3_hangman import loadWords,chooseWord

WORDLIST_FILENAME = "words.txt"



def hangman(secretWord):
    print('Welcome to the game, Hangman!')
    print('I am thinking of a word that is %s letters long.' % len(secretWord)) 
    print('-'*10)
    lettersGuessed = []
    mistakesMade = 0
    ans = ['_']*len(secretWord)
    
    while True:
        print('You have %d guesses left.' % (8-mistakesMade))
        print'Available letters: ',getAvailableLetters(lettersGuessed)
        
        newchar = raw_input('Please guess a letter:').lower()
        
        if newchar not in lettersGuessed:
            lettersGuessed.append(newchar)
            ans = compare(newchar,secretWord,ans)
            mistakesMade += 1

        else :
            print"Oops! You've already guessed that letter:",formatAns(ans)

        
        print'-'*10
        
        if 8-mistakesMade <= 0:
            print'Sorry, you ran out of guesses. The word was %s.' % secretWord
            break
        
        if formatAns(ans) == secretWord:
            print('Congratulations, you won!')
            break
        
        
if __name__ == '__main__':
    #print(isWordGuessed('grapefruit',['z', 'x', 'q', 'g', 'r', 'a', 'p', 'e', 'f', 'r', 'u', 'i', 't']))
    #print(getGuessedWord('apple',['e', 'i', 'k', 'p', 'r', 's']))
    #print(getAvailableLetters(['e', 'i', 'k', 'p', 'r', 's']))
    secretWord = chooseWord(loadWords())
    print secretWord
    hangman('apple')