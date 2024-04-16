import json
import os
from django.http import JsonResponse, HttpRequest
from .logic import makeAPIRequestFreshSystem
from .logic import makeAPIRequestFreshSystemTurbo
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def returnJSONObject(request: HttpRequest):
    print("Start running")
    motion = "This house believes that religion does more harm than good"
    infoSlide = ""
    position = "OG"
    parse_RawArguments(rawDebateInput, rawDebateOutput)
    clean_RawArguments(rawDebateOutput, cleanDebateOutput)
    answerArguments(cleanDebateOutput, answerDebateOutput)
    caseGeneration(motion, infoSlide, position)
    return JsonResponse({"ai_response": "dfdai_response"})

def caseGeneration(motion, infoSlide, position):
    
    speechDetails = ("The motion you need to brainstorm reads: " +motion + " The info slide, if it exists reads: " + infoSlide + "You are to think of arguments for side :" + position)
    with open(BrainStormMessageFile, 'r') as file:
        brainStormMessage = file.read()
    brainStormedIdeas = makeAPIRequestFreshSystem(brainStormMessage, speechDetails)
    with open(BrainStormOutput, 'w') as file:
        file.write(brainStormedIdeas)
    print(f"Brainstorming has been written to {BrainStormMessageFile}")

def clean_RawArguments(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        data = json.load(file)
    with open(cleanMessageFile, 'r') as file:
        cleanMessage = file.read()
    clean_data = {}
    for speech_type, arguments in data.items():
        clean_data[speech_type] = [{
            'text': makeAPIRequestFreshSystemTurbo(cleanMessage, arg['text']),
            'strength': arg['strength']
        } for arg in arguments]

    with open(output_filename, 'w') as file:
        json.dump(clean_data, file, indent=4)

    print(f"Clean data has been written to {output_filename}")

def answerArguments(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        data = json.load(file)
    with open(answerMessageFile, 'r') as file:
        answerMessage = file.read()
    clean_data = {}
    for speech_type, arguments in data.items():
        clean_data[speech_type] = [{
            'text': makeAPIRequestFreshSystem(answerMessage, arg['text']),
            'strength': arg['strength']
        } for arg in arguments]

    with open(output_filename, 'w') as file:
        json.dump(clean_data, file, indent=4)

    print(f"Answered data has been written to {output_filename}")

def parse_RawArguments(input_filename, output_filename):
    debate_data = {}
    try:
        with open(output_filename, 'r') as file:
            debate_data = json.load(file)
            if not isinstance(debate_data, dict):
                raise ValueError("Expected a dictionary in the JSON file")
    except (FileNotFoundError, ValueError):
        debate_data = {key: [] for key in ['PM', 'LO', 'DPM', 'DLO', 'MG', 'MO', 'GW', 'OW']}

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

rawDebateInput = os.getcwd() + '/VapYapDjango/content/speech.txt'
rawDebateOutput = os.getcwd() + '/VapYapDjango/content/RawTracking.json'
cleanDebateOutput = os.getcwd() + '/VapYapDjango/content/CleanTracking.json'
answerDebateOutput = os.getcwd() + '/VapYapDjango/content/AnswerTracking.json'
BrainStormOutput = os.getcwd() + '/VapYapDjango/content/BrainStorm.txt'

cleanMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentCleaning.txt'
BrainStormMessageFile = os.getcwd() + '/VapYapDjango/prompts/motionBrainStorm.txt'
answerMessageFile = os.getcwd() + '/VapYapDjango/prompts/argumentAnswer.txt'
