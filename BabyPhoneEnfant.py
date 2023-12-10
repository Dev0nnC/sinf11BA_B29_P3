from microbit import *
import radio
import random as rd
import music

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

#nonce
usedNonceList = []
maxCommunicationNumber = 9999
def nonceGen(usedNonceList, maxCommunicationNumber):
    if len(usedNonceList) > maxCommunicationNumber - 1:
        display.scroll('RESTART PLEASE')
        return
        
    nonce = rd.randint(1,maxCommunicationNumber)
    while nonce in usedNonceList:
        nonce = rd.randint(1,maxCommunicationNumber)
    
    usedNonceList.append(nonce)
    return nonce

#initialisation de variables du babyphone
milkDoses = 0
agitationState = 0
OldtotalStrength = 0

x_strength = accelerometer.get_x()/1000
y_strength = accelerometer.get_y()/1000
z_strength = accelerometer.get_z()/1000

while True:
    
    if button_a.is_pressed():
        milkDoses += 1
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        milkUpdate = 'V_m_' + str(milkDoses) + '_' + nonce
        radio.send(crypt(milkUpdate, key))
        display.scroll(milkDoses)

    if button_b.is_pressed():
        milkDoses = max(0, milkDoses - 1)
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        milkUpdate = 'V_m_' + str(milkDoses)  + '_' + nonce
        radio.send(crypt(milkUpdate, key))
        display.scroll(milkDoses)
        
    if pin_logo.is_touched():
        display.show(Image.HAPPY)
        display.scroll(milkDoses)

    
    newX_Strength = accelerometer.get_x()/1000
    newY_Strength = accelerometer.get_y()/1000
    newZ_Strength = accelerometer.get_z()/1000

    diffX = abs(newX_Strength - x_strength)
    diffY = abs(newY_Strength - y_strength)
    diffZ = abs(newZ_Strength - z_strength)

    x_strength = newX_Strength
    y_strength = newY_Strength
    z_strength = newZ_Strength
    
    diff = max(diffX, diffY, diffZ)

    if  diff >= 0.4 and diff < 1.5:
        display.show(Image.SQUARE_SMALL)
        sleep(100)
        agitationState = 1
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        agitationUpdate = 'V_a_' + str(agitationState)  + '_' + nonce
        radio.send(crypt(agitationUpdate, key))
    elif diff >= 1.5:
        display.show(Image.SQUARE)
        sleep(100)
        music.play(music.BA_DING)
        agitationState = 2
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        agitationUpdate = 'V_a_' + str(agitationState)  + '_' + nonce
        radio.send(crypt(agitationUpdate, key))

    
    message = radio.receive()
    if message:
        message = decrypt(message, key)
        #display.scroll(message)
        if(message[2] == 'm'):
            milkDoses = int(message[4])
            #display.scroll('Milk Update = ' + message[4])
            #display.scroll('Full : ' + message[-1])
            usedNonceList.append(int(message[-1]))
        elif (message[2] == 'a'):
            agitationState = int(message[4])
            #display.scroll('Agitation Update = ' + message[4])
            #display.scroll('Full : ' + message)
            if(message[4] == 1):
                agitationState = 1
            elif(message[4] == 2):
                agitationState = 2   
            usedNonceList.append(int(message[-1]))

    #USER INTERFACE
    if(agitationState ==0):
        display.show(Image.HOUSE)
    elif(agitationState == 1):
        display.show(Image.SMILE)
    elif(agitationState == 2):
        display.show('! ! ! !')
        music.play(music.BA_DING)
    
        
    
