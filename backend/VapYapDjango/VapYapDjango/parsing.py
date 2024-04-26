import json
import os
from django.http import JsonResponse, HttpRequest
from .length import adjustLength
from .summarize import broadSummary
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


@csrf_exempt
def returnJSONObject(request: HttpRequest):
    print("Start running")
    motion = "This House believes that democratic states should grant an amnesty to whistleblowers who expose unethical practices in the government."
    infoSlide = ""
    position = "OG"

    for speechType in orderOfSpeeches:
        if speechType in positionToOrderOfSpeeches[position]:
            parse_RawArguments(rawDebateInput, rawDebateOutput)
            clean_RawArguments(rawDebateOutput, cleanDebateOutput)
            answerArguments(cleanDebateOutput, answerDebateOutput)

    summary = broadSummary()

    # Kshtej put ur array thing here because of it is saving arguments which happens for every speech.
    # Case generation only happens sometimes.

    speechNeeded = "MG"

    caseGeneration(motion, infoSlide, position, speechNeeded)

    return JsonResponse({"ai_response": "dfdai_response"})


def caseGeneration(motion, infoSlide, position, speechNeeded):
    brainStormedIdeas = read_file(BrainStormOutput)
    debateInfo = ("The motion reads: " + motion + " The info slide, if it exists reads: " +
                  infoSlide + "My ideas for the motion are: " + brainStormedIdeas)

    if speechNeeded == "PM":

        PMMessage = read_file(PMCaseGeneration)
        PM = makeAPIRequestFreshSystem(PMMessage, debateInfo)
        lengthAdjustedPM = adjustLength(PM)
        write_file(PMOutput, lengthAdjustedPM)

        print(f"PM Case has been written to {PMOutput}")

    elif speechNeeded == "LO":

        defintions = 0
        json_data = read_json(cleanDebateOutput)
        pm_speeches = json_data['PM']
        for argument in pm_speeches:
            if argument.get('type') == 'defintion':
                defintions = defintions + 1
        if defintions != 0:
            debateInfo = debateInfo + "The key defintions from the OG speech were"
            for speech in pm_speeches:
                if speech.get('type') == 'defintion':
                    debateInfo = debateInfo + (speech.get('text')) + ",  "

        LOMessage = read_file(LOCaseGeneration)
        LO = makeAPIRequestFreshSystem(LOMessage, debateInfo)
        lengthAdjustedLO = adjustLength(LO)
        write_file(LOOutput, lengthAdjustedLO)

        print(f"LO Case has been written to {LOOutput}")

    elif speechNeeded == "MG":
        summary = broadSummary()
        debateInfo = debateInfo + \
                     "The summary of the debate so far speech by speech is: " + summary
        MGCaseDecisonMessage = read_file(MGCaseDecison)
        MGCaseGenerationMessage = read_file(MGCaseGeneration)
        MGCaseDecision = makeAPIRequestFreshSystem(
            MGCaseDecisonMessage, debateInfo)
        print("The MG case decision has been made " + MGCaseDecision)
        caseInfo = ("The motion reads: " + motion +
                    " The info slide, if it exists reads: " +
                    infoSlide +
                    "My loose plan for the case are: " +
                    MGCaseDecision)
        MGCase = makeAPIRequestFreshSystem(MGCaseGenerationMessage, caseInfo)
        write_file(MGCaseOutput, MGCase)
        print(f"MG Case has been written to {MGCaseOutput}")

    elif speechNeeded == "MO":
        summary = broadSummary()

    else:
        print("Invalid speech type")


def brainStormArguments(motion, infoSlide, position):
    speechDetails = f"The motion you need to brainstorm reads: {motion} The info slide, if it exists reads: {infoSlide} You are to think of arguments for side :{position}"
    brainStormMessage = read_file(BrainStormMessageFile)
    brainStormedIdeas = makeAPIRequestFreshSystem(
        brainStormMessage, speechDetails)
    write_file(BrainStormOutput, brainStormedIdeas)
    print(f"Brainstorming has been written to {BrainStormMessageFile}")


def brainStormBroadAnswers():
    return


def brainStormInteractions():
    return


def evalValue():
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


rawDebateInput = os.getcwd() + '/VapYapDjango/content/speech.txt'
rawDebateOutput = os.getcwd() + '/VapYapDjango/content/RawTracking.json'
cleanDebateOutput = os.getcwd() + '/VapYapDjango/content/CleanTracking.json'
answerDebateOutput = os.getcwd() + '/VapYapDjango/content/AnswerTracking.json'
BrainStormOutput = os.getcwd() + '/VapYapDjango/content/BrainStorm.txt'

PMOutput = os.getcwd() + '/VapYapDjango/content/PMCase.txt'
LOOutput = os.getcwd() + '/VapYapDjango/content/LOCase.txt'
MGCaseOutput = os.getcwd() + '/VapYapDjango/content/MGCase.txt'


cleanMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentCleaning.txt'
BrainStormMessageFile = os.getcwd() + '/VapYapDjango/prompts/motionBrainStorm.txt'
answerMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentAnswer.txt'

PMCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/PMCaseGeneration.txt'
LOCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/LOCaseGeneration.txt'
MGCaseDecison = os.getcwd() + '/VapYapDjango/prompts/caseGen/caseDecision/MGCaseDecision.txt'
MGCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/MGCaseGeneration.txt'
