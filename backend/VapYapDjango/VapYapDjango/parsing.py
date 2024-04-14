import json

def parse_arguments(input_filename, output_filename):
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

input_filename = 'content/debate.txt'
output_filename = 'content/RawTracking.json'
parse_arguments(input_filename, output_filename)
