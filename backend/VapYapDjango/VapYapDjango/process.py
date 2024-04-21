import json
import os
def broadSummary():
    debate_data = json.loads(read_file(cleanDebateOutput))

    team_roles = {
        "OG": ["PM", "DPM"],
        "OO": ["LO", "DLO"],
        "CG": ["MG", "GW"],
        "CO": ["MO", "OW"]
    }
    summary = []
    
    for team, roles in team_roles.items():
        team_summary = []
        for role in roles:
            speech = debate_data.get(role, [])
            if speech:
                summarized_text = summarize(speech)
                team_summary.append(f"{role} argued that {summarized_text}")
    
        if team_summary:
            team_summary_joined = " and also ".join(team_summary)
            summary.append(f"{team} has stated: {team_summary_joined}")
    
    return " ".join(summary)

def summarize(speech):
    texts = [argument['text'] for argument in speech]
    combined_text = " Next they said ".join(texts)
    return combined_text

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

cleanDebateOutput = os.getcwd() + '/VapYapDjango/content/CleanTracking.json'
