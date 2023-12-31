from microbit import *
import radio
radio.on()
radio.config(group=23)

textToEncrypt = 'un assez long texte 18973 avec des chiffres'
key0 = 'cledechiffrement'

def generateKey(key0, textToEncrypt):
    keyLength = abs(len(textToEncrypt) - len(key0))
    key = key0
    for i in range(keyLength):
        if i < len(key):
            j = i
        else:
            j = i - int(i/len(key)) * len(key)
            
        key += key[j]
    return key

key = generateKey(key0, textToEncrypt)

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# CREATION DE TABLE VIEGENERE
vigenere0 = [alphabet]
for i in range(len(alphabet)-1):
    lastList = vigenere0[-1]
    newlist = lastList[1:]
    newlist.append(lastList[0])
    vigenere0.append(newlist)

vigenere = [list(row) for row in vigenere0]

# CREATION DES FONCTIONS DE TRADUCTIONS
alphabetIndexes = list(range(len(alphabet)))
alphabetFromNumbers = dict(zip(alphabetIndexes, alphabet))
numbersFromAlphabet = dict(zip(alphabet, alphabetIndexes))

def lettersToNumbersF(textToTranslate):
    numberTextList = []
    for TextChar in textToTranslate:
        if TextChar in alphabet: 
            numberTextList.append(numbersFromAlphabet.get(TextChar))
        else:
            numberTextList.append(TextChar)
    return numberTextList

def numbersToLettersF(textToTranslate):
    letterTextList = []
    for TextChar in textToTranslate:
        TextChar = int(TextChar)
        if (TextChar) in alphabetIndexes:
            letterTextList.append(alphabetFromNumbers.get(TextChar))
        else:
            letterTextList.append(TextChar)
    return letterTextList

# FONCTION DE CHIFFREMENT
def crypt(textToCrypt, key):
    crypted = []
    for element in range(len(textToCrypt)):
        currentLetterIndex = lettersToNumbersF(textToCrypt[element])
        getCurrentKey = lettersToNumbersF(key[element])
        
        if textToCrypt[element] in alphabet:
            nextLetter = str(vigenere[getCurrentKey[0]][currentLetterIndex[0]])
        
        elif textToCrypt[element].isdigit():
            transformedIntoVigenereLetter = str(vigenere[getCurrentKey[0]][int(textToCrypt[element])])
            nextLetter = str(lettersToNumbersF(transformedIntoVigenereLetter)[0])
        else:
            nextLetter = str(textToCrypt[element])

        crypted.append(nextLetter)
        
        cryptedStr = ''
        for char in range(len(crypted)):
            cryptedStr += crypted[char]
            if char < len(crypted) - 1:
                cryptedStr += '--'

    return cryptedStr

# FONCTION DE DECHIFFREMENT
def decrypt(cryptedMessageStr, key):
    cryptedMessage = cryptedMessageStr.split('--')
    realText = []
    for i in range(len(cryptedMessage)):
        column = 0
        line = lettersToNumbersF(key[i])[0]
        if cryptedMessage[i] in alphabet:
            for element in vigenere[line]:
                if element != cryptedMessage[i]:
                    column += 1
                else:
                    break
            nextLetter = vigenere[0][column]
            
        elif cryptedMessage[i].isdigit():
            notANumber = alphabetFromNumbers[int(cryptedMessage[i])]
            column = 0
            line = lettersToNumbersF(key[i])[0]
            for element in vigenere[line]:
                if element != notANumber:
                    column += 1
                else:
                    break
            fakeLetter = vigenere[0][column]
            nextLetter = numbersFromAlphabet[fakeLetter]
            
        else:
            nextLetter = cryptedMessage[i]
        
        realText.append(nextLetter)
        
        realTextStr = ''
        for char in realText:
            realTextStr += str(char)

    return realTextStr

#initialisation de variables du babyphone
milkDoses = 0
agitationState = 0

while True:
    #Microbit Name Display
    display.show(Image.HOUSE)
    
    if button_a.is_pressed():
        milkDoses += 1
        milkUpdate = 'V_m_' + str(milkDoses)
        radio.send(crypt(milkUpdate, key))
        display.scroll(milkDoses)

    if button_b.is_pressed():
        milkDoses = max(0, milkDoses - 1)
        milkUpdate = 'V_m_' + str(milkDoses)
        radio.send(crypt(milkUpdate, key))
        display.scroll(milkDoses)
        
    if pin_logo.is_touched():
        display.show(Image.HAPPY)
        display.scroll(milkDoses)
        
    message = radio.receive()
    if message:
        message = decrypt(message, key)
        #display.scroll(message)
        if(message[2] == 'm'):
            milkDoses = int(message[4])
            display.scroll('Milk Update = ' + message[4])
    
