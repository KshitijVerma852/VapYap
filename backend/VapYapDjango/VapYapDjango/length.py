import os
import array
from .logic import makeAPIRequestFreshSystem
from .logic import makeAPIRequestFreshSystemTurbo

def split_into_paragraphs(text):
    paragraphs = text.strip().split('\n')
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]
    return paragraphs

def join_paragraphs(paragraphs):
    return '\n\n'.join(paragraphs)

def adjustLength(inputString):
    space_count = len(inputString.split())

    with open(speechTooLongFile, 'r') as file:
        speechTooLong = file.read()
    with open(speechTooShortFile, 'r') as file:
        speechTooShort = file.read()
    outputString = inputString
    print("speech is currently " + str(space_count)+ " before adjustment")
    if space_count > 950:
        paragraphs = split_into_paragraphs(inputString)
        newParagraphs = []
        for paragraph in paragraphs:
            newParagraphs.append(makeAPIRequestFreshSystemTurbo(speechTooLong, paragraph))
        outputString = join_paragraphs(newParagraphs)
        print("Speech made shorter")
        adjustLength(outputString)
    if space_count < 850:
        paragraphs = split_into_paragraphs(inputString)
        newParagraphs = []
        for paragraph in paragraphs:
            newParagraphs.append(makeAPIRequestFreshSystemTurbo(speechTooShort, paragraph))
        outputString = join_paragraphs(newParagraphs)
        print("Speech made longer")
        adjustLength(outputString)
    return outputString


speechTooLongFile = os.getcwd() + '/VapYapDjango/prompts/length/speechTooLong.txt'
speechTooShortFile = os.getcwd() + '/VapYapDjango/prompts/length/speechTooShort.txt'
