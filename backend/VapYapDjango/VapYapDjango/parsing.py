import json
import os
from django.http import JsonResponse, HttpRequest
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
firstRun = True
speechNumberIndex = 0
position = ""
motion = ""

def initializeFormData(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        return data.get("motion"), data.get("infoSlide"), data.get("position")

def fetchNextSpeechFromFrontend(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        return data.get("title"), data.get("content"), data.get("position")

@csrf_exempt
def returnJSONObject(request: HttpRequest):
    global speechNumberIndex, firstRun, position, motion, debateWelcomeInfo, brainStormedIdeas
    speechType = orderOfSpeeches[speechNumberIndex]
    print ("Speech number index is", speechNumberIndex)
    print("firstRun is", firstRun)  
    if firstRun:
        firstRun = False
        motion, infoSlide, position = initializeFormData(request)
        if infoSlide is None:
            debateWelcomeInfo = f"You are a British Parliamentary debater. You are debating the motion {motion}. You are set to represent the {position} position."
        else:
            debateWelcomeInfo = f"You are a British Parliamentary debater. You are debating the motion {motion}. The info slide for the motion reads: {infoSlide}. You are set to represent the {position} position."
        brainStormArguments(debateWelcomeInfo)
        brainStormedIdeas = read_file(BrainStormOutput)
        
        if position == "OG":
            speechNumberIndex = 0
            speechType = orderOfSpeeches[speechNumberIndex]
            print("Trying to make a speech for " + speechType)
            makeSpeech(debateWelcomeInfo, brainStormedIdeas, speechType)
            print("Made a speech for PM " + speechType)
            convertOutputSpeechToInputSpeech(read_file(PMOutput))
            speechNumberIndex += 1
            print("After making PM speech speechType is  =", orderOfSpeeches[speechNumberIndex])
            return JsonResponse({"success": True, "speechFor": speechType, "speech": read_file(PMOutput)})
        print("First run is done, speechNumberIndex is" + str(speechNumberIndex))
        return JsonResponse({"success": True})
    print("Trying to enter in data for " + speechType)
    title, content, position = fetchNextSpeechFromFrontend(request)
    if position != speechType:
        print("Wrong speech button pressed lowkey or speechType is wrong")
        return JsonResponse({"success": False, "error": "Invalid position"})
    with open(os.getcwd() + f'/VapYapDjango/content/input/{title.upper()}.txt', "w") as speechFile:
        speechFile.write(title)
        speechFile.write("\n")
        speechFile.write(content)
    parse_RawArguments(
        rawDebateInput + title.upper() + ".txt", cleanDebateOutput)
    speechNumberIndex += 1
    if orderOfSpeeches[speechNumberIndex] in positionToOrderOfSpeeches[position]:
        speechType = orderOfSpeeches[speechNumberIndex]
        print("Trying to make a speech for " + speechType)
        makeSpeech(debateWelcomeInfo, brainStormedIdeas, speechType)
        print("Made a speech for PM " + speechType)
        convertOutputSpeechToInputSpeech(read_file(speechType + "Output"))
        speechNumberIndex += 1
        return JsonResponse({"success": True, "speechFor": speechType, "speech": read_file(speechType + "Output")})
    speechType = orderOfSpeeches[speechNumberIndex]
    print("After all that speechtype will be =", speechType)
    return JsonResponse({"success": True})

def convertOutputSpeechToInputSpeech():
   return
    #Make later

def makeSpeech(debateWelcomeInfo, brainStormedIdeas, speechNeeded):

    if speechNeeded in ("PM", "LO", "MG", "MO"):
        caseGeneration(debateWelcomeInfo, brainStormedIdeas, speechNeeded)
        if speechNeeded in ("PM", "LO"):
            return
        else:
            brainStormBroadAnswers(debateWelcomeInfo, speechNeeded)
            frontline(debateWelcomeInfo, speechNeeded)
            if speechNeeded == "MG":
                read_file(MGCaseOutput)
                finalSpeech = formalize(debateWelcomeInfo, read_file(
                    MGCaseOutput) + " " + read_file(answerBroadDebateOutput))
                write_file(MGSpeechOutput, finalSpeech)
            if speechNeeded == "MO":
                frontline(debateWelcomeInfo, "MO")
                read_file(MOCaseOutput)
                finalSpeech = formalize(debateWelcomeInfo, read_file(
                    MOCaseOutput) + " " + read_file(answerBroadDebateOutput) + " " + read_file(frontlineOutputFile))
                write_file(MOSpeechOutput, finalSpeech)

    else:
        broadAnswersMessage = read_file(answerBroadMessageFile)
        broadAnswers = makeAPIRequestFreshSystem(
            debateWelcomeInfo, broadAnswersMessage)
        write_file(answerBroadDebateOutput, broadAnswers)
        print(f"Broad answers have been written to {answerBroadDebateOutput}")
        if speechNeeded == "DPM":
            finalSpeech = formalize(debateWelcomeInfo, broadAnswers)
            write_file(DPMOutput, finalSpeech)
        if speechNeeded == "DLO":
            write_file(frontlineOutputFile, frontline(
                debateWelcomeInfo, "DLO"))
            finalSpeech = formalize(
                debateWelcomeInfo, broadAnswers + " " + read_file(frontlineOutputFile))
            write_file(DLOOutput, finalSpeech)
        else:
            if speechNeeded == "GW":
                write_file(frontlineOutputFile, frontline(
                    debateWelcomeInfo, "GW"))
                finalSpeech = formalize(debateWelcomeInfo, broadAnswers)
                write_file(GWOutput, finalSpeech)
            if speechNeeded == "OW":
                write_file(frontlineOutputFile, frontline(
                    debateWelcomeInfo, "OW"))
                finalSpeech = formalize(debateWelcomeInfo, broadAnswers)
                write_file(OWOutput, finalSpeech)


def formalize(debateWelcomeInfo, content):
    finalSpeech = makeAPIRequestFreshSystemTurbo(
        debateWelcomeInfo, "This speech is almost ready to ouput. Make sure that everything looks ok. The speech should be ready for me to read verbatim, so make sure that there is no refrences to what I was thinking when I decided to make these arguments. Intead, focus on making the arguments themselves in the debate", content)
    return finalSpeech


def caseGeneration(debateWelcomeInfo, brainStormedIdeas, speechNeeded):

    AlienExample = ("Here is the example case. This is from a debate with the motion This house hopes for the existence of aliens. This is the OG Speech from that debate" + read_file(AlienExampleFile))

    if speechNeeded == "PM":

        PMMessage = read_file(PMCaseGeneration)
        PM = makeAPIRequestFreshSystem(
            debateWelcomeInfo, PMMessage, AlienExample, brainStormedIdeas)

        write_file(PMOutput, PM)

        print(f"PM Case has been written to {PMOutput}")

    elif speechNeeded == "LO":
        LOMessage = read_file(LOCaseGeneration)

        json_data = read_json(cleanDebateOutput)
        pm_speeches = json_data['PM']
        definitions = [speech['text']
                       for speech in pm_speeches if speech.get('type') == 'definition']

        if definitions:
            defintionsInfo = "The key definitions from the OG speech were: " + \
                ", ".join(definitions)
            LO = makeAPIRequestFreshSystem(
                debateWelcomeInfo, LOMessage, AlienExample, brainStormedIdeas + defintionsInfo)
        else:
            LO = makeAPIRequestFreshSystem(
                debateWelcomeInfo, LOMessage, AlienExample, brainStormedIdeas)
        write_file(LOOutput, LO)

        print(f"LO Case has been written to {LOOutput}")

    elif speechNeeded in ("MG", "MO"):
        speechSpecifcInfo = f"You are on the team of {speechNeeded}"
        summaryInfo = "The summary of the debate so far speech by speech is: " + broadSummary()

        MGMOCaseDecisionMessage = read_file(MGMOCaseDecision)
        MGMOCaseGenerationMessage = read_file(MGMOCaseGeneration)

        MGMOCaseDecisionOutput = makeAPIRequestFreshSystem(
            debateWelcomeInfo, speechSpecifcInfo, MGMOCaseDecisionMessage, summaryInfo)

        print("The MG/MO case decision has been made")

        MGMOCase = makeAPIRequestFreshSystem(
            debateWelcomeInfo, speechSpecifcInfo, MGMOCaseGenerationMessage, MGMOCaseDecisionOutput, summaryInfo)
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

    summaryOpponentsInfo = "The summary of the opponents cases so far is: " + \
        broadSummaryOpponents(position)
    broadAnswersMessage = read_file(answerBroadMessageFile)

    broadAnswers = makeAPIRequestFreshSystem(
        debateWelcomeInfo, broadAnswersMessage,summaryOpponentsInfo)

    write_file(answerBroadDebateOutput, broadAnswers)
    print(f"Broad answers have been written to {answerBroadDebateOutput}")
    return


def frontline(debateWelcomeInfo, position):

    summaryOpponentsInfo = "The opponents have made the following arguments against us  " + \
        broadSummaryOpponentsAttacks(position)
    frontLineMessage = read_file(frontLineMessage)

    frontlines = makeAPIRequestFreshSystem(
        debateWelcomeInfo, frontLineMessage, summaryOpponentsInfo)

    write_file(frontlineOutputFile, frontlines)
    print(f"Broad answers have been written to {frontlineOutputFile}")
    return


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
cleanDebateOutput = os.getcwd() + '/VapYapDjango/content/globalTracking/RawTracking.json'
answerDebateOutput = os.getcwd() + '/VapYapDjango/content/globalTracking/AnswerTracking.json'

answerBroadDebateOutput = os.getcwd() + '/VapYapDjango/content/AnswerBroadOutput.txt'
BrainStormOutput = os.getcwd() + '/VapYapDjango/content/BrainStorm.txt'
frontlineOutputFile = os.getcwd() + '/VapYapDjango/content/frontlineOutput.txt'


PMOutput = os.getcwd() + '/VapYapDjango/content/PMSpeech.txt'
LOOutput = os.getcwd() + '/VapYapDjango/content/LOSpeech.txt'
DPMOutput = os.getcwd() + '/VapYapDjango/content/DPMSpeech.txt'
DLOOutput = os.getcwd() + '/VapYapDjango/content/DLOSpeech.txt'

MGCaseOutput = os.getcwd() + '/VapYapDjango/content/MGCase.txt'
MGSpeechOutput = os.getcwd() + '/VapYapDjango/content/MGSpeech.txt'

MOCaseOutput = os.getcwd() + '/VapYapDjango/content/MOCase.txt'
MOSpeechOutput = os.getcwd() + '/VapYapDjango/content/MOSpeech.txt'

GWOutput = os.getcwd() + '/VapYapDjango/content/GWSpeech.txt'
OWOutput = os.getcwd() + '/VapYapDjango/content/OWSpeech.txt'

cleanMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentCleaning.txt'
BrainStormMessageFile = os.getcwd() + '/VapYapDjango/prompts/motionBrainStorm.txt'
answerMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentAnswer.txt'
answerBroadMessageFile = os.getcwd() + '/VapYapDjango/prompts/answerBroad.txt'
frontLineMessage = os.getcwd() + '/VapYapDjango/prompts/frontline.txt'


PMCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/PMCaseGeneration.txt'
LOCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/LOCaseGeneration.txt'
MGMOCaseDecision = os.getcwd() + '/VapYapDjango/prompts/caseGen/caseDecision/MGMOCaseDecision.txt'
MGMOCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/MGMOCaseGeneration.txt'
AlienExampleFile = os.getcwd() + '/VapYapDjango/prompts/caseGen/CaseExampleAlien.txt'
