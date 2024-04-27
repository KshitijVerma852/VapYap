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
    useFrontend = True
    useSetupPageData = True
    print("Start running")

    motion = ("This House believes that democratic states should grant an amnesty to whistleblowers who expose "
              "unethical practices in the government.")
    infoSlide = ""
    position = "OG"
    content = ""
    title = ""
    if useFrontend:
        if request.method == "POST":
            data = json.loads(request.body)
            if "title" in data and "content" in data:
                title = data.get("title")
                content = data.get("content")
                with open(f"content/input/{title.upper()}Speech.txt", "w") as speechFile:
                    speechFile.write(title)
                    speechFile.write(content)
            else:
                motion = data.get("motion")
                infoSlide = data.get("infoSlide")
                position = data.get("position")

    for speechType in orderOfSpeeches:
        if speechType in positionToOrderOfSpeeches[position]:
            parse_RawArguments(rawDebateInput+speechType, rawDebateOutput)
            clean_RawArguments(rawDebateOutput, cleanDebateOutput)
            answerArguments(cleanDebateOutput, answerDebateOutput)
            caseGeneration(motion, infoSlide, position, speechType)

    return JsonResponse({"ai_response": "dfdai_response"})


def caseGeneration(motion, infoSlide, position, speechNeeded):
    brainStormedIdeas = read_file(BrainStormOutput)

    brainStormedIdeasInfo = ("My ideas for the motion are: " + brainStormedIdeas)
    debateInfo = ("The motion reads: " + motion + " The info slide, if it exists reads: " +
                  infoSlide)

    if speechNeeded == "PM":

        PMMessage = read_file(PMCaseGeneration)
        PM = makeAPIRequestFreshSystem(PMMessage, debateInfo, brainStormedIdeasInfo)
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
            LO = makeAPIRequestFreshSystem(LOMessage, debateInfo, brainStormedIdeasInfo + defintionsInfo)
        else:
            LO = makeAPIRequestFreshSystem(LOMessage, debateInfo, brainStormedIdeasInfo)

        lengthAdjustedLO = adjustLength(LO)
        write_file(LOOutput, lengthAdjustedLO)

        print(f"LO Case has been written to {LOOutput}")

    elif speechNeeded in ("MG", "MO"):
        welcomeInfo = "You are a British Parli debater on the team of {speechNeeded}"
        summaryInfo = "The summary of the debate so far speech by speech is: " + broadSummary()

        MGMOCaseDecisionMessage = read_file(MGMOCaseDecision)
        MGMOCaseGenerationMessage = read_file(MGMOCaseGeneration)

        MGMOCaseDecisionOutput = makeAPIRequestFreshSystem(welcomeInfo, MGMOCaseDecisionMessage, debateInfo,
                                                           brainStormedIdeasInfo, summaryInfo)

        print("The MG/MO case decision has been made")

        MGMOCase = makeAPIRequestFreshSystem(MGMOCaseGenerationMessage, debateInfo, MGMOCaseDecisionOutput, summaryInfo)
        if speechNeeded == "MG":
            write_file(MGCaseOutput, MGMOCase)
            print(f"MG Case has been written to {MGCaseOutput}")

        if speechNeeded == "MO":
            write_file(MOCaseOutput, MGMOCase)
            print(f"MG Case has been written to {MOCaseOutput}")


    else:
        print("Invalid speech type")


def brainStormArguments(debateInfo):
    brainStormMessage = read_file(BrainStormMessageFile)
    brainStormedIdeas = makeAPIRequestFreshSystem(
        brainStormMessage, debateInfo)
    write_file(BrainStormOutput, brainStormedIdeas)
    print(f"Brainstorming has been written to {BrainStormMessageFile}")


def brainStormBroadAnswers(debateInfo, position):
    welcomeInfo = "You are a British Parli debater on the team of{position}. "
    summaryInfo = "The summary of the debate so far speech by speech is: " + broadSummary()
    broadAnswers = read_file(answerBroadMessageFile)
    broadAnswers = makeAPIRequestFreshSystem(
        welcomeInfo, debateInfo, broadAnswers ,summaryInfo)
    write_file(answerBroadDebateOutput, broadAnswers)
    print("Broad answers have been written to {answerBroadDebateOutput}")
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


PMOutput = os.getcwd() + '/VapYapDjango/content/PMCase.txt'
LOOutput = os.getcwd() + '/VapYapDjango/content/LOCase.txt'
MGCaseOutput = os.getcwd() + '/VapYapDjango/content/MGCase.txt'
MOCaseOutput = os.getcwd() + '/VapYapDjango/content/MOCase.txt'

cleanMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentCleaning.txt'
BrainStormMessageFile = os.getcwd() + '/VapYapDjango/prompts/motionBrainStorm.txt'
answerMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentAnswer.txt'
answerBroadMessageFile = os.getcwd() + '/VapYapDjango/prompts/answerBroad.txt'

PMCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/PMCaseGeneration.txt'
LOCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/LOCaseGeneration.txt'
MGMOCaseDecision = os.getcwd() + '/VapYapDjango/prompts/caseGen/caseDecision/MGMOCaseDecision.txt'
MGMOCaseGeneration = os.getcwd() + '/VapYapDjango/prompts/caseGen/MGMOCaseGeneration.txt'
