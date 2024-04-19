import os
from .logic import makeAPIRequestFreshSystem
from .logic import makeAPIRequestFreshSystemTurbo

def adjustLength(inputString):
    space_count = len(inputString.split())

    with open(speechTooLongFile, 'r') as file:
        speechTooLong = file.read()
    with open(speechTooShortFile, 'r') as file:
        speechTooShort = file.read()
    outputString = inputString
    print("speech is currently " + str(space_count)+ " before adjustment")
    if space_count > 1400:
        outputString = makeAPIRequestFreshSystem(speechTooLong, inputString)
        print("Speech made shorter")
        adjustLength(outputString)
    if space_count < 1100:
        outputString = makeAPIRequestFreshSystem(speechTooShort+str(space_count), inputString)
        print("Speech made longer")
        adjustLength(outputString)

    return outputString


speechTooLongFile = os.getcwd() + '/VapYapDjango/prompts/length/speechTooLong.txt'
speechTooShortFile = os.getcwd() + '/VapYapDjango/prompts/length/speechTooShort.txt'
