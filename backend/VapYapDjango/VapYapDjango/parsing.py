import json
import os
import threading
from django.http import JsonResponse, HttpRequest
from .length import adjustLength
from .summarize import broadSummary
from .summarize import broadSummaryOpponents
from .summarize import broadSummaryOpponentsAttacks
from .logic import makeAPIRequestFreshSystem
from .logic import makeAPIRequestFreshSystemTurbo
from django.views.decorators.csrf import csrf_exempt

positionToOrderOfSpeeches = {
    "OG": ["PM", "DPM"],
    "OO": ["LO", "DLO"],
    "CG": ["MG", "GW"],
    "CO": ["MO", "OW"]
}
orderOfSpeeches = ["PM", "LO", "DPM", "DLO", "MG", "MO", "GW", "OW"]
speechNumberIndex = 0


def initializeFormData(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        return data.get("motion"), data.get("infoSlide"), data.get("position")


def fetchNextSpeechFromFrontend(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        return data.get("title"), data.get("content")


@csrf_exempt
def returnJSONObject(request: HttpRequest):
    useFrontend = True

    print("Start running")

    motion = ("This House believes that democratic states should grant an amnesty to whistleblowers who expose "
              "unethical practices in the government.")
    infoSlide = ""
    position = "OG"
    content = ""
    title = ""

    if useFrontend:
        motion, infoSlide, position = initializeFormData(request)
        
        if infoSlide is None:
            debateWelcomeInfo = f"You are a British Parliamentary debater. You are debating the motion {motion}. You are set to represent the {position} position."
        else:
            debateWelcomeInfo = f"You are a British Parliamentary debater. You are debating the motion {motion}. The info slide reads: {infoSlide}. You are set to represent the {position} position."

        brainStormedIdeas = brainStormArguments(debateWelcomeInfo)


        for speechType in orderOfSpeeches:
            if speechType in positionToOrderOfSpeeches[position]:
                makeSpeech(debateWelcomeInfo, brainStormedIdeas, speechType)
            else:
                title, content = fetchNextSpeechFromFrontend(request)
                with open(f"content/input/{title.upper()}.txt", "w") as speechFile:
                    speechFile.write(title)
                    speechFile.write(content)

            parse_RawArguments(rawDebateInput + speechType + "Speech", rawDebateOutput)
            clean_RawArguments(rawDebateOutput, cleanDebateOutput)
            answerArguments(cleanDebateOutput, answerDebateOutput)

    return JsonResponse({"ai_response": "dfdai_response"})

def makeSpeech(debateWelcomeInfo, brainStormedIdeas, speechNeeded):

    if speechNeeded in ("OG", "LO", "MG", "MO"):
        caseGeneration(debateWelcomeInfo, brainStormedIdeas, speechNeeded)
        if speechNeeded in ("OG", "LO"):
            return
        else:
            brainStormBroadAnswers(debateWelcomeInfo, speechNeeded)
            if speechNeeded == "MG":
                read_file(MGCaseOutput)
                finalSpeech = formalize(debateWelcomeInfo, read_file(MGCaseOutput)+ " " + read_file(answerBroadDebateOutput))
                write_file(MGSpeechOutput, finalSpeech)
            if speechNeeded == "MO":
                read_file(MOCaseOutput)
                finalSpeech = formalize(debateWelcomeInfo, read_file(MOCaseOutput)+ " " + read_file(answerBroadDebateOutput))
                write_file(MOSpeechOutput, finalSpeech)

    elif speechNeeded in ("GW", "OW", "DPM", "DLO"):
        print("HGi")
    
def formalize(debateWelcomeInfo, content):
    adjustedContent = adjustLength(content)
    finalSpeech = makeAPIRequestFreshSystemTurbo(debateWelcomeInfo, "This speech is almost ready to ouput. Make sure that everything looks ok. The speech should be ready for me to read verbatim, so make sure that there is no refrences to what I was thinking when I decided to make these arguments. Intead, focus on making the arguments themselves in the debate" ,adjustedContent)
    return finalSpeech
def caseGeneration(debateWelcomeInfo, brainStormedIdeas, speechNeeded):

    if speechNeeded == "PM":

        PMMessage = read_file(PMCaseGeneration)
        PM = makeAPIRequestFreshSystem(debateWelcomeInfo, PMMessage, brainStormedIdeas)
        
        lengthAdjustedPM = adjustLength(PM)
        write_file(PMOutput, lengthAdjustedPM)

        print(f"PM Case has been written to {PMOutput}")

    elif speechNeeded == "LO":
        LOMessage = read_file(LOCaseGeneration)

        json_data = read_json(cleanDebateOutput)
        pm_speeches = json_data['PM']
        definitions = [speech['text'] for speech in pm_speeches if speech.get('type') == 'definition']

        if definitions:
            defintionsInfo = "The key definitions from the OG speech were: " + ", ".join(definitions)
            LO = makeAPIRequestFreshSystem(debateWelcomeInfo, LOMessage, brainStormedIdeas + defintionsInfo)
        else:
            LO = makeAPIRequestFreshSystem(debateWelcomeInfo, LOMessage , brainStormedIdeas)

        lengthAdjustedLO = adjustLength(LO)
        write_file(LOOutput, lengthAdjustedLO)

        print(f"LO Case has been written to {LOOutput}")

    elif speechNeeded in ("MG", "MO"):
        speechSpecifcInfo = "You are on the team of {speechNeeded}"
        summaryInfo = "The summary of the debate so far speech by speech is: " + broadSummary()

        MGMOCaseDecisionMessage = read_file(MGMOCaseDecision)
        MGMOCaseGenerationMessage = read_file(MGMOCaseGeneration)

        MGMOCaseDecisionOutput = makeAPIRequestFreshSystem(debateWelcomeInfo, speechSpecifcInfo , MGMOCaseDecisionMessage, summaryInfo)

        print("The MG/MO case decision has been made")

        MGMOCase = makeAPIRequestFreshSystem(debateWelcomeInfo,speechSpecifcInfo ,MGMOCaseGenerationMessage, MGMOCaseDecisionOutput, summaryInfo)
        if speechNeeded == "MG":
            write_file(MGCaseOutput, MGMOCase)
            print(f"MG Case has been written to {MGCaseOutput}")

        if speechNeeded == "MO":
            write_file(MOCaseOutput, MGMOCase)
            print(f"MO Case has been written to {MOCaseOutput}")


    else:
        print("Invalid speech type")


def brainStormArguments(debateInfo):
    brainStormMessage = read_file(BrainStormMessageFile)
    brainStormedIdeas = makeAPIRequestFreshSystem(
        brainStormMessage, debateInfo)
    write_file(BrainStormOutput, brainStormedIdeas)
    print(f"Brainstorming has been written to {BrainStormMessageFile}")


def brainStormBroadAnswers(debateWelcomeInfo, position):
    
    summaryOpponentsInfo = "The summary of the opponents cases so far is: " + broadSummaryOpponents(position)
    broadAnswersMessage = read_file(answerBroadMessageFile)
    
    broadAnswers = makeAPIRequestFreshSystem(
        debateWelcomeInfo, broadAnswersMessage, summaryOpponentsInfo)
    
    write_file(answerBroadDebateOutput, broadAnswers)
    print("Broad answers have been written to {answerBroadDebateOutput}")
    return

def frontline (debateWelcomeInfo, position): 

    summaryOpponentsInfo = "The opponents have made the following arguments against us  " + broadSummaryOpponentsAttacks(position)
    frontLineMessage = read_file(frontLineMessage)
    
    frontlines = makeAPIRequestFreshSystem(
        debateWelcomeInfo, frontLineMessage, summaryOpponentsInfo)
    
    write_file(frontlineOutputFile, frontlines)
    print("Broad answers have been written to {frontlineOutputFile}")
    return

def evalValueOfAnswers():
    welcomeInfo = "You are a British Parli debater on the team of {position}"
    broadSummaryInfo = "The summary of the debate so far speech by speech is: " + broadSummary()
    broadAnswers = read_file(answerBroadDebateOutput)

    return


def clean_RawArguments(input_filename, output_filename):
    data = read_json(input_filename)
    cleanMessage = read_file(cleanMessageFile)

    clean_data = {}
    for speech_type, arguments in data.items():
        clean_data[speech_type] = [{
            'text': makeAPIRequestFreshSystemTurbo(cleanMessage, arg['text']),
            'strength': arg['strength']
        } for arg in arguments]

    write_json(output_filename, clean_data)
    print(f"Clean data has been written to {output_filename}")


def answerArguments(input_filename, output_filename):
    data = read_json(input_filename)
    answerMessage = read_file(answerMessageFile)
    clean_data = {}
    for speech_type, arguments in data.items():
        clean_data[speech_type] = [{
            'text': makeAPIRequestFreshSystemTurbo(answerMessage, arg['text']),
            'strength': arg['strength']
        } for arg in arguments]

    write_json(output_filename, clean_data)

    print(f"Answered data has been written to {output_filename}")


def parse_RawArguments(input_filename, output_filename):
    debate_data = {}
    try:
        with open(output_filename, 'r') as file:
            debate_data = json.load(file)
            if not isinstance(debate_data, dict):
                raise ValueError("Expected a dictionary in the JSON file")
    except (FileNotFoundError, ValueError):
        debate_data = {key: []
                       for key in ['PM', 'LO', 'DPM', 'DLO', 'MG', 'MO', 'GW', 'OW']}

    with open(input_filename, 'r') as file:
        lines = file.readlines()

    speech_type = lines[0].strip()
    arguments = debate_data.get(speech_type, [])

    for line in lines[1:]:
        line = line.strip().replace(' /n', '')
        last_space_index = line.rfind(' ')
        argument_text = line[:last_space_index].strip()
        argument_strength = line[last_space_index:].strip()

        if not any(arg['text'] == argument_text for arg in arguments):
            arguments.append({
                'text': argument_text,
                'strength': int(argument_strength)
            })

    debate_data[speech_type] = arguments
    debate_data_json = json.dumps(debate_data, indent=4)

    with open(output_filename, 'w') as json_file:
        json_file.write(debate_data_json)

    print(f"Data has been written to {output_filename}")


def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()


def write_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)


def read_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def write_json(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


rawDebateInput = os.getcwd() + '/VapYapDjango/content/input/'
rawDebateOutput = os.getcwd() + '/VapYapDjango/content/globalTracking/RawTracking.json'
cleanDebateOutput = os.getcwd() + '/VapYapDjango/content/globalTracking/CleanTracking.json'
answerDebateOutput = os.getcwd() + '/VapYapDjango/content/globalTracking/AnswerTracking.json'

answerBroadDebateOutput = os.getcwd() + '/VapYapDjango/content/AnswerBroadOutput.txt'
BrainStormOutput = os.getcwd() + '/VapYapDjango/content/BrainStorm.txt'
frontlineOutputFile = os.getcwd() + '/VapYapDjango/content/frontlineOutput.txt'


PMOutput = os.getcwd() + '/VapYapDjango/content/PMCase.txt'
LOOutput = os.getcwd() + '/VapYapDjango/content/LOCase.txt'

MGCaseOutput = os.getcwd() + '/VapYapDjango/content/MGCase.txt'
MGSpeechOutput = os.getcwd() + '/VapYapDjango/content/MGSpeech.txt'

MOCaseOutput = os.getcwd() + '/VapYapDjango/content/MOCase.txt'
MOSpeechOutput = os.getcwd() + '/VapYapDjango/content/MOSpeech.txt'


cleanMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentCleaning.txt'
BrainStormMessageFile = os.getcwd() + '/VapYapDjango/prompts/motionBrainStorm.txt'
answerMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentAnswer.txt'
answerBroadMessageFile = os.getcwd() + '/VapYapDjango/prompts/answerBroad.txt'
frontLineMessage = os.getcwd() + '/VapYapDjango/prompts/frontline.txt'



PMCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/PMCaseGeneration.txt'
LOCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/LOCaseGeneration.txt'
MGMOCaseDecision = os.getcwd() + '/VapYapDjango/prompts/caseGen/caseDecision/MGMOCaseDecision.txt'
MGMOCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/MGMOCaseGeneration.txt'
