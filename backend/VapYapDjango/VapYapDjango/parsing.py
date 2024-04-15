import json
import os
from django.http import JsonResponse, HttpRequest
from .logic import makeAPIRequestFreshSystem
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def returnJSONObject(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        motion = data.get("motion")
        infoSlide = data.get("infoSlide")
        position = data.get("position")

        parse_RawArguments(rawDebateInput, rawDebateOutput)
        clean_RawArguments(rawDebateOutput, cleanDebateOutput)

        return JsonResponse({"ai_response": "dfdai_response"})

    return JsonResponse({"ai_response": "dfdai_response"})


def clean_RawArguments(input_filename, output_filename):
    cleanMessage = "Please fix grammar errors and spelling errors in these sentences without altering the meaning significantly."
    with open(input_filename, 'r') as file:
        data = json.load(file)

    clean_data = {}
    for speech_type, arguments in data.items():
        clean_data[speech_type] = [{
            'text': makeAPIRequestFreshSystem(cleanMessage, arg['text']),
            'strength': arg['strength']
        } for arg in arguments]

    with open(output_filename, 'w') as file:
        json.dump(clean_data, file, indent=4)

    print(f"Clean data has been written to {output_filename}")


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


rawDebateInput = os.getcwd() + '/VapYapDjango/content/debate.txt'
rawDebateOutput = os.getcwd() + '/VapYapDjango/content/RawTracking.json'
cleanDebateOutput = os.getcwd() + '/VapYapDjango/content/CleanTracking.json'
