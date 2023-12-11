from microbit import *
import radio
import random as rd
import music

key = 'cledechiffrementassezlongue'

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
def encrypt(textToEncrypt, key):
    encrypted = []
    for element in range(len(textToEncrypt)):
        currentLetterIndex = lettersToNumbersF(textToEncrypt[element])
        getCurrentKey = lettersToNumbersF(key[element])
        
        if textToEncrypt[element] in alphabet:
            nextLetter = str(vigenere[getCurrentKey[0]][currentLetterIndex[0]])
        
        elif textToEncrypt[element].isdigit():
            transformedIntoVigenereLetter = str(vigenere[getCurrentKey[0]][int(textToEncrypt[element])])
            nextLetter = str(lettersToNumbersF(transformedIntoVigenereLetter)[0])
        else:
            nextLetter = str(textToEncrypt[element])

        encrypted.append(nextLetter)
        
        encryptedStr = ''
        for char in range(len(encrypted)):
            encryptedStr += encrypted[char]
            if char < len(encrypted) - 1:
                encryptedStr += '--'

    return encryptedStr

# FONCTION DE DECHIFFREMENT
def decrypt(encryptedMessageStr, key):
    encryptedMessage = encryptedMessageStr.split('--')
    realText = []
    for i in range(len(encryptedMessage)):
        column = 0
        line = lettersToNumbersF(key[i])[0]
        if encryptedMessage[i] in alphabet:
            for element in vigenere[line]:
                if element != encryptedMessage[i]:
                    column += 1
                else:
                    break
            nextLetter = vigenere[0][column]
            
        elif encryptedMessage[i].isdigit():
            notANumber = alphabetFromNumbers[int(encryptedMessage[i])]
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
            nextLetter = encryptedMessage[i]
        
        realText.append(nextLetter)
        
        realTextStr = ''
        for char in realText:
            realTextStr += str(char)

    return realTextStr

#nonce
usedNonceList = []
maxCommunicationNumber = 999
def nonceGen(usedNonceList, maxCommunicationNumber):
    if len(usedNonceList) > maxCommunicationNumber - 1:
        #nombre maximal de communications atteinte
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
soundLevel = 0

#configuration radio
radio.on()
radio.config(group=23)

while True:
    #Gestion des doses de lait

    #Ajout d'une dose
    if button_a.is_pressed():
        milkDoses += 1
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        milkUpdate = 'V_m_' + str(milkDoses) + '_' + nonce
        radio.send(encrypt(milkUpdate, key))
        display.scroll(milkDoses)

    #retrait d'une dose
    if button_b.is_pressed():
        milkDoses = max(0, milkDoses - 1)
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        milkUpdate = 'V_m_' + str(milkDoses)  + '_' + nonce
        radio.send(encrypt(milkUpdate, key))
        display.scroll(milkDoses)

    #consultation des doses
    if pin_logo.is_touched():
        display.scroll(milkDoses)

    #Reception d'information du Be:bi enfant
    message = radio.receive()
    if message:
        #decryptage et organisation des données dans une liste 'resultList'
        message = decrypt(message, key)
        resultList = message.split('_')

        #verification d'erreur/attaque par rejeu
        if(resultList[-1] in usedNonceList):
            display.show(Image.HEART)
        else:
            #identification du type de donnée recue + mise à jour des données internes. 
            #'m' : lait ; 'a' : agitation ; 's' : niveau sonore
            if(resultList[1] == 'm'):
                milkDoses = int(resultList[2])
                usedNonceList.append(int(resultList[-1]))
                display.show(Image('09090:'
                                   '90909:'
                                   '90009:'
                                   '09090:'
                                   '00900'))
                sleep(500)
                
            elif (resultList[1] == 'a'):
                agitationState = int(resultList[2])
                usedNonceList.append(int(resultList[-1]))
                
            elif (resultList[1] == 's'):
                soundLevel = int(resultList[2])
                usedNonceList.append(int(resultList[-1]))

    #USER INTERFACE
    #Interraction utilisateur - machine
    if(agitationState ==0):
        display.show(Image.HOUSE)
        
    elif(agitationState == 1):
        display.show(Image.SQUARE_SMALL)
        
    elif(agitationState == 2):
        music.play(music.BA_DING)
        animationCount = 0
        while animationCount < 5:
            display.show(Image('00000:'
                               '00000:'
                               '00900:'
                               '00000:'
                               '00000'))
            sleep(100)
            display.show(Image('00000:'
                               '09990:'
                               '09790:'
                               '09990:'
                               '00000'))
            sleep(100)
            display.show(Image('99999:'
                               '97779:'
                               '97579:'
                               '97779:'
                               '99999'))
            sleep(100)
            display.show(Image('99999:'
                               '95559:'
                               '95359:'
                               '95559:'
                               '99999'))
            sleep(50)
            display.show(Image('99999:'
                               '93339:'
                               '93039:'
                               '93339:'
                               '99999'))
            sleep(50)
            display.show(Image('77777:'
                               '79997:'
                               '79097:'
                               '79997:'
                               '77777'))
            sleep(50)
            display.show(Image('55555:'
                               '59995:'
                               '59095:'
                               '59995:'
                               '55555'))
            sleep(100)
            
            animationCount +=1
        music.play(music.BA_DING)

    if(soundLevel == 1):
        music.play(music.JUMP_UP)
        animationCount = 0
        while animationCount < 5:
            display.show(Image('11111:'
                               '00001:'
                               '33301:'
                               '00301:'
                               '70301'))
            sleep(200)
            display.show(Image('33333:'
                               '00003:'
                               '77703:'
                               '00703:'
                               '70703'))
            sleep(200)
            display.show(Image('99999:'
                               '00009:'
                               '88809:'
                               '00809:'
                               '70809'))
            sleep(200)
            animationCount += 1
        display.scroll('Loud noises')
        sleep(2000)
