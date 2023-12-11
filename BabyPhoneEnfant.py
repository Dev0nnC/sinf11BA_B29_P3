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
        display.scroll('RESTART PLEASE')
        return
        
    nonce = rd.randint(1,999)
    while nonce in usedNonceList:
        nonce = rd.randint(1,999)
    
    usedNonceList.append(nonce)
    return nonce

#configuration radio
radio.on()
radio.config(group=23)

#initialisation de variables du Be:bi
milkDoses = 0
agitationState = 0
oldAgitation = 0
x_Acceleration = accelerometer.get_x()/1000
y_Acceleration = accelerometer.get_y()/1000
z_Acceleration = accelerometer.get_z()/1000
soundLevel = 0
soundState = 0

while True:
    #Identification du Be:bi enfant
    display.show('B')

    #Gestion des doses de lait
    #Ajout d'une dose (bouton A)
    if button_a.is_pressed():
        milkDoses += 1
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        milkUpdate = 'V_m_' + str(milkDoses) + '_' + nonce
        radio.send(encrypt(milkUpdate, key))
        display.scroll(milkDoses)

    #Retrait d'une dose (bouton B)
    if button_b.is_pressed():
        milkDoses = max(0, milkDoses - 1)
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        milkUpdate = 'V_m_' + str(milkDoses)  + '_' + nonce
        radio.send(encrypt(milkUpdate, key))
        display.scroll(milkDoses)

    #consultation des doses (bouton tactile)
    if pin_logo.is_touched():
        display.show(Image.HAPPY)
        display.scroll(milkDoses)


    #Gestion de l'agitation

    #calcul de l'acceleration
    newX_Acceleration = accelerometer.get_x()/1000
    newY_Acceleration = accelerometer.get_y()/1000
    newZ_Acceleration = accelerometer.get_z()/1000

    diffX = abs(newX_Acceleration - x_Acceleration)
    diffY = abs(newY_Acceleration - y_Acceleration)
    diffZ = abs(newZ_Acceleration - z_Acceleration)

    x_Acceleration = newX_Acceleration
    y_Acceleration = newY_Acceleration
    z_Acceleration = newZ_Acceleration
    
    diff = max(diffX, diffY, diffZ)

    #Mise à jour des variables d'agitation. 
    #0 : relativement immobile. 2 : agitation faible. 3 : agitation forte
    if  diff >= 0.4 and diff < 1.5:
        display.show(Image.SQUARE_SMALL)
        sleep(100)
        agitationState = 1
    elif diff >= 1.5:
        agitationState = 2
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
        sleep(100)
    else:
        agitationState = 0
        sleep(100)

    #Envoi de l'etat d'agitation au Be:bi parent (uniquement si l'etat d'agitation est changé)
    if agitationState != oldAgitation:
        nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
        agitationUpdate = 'V_a_' + str(agitationState)  + '_' + nonce
        radio.send(encrypt(agitationUpdate, key))
        oldAgitation = agitationState


    #Gestion du volume sonore a proximité du Be:bi Enfant
    soundLevel = microphone.sound_level()
    if(soundLevel > 80):
        #Affichage et envoi d'une alerte au cas ou le volume dépasse le seuil défini
        if(soundState != 1):
            soundState = 1
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
            nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
            soundUpdate = 'V_s_' + str(soundState)  + '_' + nonce
            radio.send(encrypt(soundUpdate, key))
            sleep(2000)
    else:
        if soundState != 0:
            soundState = 0
            nonce = str(nonceGen(usedNonceList, maxCommunicationNumber))
            soundUpdate = 'V_s_' + str(soundState)  + '_' + nonce
            radio.send(encrypt(soundUpdate, key))
            sleep(2000)

    #Reception de données par radio
    message = radio.receive()
    if message:
        #dechiffrement du message et organisation des données dans une liste 'resultList'
        message = decrypt(message, key)
        resultList = message.split('_')

        #Verification erreur/attaque par rejeu
        if(int(resultList[-1]) in usedNonceList):
            display.show(Image.HEART)
        else:
            #distinction des types de données recues et mise à jour des variables internes.
            #'m' : lait
            if(resultList[1] == 'm'):
                milkDoses = int(resultList[2])
                usedNonceList.append(int(resultList[-1]))
                display.show(Image('09090:'
                                   '90909:'
                                   '90009:'
                                   '09090:'
                                   '00900'))
                sleep(500) 
